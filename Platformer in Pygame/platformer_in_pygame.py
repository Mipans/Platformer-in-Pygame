from platform import platform
import pygame
pygame.init()


# # # # # #


WIDHT, HEIGHT = 1000, 600
WIN = pygame.display.set_mode((WIDHT, HEIGHT))

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (250, 20, 5)

FPS = 60


# # # # # #


class Platform():
    def __init__(self, x, y, widht, height, colour):
        self.x = x
        self.y = y
        self.widht = widht
        self.height = height
        self.colour = colour

        self.x_end = self.x + self.widht
        self.y_end = self.y + self.height
    
    def draw(self, win):
        x = self.x + WIDHT//2
        y = HEIGHT - self.y
        shape = pygame.Rect(x, y, self.widht, self.height)
        pygame.draw.rect(win, self.colour, shape)



class Player():
    FORCE = 1
    UPFORCE = 25
    
    def __init__(self, x, y, radious, colour, up_key, left_key, right_key):
        self.x = x
        self.y = y
        self.radious = radious
        self.colour = colour
        self.up_key = up_key
        self.right_key = right_key
        self.left_key = left_key

        self.x_vel = 0
        self.y_vel = 0
    
    def draw(self, win):
        x = self.x + WIDHT//2
        y = HEIGHT - self.y + self.radious

        pygame.draw.circle(win, self.colour, (x, y), self.radious)
    
    def move(self):
        key = pygame.key.get_pressed()

        # pressing right
        if key[self.right_key] and self.x_vel > -50:
            self.x_vel -= Player.FORCE
        elif self.x_vel+Player.FORCE <= 0:
            self.x_vel += Player.FORCE
        
        # pressing left
        if key[self.left_key] and self.x_vel < 50:
            self.x_vel += Player.FORCE
        elif self.x_vel-Player.FORCE >= 0:
            self.x_vel -= Player.FORCE

        # moving
        if abs(self.x+self.x_vel)+self.radious < WIDHT//2:
            self.x += self.x_vel
        else:
            self.x_vel = 0
    
    def jump(self, platforms):
        key = pygame.key.get_pressed()
        
        if self.y > 1:
            self.y -= 1
        
        if self.y <= 1:
            self.y = 0
            if key[self.up_key]:
                self.y += 25


# # # # # #


def draw_window(players, platforms):
    WIN.fill(BLACK)

    for platform in platforms:
        platform.draw(WIN)
    for player in players:
        player.draw(WIN)

    pygame.display.update()


# # # # # #


def main():
    clock = pygame.time.Clock()
    run = True

    Player1 = Player(0, 300, 10, WHITE, pygame.K_w, pygame.K_d, pygame.K_a)
    Ground = Platform(-1*WIDHT//2, 100, WIDHT, 1, WHITE)

    players = [Player1]
    platforms = [Ground]

    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if (event.type == pygame.QUIT) or (pygame.key.get_pressed()[pygame.K_ESCAPE]):
                run = False

        for player in players:
            player.jump(platforms)
            player.move()
        draw_window(players, platforms)

    pygame.quit()


# # # # # #


if __name__ == '__main__':
    main()
