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
import os
import types

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from . import eqtools
from . import eqhist
from . import conversions
from .symbols import utils
from . import game

class Eq:
    def __init__(self, temp_dir, setPixmap, parent):

        init_eq = [utils.NEWARG]
        self.eq_buffer = []
        self.eq = list(init_eq) # It will be mutated by the replace functions
        self.temp_dir = temp_dir
        self.setPixmap = setPixmap
        self.parent = parent
        self.eqhist = eqhist.EqHist(init_eq)
        self.game = game.Game()
        self.sel_index = 0
        self.sel_right = True
        self.update()

    def update(self):
        """ Set pixmap to the equation boxed in the
        selection indicated by self.sel_index, which can be freely set
        by the caller before calling this function.

        (The box is the way the user know which block of the eq is editing).
        """
        if not 0 <= self.sel_index < len(self.eq):
            raise ValueError('Provided index outside the equation.')
        # Avoid pointing to a intermediate Juxt
        # That avoids selecting partial products inside a product
        #elif eqtools.is_intermediate_JUXT(self.eq, self.sel_index):
        #    cond = True
        #    while cond:
        #        self.sel_index += 1
        #        cond = eqtools.is_intermediate_JUXT(self.eq, self.sel_index)

        # Calculate the latex code of eq boxed in block given by the selection
        sel_eq = eqtools.sel_eq(self.eq, self.sel_index, self.sel_right)
        self.game.update(sel_eq)
        sel_png = conversions.eq2png(sel_eq, None, None,
                                     self.temp_dir)
        self.setPixmap(QPixmap(sel_png))
        # This may help catching all the keys
        #self.setFocus()

    def next_sel(self):
        """ Set image to the next selection according to self.sel_index. """
        if not self.sel_right:
            self.sel_right = True
        elif self.sel_index == len(self.eq) - 1:
            self.sel_index = 0
        else:
            self.sel_index += 1
        if eqtools.is_intermediate_JUXT(self.eq, self.sel_index):
            cond = True
            while cond:
                self.sel_index += 1
                cond = eqtools.is_intermediate_JUXT(self.eq, self.sel_index)

        self.update()

    def previous_sel(self):
        """ Set image to the next selection according to self.sel_index. """
        if self.sel_right:
            self.sel_right = False
        elif self.sel_index == 0:
            self.sel_index = len(self.eq) - 1
        else:
            self.sel_index -= 1
        if eqtools.is_intermediate_JUXT(self.eq, self.sel_index):
            cond = True
            while cond:
                self.sel_index -= 1
                cond = eqtools.is_intermediate_JUXT(self.eq, self.sel_index)

        self.update()

    def insert(self, oper):
        """
        Insert a symbol next to selection by Juxt and, if it is an operator,
        set all the arguments to NewArg.
        """
        def replace_op_in_eq(op):
            """
            Given an operator, it is replaced in self.eq according to
            the rules of above. It also modify self.sel_index to point to
            the smartest block.
            """            
            if isinstance(op, str):
                if self.eq[self.sel_index] == utils.NEWARG:
                    self.eq[self.sel_index] = op
                else:
                    if self.sel_right:
                        self.sel_index = eqtools.insertrbyJUXT(self.eq,
                                                               self.sel_index,
                                                               [op])
                    else:
                        self.sel_index = eqtools.insertlbyJUXT(self.eq,
                                                               self.sel_index,
                                                               [op])
            elif isinstance(op, utils.Op):
                opeq = [op] + [utils.NEWARG]*op.n_args
                if self.eq[self.sel_index] == utils.NEWARG:
                    self.eq[self.sel_index:self.sel_index+1] = opeq
                    self.sel_index += 1
                else:
                    if self.sel_right:
                        self.sel_index \
                            = 1 + eqtools.insertrbyJUXT(self.eq,
                                                        self.sel_index,
                                                        opeq)
                    else:
                        self.sel_index \
                            = 1 + eqtools.insertlbyJUXT(self.eq,
                                                        self.sel_index,
                                                        opeq)
            else:
                raise ValueError('Unknown type of operator %s' % op)

        if isinstance(oper, types.FunctionType):
            op = oper(self.parent)
            if op:
                replace_op_in_eq(op)
            else:
                return None
        else:
            replace_op_in_eq(oper)

        self.sel_right = True
        self.update()
        self.eqhist.save(self.eq, self.sel_index)

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
            if isinstance(op, str):
                eqtools.replaceby(self.eq, self.sel_index, [op])
            elif isinstance(op, utils.Op) and op.n_args == 1:
                self.eq.insert(self.sel_index, op)
            elif isinstance(op, utils.Op) and op.n_args > 1:
                index_end_arg1 = eqtools.nextblockindex(self.eq, self.sel_index)
                self.eq[self.sel_index:index_end_arg1] = [op] \
                                    + self.eq[self.sel_index:index_end_arg1] \
                                    + [utils.NEWARG] * (op.n_args-1)
                self.sel_index = index_end_arg1+1
            else:
                raise ValueError('Unknown operator passed.')

        if isinstance(oper, types.FunctionType):
            op = oper(self.parent)
            if op:
                replace_op_in_eq(op)
            else:
                return None
        else:
            replace_op_in_eq(oper)

        self.sel_right = True
        self.update()
        self.eqhist.save(self.eq, self.sel_index)

    def insert_sup_substituting(self):
        # Consider that the user specifies the first argument of index operator
        if self.eq[self.sel_index] not in utils.INDEX_OPS \
           and self.sel_index > 0 \
           and self.eq[self.sel_index-1] in utils.INDEX_OPS:
            # In that case, we change sel_index as if the index operator was
            # selected (it is a non-standard use of sel_index just to avoid
            # complicated code with more if-clauses)
            self.sel_index -= 1
        # Create a list with a index arg list
        args = eqtools.indexop2arglist(self.eq, self.sel_index)
        # Change it to add the new index
        if self.sel_right:
            up_index = 3
            if not args[up_index]:
                args[up_index] = [utils.NEWARG]
            elems = 0
            for i in range(up_index):
                if args[i] != None:
                    elems += len(args[i])
        else: # if not self.sel_right
            up_index = 4
            if not args[up_index]:
                args[up_index] = [utils.NEWARG]
            elems = 0
            for i in range(up_index):
                if args[i] != None:
                    elems += len(args[i])

        new_op = eqtools.arglist2indexop(args)
        # Flat the list of args
        new_args = eqtools.flat_arglist(args)
        new_block = [new_op] + new_args
        end_old_block = eqtools.nextblockindex(self.eq, self.sel_index) 
        self.eq[self.sel_index:end_old_block] = new_block

        # There is always an operator after adding an index
        self.sel_index += 1 + elems
        self.sel_right = True
        self.update()
        self.eqhist.save(self.eq, self.sel_index)

    def insert_sub_substituting(self):
        # Consider that the user specifies the first argument of index operator
        if self.eq[self.sel_index] not in utils.INDEX_OPS \
           and self.sel_index > 0 \
           and self.eq[self.sel_index-1] in utils.INDEX_OPS:
            # In that case, we change sel_index as if the index operator was
            # selected (it is a non-standard use of sel_index just to avoid
            # complicated code with more if-clauses)
            self.sel_index -= 1
        # Create a list with a index arg list
        args = eqtools.indexop2arglist(self.eq, self.sel_index)
        # Change it to add the new index
        if self.sel_right:
            down_index = 2
            if not args[down_index]:
                args[down_index] = [utils.NEWARG]
            elems = 0
            for i in range(down_index):
                if args[i] != None:
                    elems += len(args[i])
        else: # if not self.sel_right
            down_index = 1
            if not args[down_index]:
                args[down_index] = [utils.NEWARG]
            elems = 0
            for i in range(down_index):
                if args[i] != None:
                    elems += len(args[i])

        new_op = eqtools.arglist2indexop(args)
        # Flat the list of args
        new_args = eqtools.flat_arglist(args)
        new_block = [new_op] + new_args
        end_old_block = eqtools.nextblockindex(self.eq, self.sel_index) 
        self.eq[self.sel_index:end_old_block] = new_block

        # There is always an operator after adding an index
        self.sel_index += 1 + elems
        self.sel_right = True
        self.update()
        self.eqhist.save(self.eq, self.sel_index)

    def remove_sel(self):
        """
        If self.sel_index points to the first or second arg of a Juxt,
        it removes the Juxt and leaves the other argument in its place.
        If it is a script, it removes it if it is equal to square.
        Else, it removes the block pointed and put a NEWARG.
        """
        cond_arg_JUXT, JUXT_index, other_arg_index = eqtools.is_arg_of_JUXT(
            self.eq, self.sel_index)
        if cond_arg_JUXT:
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
            # If it is the index of a script, downgrade the index operator
            cond_script, script_op_index, arg_pos = eqtools.is_script(
                self.eq, self.sel_index)
            if cond_script:
                args = eqtools.indexop2arglist(self.eq, script_op_index)
                # Find which element of the list has to be removed
                arg_index = 0
                for index, arg in enumerate(args):
                    if arg is not None:
                        if arg_index == arg_pos:
                            args[index] = None
                            break
                        else:
                            arg_index += 1
                new_op = eqtools.arglist2indexop(args)
                end_block = eqtools.nextblockindex(self.eq, script_op_index)
                if new_op is None:
                    self.eq[script_op_index:end_block] = args[0]
                else:
                    new_args = eqtools.flat_arglist(args)
                    self.eq[script_op_index:end_block] = [new_op] + new_args
                self.sel_index = script_op_index
            elif self.eq[self.sel_index] != utils.NEWARG:
                eqtools.replaceby(self.eq, self.sel_index, [utils.NEWARG])
            else:
                # Avoid saving in history if nothing to do
                return

        self.sel_right = True
        self.update()
        self.eqhist.save(self.eq, self.sel_index)

    def open_eq(self, filename=None):
        neweq = conversions.open_eq(self.parent, filename)
        if neweq != None:
            self.eq = list(neweq)
            self.sel_index = 0
            self.update()
            self.eqhist.save(neweq, 0)

    def save_eq(self):
        items = ["PNG", "PDF", "EPS", "SVG"]
        msg = "Select format:\n\nNote: Eqs. can only be recovered\n" \
              + "from PNG and PDF."
        item, ok = QInputDialog.getItem(self.parent, "Save equation",
                                        msg, items, 0, False)
        if not ok:
            return None
        # Implement a Save File dialog
        # The staticmethod does not accept default suffix
        itemfilter = item + " (*." + item.lower() + ")"
        dialog = QFileDialog(self.parent, 'Save equation', '', itemfilter)
        dialog.setFileMode(QFileDialog.AnyFile)
        dialog.setAcceptMode(QFileDialog.AcceptSave)
        dialog.setDefaultSuffix(item.lower())
        dialog.setOption(QFileDialog.DontConfirmOverwrite, True)
        if not dialog.exec_():
            return
        filename = dialog.selectedFiles()[0]
        # Implement an Overwrite? dialog since the default one does not
        # check filename when default suffix extension has to be added
        if os.path.exists(filename):
            msg = 'A file named "' + os.path.basename(filename) \
                  + '" already exists. Do you want to replace it?'
            ret_val = QMessageBox.question(self.parent, 'Overwrite', msg)
            if ret_val != QMessageBox.Yes:
                return
        if item == 'PNG':
            conversions.eq2png(self.eq, 600, None, self.temp_dir,
                               filename, True)
        elif item == 'PDF':
            conversions.eq2pdf(self.eq, self.temp_dir, filename)
        elif item == 'SVG':
            conversions.eq2svg(self.eq, self.temp_dir, filename)
        elif item == 'EPS':
            conversions.eq2eps(self.eq, self.temp_dir, filename)

    def recover_prev_eq(self):
        """ Recover previous equation from the historial, if any """
        preveq, self.sel_index = self.eqhist.get_prev()
        self.eq = list(preveq)
        self.update()

    def recover_next_eq(self):
        """ Recover next equation from the historial, if any """
        nexteq, self.sel_index = self.eqhist.get_next()
        self.eq = list(nexteq)
        self.update()

    def sel2eqbuffer(self):
        """ Copy block pointed by self.sel_index to self.eq_buffer """
        end_sel_index = eqtools.nextblockindex(self.eq, self.sel_index)
        self.eq_buffer = self.eq[self.sel_index:end_sel_index]

    def eqbuffer2sel(self):
        """
        Append self.eq_buffer to the right of the block pointed by
        self.sel_index. If the block is a NEWARG, just replace it.
        """
        if self.eq_buffer != []:
            if self.eq[self.sel_index] == utils.NEWARG:
                self.eq[self.sel_index:self.sel_index+1] = self.eq_buffer
            else:
                if self.sel_right:
                    self.sel_index = eqtools.insertrbyJUXT(self.eq,
                                                           self.sel_index,
                                                           self.eq_buffer)
                else:
                    self.sel_index = eqtools.insertlbyJUXT(self.eq,
                                                           self.sel_index,
                                                           self.eq_buffer)
            self.sel_right = True
            self.update()
            self.eqhist.save(self.eq, self.sel_index)
