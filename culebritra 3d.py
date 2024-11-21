import math
import random
import pygame
import tkinter as tk
from tkinter import messagebox

# Clase que representa un cubo
class Cube:
    rows = 20
    width = 500

    def __init__(self, start, dirnx=1, dirny=0, color=(176, 38, 255)):
        self.pos = start
        self.dirnx = dirnx
        self.dirny = dirny
        self.color = color

    def move(self, dirnx, dirny):
        self.dirnx = dirnx
        self.dirny = dirny
        self.pos = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny)

    def draw(self, surface, eyes=False):
        dis = self.width // self.rows
        i, j = self.pos
        pygame.draw.rect(surface, self.color, (i * dis + 1, j * dis + 1, dis - 2, dis - 2))

        if eyes:
            center = dis // 2
            radius = 3
            circleMiddle = (i * dis + center - radius, j * dis + 8)
            circleMiddle2 = (i * dis + dis - radius * 2, j * dis + 8)
            pygame.draw.circle(surface, (0, 0, 0), circleMiddle, radius)
            pygame.draw.circle(surface, (0, 0, 0), circleMiddle2, radius)

# Clase de la serpiente
class Snake:
    def __init__(self, color, pos):
        self.color = color
        self.head = Cube(pos)
        self.body = [self.head]
        self.turns = {}
        self.dirnx = 0
        self.dirny = 1

    def move(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            keys = pygame.key.get_pressed()
            for key in keys:
                if keys[pygame.K_LEFT]:
                    self.dirnx, self.dirny = -1, 0
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
                elif keys[pygame.K_RIGHT]:
                    self.dirnx, self.dirny = 1, 0
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
                elif keys[pygame.K_UP]:
                    self.dirnx, self.dirny = 0, -1
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
                elif keys[pygame.K_DOWN]:
                    self.dirnx, self.dirny = 0, 1
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

        for i, c in enumerate(self.body):
            p = c.pos[:]
            if p in self.turns:
                turn = self.turns[p]
                c.move(turn[0], turn[1])
                if i == len(self.body) - 1:
                    self.turns.pop(p)
            else:
                self.handle_boundary_collision(c)

    def handle_boundary_collision(self, cube):
        if cube.dirnx == -1 and cube.pos[0] <= 0:
            cube.pos = (cube.rows - 1, cube.pos[1])
        elif cube.dirnx == 1 and cube.pos[0] >= cube.rows - 1:
            cube.pos = (0, cube.pos[1])
        elif cube.dirny == 1 and cube.pos[1] >= cube.rows - 1:
            cube.pos = (cube.pos[0], 0)
        elif cube.dirny == -1 and cube.pos[1] <= 0:
            cube.pos = (cube.pos[0], cube.rows - 1)
        else:
            cube.move(cube.dirnx, cube.dirny)

    def reset(self, pos):
        self.head = Cube(pos)
        self.body = [self.head]
        self.turns = {}
        self.dirnx = 0
        self.dirny = 1

    def add_cube(self):
        tail = self.body[-1]
        dx, dy = tail.dirnx, tail.dirny

        if dx == 1 and dy == 0:
            self.body.append(Cube((tail.pos[0] - 1, tail.pos[1])))
        elif dx == -1 and dy == 0:
            self.body.append(Cube((tail.pos[0] + 1, tail.pos[1])))
        elif dx == 0 and dy == 1:
            self.body.append(Cube((tail.pos[0], tail.pos[1] - 1)))
        elif dx == 0 and dy == -1:
            self.body.append(Cube((tail.pos[0], tail.pos[1] + 1)))

        self.body[-1].dirnx = dx
        self.body[-1].dirny = dy

    def draw(self, surface):
        for i, c in enumerate(self.body):
            c.draw(surface, eyes=(i == 0))

# Funciones de utilidad
def bubble_sort(scores):
    n = len(scores)
    for i in range(n):
        for j in range(0, n - i - 1):
            if scores[j] < scores[j + 1]:
                scores[j], scores[j + 1] = scores[j + 1], scores[j]
    return scores

def draw_grid(width, rows, surface):
    size_between = width // rows
    for l in range(rows):
        x, y = l * size_between, l * size_between
        pygame.draw.line(surface, (255, 255, 255), (x, 0), (x, width))
        pygame.draw.line(surface, (255, 255, 255), (0, y), (width, y))

def redraw_window(surface, snake, snack, width, rows):
    surface.fill((0, 0, 0))
    snake.draw(surface)
    snack.draw(surface)
    draw_grid(width, rows, surface)
    pygame.display.update()

def random_snack(rows, snake):
    while True:
        x, y = random.randrange(rows), random.randrange(rows)
        if all(cube.pos != (x, y) for cube in snake.body):
            break
    return (x, y)

def message_box(subject, content):
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    messagebox.showinfo(subject, content)
    try:
        root.destroy()
    except Exception:
        pass

# Menú principal
def show_menu(scores):
    while True:
        print("===== MENÚ PRINCIPAL =====")
        print("1. Jugar")
        print("2. Ver puntajes altos")
        print("3. Salir")
        choice = input("Selecciona una opción: ")

        if choice == "1":
            return True
        elif choice == "2":
            show_scores(scores)
        elif choice == "3":
            print("¡Gracias por jugar!")
            exit()
        else:
            print("Opción no válida, inténtalo de nuevo.")

# Muestra los puntajes altos
def show_scores(scores):
    print("\n===== PUNTAJES ALTOS =====")
    if not scores:
        print("No hay puntajes registrados aún.")
    else:
        sorted_scores = bubble_sort(scores)
        for i, score in enumerate(sorted_scores):
            print(f"{i + 1}. {score}")
    print()

# Función principal
def main():
    scores = []
    while True:
        if not show_menu(scores):
            continue

        width, rows = 500, 20
        window = pygame.display.set_mode((width, width))
        snake = Snake((255, 0, 0), (10, 10))
        snack = Cube(random_snack(rows, snake), color=(255, 0, 0))
        clock = pygame.time.Clock()
        running = True

        while running:
            pygame.time.delay(50)
            clock.tick(10)
            snake.move()

            if snake.body[0].pos == snack.pos:
                snake.add_cube()
                snack = Cube(random_snack(rows, snake), color=(255, 0, 127))

            for i, cube in enumerate(snake.body):
                if cube.pos in list(map(lambda z: z.pos, snake.body[i + 1:])):
                    score = len(snake.body)
                    print(f"Perdiste. Puntaje: {score}")
                    scores.append(score)
                    message_box("Has perdido!", f"Puntaje: {score}")
                    running = False
                    break

            redraw_window(window, snake, snack, width, rows)

if __name__ == "__main__":
    main()
