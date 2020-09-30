import pygame
import random

pygame.init()
win = pygame.display.set_mode((500, 500))
pygame.display.set_caption("Snaek")


class cube:
    width = 500
    rows = 20

    def __init__(self, start, color=(0, 255, 0)):
        self.pos = start
        self.color = color
        self.dirx = 1
        self.diry = 0
        self.eyes = False

    def move(self, dirx, diry):
        self.dirx = dirx
        self.diry = diry
        self.pos = (self.pos[0] + self.dirx, self.pos[1] + self.diry)

    def draw(self, win):
        dis = self.width // self.rows
        i = self.pos[0]
        j = self.pos[1]
        pygame.draw.rect(win, self.color, (i * dis + 1, j * dis + 1, dis - 2, dis - 2))

        if self.eyes:
            centre = dis // 2
            radius = 3
            circleMiddle = (i * dis + centre - radius, j * dis + 8)
            circleMiddle2 = (i * dis + dis - radius * 2, j * dis + 8)
            pygame.draw.circle(win, (0, 0, 0), circleMiddle, radius)
            pygame.draw.circle(win, (0, 0, 0), circleMiddle2, radius)


class snaek:
    body = []
    turns = {}

    def __init__(self, color, pos):
        self.color = color
        self.head = cube(pos)
        self.body.append(self.head)
        self.dirx = 1
        self.diry = 0
        self.score = 0

    def move(self):

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.dirx = -1
            self.diry = 0
            self.turns[self.head.pos[:]] = [self.dirx, self.diry]

        elif keys[pygame.K_RIGHT]:
            self.dirx = 1
            self.diry = 0
            self.turns[self.head.pos[:]] = [self.dirx, self.diry]

        elif keys[pygame.K_DOWN]:
            self.dirx = 0
            self.diry = 1
            self.turns[self.head.pos[:]] = [self.dirx, self.diry]

        elif keys[pygame.K_UP]:
            self.dirx = 0
            self.diry = -1
            self.turns[self.head.pos[:]] = [self.dirx, self.diry]

        for i, c in enumerate(self.body):
            p = c.pos[:]
            if p in self.turns:
                turn = self.turns[p]
                c.move(turn[0], turn[1])
                if i == len(self.body) - 1:
                    self.turns.pop(p)

            else:
                if c.dirx == -1 and c.pos[0] <= 0:
                    c.pos = (c.rows - 1, c.pos[1])
                elif c.dirx == 1 and c.pos[0] >= c.rows - 1:
                    c.pos = (0, c.pos[1])
                elif c.diry == -1 and c.pos[1] <= 0:
                    c.pos = (c.pos[0], c.rows - 1)
                elif c.diry == 1 and c.pos[1] >= c.rows - 1:
                    c.pos = (c.pos[0], 0)
                else:
                    c.move(c.dirx, c.diry)

    def AddCube(self):
        tail = self.body[-1]
        if tail.dirx == 1 and tail.diry == 0:
            nstart = (tail.pos[0] - 1, tail.pos[1])
        elif tail.dirx == -1 and tail.diry == 0:
            nstart = (tail.pos[0] + 1, tail.pos[1])
        elif tail.dirx == 0 and tail.diry == 1:
            nstart = (tail.pos[0], tail.pos[1] - 1)
        elif tail.dirx == 0 and tail.diry == -1:
            nstart = (tail.pos[0], tail.pos[1] + 1)
        self.body.append(cube(nstart))
        self.body[-1].dirx = tail.dirx
        self.body[-1].diry = tail.diry

    def Reset(self):
        self.pos = (5, 5)
        s.head = cube(self.pos)
        self.dirx = 1
        self.diry = 0
        self.body = []
        self.body.append(s.head)
        self.turns = {}
        self.score = 0

    def draw(self, win):
        for i, c in enumerate(self.body):
            if i == 0:
                c.eyes = True
                c.draw(win)
            else:
                c.draw(win)


def GameOver(win):
    win.fill((0, 0, 0))
    font1 = pygame.font.Font("ARCADE.TTF", 80)
    go_txt = font1.render("GAME OVER",True,(255,255,255))
    win.blit(go_txt,(75,50))
    font2 = pygame.font.Font("ARCADE.TTF", 50)
    score_txt = font2.render("SCORE: " + str(final_score), True, (255, 255, 255))
    win.blit(score_txt, (150, 180))
    font3 = pygame.font.Font("ARCADE.TTF", 30)
    press_space_txt = font3.render("PRESS SPACE TO RESTART", True, (255, 255, 255))
    win.blit(press_space_txt, (80, 350))
    pygame.display.update()


def Respawnfruit():
    x = random.randint(0, 19)
    y = random.randint(0, 19)
    return (x, y)


def drawgrid(width, rows, win):
    dist = round(width / rows)
    x = 0
    y = 0
    for r in range(rows):
        x = x + dist
        y = y + dist
        pygame.draw.line(win, (255, 255, 255), (x, 0), (x, width))
        pygame.draw.line(win, (255, 255, 255), (0, y), (width, y))


def redraw():
    global width, rows, s
    win.fill((0, 0, 0))
    s.draw(win)
    drawgrid(width, rows, win)
    fruit.draw(win)
    pygame.display.update()


def main():
    global width, rows, s, fruit, playing, running
    running = True
    width = 500
    rows = 20
    s = snaek((0, 255, 0), (5, 5))
    fruitx = random.randint(0, rows - 1)
    fruity = random.randint(0, rows - 1)
    fruit = cube((fruitx, fruity), (255, 0, 0))
    playing = True
    clock = pygame.time.Clock()

    while running:
        if playing:
            pygame.time.delay(100)
            clock.tick(10)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            s.move()
            if s.body[0].pos == fruit.pos:
                print("omer is the king")
                s.score += 1
                s.AddCube()
                fruit = cube(Respawnfruit(), (255, 0, 0))
            CubesPos = []
            for c in s.body:
                if c == s.body[0]:
                    pass
                else:
                    CubesPos.append(c.pos)
            if s.head.pos in CubesPos:
                global final_score
                final_score = s.score
                s.Reset()
                playing = False

            redraw()
        if not playing:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                playing = True
            else:
                GameOver(win)


main()
