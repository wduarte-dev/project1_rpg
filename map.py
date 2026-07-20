from random import randint, choice, choices
from rich import print
from os import system, name
from dataclasses import dataclass, field
from player import Player
from enemy import DrunkEnemy, SmartEnemy
from copy import deepcopy
from terminal_utils import get_key, clear_terminal
import time

@dataclass
class Map:
    x_len : int = field(default=0, init=False)
    y_len : int = field(default=0, init=False)
    chest_with_key_coordinates : list = field(default_factory=lambda:['Not generated'], init=False)
    chests_generations_coordinates : list = field(default_factory=lambda:['Not generated'], init=False) 
    map_matrix : list = field(default_factory=lambda:['Not generated'], init=False)
    level : int = field(default=0, init=False)
    generate_next_level : bool = field(default=False, init=False)
    grass_coordinates : list = field(default_factory=lambda:['Not generated'], init=False)
    game_over_state : bool = field(default=False, init=False)
    list_of_enemies : list = field(default_factory=lambda:[], init=False)

    def randomize_geometry(self, player_obj, enemies_obj) -> None:
        gmm = self.level # lmm -> geometry map multiplier
        self.x_len, self.y_len = randint(15 + gmm, 30 + gmm), randint(10 + gmm, 15 + gmm)
    
    def chest_generation(self):
        self.chests_generations_coordinates = []
        self.chest_with_key_coordinates = []
        self.generate_chests(5)
        self.generate_obstacles_in_chests()
  
    def generate(self, player_obj, enemies_obj):
        print('[yellow]Loading...[/]')
        player_obj.reset_stats_and_pos(self.x_len, self.y_len) 
        enemies_obj = self.enemy_generation()
        while True:
            self.map_matrix = [['.' for _ in range(self.x_len)] for _ in range(self.y_len)]
            self.map_matrix[0][-1] = 'D'
            self.chest_generation()
            if self.is_map_solvable(player_obj):
                self.generate_grass()
                self.enemy_generation()
                break
            continue
    
    def draw_player(self, player_obj):
        cmd = get_key()
        old_x, old_y = player_obj.x_pos, player_obj.y_pos
        new_positions_tuple = player_obj.move(cmd)
        # move verifier
        new_x_pos, new_y_pos = new_positions_tuple
        if 'E' in self.map_matrix[new_y_pos][new_x_pos]:
            self.map_matrix[old_y][old_x] = '[blue].[/]'
            self.game_over()
        if self.map_matrix[new_y_pos][new_x_pos] == '#':
            player_obj.x_pos, player_obj.y_pos = old_x, old_y
        ## end
        self.map_matrix[old_y][old_x] = '[blue].[/]'
        if [player_obj.x_pos, player_obj.y_pos] == self.chest_with_key_coordinates:
            player_obj.has_key = True
        self.map_matrix[player_obj.y_pos][player_obj.x_pos] = '[blue]P[/]'

    def draw_enemy(self, list_of_enemies, player_obj):
        for enemy in list_of_enemies:
            if not enemy[1]:
                while True:
                    x_gen, y_gen = randint(0, self.x_len - 1), randint(0, self.y_len - 1)
                    if (y_gen >= self.y_len - 3) and (x_gen <= 2): # this enemy can only generate 2 lines above or more and 2 columns right or more
                        continue
                    elif '.' not in self.map_matrix[y_gen][x_gen]:
                        continue
                    break
                enemy[0].x_pos, enemy[0].y_pos = x_gen, y_gen
                self.map_matrix[enemy[0].y_pos][enemy[0].x_pos] = enemy[2]
                enemy[1] = True
            else:
                old_x, old_y = enemy[0].x_pos, enemy[0].y_pos
                new_positions_tuple = enemy[0].move((player_obj.x_pos, player_obj.y_pos))
                new_x_pos, new_y_pos = new_positions_tuple
                # move verifier
                if 'P' in self.map_matrix[new_y_pos][new_x_pos]:
                    self.map_matrix[old_y][old_x] = enemy[3]
                    self.map_matrix[new_y_pos][new_x_pos] = enemy[2]
                    self.game_over()
                elif '.' not in self.map_matrix[new_y_pos][new_x_pos]:
                    enemy[0].x_pos, enemy[0].y_pos = old_x, old_y
                ## end
                self.map_matrix[old_y][old_x] = enemy[3]
                self.map_matrix[enemy[0].y_pos][enemy[0].x_pos] = enemy[2]
            
    def enemy_generation(self):
        self.list_of_enemies = []
        if self.level >= 1:
            e1 = DrunkEnemy(self.x_len, self.y_len)
            self.list_of_enemies.append([e1, False, '[red]E[/]', '[red].[/]']) # -> [object, bool, appearance, path]
        if self.level >= 3:
            e2 = DrunkEnemy(self.x_len, self.y_len)
            self.list_of_enemies.append([e2, False, '[red]E[/]', '[red].[/]'])
        if self.level >= 5:
            e3 = SmartEnemy(self.x_len, self.y_len)
            self.list_of_enemies.append([e3, False, '[purple]E[/]', '[purple].[/]'])
        if self.level >= 10:
            e4 = SmartEnemy(self.x_len, self.y_len)
            self.list_of_enemies.append([e4, False, '[purple]E[/]', '[purple].[/]'])
        
    def draw_entities(self, player_obj):
        self.draw_player(player_obj)
        self.draw_enemy(self.list_of_enemies, player_obj)

    def generate_chests(self, quantity) -> tuple | None:
        for generation in range(quantity):
            while True:
                key_on_chest = False
                x_gen, y_gen = randint(0, self.x_len - 1), randint(0, self.y_len) # dont need to self.y_len - 1 bc of conditions
                # conditions 
                if (y_gen >= self.y_len - 4) or (y_gen <= 2): # chest can only generate 2 lines or more above player
                    continue
                break
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

    def generate_grass(self):
        self.grass_coordinates = []
        for y in range(self.y_len):
            for x in range(self.x_len):
                if self.map_matrix[y][x] == '.' and (x, y) not in self.grass_coordinates:
                    if randint(0, 100) <= 20:
                        self.grass_coordinates.append((x, y))


    def show_map(self):
        map_str = deepcopy(self.map_matrix)
        if not self.game_over_state:
            for y in range(self.y_len):
                for x in range(self.x_len):
                    if map_str[y][x] == '.' and (x, y) in self.grass_coordinates:
                        map_str[y][x] = ','
        map_str = [' '.join(y) for y in map_str]
        print('\n'.join(map_str))

            
    def header_text(self, player_obj):
        if player_obj.has_key:
            print('HAS KEY? ( ) NO [blue](x) YES[/]')
        else:
            if player_obj.can_next_level == 2:
                print('HAS KEY? [red](x) NO[/] ( ) YES\n[red]FIND THE KEY FIRST.[/]' + '    '*self.x_len)
            else:
                print('HAS KEY? [red](x) NO[/] ( ) YES')
        if player_obj.can_next_level == 1:
            clear_terminal(1)
            print('[blue]Congrats.[/]\nPress ENTER to CONTINUE.\n> ', end='')
            input()
            self.generate_next_level = True

    def footer_text(self):
        print(f'LEVEL {self.level}' + '    '*self.x_len + '\n' + '    '*self.x_len)

    def renderize(self):
        p1 = Player(0, 0)
        enemies_obj = None
        input('Press ENTER to START\nWASD to MOVE, E to EXIT\n> ')
        while True:
            clear_terminal(1)
            self.randomize_geometry(p1, enemies_obj) # JÁ MUDO O X_MAP E Y_MAP DO PLAYER E INIMIGO AQUI
            self.generate(p1, enemies_obj)
            while True:
                self.draw_entities(p1)
                clear_terminal(0)
                self.header_text(p1)
                if self.generate_next_level:
                    self.level += 1
                    self.generate_next_level = False
                    p1.has_key = False
                    self.enemy_has_generated = False
                    break
                self.show_map()
                self.footer_text()

    def game_over(self):
        self.game_over_state = True
        clear_terminal(1)
        for _ in range(10):
            if _ % 2 == 0: self.map_matrix[0][0] = '[red].'
            else: self.map_matrix[0][0] = '[blue].'
            self.show_map()
            time.sleep(0.10)
            clear_terminal(1)
        for _ in range (0, self.y_len):
            if _ % 2 == 0: self.map_matrix[0][0] = '[blue].'
            else: self.map_matrix[0][0] = '[red].'
            self.map_matrix.pop(-1)
            self.show_map()
            time.sleep(0.10)
            clear_terminal(1)
        time.sleep(2)
        print(f'SCORE: {self.level}')
        time.sleep(2)
        input('Press ENTER to EXIT.')
        exit()