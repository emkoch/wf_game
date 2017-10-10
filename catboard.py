from collections import Counter
import pygame, sys
from pygame.locals import *
from pygame import gfxdraw
import numpy as np
import random


class catboard(object):
    def __init__(self, surf, default_catcolor, num_cats, bgcolor, fpsclock):
        self.DISPLAYSURF = surf
        self.BGCOLOR = bgcolor
        self.FPSCLOCK = fpsclock
        self.DEFAULT_CATCOLOR = default_catcolor
        self.NCATS = num_cats
        self.CAT_SIZE = int(surf.get_height() / ((11.*num_cats + 1)/10.))
        self.MARGIN = int(float(self.CAT_SIZE)/10.) + 1
        self.CAT_STATES = self.initialize_cat_states()
        self.COLOR_FIT = {self.DEFAULT_CATCOLOR:1.}

    def initialize_cat_states(self):
        # Start off by putting a column of cats at the right side of the screen
        result = [[]]
        for cat_i in range(1, self.NCATS + 1):
            cat_topx = int(self.DISPLAYSURF.get_width() - self.MARGIN - self.CAT_SIZE)
            cat_topy = int(cat_i*self.MARGIN + (cat_i - 1)*self.CAT_SIZE)
            result[0].append([cat_topx, cat_topy, self.DEFAULT_CATCOLOR])
        return result

    def draw_current(self, cat_position):
        for cat_col in self.CAT_STATES:
            for cat in cat_col:
                drawCat(cat[0], cat[1], self.CAT_SIZE, cat_position,
                        self.DISPLAYSURF, cat[2])

    def wiggle_cats(self, fps, iterations=1):
        for pos in ["out", "middle", "in", "middle"]*iterations:
            self.DISPLAYSURF.fill(self.BGCOLOR)
            self.draw_current(pos)
            pygame.display.update()
            self.FPSCLOCK.tick(fps)

    def backshift(self):
        for idx, cat_col in enumerate(self.CAT_STATES):
            new_cat_col_x = cat_col[0][0] - self.MARGIN - self.CAT_SIZE
            if new_cat_col_x < 0:
                del self.CAT_STATES[idx]
            else:
                for cat in cat_col:
                    # Shift x position of cat backwards
                    cat[0] = new_cat_col_x

    def mutate_cats(self, frequency, new_color):
        num_mutate_cats = int(frequency*self.NCATS)
        current_color = self.CAT_STATES[-1][0][2]
        colors = sorted([current_color, new_color])
        color_order = sorted([current_color, new_color]).index(new_color)
        for idx, cat in enumerate(self.CAT_STATES[-1]):
            if color_order == 1:
                if idx > self.NCATS - num_mutate_cats - 1:
                    cat[2] = colors[1]
                else:
                    cat[2] = colors[0]
            else:
                if idx < num_mutate_cats:
                    cat[2] = colors[0]
                else:
                    cat[2] = colors[1]

    def is_poly(self):
        assert len(self.CAT_STATES) > 0, "ran out of cats!!!"
        current_cats = self.CAT_STATES[-1]
        if len(Counter([cat[2] for cat in current_cats]).keys()) > 1:
            return True
        else:
            return False

    def add_new_gen(self):
        assert len(self.CAT_STATES) > 0, "ran out of cats!!!"
        current_cats = self.CAT_STATES[-1]
        cat_colors = Counter([cat[2] for cat in current_cats])
        cat_color_prs = sorted([(cat_color, float(cat_colors[cat_color])/self.NCATS)
                                for cat_color in cat_colors.keys()])
        new_color_counts = np.random.multinomial(self.NCATS,
                                                 [cat_color_pr[1] for
                                                  cat_color_pr in cat_color_prs])
        new_gen = []
        cat_i = 0
        cat_topx = int(self.DISPLAYSURF.get_width() - self.MARGIN - self.CAT_SIZE)
        print(new_color_counts)
        for idx, cat_color in enumerate(cat_color_prs):
            if new_color_counts[idx] > 0:
                cat_i += 1
                for cat_i in range(cat_i, cat_i + new_color_counts[idx]):
                    cat_topy = int(cat_i*self.MARGIN + (cat_i - 1)*self.CAT_SIZE)
                    new_gen.append([cat_topx, cat_topy, cat_color[0]])
        self.CAT_STATES.append(new_gen)

    def add_new_gen_sel(self):
        assert len(self.CAT_STATES) > 0, "ran out of cats!!!"
        current_cats = self.CAT_STATES[-1]
        cat_colors = Counter([cat[2] for cat in current_cats])
        cat_color_prs = sorted([(cat_color,
                                 float(cat_colors[cat_color]*
                                       self.COLOR_FIT[cat_color]/(self.NCATS -
                                                                  cat_colors[cat_color]
                                                                  + cat_colors[cat_color]*
                                                                  self.COLOR_FIT[cat_color])))
                                for cat_color in cat_colors.keys()])
        new_color_counts = np.random.multinomial(self.NCATS,
                                                 [cat_color_pr[1] for
                                                  cat_color_pr in cat_color_prs])
        new_gen = []
        cat_i = 0
        cat_topx = int(self.DISPLAYSURF.get_width() - self.MARGIN - self.CAT_SIZE)
        for idx, cat_color in enumerate(cat_color_prs):
            if new_color_counts[idx] > 0:
                cat_i += 1
                for cat_i in range(cat_i, cat_i + new_color_counts[idx]):
                    cat_topy = int(cat_i*self.MARGIN + (cat_i - 1)*self.CAT_SIZE)
                    new_gen.append([cat_topx, cat_topy, cat_color[0]])
        self.CAT_STATES.append(new_gen)

