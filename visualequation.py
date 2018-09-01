#!/usr/bin/env python2
"""This is the file to execute the program."""
import sys
import tempfile
import shutil
import os

import pygame
from pygame.locals import *

import ops
import maineq
import conversions
import menu

def display_splash_screen(screen, temp_dir, version):
    """ Load a nice pygame badge while the user waits"""
    # Background image
    screen_w = screen.get_width()
    screen_h = screen.get_height()
    badge = pygame.image.load("pygame-badge-SMA.png")
    screen.blit(badge, ((screen_w-badge.get_width())//2,
                        (screen_h-badge.get_height())//2))
    # Title
    title = r"\color{white}(\text{Visual Equation})}_{\text{%s}}" % version
    title_png = conversions.eq2png([title], 270, temp_dir)
    title_im = pygame.image.load(title_png)
    screen.blit(title_im, ((screen_w-title_im.get_width())//2, 30))
    # LaTeX ackknowledgement
    latex_m = r"\color{white}\& \LaTeX"
    latex_png = conversions.eq2png([latex_m], 250, temp_dir)
    latex_im = pygame.image.load(latex_png)
    screen.blit(latex_im, (530, 500))
    pygame.display.flip()

def print_delay_message(screen, current, total, temp_dir):
    """ Print a message in the bottom of the screen showing the current/total
    generation of operators' images.
    """
    screen_w = screen.get_width()
    screen_h = screen.get_height()
    message = r"""
    \color{{white}}\text{{It is the first time that the program is running.
    Generating symbols...............}}{0}/{1}
    """.format(current, total)
    message_png = conversions.eq2png([message], 150, temp_dir)
    message_im = pygame.image.load(message_png)
    message_pos = ((screen_w-message_im.get_width())//2, screen_h - 40)
    message_rect = message_im.get_rect()
    message_rect.topleft = message_pos
    screen.fill((0, 0, 0), message_rect)
    screen.blit(message_im, message_pos)
    pygame.display.flip()

def generate_ops_images(menuitem, png_dir, temp_dir):
    """
    Generate the png of the operators and place them in a given directory.
    A temporal directory must be passed too, where auxiliary files are
    generated.
    """
    for oper in menuitem.ops_l:
        filename = os.path.join(png_dir, oper[0] + ".png")
        if not os.path.exists(filename):
            # Determine the appearance of op
            if isinstance(oper[1], tuple):
                op_eq = oper[1][1]
            elif isinstance(oper[1], basestring):
                op_eq = [oper[1]]
            elif isinstance(oper[1], ops.Op) and oper[1].n_args == 1:
                op_eq = [oper[1], ops.SelArg]
            elif isinstance(oper[1], ops.Op) and oper[1].n_args > 1:
                op_eq = [oper[1], ops.SelArg] + \
                    [ops.NewArg]*(oper[1].n_args - 1)
            # Create and save image of that op
            conversions.eq2png(op_eq, menuitem.dpi, temp_dir, filename)

def main(*args):
    """ This the main function of the program."""

    version = '0.1.0'
    # Prepare a temporal directory to manage all LaTeX files
    temp_dirpath = tempfile.mkdtemp()
    # Set the path to main directories
    program_dir = os.path.join(os.path.expanduser('~'), '.visualequation')
    ops_dir = os.path.join(program_dir, 'data')

    # Prepare pygame
    screen_w = 800
    screen_h = 600
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((screen_w, screen_h))
    pygame.display.set_caption("Visual Equation")
    display_splash_screen(screen, temp_dirpath, version)

    # Generate operators' images if the folder is not found
    if not os.path.exists(program_dir):
        os.makedirs(program_dir)
    if not os.path.exists(ops_dir):
        os.makedirs(ops_dir)
        print_message = True
    else:
        print_message = False

    for index, menuitem in enumerate(ops.MENUITEMS):
        if print_message:
            # Print message about the delay by creating operators' images
            print_delay_message(screen, index+1, len(ops.MENUITEMS),
                                temp_dirpath)
        generate_ops_images(menuitem, ops_dir, temp_dirpath)

    # Prepare the equation to edit which will be showed by default
    init_eq = [ops.NewArg]
    screen_center = (screen_w//2, screen_h//2)
    main_eqsprite = maineq.EditableEqSprite(init_eq, screen_center,
                                            temp_dirpath)

    # Create the menu
    mainmenu = menu.Menu(screen_w, screen_h, ops_dir, temp_dirpath)

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
                elif event.unicode == '!':
                    main_eqsprite.insert('!')
                elif event.unicode == '$':
                    main_eqsprite.insert(r'\$')
                elif event.unicode == '%':
                    main_eqsprite.insert(r'\%')
                elif event.unicode == '&':
                    main_eqsprite.insert(r'\&')
                elif event.unicode == '/':
                    main_eqsprite.insert('/')
                elif event.unicode == ')':
                    main_eqsprite.insert(')')
                elif event.unicode == '(':
                    main_eqsprite.insert('(')
                elif event.unicode == '=':
                    main_eqsprite.insert('=')
                elif event.unicode == '?':
                    main_eqsprite.insert('?')
                elif event.unicode == "'":
                    main_eqsprite.insert("'")
                elif event.unicode == '@':
                    main_eqsprite.insert('@')
                elif event.unicode == '#':
                    main_eqsprite.insert(r'\#')
                elif event.unicode == '[':
                    main_eqsprite.insert('[')
                elif event.unicode == ']':
                    main_eqsprite.insert(']')
                elif event.unicode == '{':
                    main_eqsprite.insert(r'\{')
                elif event.unicode == '}':
                    main_eqsprite.insert(r'\}')
                elif event.unicode == '*':
                    main_eqsprite.insert('*')
                elif event.unicode == '+':
                    main_eqsprite.insert('+')
                elif event.unicode == '-':
                    main_eqsprite.insert('-')
                elif event.unicode == '_':
                    main_eqsprite.insert(r'\_')
                elif event.unicode == '<':
                    main_eqsprite.insert('<')
                elif event.unicode == '>':
                    main_eqsprite.insert('>')
                elif event.unicode == ',':
                    main_eqsprite.insert(',')
                elif event.unicode == '.':
                    main_eqsprite.insert('.')
                elif event.unicode == ';':
                    main_eqsprite.insert(';')
                elif event.unicode == ':':
                    main_eqsprite.insert(':')
                    # First cases with mods, this avoids false positives
                    # CONTROL + letter
                elif event.key == K_z and pygame.key.get_mods() & KMOD_CTRL:
                    main_eqsprite.recover_prev_eq()
                elif event.key == K_y and pygame.key.get_mods() & KMOD_CTRL:
                    main_eqsprite.recover_next_eq()
                elif event.key == K_s and pygame.key.get_mods() & KMOD_CTRL:
                    main_eqsprite.save_eq()
                elif event.key == K_c and pygame.key.get_mods() & KMOD_CTRL:
                    main_eqsprite.sel2eqbuffer()
                elif event.key == K_x and pygame.key.get_mods() & KMOD_CTRL:
                    main_eqsprite.sel2eqbuffer()
                    main_eqsprite.remove_sel()
                elif event.key == K_v and pygame.key.get_mods() & KMOD_CTRL:
                    main_eqsprite.eqbuffer2sel()
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
                    main_eqsprite.insert(r'\,')
                elif event.key == K_TAB:
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

if __name__ == '__main__':
    main(*sys.argv[1:])
