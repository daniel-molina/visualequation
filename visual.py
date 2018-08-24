#!/usr/bin/env python3
import sys
import tempfile
import shutil

import pygame
from pygame.locals import *

from operators import *
import sprites
import latex
import conversions

def distr_in_circle(n_elems, surf_w, surf_h, r_as_percent):
    import math
    centerx = surf_w//2
    centery = surf_h//2
    r = r_as_percent*min(surf_w, surf_h)/2
    theta_incr = 2.*math.pi/n_elems
    for i in range(n_elems):
        theta = i*theta_incr
        yield (centerx + int(r*math.cos(theta)),
               centery + int(r*math.sin(theta)))
    else:
        raise StopIteration

if __name__ == "__main__":

    # Prepare a temporal directory to manage all LaTeX files
    temp_dirpath = tempfile.mkdtemp()

    # Prepare pygame
    pygame.init()
    clock = pygame.time.Clock()

    # Prepare display
    screen_w = 800
    screen_h = 600
    screen = pygame.display.set_mode((screen_w, screen_h))
    bg = pygame.image.load("pygame-badge-SMA.png")

    # Load a nice pygame badge while the user waits
    screen.blit(bg, ((screen_w-bg.get_width())//2,
                     (screen_h-bg.get_height())//2))
    pygame.display.set_caption("Visual Equation")
    pygame.display.flip()

    # Prepare the equation to edit that will be showed by default
    init_eq = [Square]
    main_eqsprite = sprites.EditableEqSprite(init_eq, screen, temp_dirpath)

    # Prepare symbols and operators that are around the window
    eqs_select = [[Frac, SelArg, NewArg], ['x'], ['y'], [Pi], ['2'],
                  [Pow, SelArg, NewArg], [Parenthesis, SelArg],
                  [Prod, SelArg, NewArg], [Vec, SelArg]]
    positions = [pos for pos in distr_in_circle(len(eqs_select), screen_w,
                                                screen_h, 0.7)]
    opers_sprite = tuple(sprites.OperSprite(eq, pos, temp_dirpath) for eq, pos
                              in zip(eqs_select, positions))
 
    allsprites = pygame.sprite.RenderPlain(opers_sprite + (main_eqsprite,))

    # Pygame loop
    ongoing = True
    while ongoing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                ongoing = False
            elif event.type == MOUSEBUTTONDOWN:
                for eqsprite in opers_sprite:
                    if eqsprite.mousepointed():
                        main_eqsprite.replace_sel_by(eqsprite.OP)
                if main_eqsprite.mousepointed():
                    main_eqsprite.next_sel()

        screen.fill((255, 255, 255))
        allsprites.update()
        allsprites.draw(screen)
        pygame.display.flip()
        clock.tick(30)

    # Delete the temporary directory and files before exit
    shutil.rmtree(temp_dirpath)
    sys.exit(0)
    
