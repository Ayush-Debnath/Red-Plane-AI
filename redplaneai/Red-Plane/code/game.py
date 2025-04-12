import pygame, sys, time
from settings import *
from sprites import BG, Ground, Plane, Obstacle

class Game:
    def __init__(self):
        
        # setup
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Flappy Bird - Player vs Player')
        self.clock = pygame.time.Clock()
        self.active = True

        # sprite groups
        self.all_sprites = pygame.sprite.Group()
        self.collision_sprites = pygame.sprite.Group()

        # scale factor
        bg_height = pygame.image.load('graphics/environment/bg.jpg').get_height()
        self.scale_factor = WINDOW_HEIGHT / bg_height

        # sprite setup 
        BG(self.all_sprites, self.scale_factor)
        Ground([self.all_sprites, self.collision_sprites], self.scale_factor)

        # Create two planes for two players
        self.plane1 = Plane(self.all_sprites, self.scale_factor / 1.7, color="red")  # Player 1
        self.plane2 = Plane(self.all_sprites, self.scale_factor / 1.7, color="blue")  # Player 2

        # timer
        self.obstacle_timer = pygame.USEREVENT + 1
        pygame.time.set_timer(self.obstacle_timer, 1400)

        # text
        self.font = pygame.font.Font('graphics/font/BD_Cartoon_Shout.ttf', 30)
        self.score1 = 0
        self.score2 = 0
        self.start_offset = 0

        # menu
        self.menu_surf = pygame.image.load('graphics/ui/menu.png').convert_alpha()
        self.menu_rect = self.menu_surf.get_rect(center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))

        # music
        self.music = pygame.mixer.Sound('sounds/music.mp3')
        self.music.play(loops = -1)

    def collisions(self):
        # Check for collisions with obstacles and the top of the screen for both planes
        for plane in [self.plane1, self.plane2]:
            if pygame.sprite.spritecollide(plane, self.collision_sprites, False, pygame.sprite.collide_mask) or plane.rect.top <= 0:
                plane.kill()  # Player loses when they collide
                self.active = False

    def display_score(self):
        # Display scores for both players
        if self.active:
            self.score1 = (pygame.time.get_ticks() - self.start_offset) // 1000
            self.score2 = self.score1  # Both players share the same time for simplicity
            y = WINDOW_HEIGHT / 10
        else:
            y = WINDOW_HEIGHT / 2 + (self.menu_rect.height / 1.5)

        score_surf1 = self.font.render(str(self.score1), True, 'red')
        score_rect1 = score_surf1.get_rect(midtop=(WINDOW_WIDTH / 3, y))
        self.display_surface.blit(score_surf1, score_rect1)

        score_surf2 = self.font.render(str(self.score2), True, 'blue')
        score_rect2 = score_surf2.get_rect(midtop=(2 * WINDOW_WIDTH / 3, y))
        self.display_surface.blit(score_surf2, score_rect2)

    def run(self):
        last_time = time.time()
        while True:
            # delta time
            dt = time.time() - last_time
            last_time = time.time()

            # event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and self.active:  # Player 1 presses space
                        self.plane1.jump()
                    if event.key == pygame.K_RETURN and self.active:  # Player 2 presses enter
                        self.plane2.jump()
                    
                    if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                        if not self.active:
                            # Reset the game if it's over
                            self.plane1 = Plane(self.all_sprites, self.scale_factor / 1.7, color="red")
                            self.plane2 = Plane(self.all_sprites, self.scale_factor / 1.7, color="blue")
                            self.active = True
                            self.start_offset = pygame.time.get_ticks()

                if event.type == self.obstacle_timer and self.active:
                    # Generate obstacles for both players
                    Obstacle([self.all_sprites, self.collision_sprites], self.scale_factor * 1.1)

            # game logic
            self.display_surface.fill('black')
            self.all_sprites.update(dt)
            self.all_sprites.draw(self.display_surface)
            self.display_score()

            if self.active: 
                self.collisions()
            else:
                self.display_surface.blit(self.menu_surf, self.menu_rect)

            pygame.display.update()
            # self.clock.tick(FRAMERATE)

if __name__ == '__main__':
    game = Game()
    game.run()
