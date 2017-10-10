import pygame, sys
from pygame.locals import *
from pygame import gfxdraw
from catboard import *

FPS = 30
WINDOWWIDTH = 1000
WINDOWHEIGHT = 1000

NUM_CATS = 35

BGCOLOR = (60, 60, 100)
CATCOLOR = (34, 200, 90)
BLACK = (0, 0, 0)

def main():
    global FPSCLOCK, DISPLAYSURF
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))

    DISPLAYSURF.fill(BGCOLOR)

    CATBOARD = catboard(DISPLAYSURF, CATCOLOR, NUM_CATS, BGCOLOR, FPSCLOCK)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == KEYUP and event.key == K_SPACE and not CATBOARD.is_poly():
                CATBOARD.mutate_cats(0.5)

        CATBOARD.wiggle_cats(10)
        CATBOARD.backshift()
        CATBOARD.add_new_gen()

if __name__ == "__main__":
    main()