def drawCat(topx, topy, width, position, surf, cat_color):
    BLACK = (0, 0, 0)
    if position == 'middle':
        ## front
        gfxdraw.aatrigon(surf, int(topx + 3*width/32), int(topy + width/2),
                         int(topx + 5*width/32), int(topy + width/2),
                         int(topx + 4*width/32), int(topy + 7*width/8), cat_color)
        gfxdraw.filled_trigon(surf, int(topx + 3*width/32), int(topy + width/2),
                              int(topx + 5*width/32), int(topy + width/2),
                              int(topx + 4*width/32), int(topy + 7*width/8), cat_color)
        gfxdraw.aatrigon(surf, int(topx + 5*width/32), int(topy + width/2),
                         int(topx + 7*width/32), int(topy + width/2),
                         int(topx + 6*width/32), int(topy + 7*width/8), cat_color)
        gfxdraw.filled_trigon(surf, int(topx + 5*width/32), int(topy + width/2),
                              int(topx + 7*width/32), int(topy + width/2),
                              int(topx + 6*width/32), int(topy + 7*width/8), cat_color)
        ## back
        gfxdraw.aatrigon(surf, int(topx + 25*width/32), int(topy + width/2),
                         int(topx + 23*width/32), int(topy + width/2),
                         int(topx + 24*width/32), int(topy + 7*width/8), cat_color)
        gfxdraw.filled_trigon(surf, int(topx + 25*width/32), int(topy + width/2),
                              int(topx + 23*width/32), int(topy + width/2),
                              int(topx + 24*width/32), int(topy + 7*width/8), cat_color)
        gfxdraw.aatrigon(surf, int(topx + 23*width/32), int(topy + width/2),
                         int(topx + 21*width/32), int(topy + width/2),
                         int(topx + 22*width/32), int(topy + 7*width/8), cat_color)
        gfxdraw.filled_trigon(surf, int(topx + 23*width/32), int(topy + width/2),
                              int(topx + 21*width/32), int(topy + width/2),
                              int(topx + 22*width/32), int(topy + 7*width/8), cat_color)
    elif position == 'out':
        ## front
        gfxdraw.aatrigon(surf, int(topx + 3*width/32), int(topy + width/2),
                         int(topx + 5*width/32), int(topy + 7*width/16),
                         int(topx + 1*width/32), int(topy + 7*width/8), cat_color)
        gfxdraw.filled_trigon(surf, int(topx + 3*width/32), int(topy + width/2),
                              int(topx + 5*width/32), int(topy + 7*width/16),
                              int(topx + 1*width/32), int(topy + 7*width/8), cat_color)
        gfxdraw.aatrigon(surf, int(topx + 5*width/32), int(topy + width/2),
                         int(topx + 7*width/32), int(topy + 7*width/16),
                         int(topx + 3*width/32), int(topy + 7*width/8), cat_color)
        gfxdraw.filled_trigon(surf, int(topx + 5*width/32), int(topy + width/2),
                              int(topx + 7*width/32), int(topy + 7*width/16),
                              int(topx + 3*width/32), int(topy + 7*width/8), cat_color)
        ## back
        gfxdraw.aatrigon(surf, int(topx + 25*width/32), int(topy + width/2),
                         int(topx + 23*width/32), int(topy + 7*width/16),
                         int(topx + 27*width/32), int(topy + 7*width/8), cat_color)
        gfxdraw.filled_trigon(surf, int(topx + 25*width/32), int(topy + width/2),
                              int(topx + 23*width/32), int(topy + 7*width/16),
                              int(topx + 27*width/32), int(topy + 7*width/8), cat_color)
        gfxdraw.aatrigon(surf, int(topx + 23*width/32), int(topy + width/2),
                         int(topx + 21*width/32), int(topy + 7*width/16),
                         int(topx + 25*width/32), int(topy + 7*width/8), cat_color)
        gfxdraw.filled_trigon(surf, int(topx + 23*width/32), int(topy + width/2),
                              int(topx + 21*width/32), int(topy + 7*width/16),
                              int(topx + 25*width/32), int(topy + 7*width/8), cat_color)
    elif position == "in":
        ## front
        gfxdraw.aatrigon(surf, int(topx + 3*width/32), int(topy + width/2),
                         int(topx + 5*width/32), int(topy + 7*width/16),
                         int(topx + 7*width/32), int(topy + 7*width/8), cat_color)
        gfxdraw.filled_trigon(surf, int(topx + 3*width/32), int(topy + width/2),
                              int(topx + 5*width/32), int(topy + 7*width/16),
                              int(topx + 7*width/32), int(topy + 7*width/8), cat_color)
        gfxdraw.aatrigon(surf, int(topx + 5*width/32), int(topy + width/2),
                         int(topx + 7*width/32), int(topy + 7*width/16),
                         int(topx + 9*width/32), int(topy + 7*width/8), cat_color)
        gfxdraw.filled_trigon(surf, int(topx + 5*width/32), int(topy + width/2),
                              int(topx + 7*width/32), int(topy + 7*width/16),
                              int(topx + 9*width/32), int(topy + 7*width/8), cat_color)
        ## back
        gfxdraw.aatrigon(surf, int(topx + 25*width/32), int(topy + 7*width/16),
                         int(topx + 23*width/32), int(topy + width/2),
                         int(topx + 21*width/32), int(topy + 7*width/8), cat_color)
        gfxdraw.filled_trigon(surf, int(topx + 25*width/32), int(topy + 7*width/16),
                              int(topx + 23*width/32), int(topy + width/2),
                              int(topx + 21*width/32), int(topy + 7*width/8), cat_color)
        gfxdraw.aatrigon(surf, int(topx + 23*width/32), int(topy + 7*width/16),
                         int(topx + 21*width/32), int(topy + width/2),
                         int(topx + 19*width/32), int(topy + 7*width/8), cat_color)
        gfxdraw.filled_trigon(surf, int(topx + 23*width/32), int(topy + 7*width/16),
                              int(topx + 21*width/32), int(topy + width/2),
                              int(topx + 19*width/32), int(topy + 7*width/8), cat_color)
    # draw the body of the cat
    pygame.draw.ellipse(surf, cat_color,
                        (int(topx + width/16), int(topy + width/4),
                         int(3*width/4), int(width/2)))
    # pygame.draw.ellipse(surf, BLACK,
    #                     (int(topx + width/16), int(topy + width/4),
    #                      int(3*width/4), int(width/2)), 5)
    # draw the ears of the cat
    pygame.draw.aalines(surf, cat_color, False, ((int(topx + 7*width/12), int(topy + width/4)),
                                                       (int(topx + 8*width/12), int(topy)),
                                                       (int(topx + 9*width/12), int(topy + width/4))))
    pygame.draw.aalines(surf, cat_color, False, ((int(topx + 9*width/12), int(topy + width/4)),
                                                       (int(topx + 10*width/12), int(topy)),
                                                       (int(topx + 11*width/12), int(topy + width/4))))
    # draw the head of the cat
    gfxdraw.filled_circle(surf, int(topx + 3*width/4), int(topy + width/4), int(width/6),
                          cat_color)
    gfxdraw.aacircle(surf,
                            int(topx + 3*width/4), int(topy + width/4), int(width/6), cat_color)
    # draw the eyes of the cat
    pygame.draw.ellipse(surf, BLACK,
                        (int(topx + 5.2*width/8), int(topy + width/8),
                         int(width/10), int(width/12)))
    pygame.draw.ellipse(surf, BLACK,
                        (int(topx + 6.2*width/8), int(topy + width/8),
                         int(width/10), int(width/12)))
