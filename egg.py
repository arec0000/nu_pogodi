from pygame.sprite import Sprite
from pygame.image import load
from pygame.transform import flip, rotate
from time import time
import config

class Egg(Sprite):
    def __init__(self, game_class, position):
        super().__init__()
        self.game = game_class
        self.image = load(config.EGG[0])
        self.rect = self.image.get_rect()

        self.images_left = [load(path) for path in config.EGG]

        self.images_right = self.images_left.copy()
        for img in self.images_right:
            flip(img, 1, 0)

        chick_left = ((160, 480), (132, 480), (96, 480), (62, 480), (38, 480))
        chick_right = ((720, 480), (760, 480), (826, 480), (860, 480), (920, 480))

        right_top = ((884, 182), (840, 200), (806, 222), (770, 254), (730, 258))
        right_bottom = ((880, 320), (840, 334), (804, 356), (770, 384), (730, 390))
        left_bottom = ((76, 318), (96, 332), (126, 351), (166, 378), (190, 384))
        left_top = ((80, 188), (100, 202), (131, 222), (170, 247), (200, 248))

        self.animations = {
            'right-top': [(x, self.images_left[0]) for x in right_top] + \
                [(x, y) for x, y in zip(chick_right, self.images_right[1:])],
            'right-bottom': [(x, self.images_left[0]) for x in right_bottom] + \
                [(x, y) for x, y in zip(chick_right, self.images_right[1:])],
            'left-bottom': [(x, self.images_left[0]) for x in left_bottom] + \
                [(x, y) for x, y in zip(chick_left, self.images_left[1:])],
            'left-top': [(x, self.images_left[0]) for x in left_top] + \
                [(x, y) for x, y in zip(chick_left, self.images_left[1:])]
        }

        self.right_angle = 30
        self.left_angle = -30
        self.position = position
        self.animation = self.animate(position)
        self.rect.x = self.animation[0][0][0]
        self.rect.y = self.animation[0][0][1]
        self.state = 0
        self.dropped = False
        self.time = time()

    def animate(self, position):
        if position in self.animations:
            return self.animations[position]

    def update(self):
        if self.state == 4 and self.position == self.game.player.position:
            self.game.score += 1
            self.game.catch_sound.play()
            self.kill()
        if self.state > 4 and not self.dropped:
            self.dropped = True
            self.game.lives -= 1
            self.game.crash_sound.play()
        if self.state > 10:
            return self.kill()
        if abs(self.time - time()) >= config.DELAY and not self.dropped:
            self.time = time()
            self.state += 1
        elif abs(self.time - time()) >= 0.2 and self.dropped:
            self.time = time()
            self.state += 1
        (x, y), img = self.animation[min(self.state, 9)]
        self.image = img
        self.rect.x = x
        self.rect.y = y
        if self.state <= 4:
            if self.position == 'right-top' or self.position == 'right-bottom':
                self.image = rotate(self.image, self.left_angle * self.state)
            else:
                self.image = rotate(self.image, self.right_angle * self.state)
                