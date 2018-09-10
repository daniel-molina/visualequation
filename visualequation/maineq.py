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

""" The module that manages the editing equation. """
import types

import pygame
import Tkinter, tkFileDialog

import eqtools
import conversions
import symbols

class EditableEqSprite(pygame.sprite.Sprite):
    """ A Sprite for the equation that is going to be edited."""
    def __init__(self, eq, screen_center, temp_dir):
        pygame.sprite.Sprite.__init__(self)
        self.image = None
        self.rect = None
        self.eq_hist = [(list(eq), 0)]
        self.eq_hist_index = 0
        self.eq_buffer = []
        self.eq = list(eq) # It will be mutated by the replace functions
        self.screen_center = screen_center
        self.temp_dir = temp_dir
        self.sel_index = 0
        self._set_sel()

    def set_center(self, x, y):
        self.screen_center = (x, y)
        self.rect = self.image.get_rect(center=self.screen_center)

    def is_intermediate_JUXT(self, index):
        """
        Check whether if index points to a JUXT that is the argument of
        other JUXT.
        """
        if self.eq[index] == symbols.JUXT:
            cond, _, _ = eqtools.is_arg_of_JUXT(self.eq, index)
            if cond:
                return True
        return False

    def _set_sel(self):
        """ Set the self.image to the equation boxed in the
        selection indicated by self.sel_index, which can be freely set
        by the caller before calling this function.

        The box is the way the user know which block of the eq is editing.
        """
        if not 0 <= self.sel_index < len(self.eq):
            raise ValueError('Provided index outside the equation.')
        # Avoid pointing to a intermediate Juxt
        # That avoids selecting partial products inside a product
        elif self.is_intermediate_JUXT(self.sel_index):
            cond = True
            while cond:
                self.sel_index += 1
                cond = self.is_intermediate_JUXT(self.sel_index)

        # Calculate the latex code of eq boxed in block given by the selection
        sel_latex_code = eqtools.sel_eq(self.eq, self.sel_index)
        sel_png = conversions.eq2png(sel_latex_code, None, None,
                                     self.temp_dir)
        try:
            self.image = pygame.image.load(sel_png)
        except pygame.error as message:
            raise SystemExit(message)
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
        if self.is_intermediate_JUXT(self.sel_index):
            cond = True
            while cond:
                self.sel_index += 1
                cond = self.is_intermediate_JUXT(self.sel_index)

        self._set_sel()

    def previous_sel(self):
        """ Set image to the next selection according to self.sel_index. """
        if self.sel_index == 0:
            self.sel_index = len(self.eq) - 1
        else:
            self.sel_index -= 1
        if self.is_intermediate_JUXT(self.sel_index):
            cond = True
            while cond:
                self.sel_index -= 1
                cond = self.is_intermediate_JUXT(self.sel_index)

        self._set_sel()

    def insert_substituting(self, oper):
        """
        Given an operator, the equation block pointed by self.sel_index
        is replaced by that operator and the selection is used as follows:

        If op is a str, just replace it.

        If op is an unary operator, put the selected block as the argument
        of the operator.

        If the operator has more than one argument, put the selected block
        as the first argument of the operator. Put NewArg symbols in the
        rest of the arguments.

        If the operator has more than one argument, selection index is
        changed to the second argument of the operator because the user
        probably will want to change that argument.
        """
        def replace_op_in_eq(op):
            """
            Given an operator, it is replaced in self.eq according to
            the rules of above. It also modify self.sel_index to point to
            the smartest block.
            """
            if isinstance(op, basestring):
                eqtools.replaceby(self.eq, self.sel_index, [op])
            elif isinstance(op, symbols.Op) and op.n_args == 1:
                self.eq.insert(self.sel_index, op)
            elif isinstance(op, symbols.Op) and op.n_args > 1:
                index_end_arg1 = eqtools.nextblockindex(self.eq, self.sel_index)
                self.eq[self.sel_index:index_end_arg1] = [op] \
                                    + self.eq[self.sel_index:index_end_arg1] \
                                    + [symbols.NEWARG] * (op.n_args-1)
                self.sel_index = index_end_arg1+1
            else:
                raise ValueError('Unknown operator passed.')

        if isinstance(oper, types.FunctionType):
            replace_op_in_eq(oper())
        else:
            replace_op_in_eq(oper)

        self._set_sel()
        self.add_eq2hist()

    def insert(self, oper):
        """
        Insert the operator next to selection by Juxt.
        If operator has one or more args, all of them are set to NewArg.
        """
        def replace_op_in_eq(op):
            """
            Given an operator, it is replaced in self.eq according to
            the rules of above. It also modify self.sel_index to point to
            the smartest block.
            """            
            if isinstance(op, basestring):
                if self.eq[self.sel_index] == symbols.NEWARG:
                    self.eq[self.sel_index] = op
                else:
                    self.sel_index = eqtools.appendbyJUXT(self.eq,
                                                          self.sel_index,
                                                          [op])
            elif isinstance(op, symbols.Op):
                opeq = [op] + [symbols.NEWARG]*op.n_args
                if self.eq[self.sel_index] == symbols.NEWARG:
                    self.eq[self.sel_index:self.sel_index+1] = opeq
                    self.sel_index += 1
                else:
                    self.sel_index = 1 + eqtools.appendbyJUXT(self.eq,
                                                              self.sel_index,
                                                              opeq)
            else:
                raise ValueError('Unknown type of operator %s' % op)

        if isinstance(oper, types.FunctionType):
            replace_op_in_eq(oper())
        else:
            replace_op_in_eq(oper)

        self._set_sel()
        self.add_eq2hist()

    def add_eq2hist(self):
        """
        Save current equation to the historial and delete any future elements
        from this point
        """
        self.eq_hist[self.eq_hist_index+1:] = [(list(self.eq), self.sel_index)]
        self.eq_hist_index += 1

    def recover_prev_eq(self):
        """ Recover previous equation from the historial, if any """
        if self.eq_hist_index != 0:
            self.eq_hist_index -= 1
            eq, sel_index = self.eq_hist[self.eq_hist_index]
            self.eq = list(eq)
            self.sel_index = sel_index
            self._set_sel()

    def recover_next_eq(self):
        """ Recover next equation from the historial, if any """
        if self.eq_hist_index != len(self.eq_hist)-1:
            self.eq_hist_index += 1
            eq, sel_index = self.eq_hist[self.eq_hist_index]
            self.eq = list(eq)
            self.sel_index = sel_index
            self._set_sel()

    def remove_sel(self):
        """
        If self.sel_index points to the first or second arg of a Juxt,
        it removes the Juxt and leaves the other argument in its place.
        Else, it removes the block pointed and put a NEWARG.
        """
        cond, JUXT_index, other_arg_index = eqtools.is_arg_of_JUXT(
            self.eq, self.sel_index)
        if cond:
            JUXT_end = eqtools.nextblockindex(self.eq, JUXT_index)
            # If sel_index is the first argument (instead of the second)
            if JUXT_index + 1 == self.sel_index:
                self.eq[JUXT_index:JUXT_end] = self.eq[
                    other_arg_index:JUXT_end]
            else:
                self.eq[JUXT_index:JUXT_end] = self.eq[
                    other_arg_index:self.sel_index]
            self.sel_index = JUXT_index
        else:
            eqtools.replaceby(self.eq, self.sel_index, [symbols.NEWARG])

        self._set_sel()
        self.add_eq2hist()

    def sel2eqbuffer(self):
        """ Copy block pointed by self.sel_index to self.eq_buffer """
        end_sel_index = eqtools.nextblockindex(self.eq, self.sel_index)
        self.eq_buffer = self.eq[self.sel_index:end_sel_index]

    def eqbuffer2sel(self):
        """
        Append self.eq_buffer to the right of the block pointed by
        self.sel_index. If the block is a NEWARG, just replace it.
        """
        if self.eq[self.sel_index] == symbols.NEWARG:
            self.eq[self.sel_index:self.sel_index+1] = self.eq_buffer
        else:
            self.sel_index = eqtools.appendbyJUXT(self.eq, self.sel_index,
                                                self.eq_buffer)
        self._set_sel()
        self.add_eq2hist()

    def left_NEWARG(self):
        """
        Append by JUXT a NEWARG at the left of the block pointed by
        self.sel_index. """
        self.eq[self.sel_index:self.sel_index] = [symbols.JUXT, symbols.NEWARG]
        self.sel_index += 1
        self._set_sel()
        self.add_eq2hist()

    def save_eq(self):
        """ Open Dialog to save the equation to PNG """
        class FileFormat(object):
            """Choose a file format."""
            def __init__(self):
                self.fileformat = ''
            def set(self, root, fileformat):
                self.fileformat = fileformat
                root.quit()
            def get_ext(self):
                return '.' + self.fileformat
        fileformat = FileFormat()
        root = Tkinter.Tk()
        root.title("Save equation")
        Tkinter.Label(root, text='Choose format').pack(side=Tkinter.TOP)
        Tkinter.Button(root, text='PNG',
                       command=lambda *args: fileformat.set(root, 'png')
        ).pack(side=Tkinter.TOP)
        Tkinter.Button(root, text='PDF',
                       command=lambda *args: fileformat.set(root, 'pdf')
        ).pack(side=Tkinter.TOP)
        Tkinter.Button(root, text='SVG*',
                       command=lambda *args: fileformat.set(root, 'svg')
        ).pack(side=Tkinter.TOP)
        Tkinter.Button(root, text='EPS*',
                       command=lambda *args: fileformat.set(root, 'ps')
        ).pack(side=Tkinter.TOP)
        Tkinter.Label(root,
                      text="* It will NOT be possible\nto open equations\n" +
                      "for further edition\nfrom files in this format."
                      ).pack(side=Tkinter.TOP)
        root.mainloop()
        # Hide the root window
        if fileformat.get_ext() != '.':
            root.withdraw()
            file_path = tkFileDialog.asksaveasfilename(
                defaultextension=fileformat.get_ext(),
                filetypes=[(fileformat.get_ext()[1:], fileformat.get_ext())])
            # It returns () or '' if file is not chosen (Exit or Cancel)
            if file_path:
                if fileformat.get_ext() == '.png':
                    conversions.eq2png(self.eq, 600, None, self.temp_dir,
                                       file_path, True)
                elif fileformat.get_ext() == '.pdf':
                    conversions.eq2pdf(self.eq, self.temp_dir, file_path)
                elif fileformat.get_ext() == '.svg':
                    conversions.eq2svg(self.eq, self.temp_dir, file_path)
                elif fileformat.get_ext() == '.ps':
                    conversions.eq2eps(self.eq, self.temp_dir, file_path)
            root.destroy()
