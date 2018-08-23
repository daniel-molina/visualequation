#!/usr/bin/env python3
import sys

import pygame
from pygame.locals import *

from operators import *
import latex
import conversions

class EqSprite(pygame.sprite.Sprite):
    def __init__(self, eq, pos):
        pygame.sprite.Sprite.__init__(self)
        # Create image of the equation in a file
        eq_png = conversions.eq2png(eq, "overwrite_me")
        # Load the image
        try:
            self.image = pygame.image.load(eq_png).convert_alpha()
        except pygame.error as message:
            raise SystemExit(message)

        self.rect = self.image.get_rect(center=pos)

class SelectEqSprite(EqSprite):
    def __init__(self, eq, pos):
        EqSprite.__init__(self, eq, pos)

    def clicked(self):
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            return True

class EditableEqSprite(pygame.sprite.Sprite):
    def __init__(self, eq, pos):
        pygame.sprite.Sprite.__init__(self)
        self.sels = []
        for sel_code in latex.eq2sels_code(eq):
            sel_png = conversions.eq2png(sel_code, "foo")
            self.sels.append(pygame.image.load(sel_png))
        self.sels_index = 0
        self.image = self.sels[self.sels_index]
        self.rect = self.image.get_rect(center=pos)

    def clicked(self):
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            return True

    def next_sel(self):
        self.sels_index += 1
        if self.sels_index == len(self.sels):
            self.sels_index = 0
        self.image = self.sels[self.sels_index]
        #self.rect = self.image.get_rect(center=pos)

def distr_in_circle(n_elems, surf_w, surf_h, r_as_percent):
    import math
    centerx = surf_w//2
    centery = surf_h//2
    r = r_as_percent*min(surf_w, surf_h)/2
    theta_incr = 2.*math.pi/n_elems
    theta = 0.
    while theta < 2*math.pi:
        yield (centerx + int(r*math.cos(theta)),
               centery + int(r*math.sin(theta)))
        theta += theta_incr
    else:
        raise StopIteration

if __name__ == "__main__":

    # Prepare pygame
    pygame.init()
    clock = pygame.time.Clock()

    # Prepare display
    screen_w = 800
    screen_h = 600
    screen = pygame.display.set_mode((screen_w, screen_h))
    background = pygame.image.load("pygame-badge-SMA.png")
    screen.blit(background, (0, 0))
    pygame.display.set_caption("Visual Equation")
    pygame.display.flip()

    # Display an equation in the middle
    eq = [Prod, Frac, Prod, Prod, Prod, '2', Pi, 'r', 'j' , Bullet, Pow, 'y', Prod, '2', 'h']
    main_eqsprite = EditableEqSprite(eq, (screen_w//2, screen_h//2))

    # Prepare equations to move around the window
    eqs_select = [[Frac, Bullet, Bullet], ['x'], ['y'], [Pi], ['2'],
                  [Pow, Bullet, Bullet], [Parenthesis, Bullet]]
    positions = [pos for pos in distr_in_circle(len(eqs_select), screen_w,
                                                screen_h, 0.7)]
    eqs_select_sprite = tuple(SelectEqSprite(eq, pos) for eq, pos
                              in zip(eqs_select, positions))
 
    allsprites = pygame.sprite.RenderPlain(eqs_select_sprite
                                           + (main_eqsprite,))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
            elif event.type == MOUSEBUTTONDOWN:
                for eq in eqs_select_sprite:
                    if eq.clicked():
                        print("Clicked!")
                if main_eqsprite.clicked():
                    main_eqsprite.next_sel()

        screen.fill((255, 255, 255))
        allsprites.update()
        allsprites.draw(screen)
        pygame.display.flip()
        clock.tick(30)
