#  visualequation is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  visualequation is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.

import os

from PyQt5.QtWidgets import QDialog, QTextEdit, QDialogButtonBox, \
    QVBoxLayout, QMessageBox, QLabel, QComboBox, QDoubleSpinBox, QFileDialog
from PyQt5.QtGui import QTextCursor
from PyQt5.QtCore import Qt

from data.usage import getusage
from . import commons
from .eqlib import conversions
from . import latexdialogs


class UsageDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setModal(False)
        self.setWindowTitle(_('Usage'))
        self.resize(1000, 600)
        self.setSizeGripEnabled(True)
        text = QTextEdit(self)
        text.setReadOnly(True)
        text.insertHtml(getusage())
        text.moveCursor(QTextCursor.Start)
        buttons = QDialogButtonBox(QDialogButtonBox.Ok, self)
        vbox = QVBoxLayout(self)
        vbox.addWidget(text)
        vbox.addWidget(buttons)
        buttons.accepted.connect(self.accept)


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


class UIDialogs:
    def __init__(self, mwin):
        self.mwin = mwin

    def usage(self):
        dialog = UsageDialog(self.mwin)
        dialog.show()

    def about(self):
        msg = _("<p>Visual Equation</p>"
                "<p><em>Version:</em> %s </p>"
                "<p><em>Author:</em> Daniel Molina García</p>"
                "<p><em>Sources:</em> "
                "<a href=\"https://github.com/daniel-molina"
                "/visualequation\">Webpage</a></p>"
                "<p><em>License:</em> GPLv3 or above</p>") % \
              commons.VERSION
        QMessageBox.about(self.mwin, _("About"), msg)

    def edit_latex(self):
        s = self.mwin.deq.get_sel()
        latexcode_new = latexdialogs.EditLatexDialog.editlatex(
            s, self.mwin.tempdir, self.mwin)
        if latexcode_new:
            self.mwin.deq.replace_with_latex(latexcode_new)

    def show_latex(self):
        latexdialogs.ShowLatexDialog.showlatex(
            self.mwin.deq.get_eq(), self.mwin.deq.get_sel(), self.mwin)

    def open_eq(self):
        filename, ignored = QFileDialog.getOpenFileName(
            self.mwin,
            _('Open equation'), '',
            _('Valid formats (*.png *.pdf)'))
        if not filename:
            return
        neweq = conversions.get_eq_from_file(self.mwin, filename)
        if neweq is not None:
            self.mwin.deq.reset_eq()

    def export_eq(self):
        (save_format, size), ok = SaveDialog.get_save_options(self.mwin)
        if not ok:
            return
        # Implement a Save File dialog
        # The staticmethod does not accept default suffix
        formatfilter = save_format + " (*." + save_format.lower() + ")"
        dialog = QFileDialog(self.mwin, 'Save equation', '', formatfilter)
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
            ret_val = QMessageBox.question(self.mwin, _('Overwrite'), msg)
            if ret_val != QMessageBox.Yes:
                return
        if save_format == 'PNG':
            conversions.eq2png(self.mwin.deq.eq, dpi=size, bg=None,
                               directory=self.mwin.tempdir, png_fpath=filename,
                               add_metadata=True)
        elif save_format == 'PDF':
            conversions.eq2pdf(self.mwin.deq.eq, size, self.mwin.tempdir,
                               filename)
        elif save_format == 'SVG':
            conversions.eq2svg(self.mwin.deq.eq, size, self.mwin.tempdir,
                               filename)
        elif save_format == 'EPS':
            conversions.eq2eps(self.mwin.deq.eq, size, self.mwin.tempdir,
                               filename)
