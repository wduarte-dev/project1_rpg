from random import randint
from rich import print
from os import system, name
from dataclasses import dataclass, field
from player import Player

@dataclass
class Map:
    x_len : int = field(default=0, init=False)
    y_len : int = field(default=0, init=False)
    chest_with_key_coordinates : list = field(default_factory=lambda:['Not generated'], init=False)
    map_matrix : list = field(default_factory=lambda:['Not generated'], init=False)

    def clear_terminal(self):
        system('cls' if name == 'nt' else 'clear')

    def randomize_geometry(self):
        self.x_len, self.y_len = randint(10, 15), randint(10, 15)
  
    def generate(self):
        self.map_matrix = [['.' for _ in range(self.x_len)] for _ in range(self.y_len)]
        self.map_matrix[0][-1] = 'P'
        self.generate_chests(3)
    
    def draw_player(self, player_obj):
        cmd = input('> ').lower()
        old_x, old_y = player_obj.x_pos, player_obj.y_pos
        player_obj.move(cmd, self.x_len, self.y_len)
        self.map_matrix[old_y][old_x] = '.'
        if [player_obj.x_pos, player_obj.y_pos] == self.chest_with_key_coordinates:
            player_obj.has_key = True
        self.map_matrix[player_obj.y_pos][player_obj.x_pos] = 'J'

    
    def draw_entities(self, player_obj):
        self.draw_player(player_obj)

    def generate_chests(self, quantity) -> tuple | None:
        for generation in range(quantity):
            key_on_chest = False
            x_gen, y_gen = randint(0, self.x_len - 1), randint(0, self.y_len - 1)
            while self.map_matrix[y_gen][x_gen] != '.':
                x_gen, y_gen = randint(0, self.x_len - 1), randint(0, self.y_len - 1)  
            self.map_matrix[y_gen][x_gen] = 'C'
            if not key_on_chest:
                key_on_chest = True
                self.chest_with_key_coordinates = [x_gen, y_gen]
    
    def show_map(self):
        for y in self.map_matrix:
            print(' '.join(y)) 

    def renderize(self):
        self.randomize_geometry()
        self.generate()
        print('Press ENTER to START')
        p1 = Player(self.y_len)
        while True:
            self.draw_entities(p1)
            self.clear_terminal()
            if p1.has_key:
                print('HAS KEY? ( ) NO [blue](x) YES[/]')
            else:
                print('HAS KEY? [red](x) NO[/] ( ) YES')
            self.show_map()

def main():
    map1 = Map()
    map1.renderize()

if __name__ == '__main__':
    main()