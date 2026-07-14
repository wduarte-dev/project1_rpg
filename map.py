from random import randint, choice
from rich import print
from os import system, name
from dataclasses import dataclass, field
from player import Player
import sys

if name == 'nt': 
    import msvcrt
    def get_key():
        return msvcrt.getch().decode('utf-8', errors='ignore').lower()
else: 
    import tty, termios
    def get_key():
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch.lower()

@dataclass
class Map:
    x_len : int = field(default=0, init=False)
    y_len : int = field(default=0, init=False)
    chest_with_key_coordinates : list = field(default_factory=lambda:['Not generated'], init=False)
    chests_generations_coordinates : list = field(default_factory=lambda:['Not generated'], init=False) 
    map_matrix : list = field(default_factory=lambda:['Not generated'], init=False)
    level : int = field(default=0, init=False)
    generate_next_level : bool = field(default=False, init=False)

    def clear_terminal(self):
        system('cls' if name == 'nt' else 'clear')

    def randomize_geometry(self):
        self.x_len, self.y_len = randint(10, 15), randint(10, 15)
  
    def generate(self, player_obj):
        while True:
            self.chests_generations_coordinates = []
            self.chest_with_key_coordinates = []
            self.map_matrix = [['.' for _ in range(self.x_len)] for _ in range(self.y_len)]
            self.map_matrix[0][-1] = 'P'
            self.generate_chests(3)
            self.generate_obstacles_in_chests()
            if self.is_map_solvable(player_obj):
                break
            continue
    
    def draw_player(self, player_obj):
        cmd = get_key()
        old_x, old_y = player_obj.x_pos, player_obj.y_pos
        player_obj.move(cmd)
        self.map_matrix[old_y][old_x] = '.'
        if [player_obj.x_pos, player_obj.y_pos] == self.chest_with_key_coordinates:
            player_obj.has_key = True
        self.map_matrix[player_obj.y_pos][player_obj.x_pos] = 'J'
  
    def draw_entities(self, player_obj):
        self.draw_player(player_obj)

    def generate_chests(self, quantity) -> tuple | None:
        for generation in range(quantity):
            key_on_chest = False
            x_gen, y_gen = randint(0, self.x_len - 1), randint(0, self.y_len - 4) # chest can only generate 2 lines or more above player
            while self.map_matrix[y_gen][x_gen] != '.':
                x_gen, y_gen = randint(0, self.x_len - 1), randint(0, self.y_len - 1) 
            if 'Not generated' in self.chests_generations_coordinates:
                self.chests_generations_coordinates = []
            self.chests_generations_coordinates.append([x_gen, y_gen]) 
            self.map_matrix[y_gen][x_gen] = 'C'
            if not key_on_chest:
                key_on_chest = True
                self.chest_with_key_coordinates = [x_gen, y_gen]

    def generate_obstacles_in_chests(self):
        for chest_coordinates in self.chests_generations_coordinates:
            x_chest, y_chest = chest_coordinates[0], chest_coordinates[1]
            neighbors_xy = [
                (-1, -1),(0, -1),(1, -1),
                (-1,  0),        (1,  0),
                (-1,  1),(0,  1),(1,  1)
            ]
            entries = [neighbors_xy[1], neighbors_xy[3], neighbors_xy[4], neighbors_xy[6]]
            chest_entry = choice(entries)
            neighbors_xy.remove(chest_entry)
            for dx, dy in neighbors_xy:
                x_obstacle, y_obstacle = x_chest + dx, y_chest + dy
                try:
                    if self.map_matrix[y_obstacle][x_obstacle] == '.' and x_obstacle != -1 and y_obstacle != -1:
                        self.map_matrix[y_obstacle][x_obstacle] = '#'
                except IndexError:
                    pass
    
    def is_map_solvable(self, player_obj):
        queue = [(player_obj.x_pos, player_obj.y_pos)]
        visited = []
        while queue:
            curr_x, curr_y = queue[0]
            queue.pop(0)
            if (curr_x, curr_y) in visited:
                continue
            visited.append((curr_x, curr_y))
            directions = [
                   (0, -1),
            (-1, 0),     (1,  0),
                   (0,  1)
            ]
            for dx, dy in directions:
                new_x, new_y = curr_x + dx, curr_y + dy
                if 0 <= new_x < self.x_len and 0 <= new_y < self.y_len:
                    if self.map_matrix[new_y][new_x] != '#' and (new_x, new_y) not in visited:
                        queue.append((new_x, new_y))
        if (self.x_len - 1, 0) in visited:
            for x_chest, y_chest in self.chests_generations_coordinates:
                if (x_chest, y_chest) in visited:
                    continue
                else:
                    return False
            return True
        return False


    def show_map(self):
        for y in self.map_matrix:
            print(' '.join(y))
            
    def header_text(self, player_obj):
        if player_obj.has_key:
            print('HAS KEY? ( ) NO [blue](x) YES[/]')
        else:
            print('HAS KEY? [red](x) NO[/] ( ) YES')
        if player_obj.can_next_level == 1:
            self.clear_terminal()
            print('[blue]Congrats.[/]\nPress ENTER to CONTINUE.\n> ', end='')
            self.generate_next_level = True
        if player_obj.can_next_level == 2 and not player_obj.has_key:
            print('[red]FIND THE KEY FIRST.[/]')

    def footer_text(self):
        print(f'LEVEL {self.level}')

    def renderize(self):
        while True:
            self.randomize_geometry()
            if self.level == 0:
                print('Press ENTER to START\n> ', end='')
                p1 = Player(self.x_len, self.y_len)
            elif self.level != 0:
                p1.level_restart(self.x_len, self.y_len) 
            self.generate(p1)
            while True:
                self.draw_entities(p1)
                self.clear_terminal()
                self.header_text(p1)
                if self.generate_next_level:
                    self.level += 1
                    self.generate_next_level = False
                    p1.has_key = False
                    break
                self.show_map()
                self.footer_text()


def main():
    map1 = Map()
    map1.renderize()

if __name__ == '__main__':
    main()