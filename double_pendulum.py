import pygame, sys
from pygame.locals import *
import math

pygame.init()
SCREEN_SIZE = 500
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
screen.fill(BLACK)
clock = pygame.time.Clock()




def set_coords(coords):
    return (int(round(coords[0] + SCREEN_SIZE/2)), int(round(coords[1] + SCREEN_SIZE/5)))

def init_trail(screen):
    trail_screen = pygame.Surface(screen.get_size(), pygame.SRCALPHA, 32)
    trail_screen = trail_screen.convert_alpha()
    return trail_screen

def init_pendulum(screen):
    pendulum_screen = pygame.Surface(screen.get_size())
    pendulum_screen = pendulum_screen.convert()
    pendulum_screen.fill((250, 250, 250))
    return pendulum_screen
    
def calculate_a1_a(g, length1, length2, a1, a2, mass1, mass2, a1_v, a2_v):
    num1 = -1 * g * (2 * mass1 + mass2) * math.sin(a1)
    num2 = -1 * mass2 * g * math.sin(a1-2*a2)
    num3 = -2*math.sin(a1-a2)*mass2
    num4 = a2_v * a2_v * length2 + a1_v*a1_v*length1*math.cos(a1-a2)
    den = length1*(2*mass1+mass2-mass2*math.cos(2*a1-2*a2))
    a1_a = (num1 + num2 + num3 * num4) / den
    return a1_a

def calculate_a2_a(g, length1, length2, a1, a2, mass1, mass2, a1_v, a2_v):
    num1 = 2 * math.sin(a1 - a2)
    num2 = (a1_v * a1_v * length1 * (mass1 + mass2))
    num3 = g * (mass1 + mass2) * math.cos(a1)
    num4 = a2_v * a2_v * length2 * mass2 * math.cos(a1-a2)
    den = length2*(2*mass1+mass2-mass2*math.cos(2*a1-2*a2))
    a2_a = (num1 * (num2+num3+num4)) / den
    return a2_a

def draw_pendulum(pendulum, x1, y1, x2, y2, mass1, mass2):
    pendulum.fill(BLACK)
    pygame.draw.line(pendulum, WHITE, set_coords((0, 0)), set_coords((x1, y1)))
    pygame.draw.circle(pendulum, WHITE, set_coords((x1, y1)), mass1)
    pygame.draw.line(pendulum, WHITE, set_coords((x1, y1)), set_coords((x2, y2)))
    pygame.draw.circle(pendulum, WHITE, set_coords((x2, y2)), mass2)

def main():
    g = 1
    length1 = 110
    length2 = 110
    a1 = math.pi / 2
    a2 = math.pi / 2
    mass1 = 8
    mass2 = 8
    a1_v = 0
    a2_v = 0

    last_pos1 = None
    last_pos2 = None
    trail = init_trail(screen)
    pendulum = init_pendulum(screen)

    while True:
        clock.tick(60)
        a1_a = calculate_a1_a(g, length1, length2, a1, a2, mass1, mass2, a1_v, a2_v)
        a2_a = calculate_a2_a(g, length1, length2, a1, a2, mass1, mass2, a1_v, a2_v)
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        
        x1 = length1 * math.sin(a1)
        y1 = length1 * math.cos(a1)
        x2 = x1 + length2 * math.sin(a2)
        y2 = y1 + length2 * math.cos(a2)

        draw_pendulum(pendulum, x1, y1, x2, y2, mass1, mass2)

        screen.blit(pendulum, (0, 0))
        if last_pos1 is not None:
            pygame.draw.line(trail, GREEN, set_coords(last_pos1), set_coords((x1, y1)))
        if last_pos2 is not None:
            pygame.draw.line(trail, RED, set_coords(last_pos2), set_coords((x2, y2)))

        screen.blit(trail, (0, 0))
        last_pos1 = (x1, y1)
        last_pos2 = (x2, y2)
    
        a1_v += a1_a
        a2_v += a2_a
        a1 += a1_v
        a2 += a2_v
        pygame.display.update()

main()