from entity import Entity

class Player(Entity):
    def __init__(self, y_len):
        self.y_len : int = 0
        self.x_pos : int = 0
        self.y_pos : int = y_len - 1
        self.has_key = False

    def move(self, command, x_max, y_max):
        match command:
            case 'w': self.y_pos -= 1 if self.y_pos > 0 else 0
            case 'a': self.x_pos -= 1 if self.x_pos > 0 else 0
            case 's': self.y_pos += 1 if self.y_pos < y_max - 1 else 0
            case 'd': self.x_pos += 1 if self.x_pos < x_max - 1 else 0
            case _: pass

