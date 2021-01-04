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

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from .eqlib import conversions
from . import eqqueries
from . import eqhist
from . import eqsel
from .symbols import utils

"""
The module that manages the equation shown to the user to be edited.
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
        self.eqsel._display()

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
        self.eqsel._display()
        self.eqhist = eqhist.EqHist(self.eqsel)

    def new_eq(self):
        self.eq[:] = [utils.NEWARG]
        self.eqsel.idx = 0
        self.eqsel._display()
        self.eqhist = eqhist.EqHist(self.eqsel)

    def open_eq(self, filename=None):
        neweq = conversions.open_eq(self.parent, filename)
        if neweq != None:
            self.eq[:] = list(neweq)
            self.eqsel.idx = 0
            self.eqsel._display()
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
        self.eqsel._display()

    def recover_next_eq(self):
        """ Recover next equation from the historial, if any """
        self.eq[:], self.eqsel.idx, self.eqsel.dir = self.eqhist.get_next()
        self.eqsel._display()

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
