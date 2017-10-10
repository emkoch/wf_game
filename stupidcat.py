import pygame, sys
from pygame.locals import *
from pygame import gfxdraw
from catboard import *
from matplotlib import cm
import random

FPS = 30
WINDOWWIDTH = 1000
WINDOWHEIGHT = 1000
OFFSET_SIZE = 1/30.
BAR_HEIGHT = int(WINDOWHEIGHT*OFFSET_SIZE)

NUM_CATS = 30

BGCOLOR = (60, 60, 100)
CATCOLOR = (34, 200, 90)
TEXTCOLOR = (255, 255, 0)
BLACK = (0, 0, 0)


def main():
    global FPSCLOCK, DISPLAYSURF
    pygame.init()

    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('Evolution simulation')
    BASICFONT = pygame.font.Font('FreeSansBold.ttf', int(BAR_HEIGHT*0.75))

    DISPLAYSURF.fill(BGCOLOR)

    CATBOARD = catboard(DISPLAYSURF, CATCOLOR, NUM_CATS, BGCOLOR, TEXTCOLOR, FPSCLOCK, OFFSET_SIZE, BASICFONT)

    NUM_GEN = 0

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == KEYUP and event.key == K_SPACE and not CATBOARD.is_poly():
                new_cat_color = random_tab20()
                CATBOARD.mutate_cats(0.5, new_cat_color)
                CATBOARD.COLOR_FIT[new_cat_color] = 1.
            elif event.type == KEYUP and event.key == K_RSHIFT and not CATBOARD.is_poly():
                new_cat_color = random_tab20()
                CATBOARD.mutate_cats(0.1, new_cat_color)
                CATBOARD.COLOR_FIT[new_cat_color] = 2.0

        draw_num_gen(NUM_GEN, BAR_HEIGHT, BASICFONT, DISPLAYSURF)
        CATBOARD.wiggle_cats(10, 2)
        CATBOARD.backshift()
        CATBOARD.add_new_gen_fancy()
        if not CATBOARD.is_poly():
            CATBOARD.COLOR_FIT = {CATBOARD.CAT_STATES[-1][0][2]:1.}

        NUM_GEN += 1

def random_tab20():
    viridis_val = cm.get_cmap('tab20')(random.randint(0, 19))
    return (viridis_val[0]*255., viridis_val[1]*255., viridis_val[2]*255.)

if __name__ == "__main__":
    main()
