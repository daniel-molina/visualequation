# visualequation is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# visualequation is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""
Module to manage the menu of Visual Equation and the distribution of the
symbols in the above panel.
"""
import os

import pygame

import dirs
import symbols
import conversions

def distr_at_top(n_elems, surf_w, clickable_size):
    """ It returns the center of the rectangles"""
    max_elems_per_row = surf_w//clickable_size[0]
    if n_elems >= max_elems_per_row:
        start_x = (surf_w%clickable_size[0])//2 + clickable_size[0]//2
    else:
        start_x = (surf_w - n_elems*clickable_size[0])//2 \
                  + clickable_size[0]//2
    x = start_x
    y = clickable_size[1]//2
    yield (x, y)
    for elem in range(1, n_elems): # We have the first element above
        if x+clickable_size[0]+clickable_size[0]//2 <= surf_w:
            x += clickable_size[0]
            yield (x, y)
        else:
            y += clickable_size[1]
            if n_elems-elem >= max_elems_per_row: # Remaining elems
                start_x = (surf_w%clickable_size[0])//2 + clickable_size[0]//2
            else:
                start_x = (surf_w - (n_elems-elem)*clickable_size[0])//2 \
                          + clickable_size[0]//2
            x = start_x
            yield (x, y)

def distr_menuitems_hor(n_elems, surf_w, surf_h, incr_x, spacing_y):
    """ It returns the center of the rectangles """
    y = surf_h - spacing_y
    x = (surf_w - incr_x*n_elems)//2 + incr_x//2
    yield (x, y)
    for _ in range(n_elems-1): # We have the first element above
        x += incr_x
        yield (x, y)

class SymbSprite(pygame.sprite.Sprite):
    """
    A Sprite for the symbols/operators in the panel above used to construct
    the main equation. Since there are a lof of elements of this class,
    OpSprite does not generate its own images; they are loaded from a
    directory. It recieves information about the clicking area for each symbol,
    that is typically greater than the real image size, the name of the
    file (without the png extension) and the directory where it is placed."
    """
    def __init__(self, symb, center_pos, clickable_size):
        pygame.sprite.Sprite.__init__(self)
        self.code = symb.code
        # Load the image
        filename = os.path.join(dirs.SYMBOLS_DIR, symb.tag + '.png')
        if not os.path.exists(filename):
            raise SystemExit("Error: Menu symbol " + symb.tag
                             + " was not found. If you "
                             + "installed from source, did you forget to run "
                             + "the populate_symbols.py script?")
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

    def set_center(self, center_pos, clickable_size):
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
    def __init__(self, menuitem, center_pos, temp_dir, dpi=None):
        pygame.sprite.Sprite.__init__(self)
        self.eq = [menuitem.expr]
        self.center_pos = center_pos
        self.temp_dir = temp_dir
        self.dpi = dpi
        eq_png = conversions.eq2png(self.eq, dpi, None, temp_dir)
        try:
            self.image = pygame.image.load(eq_png).convert_alpha()
        except pygame.error as message:
            raise SystemExit(message)
        self.rect = self.image.get_rect(center=self.center_pos)

    def set_center(self, center_pos):
        self.center_pos = center_pos
        self.rect = self.image.get_rect(center=self.center_pos)

    def mousepointed(self):
        """ Return true if the mouse is over the button."""
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            return True

    def select(self):
        """ Put a box around the menuitem symbol"""
        sel_eq = list(self.eq)
        sel_eq.insert(0, symbols.EDIT)
        eq_png = conversions.eq2png(sel_eq, self.dpi, None, self.temp_dir)
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
        eq_png = conversions.eq2png(self.eq, self.dpi, None, self.temp_dir)
        try:
            self.image = pygame.image.load(eq_png).convert_alpha()
        except pygame.error as message:
            raise SystemExit(message)
        self.rect = self.image.get_rect(center=self.center_pos)

def _data2sprites(screen_w, screen_h, temp_dir):
    """
    Read symbols.MENUITEMSDATA and returns a list of menu items correctly set
    (position, expr, etc.) and another list with the associated "group"
    of symbols for each menu item also set.
    """
    g_menuitem_pos = distr_menuitems_hor(len(symbols.MENUITEMSDATA), screen_w,
                                         screen_h, 60, 30)
    menuitems = []
    symbsgroups = []
    for menuitemdata in symbols.MENUITEMSDATA:
        # Create menu items
        menuitem_center_pos = next(g_menuitem_pos)
        menuitemsprite = MenuItemSprite(menuitemdata, menuitem_center_pos,
                                        temp_dir, 200)
        menuitems.append(menuitemsprite)
        # Create the "group" for the symbols associated to that menu item
        g_symb_pos = distr_at_top(len(menuitemdata.symb_l), screen_w,
                                  menuitemdata.clickable_size)
        # We want to keep the order of the operators since we need
        # to change its positions (in order) when resizing the window.
        # That is the only reason I am using OrderedUpdates instead.
        # So, even if we called it group, it is not really a pygame group.
        symbsgroup = pygame.sprite.OrderedUpdates()
        # Save clickable_size as an attribute
        symbsgroup.clickable_size = menuitemdata.clickable_size
        for symb in menuitemdata.symb_l:
            symb_center_pos = next(g_symb_pos)
            symbsprite = SymbSprite(symb, symb_center_pos,
                                    menuitemdata.clickable_size)
            symbsgroup.add(symbsprite)
        symbsgroups.append(symbsgroup)
    return menuitems, symbsgroups

class Menu(object):
    """ A class that manages the menu items below and the symbols above. """
    def __init__(self, screen_w, screen_h, temp_dir):
        self.menuitems, self._symbsgroups = _data2sprites(screen_w, screen_h,
                                                          temp_dir)
        self._menuitem_index = 0
        self.menuitems[self._menuitem_index].select()
        self.active_symbs = self._symbsgroups[self._menuitem_index]

    def set_screen_size(self, screen_w, screen_h):
        # Set new menuitems' positions
        g_menuitem_pos = distr_menuitems_hor(len(symbols.MENUITEMSDATA),
                                             screen_w, screen_h, 60, 30)
        for menuitem in self.menuitems:
            menuitem.set_center(next(g_menuitem_pos))
        # Set new symbols' positions
        for symbsgroup in self._symbsgroups:
            g_ops_pos = distr_at_top(len(symbsgroup), screen_w,
                                     symbsgroup.clickable_size)
            for symb in symbsgroup:
                symb.set_center(next(g_ops_pos), symbsgroup.clickable_size)

    def select_item(self, index):
        """ Select a menu item, correcting the image that represent it,
        (boxing and unboxing) and changing the group of ops associated.
        """
        # Change the selected menu item
        self.menuitems[self._menuitem_index].unselect()
        self._menuitem_index = index
        self.menuitems[self._menuitem_index].select()
        # Change active operations
        self.active_symbs = self._symbsgroups[index]

    def next_item(self):
        """ Like self.select_item but using the next item. Useful to be called
        by keys events instead of mouse clicks."""
        self.menuitems[self._menuitem_index].unselect()
        if self._menuitem_index == len(self.menuitems) - 1:
            self._menuitem_index = 0
        else:
            self._menuitem_index += 1
        self.menuitems[self._menuitem_index].select()
        self.active_symbs = self._symbsgroups[self._menuitem_index]

    def prev_item(self):
        """ Like self.select_item but using the previous item. Useful to
        be called by keys events instead of mouse clicks."""
        self.menuitems[self._menuitem_index].unselect()
        if self._menuitem_index == 0:
            self._menuitem_index = len(self.menuitems) - 1
        else:
            self._menuitem_index -= 1
        self.menuitems[self._menuitem_index].select()
        self.active_symbs = self._symbsgroups[self._menuitem_index]
