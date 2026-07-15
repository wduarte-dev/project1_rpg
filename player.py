from entity import Entity

class Player(Entity):
    def __init__(self, map_x_len, map_y_len):
        self.map_x_len : int = map_x_len
        self.map_y_len : int = map_y_len
        self.x_pos : int = 0
        self.y_pos : int = map_y_len - 1
        self.has_key : bool = False
        self.can_next_level : int = 0 # 0 -> cannot, 1 -> can, 2 -> tried and doesnt had the key

    def level_restart(self, map_x_len, map_y_len):
        self.map_x_len : int = map_x_len
        self.map_y_len : int = map_y_len
        self.x_pos : int = 0
        self.y_pos : int = map_y_len - 1
        self.has_key : bool = False
        self.can_next_level : int = 0


    def move(self, command):
        old_x_pos, old_y_pos = self.x_pos, self.y_pos
        match command:
            case 'w': self.y_pos -= 1 if self.y_pos > 0 else 0
            case 'a': self.x_pos -= 1 if self.x_pos > 0 else 0
            case 's': self.y_pos += 1 if self.y_pos < self.map_y_len - 1 else 0
            case 'd': self.x_pos += 1 if self.x_pos < self.map_x_len - 1 else 0
            case 'e': exit()
            case _: pass
        self.next_level(old_x_pos, old_y_pos)
        return (self.x_pos, self.y_pos)

    def next_level(self, old_x_pos, old_y_pos) -> None:
        if [self.x_pos, self.y_pos] == [self.map_x_len - 1, 0] and self.has_key:
            self.can_next_level = 1
        elif [self.x_pos, self.y_pos] == [self.map_x_len - 1, 0] and not self.has_key:
            self.can_next_level = 2
            self.x_pos, self.y_pos = old_x_pos, old_y_pos

