from entity import Entity
from random import choices, randint
class DrunkEnemy(Entity):
    def __init__(self, map_x_len, map_y_len, x_pos=0, y_pos=0):
        self.x_pos : int = x_pos
        self.y_pos : int = y_pos
        self.map_x_len : int = map_x_len
        self.map_y_len : int = map_y_len

    def move(self, command=None) -> tuple:
        moves = ['up', 'down', 'left', 'right']
        command = choices(moves, k=1)[0]
        match command:
            case 'up': self.y_pos -= 1 if self.y_pos > 0 else 0
            case 'down': self.y_pos += 1 if self.y_pos < self.map_y_len - 1 else 0
            case 'left': self.x_pos -= 1 if self.x_pos > 0 else 0
            case 'right': self.x_pos += 1 if self.x_pos < self.map_x_len - 1 else 0
        return (self.x_pos, self.y_pos)
        
        
class SmartEnemy(Entity):
    def __init__(self, map_x_len, map_y_len, x_pos=0, y_pos=0):
        self.x_pos : int = x_pos
        self.y_pos : int = y_pos
        self.map_x_len : int = map_x_len
        self.map_y_len : int = map_y_len

    def move(self, command=(0, 0)) -> tuple: # command is a tuple of player's position
        do_nothing = choices([True, False], weights=[25, 75], k=1)[0]
        if do_nothing:
            return (self.x_pos, self.y_pos)
        if command[1] == self.y_pos and command[0] < self.x_pos:
            self.x_pos -= 1 if self.x_pos > 0 else 0
        elif command[1] == self.y_pos and command[0] > self.x_pos:
            self.x_pos += 1 if self.x_pos < self.map_x_len - 1 else 0
        if command[0] == self.x_pos and command[1] < self.y_pos:
            self.y_pos -= 1 if self.y_pos > 0 else 0
        elif command[0] == self.x_pos and command[1] > self.y_pos:
            self.y_pos += 1 if self.y_pos < self.map_y_len - 1 else 0
        if command[0] < self.x_pos and command[1] < self.y_pos:
            moves = randint(0, 1)
            if moves == 0:
                self.x_pos -= 1 if self.x_pos > 0 else 0
            else:
                self.y_pos -= 1 if self.y_pos > 0 else 0
        elif command[0] < self.x_pos and command[1] > self.y_pos:
            moves = randint(0, 1)
            if moves == 0:
                self.x_pos -= 1 if self.x_pos > 0 else 0
            else:
                self.y_pos += 1 if self.y_pos < self.map_y_len - 1 else 0
        if command[0] > self.x_pos and command[1] < self.y_pos:
            moves = randint(0, 1)
            if moves == 0:
                self.x_pos += 1 if self.x_pos < self.map_x_len - 1 else 0
            else:
                self.y_pos -= 1 if self.y_pos > 0 else 0
        elif command[0] > self.x_pos and command[1] > self.y_pos:
            moves = randint(0, 1)
            if moves == 0:
                self.x_pos += 1 if self.x_pos < self.map_x_len - 1 else 0
            else:
                self.y_pos += 1 if self.y_pos < self.map_y_len - 1 else 0
        return (self.x_pos, self.y_pos)

        