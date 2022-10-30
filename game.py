import pygame as pg
from time import time
from random import randint
import config
from player import Player
from egg import Egg

class Game:
    def __init__(self):
        pg.init()
        self.sc = pg.display.set_mode((config.WINDOW_WIDTH, config.WIDNDOW_HEIGHT))
        pg.display.set_caption(' nu pogodi')
        self.clock = pg.time.Clock()

        self.entities = pg.sprite.Group()
        self.eggs_sprites = pg.sprite.Group()

        self.bg = pg.image.load(config.BACKGROUND)
        self.broken_egg = pg.image.load(config.BROKEN_EGG)

        self.bg_rect = self.bg.get_rect(center=(
            config.WINDOW_WIDTH / 2,
            config.WIDNDOW_HEIGHT / 2
        ))

        self.player = Player(178, 228)
        self.entities.add(self.player)

        self.eggs = {
            'right-top': 0,
            'right-bottom': 0,
            'left-bottom': 0,
            'left-top': 0
        }

        self.positions = ('right-top', 'right-bottom', 'left-bottom', 'left-top')
        self.delay = config.DELAY
        self.score = 0
        self.lives = 3
        self.current_max_eggs = 1
        self.max_eggs = 5

        self.font = pg.font.Font('Comic-Sans-MS.ttf', config.FONT_SIZE)
        self.score_font = pg.font.Font('Comic-Sans-MS.ttf', config.FONT_SIZE * 2)

        self.new_egg_sound = pg.mixer.Sound('sound/new-egg.mp3')
        self.catch_sound = pg.mixer.Sound('sound/catch.mp3')
        self.crash_sound = pg.mixer.Sound('sound/crash.mp3')
        self.game_over_sound = pg.mixer.Sound('sound/game-over.mp3')
        pg.mixer.music.load('sound/soundtrack.mp3')
        pg.mixer.music.play(-1)

    def make_egg(self, position):
        count = min(self.current_max_eggs, self.max_eggs)
        if position in self.eggs and self.eggs[position] < count:
            return Egg(self, position)

    def count_eggs(self):
        self.eggs['right-top'] = 0
        self.eggs['right-bottom'] = 0
        self.eggs['left-bottom'] = 0
        self.eggs['left-top'] = 0
        for egg in self.eggs_sprites:
            self.eggs[egg.position] += 1

    def check_events(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_w] or keys[pg.K_UP]:
            self.player.change_pos(y='top')
        elif keys[pg.K_d] or keys[pg.K_RIGHT]:
            self.player.change_pos(x='right')
        elif keys[pg.K_s] or keys[pg.K_DOWN]:
            self.player.change_pos(y='bottom')
        elif keys[pg.K_a] or keys[pg.K_LEFT]:
            self.player.change_pos(x='left')
        for event in pg.event.get():
            if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE or event.type == pg.QUIT:
                pg.quit()

    def render_score(self):
        score = self.score_font.render(str(self.score), 1, (20, 20, 20))
        self.sc.blit(score, (660, 50))

    def render_hp(self):
        for i in range(abs(self.lives - 3)):
            self.sc.blit(self.broken_egg, (320 + i * 80, 50))
        
    def game_over(self):
        pg.mixer.music.pause()
        self.game_over_sound.play()

        self.sc.fill(config.BACKGROUND_COLOR)

        text1 = self.font.render(f'Счёт: {self.score}', 1, (20, 20, 20))
        text2 = self.font.render('Чтобы начать с начала, нажмите пробел..', 1, (20, 20, 20))

        rect1 = text1.get_rect(center=(
            config.WINDOW_WIDTH / 2,
            config.WIDNDOW_HEIGHT / 2 - 25
        ))
        rect2 = text2.get_rect(center=(
            config.WINDOW_WIDTH / 2,
            config.WIDNDOW_HEIGHT / 2 + 25
        ))

        self.sc.blit(text1, rect1)
        self.sc.blit(text2, rect2)
        pg.display.flip()
        wait = True
        while wait:
            for event in pg.event.get():
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_SPACE:
                        self.restart()
                        wait = False
                    elif event.key == pg.K_ESCAPE:
                        pg.quit()
                elif event.type == pg.QUIT:
                    pg.quit()
            self.clock.tick(config.FPS)
            
    def restart(self):
        self.delay = config.DELAY
        self.score = 0
        self.lives = 3
        self.eggs_sprites.empty()
        pg.mixer.music.load('sound/soundtrack.mp3')
        pg.mixer.music.play(-1)
        pg.mixer.music.unpause()

    def run(self):
        last_time = time()
        while True:
            self.delay = max(1. / max(config.SPEED ** (self.score // 42 + 1), 1), 0.5)
            self.current_max_eggs = max(1, self.score // 15 + 1)
            self.check_events()
            if self.lives <= 0:
                self.game_over()

            self.sc.fill(config.BACKGROUND_COLOR)
            self.sc.blit(self.bg, self.bg_rect)

            if abs(time() - last_time) >= self.delay:
                last_time = time()
                egg = self.make_egg(self.positions[randint(0, 3)])
                if egg:
                    self.eggs_sprites.add(egg)
                    self.new_egg_sound.play()

            self.count_eggs()

            self.entities.draw(self.sc)
            self.eggs_sprites.draw(self.sc)
            self.entities.update()
            self.eggs_sprites.update()
            self.render_hp()
            self.render_score()
            pg.display.flip()
            self.clock.tick(config.FPS)
