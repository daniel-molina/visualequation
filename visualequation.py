#!/usr/bin/env python3
import sys
import tempfile
import shutil

import pygame
from pygame.locals import *

import operators
import maineq
import latex
import conversions
import menu

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

    # Load a nice pygame badge while the user waits
    bg = pygame.image.load("pygame-badge-SMA.png")
    screen.blit(bg, ((screen_w-bg.get_width())//2,
                     (screen_h-bg.get_height())//2))
    pygame.display.set_caption("Visual Equation")
    pygame.display.flip()

    # Prepare the equation to edit that will be showed by default
    init_eq = [operators.NewArg]
    screen_center = (screen.get_width()//2, screen.get_height()//2)
    main_eqsprite = maineq.EditableEqSprite(init_eq, screen_center,
                                             temp_dirpath)

    # Prepare symbols and operators that are around the window
    #ops = operators.functions
    #g_letters = distr_at_top(len(ops), screen_w, 40, 50)
    #g_math_construct = distr_at_top(len(ops), screen_w, 90, 110)
    #g_delimiters = distr_at_top(len(ops), screen_w, 120, 60)
    #g_variable_size =  distr_at_top(len(ops), screen_w, 50, 80)
    #g_pos =  distr_at_top(len(ops), screen_w, 100, 30)

    # Create the Menu    
    mainmenu = menu.Menu(screen_w, screen_h, temp_dirpath)

    #menusprites = pygame.sprite.RenderPlain(tuple(menu))
    #allsprites = pygame.sprite.RenderPlain(
    #    tuple(ops_sprite) + (main_eqsprite,) + tuple(menu))


    # Pygame loop
    ongoing = True
    while ongoing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                ongoing = False
            elif event.type == MOUSEBUTTONDOWN:
                for index, menuitem in enumerate(mainmenu.items):
                    if menuitem.mousepointed():
                        mainmenu.change_ops(index)
                for op_sprite in mainmenu.active_ops:
                    if op_sprite.mousepointed():
                        main_eqsprite.replace_sel_by(op_sprite.OP)
                if main_eqsprite.mousepointed():
                    main_eqsprite.next_sel()
            elif event.type == KEYDOWN:
                if event.key == K_RIGHT:
                    main_eqsprite.next_sel()
                elif event.key == K_LEFT:
                    main_eqsprite.previous_sel()
                elif event.key == K_SPACE:
                    main_eqsprite.replace_sel_by(operators.Juxt)
                elif event.key == K_BACKSPACE or event.key == K_DELETE:
                    main_eqsprite.replace_sel_by(NewArg)
                # First cases with mods, the last ones the keys alone
                # It avoids false positives
                elif event.key == K_z and pygame.key.get_mods() & KMOD_CTRL:
                    main_eqsprite.recover_prev_eq()
                elif event.key == K_y and pygame.key.get_mods() & KMOD_CTRL:
                    main_eqsprite.recover_next_eq()
                elif event.key == K_s and pygame.key.get_mods() & KMOD_CTRL:
                    main_eqsprite.save_eq()
                    
        screen.fill((255, 255, 255))
        #mainmenu.active_ops.update()
        screen.blit(main_eqsprite.image, main_eqsprite.rect)
        for item in mainmenu.items:
            screen.blit(item.image, item.rect)
        mainmenu.active_ops.draw(screen)
        pygame.display.flip()
        clock.tick(30)

    # Delete the temporary directory and files before exit
    shutil.rmtree(temp_dirpath)
    sys.exit(0)
    
