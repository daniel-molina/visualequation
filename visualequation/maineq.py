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

import functools
import os
import types

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from . import conversions
from . import eqqueries
from . import eqhist
from . import eqsel
from . import groups
from . import simpleeqcreator
from .errors import ShowError
from .symbols import utils

"""
The module that manages the equation being edited.
"""


class SaveDialog(QDialog):
    prev_format_index = 0
    prev_size = 600.

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Save equation')
        label = QLabel(
            _("Select format:\n\nNote: Equations can only be recovered"
              " from PNG and PDF."))
        label.setWordWrap(True)
        items = ["PNG", "PDF", "EPS", "SVG"]
        self.combo = QComboBox(self)
        self.combo.addItems(items)
        self.combo.setCurrentIndex(self.prev_format_index)
        self.label_spin = QLabel(_('Size (dpi):'))
        self.spin = QDoubleSpinBox(self)
        self.spin.setMaximum(10000)
        # Just avoid negative numbers
        # Minimum conditions are set later
        self.spin.setMinimum(0.01)
        self.spin.setValue(self.prev_size)
        self.buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
            Qt.Horizontal, self)
        vbox = QVBoxLayout(self)
        vbox.addWidget(label)
        vbox.addWidget(self.combo)
        vbox.addWidget(self.label_spin)
        vbox.addWidget(self.spin)
        vbox.addWidget(self.buttons)
        self.combo.currentIndexChanged.connect(self.changed_combo)
        self.spin.valueChanged.connect(self.changed_spin)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)

    def changed_combo(self, index):
        if "SVG" == self.combo.currentText():
            self.label_spin.setText(_('Size (scale):'))
            self.spin.setValue(5)
        else:
            self.label_spin.setText(_('Size (dpi):'))
            self.spin.setValue(600)

    def changed_spin(self):
        if "SVG" == self.combo.currentText():
            if self.spin.value() < 0.:
                self.buttons.button(QDialogButtonBox.Ok).setDisabled(
                    True)
            else:
                self.buttons.button(QDialogButtonBox.Ok).setEnabled(
                    True)
        else:
            if self.spin.value() < 10.:
                self.buttons.button(QDialogButtonBox.Ok).setDisabled(
                    True)
            else:
                self.buttons.button(QDialogButtonBox.Ok).setEnabled(
                    True)

    @staticmethod
    def get_save_options(parent=None):
        dialog = SaveDialog(parent)
        result = dialog.exec_()
        if result == QDialog.Accepted:
            SaveDialog.prev_format_index = dialog.combo.currentIndex()
            SaveDialog.prev_size = dialog.spin.value()
            return ((dialog.combo.currentText(),
                     dialog.spin.value()),
                    True)
        else:
            return (None, None), False


def updatestate(func):
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        # Update last entry of equation history
        self.eqhist.changecurrent(self.eqsel)

        retval = func(self, *args, **kwargs)

        # Display new equation
        self.eqsel.display()

        # Create a new entry in equation history
        self.eqhist.add(self.eqsel)
        return retval

    return wrapper


def new_selection(func):
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        pass

    return wrapper


