import math
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


class SemiSolid():
    def __init__(self, x, y, widht, height, colour):
        self.x = x
        self.y = y
        self.widht = widht
        self.height = height
        self.colour = colour

        self.x_end = self.x + self.widht
        self.y_end = self.y - self.height
    
    def draw(self, win):
        x = self.x + WIDHT//2
        y = HEIGHT - self.y
        shape = pygame.Rect(x, y, self.widht, self.height)
        pygame.draw.rect(win, self.colour, shape)



class Player():
    FORCE = 1
    GRAVITY = 3
    UPFORCE = 40
    
    def __init__(self, x, y, radious, colour, up_key, down_key, left_key, right_key):
        self.x = x
        self.y = y
        self.radious = radious
        self.colour = colour
        self.up_key = up_key
        self.down_key = down_key
        self.right_key = right_key
        self.left_key = left_key

        self.x_vel = 0
        self.y_vel = 0
    
    def draw(self, win):
        x = self.x + WIDHT//2
        y = HEIGHT - self.y - self.radious

        pygame.draw.circle(win, self.colour, (x, y), self.radious + 1)
    
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
        if abs(self.x+math.floor(self.x_vel))+self.radious < WIDHT//2:
            self.x += math.floor(self.x_vel)
        else:
            self.x_vel = 0
    
    def jump(self, semi_solids):
        
        def collision():
            for semi_solid in semi_solids:
                x_aligned = semi_solid.x_end >= self.x >= semi_solid.x
                under_if_fell = self.y + self.y_vel <= semi_solid.y
                above_ss = self.y > semi_solid.y
                
                if x_aligned and under_if_fell and above_ss:
                    return True
            return False
    
        key = pygame.key.get_pressed()

        if collision():
            self.y_vel = 0

        if not collision():
            self.y_vel -= Player.GRAVITY

        if collision():
            if key[self.up_key]:
                self.y_vel = Player.UPFORCE
            elif key[self.down_key]:
                self.y -= 3

        if not collision():
            self.y += round(self.y_vel)
    
    def death(self):
        if self.y < 0:
            return True
        return False


# # # # # #


def draw_window(players, semi_solids):
    WIN.fill(BLACK)

    for semi_solid in semi_solids:
        semi_solid.draw(WIN)
    for player in players:
        player.draw(WIN)

    pygame.display.update()


# # # # # #


def main():
    clock = pygame.time.Clock()
    run = True

    Player1 = Player(0, 300, 15, WHITE, pygame.K_w, pygame.K_s, pygame.K_d, pygame.K_a)
    Ground = SemiSolid(-1*WIDHT//2, 50, WIDHT, HEIGHT, WHITE)
    SemiSolid1 = SemiSolid(-100, 250, 2*WIDHT//5, 10, RED)
    SemiSolid2 = SemiSolid(-400, 400, 2*WIDHT//5, 10, (0, 255, 0))

    players = [Player1]
    semi_solids = [Ground, SemiSolid1, SemiSolid2]

    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if (event.type == pygame.QUIT) or (pygame.key.get_pressed()[pygame.K_ESCAPE]) or (Player1.death()):
                run = False

        for player in players:
            player.jump(semi_solids)
            player.move()
        draw_window(players, semi_solids)

    pygame.quit()


# # # # # #


if __name__ == '__main__':
    main()
