import pygame
import random
import math
import neat
import os

pygame.init()

GEN = -1
class player:
    def __init__(self, x_pos, y_pos):
        self.img = pygame.image.load("rocket.png")
        self.img_angle = -45
        self.rotated_img = self.img
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.vel = 2.5
        self.gravity = -2
        self.radius = self.img.get_rect().center[0]
        self.score = 0
        self.isjUMP = False
        self.IsGameOver = False

    def move(self):
        # keys = pygame.key.get_pressed()
        # if keys[pygame.K_SPACE]:
        #     self.y_pos -= self.vel
        #     if self.img_angle <= 0:
        #         self.img_angle += 1

        self.y_pos -= self.gravity
        if self.img_angle > -70:
            self.img_angle -= 1

        # if 551 < self.y_pos or self.y_pos < -15:
        #     self.IsGameOver = True
    def jump(self):
        self.y_pos -= self.vel
        if self.img_angle <= 0:
            self.img_angle += 1

    def Rest(self):
        self.score = 0
        self.y_pos = 300
        self.IsGameOver = False

    def draw(self, win):
        self.rotated_img = pygame.transform.rotate(self.img, self.img_angle)
        win.blit(self.rotated_img, (self.x_pos, self.y_pos))


class obsticle:

    def __init__(self, index, x_pos, y_pos, vel):
        self.img = stars_img[index]
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.radius = self.img.get_rect().center[0]
        self.vel = vel

    def move(self):
        self.x_pos += self.vel

    def draw(self, win):
        win.blit(self.img, (self.x_pos, self.y_pos))


class BackGround:
    def __init__(self, img, start_x):
        self.img = img
        self.start_x = start_x

    def Scroolbackground(self, win):
        rel_x = self.start_x % self.img.get_rect().width
        win.blit(self.img, (rel_x - self.img.get_rect().width, 0))
        if rel_x < 800:
            win.blit(self.img, (rel_x, 0))
        self.start_x -= 1


def Collition(rocket, star):
    rocket_mask = pygame.mask.from_surface(rocket.img)
    star_mask = pygame.mask.from_surface(star.img)
    offset = (round(rocket.x_pos - star.x_pos), round(rocket.y_pos - star.y_pos))
    result = star_mask.overlap(rocket_mask, offset)

    if result:
        return True


def GameOver(win):
    win.fill((0, 0, 0))
    font1 = pygame.font.Font("ARCADE.TTF", 80)
    go_txt = font1.render("GAME OVER", True, (255, 255, 255))
    win.blit(go_txt, (200, 50))
    font2 = pygame.font.Font("ARCADE.TTF", 50)
    # score_txt = font2.render("SCORE: " + str(rocket.score), True, (255, 255, 255))
    win.blit(score_txt, (300, 180))
    font3 = pygame.font.Font("ARCADE.TTF", 30)
    press_space_txt = font3.render("PRESS SPACE TO RESTART", True, (255, 255, 255))
    win.blit(press_space_txt, (220, 350))
    pygame.display.update()


def Draw(win):
    win.fill((0, 0, 0))
    BG.Scroolbackground(win)
    for rocket in rockets:
        rocket.draw(win)
    for star in stars:
        star.draw(win)
    win.blit(gen_txt, (10, 10))
    pygame.display.update()


def main(genomes, config):
    global BG, start_x, rockets, stars_img, stars, score_txt, GEN, gen_txt
    nets = []
    ge = []
    rockets = []
    GEN += 1
    for _, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        rockets.append(player(150, 400))
        g.fitness = 0
        ge.append(g)


    win = pygame.display.set_mode((800, 600))
    pygame.time.delay(50)
    BG = BackGround(pygame.image.load("space_BG2.jpg").convert(), 0)
    stars_img = [pygame.image.load("planets/p0.png"), pygame.image.load("planets/p1.png"),
                 pygame.image.load("planets/p2.png"), pygame.image.load("planets/p3.png"),
                 pygame.image.load("planets/p4.png"), pygame.image.load("planets/p5.png"),
                 pygame.image.load("planets/p6.png"), ]
    font = pygame.font.Font("ARCADE.TTF", 70)
    gen_txt = font.render("GEN:: " + str(GEN), True, (255, 255, 255))
    stars = []
    star_vel = -1
    running = True

    while running:
        # if not rocket.IsGameOver:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            star_index = 0
            if len(rockets) > 0 and len(stars) > 0:
                if rockets[0].x_pos > stars[0].x_pos + stars[0].img.get_width():
                    star_index = 1
            elif len(rockets) == 0:
                break


            if len(stars) == 0:
                stars.append(obsticle(random.randint(0, 6), 750, random.randint(-50, 520), star_vel))
            elif len(stars) < 2 and stars[-1].x_pos <= 500:
                star_vel -= 0.07
                stars.append(obsticle(random.randint(0, 6), 1000, random.randint(-50, 520), star_vel))

            for x, rocket in enumerate(rockets):
                rocket.move()
                ge[x].fitness += 0.1

                output = nets[x].activate((rocket.y_pos, (rocket.y_pos - stars[star_index].y_pos + stars[star_index].radius), (rocket.x_pos - stars[star_index].x_pos) + stars[star_index].radius))


                if output[0] > 0.5:
                    rocket.jump()

            for star in stars:
                star.move()
                # rocket_center = (rocket.x_pos + rocket.radius, rocket.y_pos + rocket.radius)
                # star_center = (star.x_pos + star.radius, star.y_pos + star.radius)
                for x, rocket in enumerate(rockets):
                    if Collition(rocket, star):
                        ge[x].fitness -= 10
                        rockets.pop(x)
                        nets.pop(x)
                        ge.pop(x)

                if star.x_pos <= -80:
                    # rocket.score += 1
                    for g in ge:
                        g.fitness += 5
                    # score_txt = font.render("Score: " + str(rocket.score), True, (255, 255, 255))
                    stars.pop(0)
            for x, rocket in enumerate(rockets):
                if 551 < rocket.y_pos or rocket.y_pos < -15:
                    rockets.pop(x)
                    nets.pop(x)
                    ge.pop(x)


            Draw(win)

        # elif rocket.IsGameOver:
        #     GameOver(win)
        #     for event in pygame.event.get():
        #         if event.type == pygame.QUIT:
        #             running = False
        #         keys = pygame.key.get_pressed()
        #         if keys[pygame.K_SPACE]:
        #             stars = []
        #             star_vel = -1
        #             rocket.Rest()
        #             score_txt = font.render("Score: " + str(rocket.score), True, (255, 255, 255))


def run(config_path):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet,
                                neat.DefaultStagnation, config_path)
    pop = neat.Population(config)

    pop.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    pop.add_reporter(stats)

    winner = pop.run(main, 50)


if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config.txt")
    run(config_path)
