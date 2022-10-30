from pygame.sprite import Sprite
from pygame.image import load
import config

class Player(Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = load(config.PLAYER[1])
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.position = 'right-bottom'
        self.position_x = 'right'
        self.position_y = 'bottom'
        self.positions = {
            'right-top': load(config.PLAYER[0]),
            'right-bottom': load(config.PLAYER[1]),
            'left-bottom': load(config.PLAYER[2]),
            'left-top': load(config.PLAYER[3])
        }

    def change_pos(self, x=None, y=None):
        if x:
            self.position_x = x
        if y:
            self.position_y = y
        self.position = f'{self.position_x}-{self.position_y}'
        self.image = self.positions[self.position]        
