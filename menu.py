"""
Module to manage the menu of Visual Equation and the distribution of the
symbols in the above panel.
"""
import os

import pygame

import ops
import conversions

#def distr_in_circle(n_elems, surf_w, surf_h, r_as_percent):
#    import math
#    centerx = surf_w//2
#    centery = surf_h//2
#    r = r_as_percent*min(surf_w, surf_h)/2
#    theta_incr = 2.*math.pi/n_elems
#    for i in range(n_elems):
#        theta = i*theta_incr
#        yield (centerx + int(r*math.cos(theta)),
#               centery + int(r*math.sin(theta)))

def distr_at_top(surf_w, clickable_size):
    """ It returns the center of the rectangles"""
    start_x = (surf_w%clickable_size[0])//2 + clickable_size[0]//2
    x = start_x
    y = clickable_size[1]//2
    yield (x, y)
    while True: # We have the first element above
        if x+clickable_size[0]+clickable_size[0]//2 <= surf_w:
            x += clickable_size[0]
            yield (x, y)
        else:
            y += clickable_size[1]
            x = start_x
            yield (x, y)

#def distr_menuitems_ver(n_elems, surf_h, spacing_x, incr_y):
#    """ It returns the center of the rectangles """
#    x = spacing_x
#    y = (surf_h - incr_y*n_elems)//2
#    yield (x, y)
#    for i in range(n_elems-1): # We have the first element above
#        y += incr_y
#        yield (x, y)

def distr_menuitems_hor(n_elems, surf_w, surf_h, incr_x, spacing_y):
    """ It returns the center of the rectangles """
    y = surf_h - spacing_y
    x = (surf_w - incr_x*n_elems)//2 + incr_x//2
    yield (x, y)
    for _ in range(n_elems-1): # We have the first element above
        x += incr_x
        yield (x, y)

class OpSprite(pygame.sprite.Sprite):
    """
    A Sprite for the symbols/operators in the panel above used to construct
    the main equation. Since there are a lof of elements of this class,
    OpSprite does not generate its own images; they are loaded from a
    directory. It recieves information about the clicking area for each symbol,
    that is typically greater than the real image size, the name of the
    file (without the png extension) and the directory where it is placed."
    """
    def __init__(self, op, center_pos, clickable_size, ops_dir):
        pygame.sprite.Sprite.__init__(self)
        # Cases: (filename, (str|Op, eq)) or, simply, (filename, str|Op)
        if isinstance(op[1], tuple):
            self.op = op[1][0]
        elif isinstance(op[1], (ops.Op, basestring)):
            self.op = op[1]
        else:
            raise ValueError('Unknown type of operator %s', op[1])
        # Load the image
        filename = os.path.join(ops_dir, op[0] + '.png')
        try:
            self.image = pygame.image.load(filename).convert_alpha()
        except pygame.error as message:
            raise SystemExit(message)
        # There is a rect for clicking and a rect with the image;
        # This last one can be very small.
        self.rect = self.image.get_rect(center=center_pos)
        left_top = (center_pos[0]-clickable_size[0]//2,
                    center_pos[1]-clickable_size[1]//2)
        self.clickable_rect = pygame.Rect(left_top, clickable_size)

    def mousepointed(self):
        """ Return true if the mouse is over the button."""
        pos = pygame.mouse.get_pos()
        if self.clickable_rect.collidepoint(pos):
            return True

class MenuItemSprite(pygame.sprite.Sprite):
    """
    A class for the menu items that are in the menu, below the editable
    equation. It contains information about its position and the equation
    that represent it.
    """
    def __init__(self, item, center_pos, temp_dir, dpi=None):
        pygame.sprite.Sprite.__init__(self)
        self.eq = item.menuitem
        self.center_pos = center_pos
        self.temp_dir = temp_dir
        self.dpi = dpi
        eq_png = conversions.eq2png(self.eq, dpi, temp_dir)
        try:
            self.image = pygame.image.load(eq_png).convert_alpha()
        except pygame.error as message:
            raise SystemExit(message)
        self.rect = self.image.get_rect(center=self.center_pos)

    def mousepointed(self):
        """ Return true if the mouse is over the button."""
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            return True

    def select(self):
        """ Put a box around the menuitem symbol"""
        sel_eq = list(self.eq)
        sel_eq.insert(0, ops.EDIT)
        eq_png = conversions.eq2png(sel_eq, self.dpi, self.temp_dir)
        try:
            self.image = pygame.image.load(eq_png).convert_alpha()
        except pygame.error as message:
            raise SystemExit(message)
        self.rect = self.image.get_rect(center=self.center_pos)

    def unselect(self):
        """
        Set the menuitem to its original symbolic equation
        (becuase, probably, it was previously boxed)
        """
        eq_png = conversions.eq2png(self.eq, self.dpi, self.temp_dir)
        try:
            self.image = pygame.image.load(eq_png).convert_alpha()
        except pygame.error as message:
            raise SystemExit(message)
        self.rect = self.image.get_rect(center=self.center_pos)

class Menu(object):
    """ A class that manages the menu items below and the symbols above. """
    def __init__(self, screen_w, screen_h, ops_dir, temp_dir):
        (self.items, self._opsgroups) = self._get_menuitemssprite_opsgroups(
            screen_w, screen_h, ops_dir, temp_dir)
        self._item_index = 0
        self.items[0].select()
        self.active_ops = self._opsgroups[0]

    def _get_menuitemssprite_opsgroups(self, screen_w, screen_h, ops_dir,
                                       temp_dir):
        """
        Read ops.MENUITEMS and returns a list of menu items correctly set
        (position, symbol, etc.) and another list with the associated
        group of symbols/operators that are displayed above for each menuitem.
        """
        g_menuitem_pos = distr_menuitems_hor(len(ops.MENUITEMS), screen_w,
                                             screen_h, 60, 30)
        menuitems = []
        opsgroups = []
        for item in ops.MENUITEMS:
            # Create menu items
            menuitem_pos = next(g_menuitem_pos)
            item_sprite = MenuItemSprite(item, menuitem_pos, temp_dir, 200)
            menuitems.append(item_sprite)
            # Create the group for the symbols associated to that menu item
            g_ops_pos = distr_at_top(screen_w, item.clickable_size)
            ops_group = pygame.sprite.Group()
            for op in item.ops_l:
                op_center_pos = next(g_ops_pos)
                op_sprite = OpSprite(op, op_center_pos, item.clickable_size,
                                     ops_dir)
                ops_group.add(op_sprite)
            opsgroups.append(ops_group)

        return menuitems, opsgroups

    def select_item(self, index):
        """ Select a menu item, correcting the image that represent it,
        (boxing and unboxing) and changing the group of ops associated.
        """
        # Change the selected menu item
        self.items[self._item_index].unselect()
        self._item_index = index
        self.items[self._item_index].select()
        # Change active operations
        self.active_ops = self._opsgroups[index]

    def next_item(self):
        """ Like self.select_item but using the next item. Useful to be called
        by keys events instead of mouse clicks."""
        self.items[self._item_index].unselect()
        if self._item_index == len(self.items) - 1:
            self._item_index = 0
        else:
            self._item_index += 1
        self.items[self._item_index].select()
        self.active_ops = self._opsgroups[self._item_index]

    def prev_item(self):
        """ Like self.select_item but using the previous item. Useful to
        be called by keys events instead of mouse clicks."""
        self.items[self._item_index].unselect()
        if self._item_index == 0:
            self._item_index = len(self.items) - 1
        else:
            self._item_index -= 1
        self.items[self._item_index].select()
        self.active_ops = self._opsgroups[self._item_index]
