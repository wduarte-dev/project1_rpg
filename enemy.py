from entity import Entity
from random import choices
class DrunkEnemy(Entity):
    def __init__(self, map_x_len, map_y_len, x_pos=0, y_pos=0):
        self.x_pos : int = x_pos
        self.y_pos : int = y_pos
        self.map_x_len : int = map_x_len
        self.map_y_len : int = map_y_len

    def move(self, command=None) -> tuple:
        moves = ['up', 'down', 'left', 'right']
        selected_move = choices(moves, k=1)[0]
        match selected_move:
            case 'up': self.y_pos -= 1 if self.y_pos > 0 else 0
            case 'down': self.y_pos += 1 if self.y_pos < self.map_y_len - 1 else 0
            case 'left': self.x_pos -= 1 if self.x_pos > 0 else 0
            case 'right': self.x_pos += 1 if self.x_pos < self.map_x_len - 1 else 0
        return (self.x_pos, self.y_pos)
        