import pygame, sys
from pygame.locals import *
from random import randint

pygame.init()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
screen = pygame.display.set_mode((500, 500))
screen.fill(WHITE)


def draw_rotate(screen, color, last_pos, mouse_position, times_rotated):
    symmetry = 360 / times_rotated
    for i in range(times_rotated):
        rotate(symmetry)
        pygame.draw.line(screen, color, last_pos, mouse_position, 6)
        invert()
        pygame.draw.line(screen, color, last_pos, mouse_position, 6)
        invert()
 


def rotate(degrees):
    rotated = pygame.transform.rotate(screen, degrees)
    new_window = rotated.get_rect(center = screen.get_rect(topleft = (0, 0)).center)
    screen.blit(rotated, new_window.topleft)

def invert():
    inverted = pygame.transform.flip(screen, 0, 1)
    new_window = inverted.get_rect(center = screen.get_rect(topleft = (0, 0)).center)
    screen.blit(inverted, new_window.topleft)

def main():
    mouse_position = (0, 0)
    drawing = False


    last_pos = None

    while True:
        color = (randint(0, 255), randint(0, 255), randint(0, 255))
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEMOTION:
                if (drawing):
                    mouse_position = pygame.mouse.get_pos()
                    if last_pos is not None:
                        draw_rotate(screen, color, last_pos, mouse_position, 6)
                    last_pos = mouse_position
            elif event.type == MOUSEBUTTONUP:
                mouse_position = (0, 0)
                drawing = False
            elif event.type == MOUSEBUTTONDOWN:
                drawing = True

        pygame.display.update()

main()