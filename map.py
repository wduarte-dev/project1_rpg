from random import randint
from rich import print
from dataclasses import dataclass, field

@dataclass
class Map:
    x_len : int = field(default=0, init=False)
    y_len : int = field(default=0, init=False)
    map_matrix : list = field(default_factory=lambda:['Not generated'], init=False)

    def randomize_geometry(self):
        self.x_len = randint(10, 15)
        self.y_len = randint(10, 15)
    
    def generate(self):
        self.map_matrix = [['.' for _ in range(self.x_len)] for _ in range(self.y_len)]
        self.draw_entities()
        self.map_matrix[0][-1] = 'P'
    
    def draw_entities(self):
        self.map_matrix[-1][0] = 'J'

    def generate_chests(self, quantity):
        for generation in range(quantity):
            x_gen = randint(0, self.x_len - 1)
            y_gen = randint(0, self.y_len - 1)
            while self.map_matrix[y_gen][x_gen] != '.':
                x_gen = randint(0, self.x_len - 1)
                y_gen = randint(0, self.y_len - 1)  
            self.map_matrix[y_gen][x_gen] = 'C'
    
    def show_map(self):
        for y in self.map_matrix:
            print(' '.join(y)) 

    def renderize(self):
        self.randomize_geometry()
        self.generate()
        self.generate_chests(3)
        self.show_map()

def main():
    map1 = Map()
    map1.renderize()

if __name__ == '__main__':
    main()