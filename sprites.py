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
    def __init__(self, eq, screen, temp_dir):
        pygame.sprite.Sprite.__init__(self)
        self.eq_hist = [list(eq)]
        self.eq_hist_index = 0
        self.eq = eq # It will be mutated by the replace functions
        self.screen_center = (screen.get_width()//2, screen.get_height()//2)
        self.screen = screen
        self.temp_dir = temp_dir
        self.sels_index = 0
        self._set_sels()

    def _set_sels(self):
        """Create a new list with the images of all the possible selections of
        the equation and set the image to the selection indicated by
        self.sels_index, which can be freely set by the caller before
        calling.

        In addition, firstly, it calculates the selection of that image and
        show it in the screen so it appears instantaneously to the user.
        It plots also some advice to the user (red background by now), which
        will disappear when refreshing the sprites, to indicate that
        user interaction is suspended due to the loading of the selections
        (it carries some time, specially for long equations).
        """
        # Calculate current selection of the new eq and blit it NOW
        # It is skipped in the first call by __init__
        if hasattr(self, 'image'):
            sel_code_current = latex.eq2sel(self.eq, self.sels_index)
            sel_png_current = conversions.eq2png(sel_code_current,
                                                 self.temp_dir)
            sel_image_current = pygame.image.load(sel_png_current)
            sel_rect_current = sel_image_current.get_rect(
                center=self.screen_center)

            self.screen.fill((255, 0, 0), self.rect)
            self.screen.blit(sel_image_current, sel_rect_current)
            pygame.display.flip()
            # Update information of displayed image
            self.image = sel_image_current
            self.rect = sel_rect_current

        # Now fulfill self.sels, independently of the above code
        self.sels = []
        for sel_code in latex.eq2sels_code(self.eq):
            sel_png = conversions.eq2png(sel_code, self.temp_dir)
            self.sels.append(pygame.image.load(sel_png))

        # Set the current image as the selection with index self.sels_index
        self.image = self.sels[self.sels_index]
        self.rect = self.image.get_rect(center=self.screen_center)

    def mousepointed(self):
        """ Returns true if the mouse is over """
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            return True

    def next_sel(self):
        """ Set image to the next selection according to self.sels_index. """
        if self.sels_index == len(self.sels) - 1:
            self.sels_index = 0
        else:
            self.sels_index += 1

        self.image = self.sels[self.sels_index]
        self.rect = self.image.get_rect(center=self.screen_center)

    def previous_sel(self):
        """ Set image to the next selection according to self.sels_index. """
        if self.sels_index == 0:
            self.sels_index = len(self.sels) - 1
        else:
            self.sels_index -= 1

        self.image = self.sels[self.sels_index]
        self.rect = self.image.get_rect(center=self.screen_center)

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
            latex.replace_by_symbol_or_str(self.eq, self.sels_index, op)
        elif isinstance(op, operators.UnaryOperator):
            latex.insert_unary_operator(self.eq, self.sels_index, op)
        elif isinstance(op, operators.BinaryOperator):
            arg2_index = latex.insert_binary_operator(self.eq,
                                                      self.sels_index, op,
                                                      operators.NewArg)
            self.sels_index = arg2_index
        else:
            raise ValueError('Unknown subeq passed.')
        self._set_sels()

        # Save current equation to the history and delete any future elements
        # from this point
        self.eq_hist[self.eq_hist_index+1:] = [list(self.eq)]
        self.eq_hist_index += 1

    def recover_prev_eq(self):
        if self.eq_hist_index != 0:
            self.eq_hist_index -= 1
            self.eq = self.eq_hist[self.eq_hist_index]
            self.sels_index = 0
            self._set_sels()

    def recover_next_eq(self):
        if self.eq_hist_index != len(self.eq_hist)-1:
            self.eq_hist_index += 1
            self.eq = self.eq_hist[self.eq_hist_index]
            self.sels_index = 0
            self._set_sels()

    def save_eq(self):
        import tkinter
        from tkinter import filedialog
        file_path = filedialog.asksaveasfilename(defaultextension='.png')
        if file_path != '': # Check if it is the documented condition (!= None)
            conversions.eq2png(self.eq, self.temp_dir, file_path)
