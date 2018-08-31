#!/usr/bin/env python3
import sys
import tempfile
import shutil
import os

import pygame
from pygame.locals import *

import ops
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
    latex_m = r"\color{blue}\& \LaTeX"""
    latex_png = conversions.eq2png([latex_m], 220, temp_dirpath)
    latex_im = pygame.image.load(latex_png)
    screen.blit(latex_im, (510, 400))
    pygame.display.flip()

    # Generate operators' images if the folder is not found
    main_dir = os.path.join(os.path.expanduser('~'), '.visualequation')
    ops_dir = os.path.join(main_dir, 'data')
    def generate_ops_images(opers):
        for op in opers.ops_l:
            filename = os.path.join(ops_dir, op[0] + ".png")
            if not os.path.exists(filename):
                if isinstance(op[1], tuple):
                    op_eq = op[1][1]
                elif isinstance(op[1], str):
                    op_eq = [op[1]]
                elif isinstance(op[1], ops.Op) and op[1].n_args == 1:
                    op_eq = [op[1], ops.SelArg]
                elif isinstance(op[1], ops.Op) and op[1].n_args > 1:
                    op_eq = [op[1], ops.SelArg] + \
                            [ops.NewArg]*(op[1].n_args - 1)
                conversions.eq2png(op_eq, opers.dpi, temp_dirpath,
                                   filename)

    if not os.path.exists(main_dir):
        os.makedirs(main_dir)
    if not os.path.exists(ops_dir):
        os.makedirs(ops_dir)
        # Print message informing about the delay by creating operators' images
        message = r"""\color{white}\text{It is the first time that the program
        is running. Generating symbols...............}"""
        message_png = conversions.eq2png([message], 150, temp_dirpath)
        message = pygame.image.load(message_png)
        screen.blit(message, (10, screen_h - 40))
        pygame.display.flip()

        ops_l = [ops.ops2, ops.ops3, ops.ops4,
                 ops.ops5, ops.ops6, ops.ops7, ops.ops8,
                 ops.ops9, ops.ops10]
        for index, opers in enumerate(ops_l):
            message = r"\color{{white}} {0}/{1}".format(index+1, len(ops_l))
            message_png = conversions.eq2png([message], 150, temp_dirpath)
            message = pygame.image.load(message_png)
            pos = (screen_w - 80, screen_h - 40)
            screen.fill((0, 0, 0), message.get_rect(topleft=pos))
            screen.blit(message, pos)
            pygame.display.flip()

            generate_ops_images(opers)

    # Prepare the equation to edit which will be showed by default
    init_eq = [ops.NewArg]
    screen_center = (screen.get_width()//2, screen.get_height()//2)
    main_eqsprite = maineq.EditableEqSprite(init_eq, screen_center,
                                             temp_dirpath)

    # Prepare symbols and operators that are around the window
    #ops = ops.functions
    #g_letters = distr_at_top(len(ops), screen_w, 40, 50)
    #g_math_construct = distr_at_top(len(ops), screen_w, 90, 110)
    #g_delimiters = distr_at_top(len(ops), screen_w, 120, 60)
    #g_variable_size =  distr_at_top(len(ops), screen_w, 50, 80)
    #g_pos =  distr_at_top(len(ops), screen_w, 100, 30)

    # Create the Menu    
    mainmenu = menu.Menu(screen_w, screen_h, ops_dir, temp_dirpath)

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
                        mainmenu.select_item(index)
                for op_sprite in mainmenu.active_ops:
                    if op_sprite.mousepointed():
                        if pygame.key.get_mods() & KMOD_SHIFT:
                            main_eqsprite.insert_substituting(op_sprite.OP)
                        else:
                            main_eqsprite.insert(op_sprite.OP)
                if main_eqsprite.mousepointed():
                    main_eqsprite.next_sel()
            elif event.type == KEYDOWN:
                try:
                    code = ord(event.unicode)
                    # If it belongs to 0-9 or A-Z or a-z
                    if 48 <= code <= 57 or 65 <= code <= 90 \
                       or 97 <= code <= 122:
                        main_eqsprite.insert(event.unicode)
                except TypeError:
                    pass
                if event.unicode == '\\':
                    main_eqsprite.insert(r'\backslash')
                if event.unicode == '!':
                    main_eqsprite.insert('!')
                if event.unicode == '$':
                    main_eqsprite.insert(r'\$')
                if event.unicode == '%':
                    main_eqsprite.insert(r'\%')
                if event.unicode == '&':
                    main_eqsprite.insert(r'\&')
                if event.unicode == '/':
                    main_eqsprite.insert('/')
                if event.unicode == ')':
                    main_eqsprite.insert(')')
                if event.unicode == '(':
                    main_eqsprite.insert('(')
                if event.unicode == '=':
                    main_eqsprite.insert('=')
                if event.unicode == '?':
                    main_eqsprite.insert('?')
                if event.unicode == "'":
                    main_eqsprite.insert("'")
                if event.unicode == '@':
                    main_eqsprite.insert('@')
                if event.unicode == '#':
                    main_eqsprite.insert('\#')
                if event.unicode == '[':
                    main_eqsprite.insert('[')
                if event.unicode == ']':
                    main_eqsprite.insert(']')
                if event.unicode == '{':
                    main_eqsprite.insert(r'\{')
                if event.unicode == '}':
                    main_eqsprite.insert(r'\}')
                if event.unicode == '*':
                    main_eqsprite.insert('*')
                if event.unicode == '+':
                    main_eqsprite.insert('+')
                if event.unicode == '-':
                    main_eqsprite.insert('-')
                if event.unicode == '_':
                    main_eqsprite.insert(r'\_')
                if event.unicode == '<':
                    main_eqsprite.insert('<')
                if event.unicode == '>':
                    main_eqsprite.insert('>')
                if event.unicode == ',':
                    main_eqsprite.insert(',')
                if event.unicode == '.':
                    main_eqsprite.insert('.')
                if event.unicode == ';':
                    main_eqsprite.insert(';')
                if event.unicode == ':':
                    main_eqsprite.insert(':')

                # First cases with mods, this avoids false positives
                # CONTROL + letter
                elif event.key == K_z and pygame.key.get_mods() & KMOD_CTRL:
                    main_eqsprite.recover_prev_eq()
                elif event.key == K_y and pygame.key.get_mods() & KMOD_CTRL:
                    main_eqsprite.recover_next_eq()
                elif event.key == K_s and pygame.key.get_mods() & KMOD_CTRL:
                    main_eqsprite.save_eq()
                # Cases without mods
                elif event.key == K_RIGHT:
                    main_eqsprite.next_sel()
                elif event.key == K_LEFT:
                    main_eqsprite.previous_sel()
                elif event.key == K_UP:
                    mainmenu.next_item()
                elif event.key == K_DOWN:
                    mainmenu.prev_item()
                elif event.key == K_SPACE:
                    main_eqsprite.left_NewArg()
                elif event.key == K_BACKSPACE or event.key == K_DELETE:
                    main_eqsprite.remove_sel()

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
    