class MainEq:
    """The class managing the main equation."""

    def __init__(self, temp_dir, setpixmap, parent):

        init_eq = [utils.NEWARG]
        self.eq_buffer = []
        self.eq = list(init_eq)  # It will be mutated by the replace functions
        self.temp_dir = temp_dir
        self.parent = parent
        self.eqsel = eqsel.Selection(self.eq, 0, temp_dir, setpixmap)
        self.eqsel.display()
        self.eqhist = eqhist.EqHist(self.eqsel)

    @staticmethod
    def _rinsert_nonjuxtsubeq(idx, subeq, eq):
        """Insert a non-juxt subeq to the right of subequation starting at idx.

        :idx: The index of a subeq behind which :subeq: will be inserted.
        :subeq: The subequation to insert_from_panel. It cannot start with a JUXT.
        :eq: The equation in which to insert_from_panel :subeq:.
        :return: Index of first inserted element and :idx: updated.
        """
        juxt_idx, arg2_idx = eqqueries.other_juxt_arg(eq, idx)
        if juxt_idx < 0 or arg2_idx < idx:
            # idx points to an usubeq or a last citizen
            end_idx = eqqueries.nextsubeq(eq, idx)
            eq[idx:end_idx] = [utils.JUXT] + eq[idx:end_idx] + subeq
            return end_idx + 1, idx + 1
        else:
            # idx points to a citizen but not the last one
            eq[arg2_idx:arg2_idx] = [utils.JUXT] + subeq
            return arg2_idx + 1, idx

    @staticmethod
    def _linsert_nonjuxtsubeq(idx, subeq, eq):
        """Insert a non-juxt subeq to the left of subequation starting at idx.

        :idx: The index of a subeq in front of which :subeq: will be inserted.
        :subeq: The subequation to insert_from_panel. It cannot start with a JUXT.
        :eq: The equation in which to insert_from_panel :subeq:.
        :return: Index of first inserted element and :idx: updated.
        """
        juxt_idx, arg2_idx = eqqueries.other_juxt_arg(eq, idx)
        if juxt_idx < 0 or arg2_idx < idx:
            # idx points to an usubeq or a last citizen
            eq[idx:idx] = [utils.JUXT] + subeq
            return idx + 1, idx + 1 + len(subeq)
        else:
            # idx points to a citizen but not the last one
            eq[idx:idx] = subeq + [utils.JUXT]
            return idx, idx + len(subeq) + 1

    @staticmethod
    def _rinsert_juxtsubeq(idx, subeq, eq):
        """Insert subeq starting by JUXT to the right of subeq starting at idx.

        :idx: The index of a subeq behind which :subeq: will be inserted.
        :subeq: The subequation to insert_from_panel. It must start with a JUXT.
        :eq: The equation in which to insert_from_panel :subeq:.
        :return: Index of last citizen inserted and :idx: updated.
        """
        subeq_last_citizen = eqqueries.last_citizen(subeq, 1)
        juxt_idx, arg2_idx = eqqueries.other_juxt_arg(eq, idx)
        if juxt_idx < 0 or arg2_idx < idx:
            # idx points to an usubeq or a last citizen
            end_idx = eqqueries.nextsubeq(eq, idx)
            eq[idx:end_idx] = [utils.JUXT] + eq[idx:end_idx] + subeq
            # We are inserting a JUXT and subeq has another:
            # first citizen od subeq has an offset of 2 JUXTs
            return end_idx + 1 + subeq_last_citizen, idx + 1
        else:
            # idx points to a citizen but not the last one
            eq[arg2_idx:arg2_idx] = subeq[:subeq_last_citizen] + [utils.JUXT] \
                                    + subeq[subeq_last_citizen:]
            return arg2_idx + subeq_last_citizen + 1, idx

    @staticmethod
    def _linsert_juxtsubeq(idx, subeq, eq):
        """Insert subeq starting by JUXT to the left of subeq starting at idx.

        :idx: The index of a subeq in front of which :subeq: will be inserted.
        :subeq: The subequation to insert_from_panel. It must start with a JUXT.
        :eq: The equation in which to insert_from_panel :subeq:.
        :return: Index of first citizen inserted and :idx: updated.
        """
        juxt_idx, arg2_idx = eqqueries.other_juxt_arg(eq, idx)
        subeq_last_citizen = eqqueries.last_citizen(subeq, 1)
        if juxt_idx < 0 or arg2_idx < idx:
            # idx points to an usubeq or a last citizen
            eq[idx:idx] = subeq[:subeq_last_citizen] + [utils.JUXT] \
                          + subeq[subeq_last_citizen:]
            return idx + 1, idx + len(subeq) + 1
        else:
            # idx points to a citizen but not the last one
            eq[idx:idx] = subeq[1:subeq_last_citizen] + [utils.JUXT] \
                          + subeq[subeq_last_citizen:] + [utils.JUXT]
            return idx, idx + len(subeq) + 2

    def rinsert(self, idx, subeq):
        """Insert subeq to the right of subequation which starts at idx.

        :idx: The index of a subeq behind which :subeq: will be inserted.
        :subeq: The subequation to insert_from_panel. It can be any valid subequation.
        :return: Index in self.eq of last citizen of usubeq if subeq is a
        JUXT-ublock or, else, the first element of usubeq.
        """
        if subeq[0] == utils.JUXT:
            lcitizen_idx, newidx = self._rinsert_juxtsubeq(idx, subeq, self.eq)
            return lcitizen_idx
        else:
            felem_idx, newidx = self._rinsert_nonjuxtsubeq(idx, subeq, self.eq)
            return felem_idx

    def linsert(self, idx, subeq):
        """Insert subeq to the left of subequation which starts at idx.

        :idx: The index of a subeq in front of which :subeq: will be inserted.
        :subeq: The subequation to insert_from_panel. It can be any valid subequation.
        :return: Index in self.eq of first citizen of usubeq if subeq is a
        JUXT-ublock or, else, the first element of usubeq.
        """
        if subeq[0] == utils.JUXT:
            fcitizen_idx, newidx = self._linsert_juxtsubeq(idx, subeq, self.eq)
            return fcitizen_idx
        else:
            felem_idx, newidx = self._linsert_nonjuxtsubeq(idx, subeq, self.eq)
            return felem_idx

    @staticmethod
    def replace_integrating(idx, subeq, eq):
        """Replace subeq starting at idx integrating citizens, if needed.

        If :idx: does not point to a citizen or :subeq: is not a JUXT-ublock,
        it is an ordinary replacement.
        Else, citizen which start at :idx: is removed and citizens of :subeq:
        are added as co-citizens of the corresponding JUXT-ublock in :eq:.

        Returned value:
            *   If any element with index i in :subeq: has index :idx: + i in
                :eq: after replacement, 0 is returned
            *   If :subeq: is a JUXT-ublock and :idx: pointed to a citizen
                which was not the last one of some JUXT-ublock in :eq:, 1 is
                returned. That mean:

                *   Any citizen except the last one with index i in :subeq: has
                    index :idx: + i - 1 in :eq:.
                *   Last citizen in :subeq: has index :idx: + i in :eq:.

        :idx: The index of a subeq which will be replaced.
        :subeq: Subeq with which subeq starting at :idx: will be replaced.
        :eq: Equation in which the replacement is done.
        :return: A flag value explained above.
        """
        juxt_idx, arg2_idx = eqqueries.other_juxt_arg(eq, idx)
        if subeq[0] != utils.JUXT or juxt_idx < 0 or arg2_idx < idx:
            # subeq does not start with JUXT or idx points to:
            #   1. An usubeq, or
            #   2. A last citizen
            end_index = eqqueries.nextsubeq(eq, idx)
            eq[idx:end_index] = subeq
            return 0
        else:
            # idx points to the first argument of a JUXT (terminal or not)
            subeq_last_citizen = eqqueries.last_citizen(subeq, 1)
            eq[idx:arg2_idx] = subeq[1:subeq_last_citizen] + [utils.JUXT] \
                               + subeq[subeq_last_citizen:]
            return 1

    @staticmethod
    def replace_grouped(idx, subeq, eq, temp=False):
        """Replace subeq which starts at idx as a group, if needed.

        Rules:
            *   If :idx: does not point to a citizen or :subeq: is not a
                JUXT-ublock, it is an ordinary replacement.
            *   Else, the citizen in :idx: is replaced by :subeq: "protected"
                with a group operator.

        If you want a group operator in front of your subeq even if it is not
        a JUXT-ublock, add it by yourself and call this (or
        self.replace_integrating) method.

        :idx: The index of a subeq which will be replaced.
        :subeq: Subeq with which subeq starting at :idx: will be replaced.
        :eq: Equation in which the replacement is done.
        :temp: Indicates whether the group will be temporal, if it is included.
        """
        if subeq[0] != utils.JUXT:
            # subeq does not start with JUXT
            end_idx = eqqueries.nextsubeq(eq, idx)
            eq[idx:end_idx] = subeq
            return

        juxt_idx, arg2_idx = eqqueries.other_juxt_arg(eq, idx)
        if juxt_idx < 0:
            # idx points to an usubeq
            end_idx = eqqueries.nextsubeq(eq, idx)
            eq[idx:end_idx] = subeq
            return

        gop = utils.TEMPGROUP if temp else utils.GROUP
        if idx < arg2_idx:
            # idx points to the first argument of a JUXT
            eq[idx:arg2_idx] = [gop] + subeq
        else:
            # idx points to the a last citizen
            end_idx = eqqueries.nextsubeq(eq, idx)
            eq[idx:end_idx] = [gop] + subeq

    def _remove_arg(self):
        """Remove arg by downgrading the script operator or flatting op.

        If a script operator is downgraded, the operator is selected.
        Else, selection rules are defined by self._flat_external_op_core.
        """
        isscript, script_op_idx, arg_pos \
            = eqqueries.is_script(self.eq, self.eqsel.idx)

        if not isscript:
            self._flat_external_op_core(remove_mode=self.eqsel.dir)
            return

        args = eqqueries.indexop2arglist(self.eq, script_op_idx)
        # Find which element of the list has to be removed
        # Note that arg_pos only applies non-None arguments
        valid_pos = 0
        for pos, arg in enumerate(args):
            if arg is not None:
                if valid_pos == arg_pos:
                    args[pos] = None
                    break
                else:
                    valid_pos += 1
        new_op = eqqueries.arglist2indexop(args)
        end_block = eqqueries.nextsubeq(self.eq, script_op_idx)
        if new_op is None:
            self.eq[script_op_idx:end_block] = args[0]
        else:
            new_args = eqqueries.flat_arglist(args)
            self.eq[script_op_idx:end_block] = [new_op] + new_args
        self.eqsel.idx = script_op_idx

    def _remove_selection(self):
        """Remove current selection. It does nothing with empty arguments.

        Rules depending on selection:
            *   If it is an usubeq, a NEWARG is put in its place, it is
                selected and direction is set to 0.
            *   Elif it is a last citizen, after its removal the co-citizen
                to the left is selected and direction is set to 1.
            *   Elif it is a first citizen, after its removal the co-citizen to
                the right is selected and direction is set to -1.
            *   Else (intermediate citizen), the citizen is removed and:

                *   If direction was 1, the co-citizen to the left is selected
                    and direction is not changed.
                *   Else (direction was -1), the co-citizen to the right is
                    selected and direction is not changed.

        It explicitly avoid selecting a non-selsubeq (needed?).

        """
        juxt_idx, otherarg = eqqueries.other_juxt_arg(self.eq,
                                                      self.eqsel.idx)
        if juxt_idx < 0:
            # Case: Remove usubeq
            # It does not matter which kind of replace you use in this case
            self.replace_grouped(self.eqsel.idx, [utils.NEWARG], self.eq)
            self.eqsel.dir = 0
            return

        # From this point, we know idx points to citizen
        if otherarg < self.eqsel.idx:
            # Case: Remove last citizen
            # It does not matter which kind of replace you use in this case
            self.replace_grouped(juxt_idx, self.eq[otherarg:self.eqsel.idx],
                                 self.eq)
            self.eqsel.idx = juxt_idx
            self.eqsel.dir = 1
            return

        # From here, selection is a citizen which is not the last one
        # Low-level hardcore starts... :P
        juxt_juxt_idx, prev_cocitizen_idx \
            = eqqueries.other_juxt_arg(self.eq, juxt_idx)
        self.eq[juxt_idx:otherarg] = []
        if juxt_juxt_idx < 0:
            # Case: first citizen WAS just removed
            if self.eq[juxt_idx] != utils.JUXT:
                self.eqsel.idx -= 1
            self.eqsel.dir = -1
        else:
            # Case: intermediate citizen WAS just removed and dir was 1
            if self.eqsel.dir == 1:
                self.eqsel.idx = prev_cocitizen_idx
            elif self.eq[juxt_idx] != utils.JUXT:
                # Subcase: Removed citizen was before last but one citizen
                self.eqsel.idx -= 1

        self.eqsel.set_selsubeq()

    @updatestate
    def remove_eq(self):
        self.eq[:] = [utils.NEWARG]
        self.eqsel.idx = 0
        self.eqsel.dir = 0

    @updatestate
    def flat_internal_op(self):
        """Flat the least internal operator.

        Rules:
            *   If selection is a symbol, operator with no arguments or
                JUXT-ublock, remove selection by the rules of
                self._remove_selection.
            *   Else, apply rules of _flat_external_op_core considering that
                operator referred there is current selection and any of its
                arguments is selected.
                Final selection will be the all the non-NEWARG arguments,
                without changing the direction, adding a temporal group if
                necessary.
        """
        if isinstance(self.eq[self.eqsel.idx], str) \
                or self.eq[self.eqsel.idx].n_args == 0 \
                or self.eq[self.eqsel.idx] == utils.JUXT:
            self._remove_selection()
            return

        arg_idx = self.eqsel.idx + 1
        vargs = []  # list of valid args
        for ignored in range(self.eq[self.eqsel.idx].n_args):
            next_arg_idx = eqqueries.nextsubeq(self.eq, arg_idx)
            if self.eq[arg_idx] != utils.NEWARG:
                vargs.append(self.eq[arg_idx:next_arg_idx])
            arg_idx = next_arg_idx

        if not vargs:
            # Subcase: No argument is valid, delete the entire operator.
            self._remove_selection()
            return

        subeq_c = simpleeqcreator.SimpleEqCreator()
        for varg in vargs:
            subeq_c.extend(varg)
        self.replace_grouped(self.eqsel.idx, subeq_c.get_eq(),
                             self.eq, temp=True)

    def _flat_external_op_core(self, remove_mode=0):
        """Flat the least external operator.

        Main behavior:

            Consider the least external operator of selected usubeq (read below
            about the behaviour if selection is a citizen):

            *   If every argument of operator is a NEWARG, remove the subeq
                defined by the operator by the rules of self._remove_selection
                supposing that it is selected with the same direction than
                :remove_mode:.
            *   If only one argument of the operator is not a NEWARG and it is
                not a JUXT-ublock, replace the subequation defined by the
                operator with that argument.
            *   If only one argument of the operator is not a NEWARG and it is
                a JUXT-ublock, replace the subequation defined by the
                operator with the JUXT-ublock preceded by a temporal group.
            *   Else (more than one non-NEWARG arguments), create a JUXT-ublock
                were citizens will be:

                *   Every non-NEWARG argument which is not a JUXT-ublock, and
                *   Every citizen of any argument which is a JUXT-ublock.

                Relative order of citizens will be the same in which they
                appear in the equation.

                The operator considered can be itself an usubeq or a citizen:

                *   If operator is an usubeq, replace it by the JUXT-ublock.
                *   Else (operator is a citizen) replace operator with the
                    citizens of the created JUXT-ublock in such a way that
                    its citizens are co-citizens of the JUXT-ublock to which
                    operator belonged.

        Finally selected subequation will be:

            *   If every argument of the operator is also a NEWARG, selection
                is decided by self._remove_selection's rules.
            *   If selection is not a NEWARG, selection will be the same than
                originally selected and with the same direction.
            *   Else (NEWARG selected and there is at least one non-NEWARG),
                remove_mode parameter decides the selection:

                *   If remove_mode == 0 (NEUTRAL node):

                    *   If there is at least one non-NEWARG argument to the
                        right, select the first one and set self.eqsel.dir = -1
                        (neither you nor I).
                    *   Else select the first non-NEWARG to the left and set
                        self.eqsel.dir = 1.
                *   If remove_mode == 1 (SUPR mode):

                    *   If there is at least one non-NEWARG argument to the
                        right, select the first one and set self.eqsel.dir = 1.
                    *   Else, select the first non-NEWARG to the left and set
                        self.eqsel.dir = 1.
                *   If remove_mode == -1 (DEL mode):

                   *    If there is at least one non-NEWARG argument to the
                        left, select the first one and set self.eqsel.dir = 1.
                    *   Else, select the first non-NEWARG to the right and set
                        self.eqsel.dir = -1.

        Special cases:

        If selection is a citizen:

            *   If the JUXT-ublock to which selection belongs is the whole
                equation, remove the whole equation.
            *   Elif there are not other non-NEWARG arguments:

                *   If operator is an usubeq, replace the operator with the
                    JUXT-ublock to which selection belongs.
                *   Else, remove operator and integrate selection and its
                    co-citizens as co-citizens of the JUXT-ublock to which
                    operator belonged.

            *   Else (there are other non-NEWARG arguments), apply the
                equivalent rule in the "Main behavior" section.

            In the last 2 cases leave selected the originally selected citizen
            and with the same direction.
            Note that remove_mode parameter is never used in this case.
        """
        # Set variables that define function's casuistic:
        #   The case in which a citizen is selected is managed by selecting its
        #   JUXT-ublock and setting and offset value.
        #   "Selected argument" below will refer to the JUXT-ublock if this
        #   case applies
        arg_idx = self.eqsel.idx
        offset = 0
        old_sel_was_last_citizen = False
        juxt_idx, arg2_idx = eqqueries.other_juxt_arg(self.eq,
                                                      self.eqsel.idx)
        if juxt_idx >= 0:
            # Current selection is a citizen
            parent_juxt = eqqueries.parent_juxt(self.eq, self.eqsel.idx)
            if parent_juxt == 0:
                # Case: Selection is a citizen of the whole equation
                self.remove_eq()
                return
            arg_idx = parent_juxt
            offset = parent_juxt - self.eqsel.idx
            if arg2_idx < self.eqsel.idx:
                old_sel_was_last_citizen = True

        # Inidex of operator and ordinal of selected argument (starting from 1)
        op_idx, arg_ord = eqqueries.whosearg(self.eq, arg_idx)
        # Get information about arguments of the operator
        arg_idx = op_idx + 1
        vargs = []  # list of valid args
        # ridx stands for "reduced index", an index of vargs
        arg_ridx = -1
        larg_ridx = -1
        rarg_ridx = -1
        for current_arg_ord in range(1, self.eq[op_idx].n_args + 1):
            next_arg_idx = eqqueries.nextsubeq(self.eq, arg_idx)
            # Consider only args != NEWARG
            if self.eq[arg_idx] != utils.NEWARG:
                if current_arg_ord == arg_ord:
                    arg_ridx = len(vargs)
                elif current_arg_ord < arg_ord:
                    larg_ridx = len(vargs)
                elif rarg_ridx < 0 and current_arg_ord > arg_ord:
                    rarg_ridx = len(vargs)
                vargs.append(self.eq[arg_idx:next_arg_idx])
            arg_idx = next_arg_idx

        if not vargs:
            # Case: No argument is valid, delete the entire operator.
            self.eqsel.idx = op_idx
            self.eqsel.dir = remove_mode
            self._remove_selection()
            return

        # Decide selected argument and its direction
        if arg_ridx >= 0:
            sel_ridx = arg_ridx  # offset != 0 managed later
        elif remove_mode == 0:
            if rarg_ridx >= 0:
                sel_ridx = rarg_ridx
                self.eqsel.dir = -1
            else:
                sel_ridx = larg_ridx
                self.eqsel.dir = 1
        elif remove_mode == 1:
            if rarg_ridx >= 0:
                sel_ridx = rarg_ridx
            else:
                sel_ridx = larg_ridx
            self.eqsel.dir = 1
        else:
            if larg_ridx >= 0:
                sel_ridx = larg_ridx
                self.eqsel.dir = 1
            else:
                sel_ridx = rarg_ridx
                self.eqsel.dir = -1

        # Create a JUXT-ublock with the arguments
        subeq_c = simpleeqcreator.SimpleEqCreator()
        for varg in vargs[:sel_ridx]:
            subeq_c.extend(varg)
        if vargs[sel_ridx][0] == utils.JUXT and not offset:
            subeq_c.extend([utils.TEMPGROUP] + vargs[sel_ridx])
        else:
            subeq_c.extend(vargs[sel_ridx])
        for varg in vargs[sel_ridx + 1:]:
            subeq_c.extend(varg)

        # Replace the equation and select correctly
        takecare = self.replace_integrating(op_idx, subeq_c.get_eq(), self.eq)
        if takecare and (sel_ridx != len(vargs)
                         or (offset and not old_sel_was_last_citizen)):
            self.eqsel.idx = op_idx + subeq_c.get_idx(offset, sel_ridx) - 1
        else:
            self.eqsel.idx = op_idx + subeq_c.get_idx(offset, sel_ridx)

    def _rremove(self):
        """Remove "to the right" of selection.

        Rules:

            *   If selection is the whole equation, do nothing.
            *   Elif it has a co-citizen to the right, remove it.
            *   Else, flat the least external operator.

        Selection and direction are not modified.
        """
        juxt_idx, otherarg = eqqueries.other_juxt_arg(self.eq,
                                                      self.eqsel.idx)
        if juxt_idx >= 0:
            # Case: selection is a citizen
            if self.eqsel.idx < otherarg:
                if self.eq[otherarg] == utils.JUXT:
                    # Subcase: selection is a citizen before the last but one
                    end_idx = eqqueries.nextsubeq(self.eq, otherarg + 1)
                    self.eq[otherarg:end_idx] = []
                else:
                    # Subcase: selection is a last but one co-citizen
                    end_idx = eqqueries.nextsubeq(self.eq, otherarg)
                    self.eq[juxt_idx:end_idx] \
                        = self.eq[self.eqsel.idx:otherarg]
                    self.eqsel.idx -= 1
            else:
                # Subcase: selection is a last citizen
                self._flat_external_op_core()
        elif self.eqsel.idx:
            # Case: selection is an usubeq but not the whole equation
            self._flat_external_op_core()

    def _lremove(self):
        """Remove "to the left" of selection.

        Rules:

            *   If selection is the whole equation, do nothing.
            *   Elif it has a co-citizen to the left, remove it.
            *   Else, flat the least external operator.

        Selection and direction are not modified.
        """
        # Check if it is the arg of a JUXT and leave it clean
        lcocitizen_idx = eqqueries.cocitizen(self.eq, self.eqsel.idx,
                                             forward=False)
        if lcocitizen_idx < 0:
            # Case: selection is not a citizen or it is a first citizen
            self._flat_external_op_core()
        elif self.eq[self.eqsel.idx - 1] == utils.JUXT:
            # Case: selection is not the last citizen
            self.eq[lcocitizen_idx - 1:self.eqsel.idx - 1] = []
            self.eqsel.idx = lcocitizen_idx
        else:
            # Case: selection is the last citizen
            self.eq[lcocitizen_idx - 1:self.eqsel.idx] = []
            self.eqsel.idx = lcocitizen_idx - 1

    def insert_from_panel(self, arg1):
        """Insert a subequation and change selection accordingly.

        Subequation to insert_from_panel:

            *   If :arg1: is a symbol, insert_from_panel it.
            *   If :arg1: is an operator, insert_from_panel it and set any argument to a
                NEWARG.
            *   If :arg1: is a function, call it will self.parent as
                argument and do the following according to the output:

                *   If None, nothing is done.
                *   If a symbol, insert_from_panel the symbol according to rules above.
                *   If an operator, insert_from_panel the operator according to rules
                    above.
                *   Otherwise, throw an error.

        Place to insert_from_panel:

            *   If self.eqsel.dir == 0, replace subequation pointed by
                self.eqsel.index.
            *   If self.eqsel.dir == 1, insert_from_panel after subequation pointed by
                self.index.
            * If self.eqsel.dir == -1, insert_from_panel before subequation pointed by
                self.index.

        Selection and direction:

            *   If introduced subequation is a symbol, select it and set
                self.eqsel.dir = 1.
            *   Else, select the first argument and set self.eqsel.dir = 0.
        """

        @updatestate
        def insert_usubeq(self, usubeq):
            """Insert according to eqsel.dir and select depending on usubeq.

            In particular, if usubeq is operator select first argument and
            set direction to 0.
            """
            if self.eqsel.dir == 0:
                self.eq[self.eqsel.idx:self.eqsel.idx + 1] = usubeq
                self.eqsel.dir = 1
            elif self.eqsel.dir == 1:
                self.eqsel.idx = self.rinsert(self.eqsel.idx, usubeq)
            else:
                self.eqsel.idx = self.linsert(self.eqsel.idx, usubeq)

            # Do some corrections if inserted subeq is an uninitialized op
            if isinstance(usubeq[0], utils.Op) and usubeq[0].n_args > 0:
                # Select first empty arg if an operator was introduced.
                self.eqsel.idx += 1
                self.eqsel.dir = 0

        if isinstance(arg1, types.FunctionType):
            elem = arg1(self.parent)
            if elem is None:
                return
        else:
            elem = arg1

        if isinstance(elem, str):
            subeq = [elem]
        elif isinstance(elem, utils.Op):
            subeq = [elem] + [utils.NEWARG] * elem.n_args
        else:
            ShowError('Unknown equation element passed to insert_from_panel: '
                      + repr(elem),
                      True)
        insert_usubeq(self, subeq)

    @updatestate
    def _insert_substituting_core(self, elem):
        """
        Substitute and set eqsel.index and eqsel.dir.
        """
        if isinstance(elem, str) or \
                (isinstance(elem, utils.Op) and elem.n_args == 0):
            self.replace_integrating(self.eqsel.idx, [elem], self.eq)
            self.eqsel.dir = 1
        elif isinstance(elem, utils.Op) and elem.n_args == 1:
            # This insert_from_panel is a list insert_from_panel, not our self.insert_from_panel.
            self.eq.insert(self.eqsel.idx, elem)
            self.eqsel.dir = 1
        elif isinstance(elem, utils.Op) and elem.n_args > 1:
            sel_end = eqqueries.nextsubeq(self.eq, self.eqsel.idx)
            self.eq[self.eqsel.idx:sel_end] \
                = [elem] + self.eq[self.eqsel.idx:sel_end] \
                  + [utils.NEWARG] * (elem.n_args - 1)
            self.eqsel.idx = sel_end + 1
            self.eqsel.dir = 0
        else:
            ShowError('Unknown type of operator in insert_subst: '
                      + repr(elem), True)

    def insert_substituting(self, arg1):
        """Substitute current selection with a new subeq depending on argument.

        New subequation will be:

            *   If arg1 is a symbol, the symbol.
            *   If arg1 is an operator:

                *   If it is a 0-argument operator, the operator.
                *   Elif it is a 1-argument operator, selection preceded by the
                    operator.
                *   Else, operator + selection + "as many NEWARGS as needed"

            *   If arg1 is a function, call it with self.parent as argument and
                substitute according to the output:

                *   If None, do nothing.
                *   If a symbol, substitute the symbol according to the rules
                    above.
                *   If an operator, substitute the operator according to the
                    rules above.
                *   Otherwise, throw an error.

        Other side-effects:
            * self.eqsel.index and self.eqsel.dir are modified:

                *   If introduced subequation is a symbol or operator with
                    zero or one arguments, select subequation and set
                    self.eqsel.dir = 1.
                *   If it is an operator with more than one argument, select
                    the second argument and set self.eqsel.dir = 0.
        """

        if isinstance(arg1, types.FunctionType):
            elem = arg1(self.parent)
            if elem is None:
                return
        else:
            elem = arg1

        self._insert_substituting_core(elem)

    @updatestate
    def _insert_script_core(self, is_superscript):
        """
        Read self.insert_script docstring.
        """
        # Select the subequation of interest in the case that selection is a
        # JUXT.
        if self.eq[self.eqsel.idx] == utils.JUXT:
            if self.eqsel.dir == 1:
                self.eqsel.idx = eqqueries.last_citizen(
                    self.eq, self.eqsel.idx)
            else:
                self.eqsel.idx += 1
        # Create an arglist with the current indices
        args = eqqueries.indexop2arglist(self.eq, self.eqsel.idx)
        # Include a NEWARG if the the index is not available
        if self.eqsel.dir != -1:
            script_id = 3 if is_superscript else 2
        else:
            script_id = 4 if is_superscript else 1
        if args[script_id] is None:
            args[script_id] = [utils.NEWARG]
            self.eqsel.dir = 0
        else:
            self.eqsel.dir = 1

        argselems_frombasetocurrent = 0
        for i in range(script_id):
            if args[i] is not None:
                argselems_frombasetocurrent += len(args[i])

        new_op = eqqueries.arglist2indexop(args)
        # Flat the list of args
        new_args = eqqueries.flat_arglist(args)
        new_ublock = [new_op] + new_args
        end_prev_ublock = eqqueries.nextsubeq(self.eq, self.eqsel.idx)
        self.eq[self.eqsel.idx:end_prev_ublock] = new_ublock

        self.eqsel.idx += 1 + argselems_frombasetocurrent

    def insert_script(self, is_superscript):
        """Insert a sub or superscript and select it.

        If it already exists, just select it.

        If a JUXT-ublock is selected, put the script to the right of last
        citizen if eqsel.dir == 1. Else, put the script to the left of the
        first citizen.

        Some elements are blacklisted. Nothing is done in that case.
        """
        # Blacklist some operators
        if not (hasattr(self.eq[self.eqsel.idx], 'type_')
                and self.eq[self.eqsel.idx].type_ in utils.INDEX_BLACKLIST):
            self._insert_script_core(is_superscript)

    @updatestate
    def delete(self, supr=False):
        """
        Interface to remove subequations.

        self.eqsel.dir works as the position of a cursor:

            * If +1, it is to the right of selection.
            * If -1, it is to the left of selection.

        By default, it removes what is to the left of the cursor (current
        selection or "something to the left").

        If :supr: is True, this function works like a suppression, removing
        what is to the right of the cursor ("something to the right" or current
        selection).

        :supr: If True, use suppression rules instead of deletion ones.
        """
        if self.eqsel.idx == 0:
            # Remove whole equation
            self.remove_eq()
        elif self.eq[self.eqsel.idx] == utils.NEWARG:
            # Downgrade script or flat least external operator
            self._remove_arg()
        elif (self.eqsel.dir == 1 and not supr) \
                or (self.eqsel.dir == -1 and supr):
            # Remove current selection and set a nice selection
            self._remove_selection()
        elif self.eqsel.dir == 1:
            # Remove to the right
            self._rremove()
        else:
            # Remove to the left
            self._lremove()

    def transpose_neighbours(self):
        w2_idx = self.eqsel.idx

        @updatestate
        def transpose_helper(self, w1_idx):
            endw2_idx = eqqueries.nextsubeq(self.eq, w2_idx)
            endw1_idx = eqqueries.nextsubeq(self.eq, w1_idx)

            temp = self.eq[w2_idx:endw2_idx]
            self.eq[w2_idx:endw2_idx] = self.eq[w1_idx:endw1_idx]
            self.eq[w1_idx:endw1_idx] = temp
            self.eqsel.idx += (endw2_idx - w2_idx) - (endw1_idx - w1_idx)
            self.eqsel.dir = 1

        w1_idx = eqqueries.prev_neighbour(self.eq, self.eqsel.idx)
        if w1_idx > 0:
            transpose_helper(self, w1_idx)


    def new_eq(self):
        self.eq[:] = [utils.NEWARG]
        self.eqsel.idx = 0
        self.eqsel.display()
        self.eqhist = eqhist.EqHist(self.eqsel)

    def open_eq(self, filename=None):
        neweq = conversions.open_eq(self.parent, filename)
        if neweq != None:
            self.eq[:] = list(neweq)
            self.eqsel.idx = 0
            self.eqsel.display()
            self.eqhist.add(self.eqsel)

    def save_eq(self):
        (save_format, size), ok = SaveDialog.get_save_options(self.parent)
        if not ok:
            return
        # Implement a Save File dialog
        # The staticmethod does not accept default suffix
        formatfilter = save_format + " (*." + save_format.lower() + ")"
        dialog = QFileDialog(self.parent, 'Save equation', '', formatfilter)
        dialog.setFileMode(QFileDialog.AnyFile)
        dialog.setAcceptMode(QFileDialog.AcceptSave)
        dialog.setDefaultSuffix(save_format.lower())
        dialog.setOption(QFileDialog.DontConfirmOverwrite, True)
        if not dialog.exec_():
            return
        filename = dialog.selectedFiles()[0]
        # Implement an Overwrite? dialog since the default one does not
        # check filename when default suffix extension has to be added
        if os.path.exists(filename):
            msg = _('A file named "%s" already exists. Do you want to'
                    ' replace it?') % os.path.basename(filename)
            ret_val = QMessageBox.question(self.parent, _('Overwrite'), msg)
            if ret_val != QMessageBox.Yes:
                return
        if save_format == 'PNG':
            conversions.eq2png(self.eq, dpi=size, bg=None,
                               directory=self.temp_dir, png_fpath=filename,
                               add_metadata=True)
        elif save_format == 'PDF':
            conversions.eq2pdf(self.eq, size, self.temp_dir, filename)
        elif save_format == 'SVG':
            conversions.eq2svg(self.eq, size, self.temp_dir, filename)
        elif save_format == 'EPS':
            conversions.eq2eps(self.eq, size, self.temp_dir, filename)

    def recover_prev_eq(self):
        """ Recover previous equation from the history, if any """
        self.eq[:], self.eqsel.idx, self.eqsel.dir = self.eqhist.get_prev()
        self.eqsel.display()

    def recover_next_eq(self):
        """ Recover next equation from the historial, if any """
        self.eq[:], self.eqsel.idx, self.eqsel.dir = self.eqhist.get_next()
        self.eqsel.display()

    def sel2buffer(self):
        """ Copy block pointed by self.eqsel.idx to self.eq_buffer """
        end_sel_index = eqqueries.nextsubeq(self.eq, self.eqsel.idx)
        self.eq_buffer = self.eq[self.eqsel.idx:end_sel_index]

    @updatestate
    def _buffer2sel_core(self):
        """Copy an existing buffer into the equation."""
        if self.eqsel.dir == 0:
            self.eq[self.eqsel.idx:self.eqsel.idx + 1] = self.eq_buffer
            self.eqsel.dir = 1
        elif self.eqsel.dir == 1:
            self.eqsel.idx = self.rinsert(self.eqsel.idx, self.eq_buffer)
            self.eqsel.dir = 1
        else:
            self.eqsel.idx = self.linsert(self.eqsel.idx, self.eq_buffer)
            self.eqsel.dir = -1

    def buffer2sel(self):
        """Copy the buffer into the equation if buffer exists."""
        if self.eq_buffer:
            self._buffer2sel_core()
