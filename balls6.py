import pygame
import random
from random import randint
from random import choice
import math

# Define some colors
BACKGROUND_COLOR = (255, 255, 255)
# BALL_COLOR = (0, 0, 0)

SCREEN_WIDTH = 700
SCREEN_HEIGHT = 500
# BALL_SIZE = 25
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


class Ball:

    def __init__(self, x, y, radius=randint(20, 45)):
        self.x = x
        self.y = y
        self.radius = radius
        self.randomize()
        self.max_x = SCREEN_WIDTH - self.radius
        self.max_y = SCREEN_HEIGHT - self.radius
        self.min_x = self.radius

    def randomize(self):
        r = randint(0, 255)
        g = randint(0, 255)
        b = randint(0, 255)
        self.color = (r, g, b)
        self.dx = randint(-3, 3)
        self.dy = randint(-3, 3)

    def move(self):
        # minim = self.radius
        # max_x = SCREEN_WIDTH - self.radius
        # max_y = SCREEN_HEIGHT - self.radius
        self.x = constrain(self.min_x, self.x + self.dx, self.max_x)
        self.y = constrain(self.min_x, self.y + self.dy, self.max_y)
        if self.x == self.max_x or self.x == self.min_x:
            self.dx *= -1
        if self.y == self.max_y or self.y == self.min_x:
            self.dy *= -1

    def draw(self, scr=screen):

        pygame.draw.circle(scr, self.color,
                           (self.x, self.y), self.radius)


class Player(Ball):

    def __init__(self):
        self.x = SCREEN_WIDTH // 2
        self.y = SCREEN_HEIGHT // 2
        self.radius = 10
        self.color = (0, 0, 0)
        self.dx = 0
        self.dy = 0
        self.max_x = SCREEN_WIDTH - self.radius
        self.max_y = SCREEN_HEIGHT - self.radius
        self.min_x = self.radius

    def move(self):
        # minim = self.radius
        # max_x = SCREEN_WIDTH - self.radius
        # max_y = SCREEN_HEIGHT - self.radius
        self.x = constrain(self.min_x, self.x + self.dx, self.max_x)
        self.y = constrain(self.min_x, self.y + self.dy, self.max_y)


class SleepingBalls(Ball):
    color = (250, 0, 0)
    radius = 15

    def __init__(self, x, y):
        speed = randint(8, 12)
        self.x = x
        self.y = y
        self.dx = choice((-1, 1)) * speed
        self.dy = choice((-1, 1)) * speed
        self.max_x = SCREEN_WIDTH - self.radius
        self.max_y = SCREEN_HEIGHT - self.radius
        self.min_x = self.radius

    def move(self):
        # minim = self.radius
        # max_x = SCREEN_WIDTH - self.radius
        # max_y = SCREEN_HEIGHT - self.radius
        self.x = constrain(self.min_x, self.x + self.dx, self.max_x)
        self.y = constrain(self.min_x, self.y + self.dy, self.max_y)
        if self.x == self.max_x or self.x == self.min_x:
            self.dx *= -1
        if self.y == self.max_y or self.y == self.min_x:
            self.dy *= -1

    def sleep(self):
        self.x = 0
        self.y = 0



def main():
    pygame.init()

    counter = 0
    # screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Balls")

    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()

    balls = []

    player = Player()

    sleeping_balls = SleepingBalls(0, 0)

    for i in range(1, 5):
        balls.append(Ball(100 * i, 100 * i))

    move_x, move_y = 0, 0

    # Loop until the user clicks the close button or ESC.
    done = False
    while not done:
        # Limit number of frames per second
        clock.tick(60)

        # Event Processing
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    done = True
                elif event.key == pygame.K_r:
                    balls[randint(0, len(balls) - 1)].randomize()
                elif event.key == pygame.K_a:
                    balls.append(Ball(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                                      5 * randint(1, 10)))
                elif event.key == pygame.K_s:
                    balls.append(SleepingBalls(0, 0))
                    counter += 1

        player.dx = 0
        player.dy = 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player.dx = -2
        if keys[pygame.K_RIGHT]:
            player.dx = 2
        if keys[pygame.K_UP]:
            player.dy = -2
        if keys[pygame.K_DOWN]:
            player.dy = 2

        for ball in balls:
            ball.move()

        player.move()
        #sleeping_balls.move()

        if counter == 100:
            sleeping_balls.sleep()

        # Draw everything
        screen.fill(BACKGROUND_COLOR)

        for ball in balls:
            # pygame.draw.circle(screen, ball.color,
            #                    (ball.x, ball.y), ball.radius)
            ball.draw()
        # pygame.draw.circle(screen, player.color,
        #                    (player.x, player.y), player.radius)
        player.draw()

        #sleeping_balls.draw()
        # Update the screen
        pygame.display.flip()

    # Close everything down
    pygame.quit()


def constrain(small, value, big):
    """Return a new value which isn't smaller than small or larger than big"""
    # TODO: Should use "small" as well.
    return max(min(value, big), small)


if __name__ == "__main__":
    main()
