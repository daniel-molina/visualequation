#!/usr/bin/env python2
"""This is the file to execute the program."""
import sys
import tempfile
import shutil
import os

import pygame
from pygame.locals import *

import dirs
import symbols
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

def generate_symb_images(menuitemdata, temp_dir):
    """
    Generate the png of the symbols and place them in a given directory.
    A temporal directory must be passed too, where auxiliary files are
    generated.
    """
    for symb in menuitemdata.symb_l:
        filename = os.path.join(dirs.SYMBOLS_DIR, symb.tag + ".png")
        if not os.path.exists(filename):
            # Create and save image of that op
            conversions.eq2png(symb.expr, menuitemdata.dpi, temp_dir, filename)

def draw_screen(screen, editingeq, mainmenu):
    """ Draw equation, menuitems and symbols."""
    screen.fill((255, 255, 255))
    screen.blit(editingeq.image, editingeq.rect)
    for menuitem in mainmenu.menuitems:
        screen.blit(menuitem.image, menuitem.rect)
    mainmenu.active_symbs.draw(screen)
    pygame.display.flip()

def main(*args):
    """ This the main function of the program."""
    version = '0.1.2'
    # Prepare a temporal directory to manage all LaTeX files
    temp_dirpath = tempfile.mkdtemp()
    # Prepare pygame
    screen_w = 800
    screen_h = 600
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((screen_w, screen_h), RESIZABLE)
    pygame.display.set_caption("Visual Equation")
    display_splash_screen(screen, temp_dirpath, version)
    # Generate operators' images if the folder is not found
    if not os.path.exists(dirs.PROGRAM_DIR):
        os.makedirs(dirs.PROGRAM_DIR)
    if not os.path.exists(dirs.SYMBOLS_DIR):
        os.makedirs(dirs.SYMBOLS_DIR)
        print_message = True
    else:
        print_message = False
    for index, menuitemdata in enumerate(symbols.MENUITEMSDATA):
        if print_message:
            # Print message about the delay by creating operators' images
            print_delay_message(screen, index+1, len(symbols.MENUITEMSDATA),
                                temp_dirpath)
        generate_symb_images(menuitemdata, temp_dirpath)
    # Create additional images used by Tk
    for symb in symbols.ADDITIONAL_LS:
        filename = os.path.join(dirs.SYMBOLS_DIR, symb.tag + ".png")
        if not os.path.exists(filename):
            conversions.eq2png(symb.expr, 200, temp_dirpath, filename)
    # Prepare the equation to edit which will be showed by default
    init_eq = [symbols.NEWARG]
    screen_center = (screen_w//2, screen_h//2)
    editingeq = maineq.EditableEqSprite(init_eq, screen_center,
                                            temp_dirpath)
    # Create the menu
    mainmenu = menu.Menu(screen_w, screen_h, temp_dirpath)
    # Pygame loop
    ongoing = True
    while ongoing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                ongoing = False
            elif event.type == VIDEORESIZE:
                screen = pygame.display.set_mode(event.size, RESIZABLE)
                editingeq.set_center(event.w//2, event.h//2)
                mainmenu.set_screen_size(event.w, event.h)
            elif event.type == MOUSEBUTTONDOWN:
                for index, menuitem in enumerate(mainmenu.menuitems):
                    if menuitem.mousepointed():
                        mainmenu.select_item(index)
                for symb in mainmenu.active_symbs:
                    if symb.mousepointed():
                        if pygame.key.get_mods() & KMOD_SHIFT:
                            editingeq.insert_substituting(symb.code)
                        else:
                            editingeq.insert(symb.code)
                if editingeq.mousepointed():
                    editingeq.next_sel()
            elif event.type == KEYDOWN:
                try:
                    code = ord(event.unicode)
                    # If it belongs to 0-9 or A-Z or a-z
                    if 48 <= code <= 57 or 65 <= code <= 90 \
                       or 97 <= code <= 122:
                        editingeq.insert(event.unicode)
                except TypeError:
                    pass
                if event.unicode == '\\ ':
                    editingeq.insert(r'\backslash ')
                elif event.unicode == '~':
                    editingeq.insert(r'\sim ')
                elif event.unicode == '!':
                    editingeq.insert('!')
                elif event.unicode == '$':
                    editingeq.insert(r'\$ ')
                elif event.unicode == '%':
                    editingeq.insert(r'\% ')
                elif event.unicode == '&':
                    editingeq.insert(r'\& ')
                elif event.unicode == '/':
                    editingeq.insert('/')
                elif event.unicode == ')':
                    editingeq.insert(')')
                elif event.unicode == '(':
                    editingeq.insert('(')
                elif event.unicode == '=':
                    editingeq.insert('=')
                elif event.unicode == '?':
                    editingeq.insert('?')
                elif event.unicode == "'":
                    editingeq.insert("'")
                elif event.unicode == '@':
                    editingeq.insert('@')
                elif event.unicode == '#':
                    editingeq.insert(r'\# ')
                elif event.unicode == '[':
                    editingeq.insert('[')
                elif event.unicode == ']':
                    editingeq.insert(']')
                elif event.unicode == '{':
                    editingeq.insert(r'\{ ')
                elif event.unicode == '}':
                    editingeq.insert(r'\} ')
                elif event.unicode == '*':
                    editingeq.insert('*')
                elif event.unicode == '+':
                    editingeq.insert('+')
                elif event.unicode == '-':
                    editingeq.insert('-')
                elif event.unicode == '_':
                    editingeq.insert(r'\_ ')
                elif event.unicode == '<':
                    editingeq.insert('<')
                elif event.unicode == '>':
                    editingeq.insert('>')
                elif event.unicode == ',':
                    editingeq.insert(',')
                elif event.unicode == '.':
                    editingeq.insert('.')
                elif event.unicode == ';':
                    editingeq.insert(';')
                elif event.unicode == ':':
                    editingeq.insert(':')
                    # First cases with mods, this avoids false positives
                    # CONTROL + letter
                elif event.key == K_z and pygame.key.get_mods() & KMOD_CTRL:
                    editingeq.recover_prev_eq()
                elif event.key == K_y and pygame.key.get_mods() & KMOD_CTRL:
                    editingeq.recover_next_eq()
                elif event.key == K_s and pygame.key.get_mods() & KMOD_CTRL:
                    editingeq.save_eq()
                elif event.key == K_c and pygame.key.get_mods() & KMOD_CTRL:
                    editingeq.sel2eqbuffer()
                elif event.key == K_x and pygame.key.get_mods() & KMOD_CTRL:
                    editingeq.sel2eqbuffer()
                    editingeq.remove_sel()
                elif event.key == K_v and pygame.key.get_mods() & KMOD_CTRL:
                    editingeq.eqbuffer2sel()
                    # Cases without mods
                elif event.key == K_RIGHT:
                    editingeq.next_sel()
                elif event.key == K_LEFT:
                    editingeq.previous_sel()
                elif event.key == K_UP:
                    mainmenu.next_item()
                elif event.key == K_DOWN:
                    mainmenu.prev_item()
                elif event.key == K_SPACE:
                    editingeq.insert(r'\,')
                elif event.key == K_TAB:
                    editingeq.left_NEWARG()
                elif event.key == K_BACKSPACE or event.key == K_DELETE:
                    editingeq.remove_sel()

        draw_screen(screen, editingeq, mainmenu)
        clock.tick(30)

    # Delete the temporary directory and files before exit
    shutil.rmtree(temp_dirpath)
    sys.exit(0)

if __name__ == '__main__':
    main(*sys.argv[1:])
