import pygame
import latex
import conversions

import operators

class OperSprite(pygame.sprite.Sprite):
    """ A Sprite for the operators to construct the main equation"""
    def __init__(self, eq, center_pos, temp_dir):
        pygame.sprite.Sprite.__init__(self)
        # Create image of the equation in a file
        eq_png = conversions.eq2png(eq, temp_dir)
        # Load the image
        try:
            self.image = pygame.image.load(eq_png).convert_alpha()
        except pygame.error as message:
            raise SystemExit(message)
        self.rect = self.image.get_rect(center=center_pos)
        self.OP = eq[0]

    def mousepointed(self):
        """ Return true if the mouse is over the button."""
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            return True

class EditableEqSprite(pygame.sprite.Sprite):
    """ A Sprite for the equation that is going to be edited."""
    def __init__(self, eq, screen_center, temp_dir):
        pygame.sprite.Sprite.__init__(self)
        self.eq_hist = [list(eq)]
        self.eq_hist_index = 0
        self.eq = eq # It will be mutated by the replace functions
        self.screen_center = screen_center
        self.temp_dir = temp_dir
        self.sel_index = 0
        self._set_sel()

    def _set_sel(self):
        """ Set the image of the sprite to the equation boxed in the
        selection indicated by self.sel_index, which can be freely set
        by the caller before calling this function.

        The box is the way the user know which block of the eq is editing.
        """
        # Calculate the latex code of eq boxed in block given by the selection
        sel_latex_code = latex.eq2sel(self.eq, self.sel_index)
        sel_png = conversions.eq2png(sel_latex_code, self.temp_dir)
        self.image = pygame.image.load(sel_png)
        self.rect = self.image.get_rect(center=self.screen_center)

    def mousepointed(self):
        """ Returns true if the mouse is over """
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            return True

    def next_sel(self):
        """ Set image to the next selection according to self.sel_index. """
        if self.sel_index == len(self.eq) - 1:
            self.sel_index = 0
        else:
            self.sel_index += 1
        self._set_sel()

    def previous_sel(self):
        """ Set image to the next selection according to self.sel_index. """
        if self.sel_index == 0:
            self.sel_index = len(self.eq) - 1
        else:
            self.sel_index -= 1
        self._set_sel()

    def replace_sel_by(self, op):
        """ 
        Given an operator, "replace" the equation block pointed by the
        selection by that operator:

        If it is really a symbol or str, just replace the selection by it.

        If it is an unary operator, put the selected block as the argument
        of the operator.
        
        If it is a binary operator, put the selected block as the first
        argument of the operator. Put NewArg symbol in the second argument.

        If operator is binary, selection index is changed to the second
        argument of the operator because the user probably will want to
        change that argument.
        """
        # Replace according to the operator
        if isinstance(op, (str, operators.Symbol)):
            latex.replace_by_symbol_or_str(self.eq, self.sel_index, op)
        elif isinstance(op, operators.UnaryOperator):
            latex.insert_unary_operator(self.eq, self.sel_index, op)
        elif isinstance(op, operators.BinaryOperator):
            arg2_index = latex.insert_binary_operator(self.eq,
                                                      self.sel_index, op,
                                                      operators.NewArg)
            self.sel_index = arg2_index
        else:
            raise ValueError('Unknown operator passed.')
        self._set_sel()

        # Save current equation to the history and delete any future elements
        # from this point
        self.eq_hist[self.eq_hist_index+1:] = [list(self.eq)]
        self.eq_hist_index += 1

    def recover_prev_eq(self):
        if self.eq_hist_index != 0:
            self.eq_hist_index -= 1
            self.eq = self.eq_hist[self.eq_hist_index]
            self.sel_index = 0
            self._set_sel()

    def recover_next_eq(self):
        if self.eq_hist_index != len(self.eq_hist)-1:
            self.eq_hist_index += 1
            self.eq = self.eq_hist[self.eq_hist_index]
            self.sel_index = 0
            self._set_sel()

    def save_eq(self):
        import tkinter
        from tkinter import filedialog
        file_path = filedialog.asksaveasfilename(defaultextension='.png')
        if file_path != '': # Check if it is the documented condition (!= None)
            conversions.eq2png(self.eq, self.temp_dir, file_path)
