import pygame
import latex
import conversions

import ops


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
        sel_png = conversions.eq2png(sel_latex_code, None, self.temp_dir)
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
        Given an operator, the equation block pointed by self.sel_index
        is "replaced" by that operator:

        If op is a str, just replace the selection by it.

        If op is an unary operator, put the selected block as the argument
        of the operator.
        
        If the operator has more than one argument, put the selected block
        as the first argument of the operator. Put NewArg symbol in the
        second argument.

        If the operator has more than one argument, selection index is
        changed to the second argument of the operator because the user
        probably will want to change that argument.
        """
        # Replace according to the operator
        if isinstance(op, str):
            latex.replace_by_str(self.eq, self.sel_index, op)
        elif isinstance(op, ops.Op) and op.n_args == 1:
            latex.insert_unary_operator(self.eq, self.sel_index, op)
        elif isinstance(op, ops.Op) and op.n_args > 1:
            arg2_index = latex.insert_multiple_operator(self.eq,
                                                        self.sel_index, op,
                                                        ops.NewArg)
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
        # Hide the root window, else it will be present after choosing file
        root = tkinter.Tk()
        root.withdraw()

        file_path = filedialog.asksaveasfilename(defaultextension='.png')
        # TODO: Check if it is the documented condition (None does not work)
        if file_path != '':
            conversions.eq2png(self.eq, None, self.temp_dir, file_path)



        
