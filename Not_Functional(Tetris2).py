import pygame
import random

BLACK, WHITE, GRAY = (0, 0, 0), (255, 255, 255), (128, 128, 128)

# Define colors
colors = [
    (0, 0, 0),
    (120, 37, 179),
    (100, 179, 179),
    (80, 34, 22),
    (80, 134, 22),
    (180, 34, 22),
    (180, 34, 122),
]

class Tetris:
    def __init__(self, height, width):
        self.height, self.width = height, width
        self.field = [[0] * width for _ in range(height)]
        self.score, self.state, self.figure = 0, "start", None

    def new_figure(self):
        self.figure = Figure(3, 0)

    def intersects(self):
        return any(
            i + self.figure.y > self.height - 1
            or j + self.figure.x > self.width - 1
            or j + self.figure.x < 0
            or self.field[i + self.figure.y][j + self.figure.x] > 0
            for i in range(4)
            for j in range(4)
            if i * 4 + j in self.figure.image()
        )

    def break_lines(self):
        lines = sum(1 for row in self.field[1:] if all(row))
        self.field = [[0] * self.width] * lines + self.field[:-lines]

    def go_space(self):
        while not self.intersects():
            self.figure.y += 1
        self.figure.y -= 1
        self.freeze()

    def go_down(self):
        self.figure.y += 1
        if self.intersects():
            self.figure.y -= 1
            self.freeze()

    def freeze(self):
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.figure.image():
                    self.field[i + self.figure.y][j + self.figure.x] = self.figure.color
        self.break_lines()
        self.new_figure()
        if self.intersects():
            self.state = "gameover"

    def go_side(self, dx):
        old_x = self.figure.x
        self.figure.x += dx
        if self.intersects():
            self.figure.x = old_x

    def rotate(self):
        old_rotation = self.figure.rotation
        self.figure.rotate()
        if self.intersects():
            self.figure.rotation = old_rotation

class Figure:
    figures = [
        [[1, 5, 9, 13], [4, 5, 6, 7]],
        [[4, 5, 9, 10], [2, 6, 5, 9]],
        [[6, 7, 9, 10], [1, 5, 6, 10]],
        [[1, 2, 5, 9], [0, 4, 5, 6], [1, 5, 9, 8], [4, 5, 6, 10]],
        [[1, 2, 6, 10], [5, 6, 7, 9], [2, 6, 10, 11], [3, 5, 6, 7]],
        [[1, 4, 5, 6], [1, 4, 5, 9], [4, 5, 6, 9], [1, 5, 6, 9]],
        [[1, 2, 5, 6]],
    ]

    def __init__(self, x, y):
        self.x, self.y = x, y
        self.type = random.randint(0, len(self.figures) - 1)
        self.color, self.rotation = random.randint(1, len(colors) - 1), 0

    def image(self):
        return self.figures[self.type][self.rotation]

    def rotate(self):
        self.rotation = (self.rotation + 1) % len(self.figures[self.type])

pygame.init()

size, fps, clock, game = (400, 500), 15, pygame.time.Clock(), Tetris(20, 10)
counter, pressing_down = 0, False

while True:
    if not game.figure:
        game.new_figure()
    counter += 1

    if counter % (fps // game.level // 2) == 0 or pressing_down:
        if game.state == "start":
            game.go_down()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                game.rotate()
            if event.key == pygame.K_DOWN:
                pressing_down = True
            if event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                game.go_side(-1 if event.key == pygame.K_LEFT else 1)
            if event.key == pygame.K_SPACE:
                game.go_space()
            if event.key == pygame.K_ESCAPE:
                game.__init__(20, 10)

        if event.type == pygame.KEYUP and event.key == pygame.K_DOWN:
            pressing_down = False

    screen.fill(WHITE)

    for i in range(game.height):
        for j in range(game.width):
            pygame.draw.rect(
                screen,
                GRAY,
                [game.x + game.zoom * j, game.y + game.zoom * i, game.zoom, game.zoom],
                1,
            )
            if game.field[i][j]:
                pygame.draw.rect(
                    screen,
                    colors[game.field[i][j]],
                    [
                        game.x + game.zoom * j + 1,
                        game.y + game.zoom * i + 1,
                        game.zoom - 2,
                        game.zoom - 1,
                    ],
                )

    if game.figure:
        for i in range(4):
            for j in range(4):
                p = i * 4 + j
                if p in game.figure.image():
                    pygame.draw.rect(
                        screen,
                        colors[game.figure.color],
                        [
                            game.x + game.zoom * (j + game.figure.x) + 1,
                            game.y + game.zoom * (i + game.figure.y) + 1,
                            game.zoom - 2,
                            game.zoom - 2,
                        ],
                    )

    font, font1, font3 = pygame.font.SysFont("Calibri", 25, True, False), pygame.font.SysFont("Calibri", 65, True, False), pygame.font.SysFont("Calibri", 15, True, False)
    text, text1, text2, text3, text4 = font.render("Score: " + str(game.score), True, BLACK), font3.render("<- move left", True, BLACK), font3.render("-> move right", True, BLACK), font3.render("down arrow move down", True, BLACK), font3.render("up arrow rotate block", True, BLACK)
    text_game_over, text_game_over1 = font1.render("Game Over", True, (255, 125, 0)), font1.render("Press ESC", True, (255, 215, 0))

    screen.blit(text, [0, 0])
    screen.blit(text1, [0, 25])
    screen.blit(text2, [0, 50

])
    screen.blit(text3, [0, 75])
    screen.blit(text4, [0, 100])

    if game.state == "gameover":
        screen.blit(text_game_over, [20, 200])
        screen.blit(text_game_over1, [25, 265])

    pygame.display.flip()
    clock.tick(fps)
