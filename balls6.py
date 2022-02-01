import pygame
from random import randint
from random import choice


# Define some colors
BACKGROUND_COLOR = (255, 255, 255)


SCREEN_WIDTH = 700
SCREEN_HEIGHT = 500

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


class Ball:
    def __init__(self, x, y, radius=None): # hoping the user won't enter None
        self.x = x
        self.y = y
        if radius == None:
            self.radius = 5 * randint(1, 10)
        else:
            self.radius = radius
        self.randomize()
        self._max_x = SCREEN_WIDTH - self.radius
        self._max_y = SCREEN_HEIGHT - self.radius
        self._min_x = self.radius

    def randomize(self):
        r = randint(0, 255)
        g = randint(0, 255)
        b = randint(0, 255)
        self.color = (r, g, b)
        self.dx = randint(-3, 3)
        self.dy = randint(-3, 3)

    def move(self):
        self.x = constrain(self._min_x, self.x + self.dx, self._max_x)
        self.y = constrain(self._min_x, self.y + self.dy, self._max_y)
        if self.x == self._max_x or self.x == self._min_x:
            self.dx *= -1
        if self.y == self._max_y or self.y == self._min_x:
            self.dy *= -1

    def draw(self, scr=screen):
        pygame.draw.circle(scr, self.color,
                           (self.x, self.y), self.radius)


class Player(Ball):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        self.color = (0, 0, 0)
        self.dx = 0
        self.dy = 0


class SleepingBalls(Ball):
    sleeping = 0

    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        self.speed = randint(8, 12)
        self.dx = choice((-1, 1)) * self.speed
        self.dy = choice((-1, 1)) * self.speed
        self.color = (250, 0, 0)

    def randomize(self):
        pass

    def move(self):
        if self.sleeping > 0:
            self.sleeping -= 1
            if self.sleeping == 0:
                self.dx = choice((-1, 1)) * self.speed
                self.dy = choice((-1, 1)) * self.speed
        else:
            self.x = constrain(self._min_x, self.x + self.dx, self._max_x)
            self.y = constrain(self._min_x, self.y + self.dy, self._max_y)
            if self.x == self._max_x or self.x == self._min_x:
                self.dx *= -1
            if self.y == self._max_y or self.y == self._min_x:
                self.dy *= -1
            if randint(0, 100) < 1:
                self.sleeping = 100


def main():
    pygame.init()
    pygame.display.set_caption("Balls")

    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()

    balls = []
    player = Player(x=SCREEN_WIDTH // 2, y=SCREEN_HEIGHT // 2, radius=10)

    for i in range(1, 5):
        balls.append(Ball(100 * i, 100 * i))

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
                    balls.append(SleepingBalls(0, 0, 15))

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

        # Draw everything
        screen.fill(BACKGROUND_COLOR)

        for ball in balls:
            ball.draw()

        player.draw()

        # Update the screen
        pygame.display.flip()

    # Close everything down
    pygame.quit()


def constrain(small, value, big):
    """Return a new value which isn't smaller than small or larger than big"""
    return max(min(value, big), small)


if __name__ == "__main__":
    main()
