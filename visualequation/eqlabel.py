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

"""It manages the Qt interaction of the main equation with the user actions."""
import os
import random

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from .symbols import utils
from .eqlib import conversions


class EqLabel(QLabel):
    def __init__(self, temp_dir, parent):
        super().__init__(parent)
        self.parent = parent
        self.maineq = maineq.MainEq(temp_dir, self.setPixmap, parent)
        self.setAcceptDrops(True)

    def event(self, event):
        if event.type() == QEvent.KeyPress:
            if event.key() == Qt.Key_Tab:
                self.maineq.eqsel.select_next_neighbour()
                # The True value prevents the event to be sent to other objects
                return True
            elif event.key() == Qt.Key_Backtab:
                self.maineq.eqsel.select_prev_neighbour()
                return True
        return QLabel.event(self, event)

    def mouseMoveEvent(self, event):
        if event.buttons() != Qt.LeftButton:
            return
        self.setAcceptDrops(False)
        base = "eq" + str(random.randint(0, 999999))
        eq_png = conversions.eq2png(
            self.maineq.eq,
            dpi=None, bg=None, directory=self.maineq.temp_dir,
            png_fpath=os.path.join(self.maineq.temp_dir, base +'.png'),
            add_metadata=True)
        mimedata = QMimeData()
        mimedata.setImageData(QImage(eq_png)) # does not work for web browser
        #mimedata.setText(eq_png) # text-editor and console
        #mimedata.setUrls([QUrl.fromLocalFile(eq_png)]) # nautilus
        drag = QDrag(self)
        drag.setPixmap(QPixmap(eq_png))
        drag.setMimeData(mimedata)
        drag.exec_()
        self.setAcceptDrops(True)

    def keyPressEvent(self, event):
        modifiers = QApplication.keyboardModifiers()
        if modifiers == Qt.ControlModifier:
            self.on_key_pressed_ctrl(event)
        elif modifiers == Qt.AltModifier:
            self.on_key_pressed_alt(event)
        else:
            self.on_other_key_pressed(event)

    def on_other_key_pressed(self, event):
        # 0-9 or A-Z or a-z excluding Ctr modifier
        try:
            code = ord(event.text())
            if 48 <= code <= 57 or 65 <= code <= 90 or 97 <= code <= 122:
                self.maineq.insert_from_panel(event.text())
        except TypeError:
            pass
        try:
            self.maineq.insert_from_panel(utils.ASCII_LATEX_TRANSLATION[event.text()])
        except KeyError:
            pass
        key = event.key()
        if key == Qt.Key_Up:
            self.maineq.insert_script(is_superscript=True)
        elif key == Qt.Key_Down:
            self.maineq.insert_script(is_superscript=False)
        elif key == Qt.Key_Right:
            self.maineq.eqsel.navigate_forward()
        elif key == Qt.Key_Left:
            self.maineq.eqsel.navigate_backward()
        elif key == Qt.Key_Backslash:
            self.maineq.insert_from_panel(r'\backslash')
        elif key == Qt.Key_AsciiTilde:
            self.maineq.insert_from_panel(r'\sim')
        elif key == Qt.Key_Backspace:
            self.maineq.delete()
        elif key == Qt.Key_Delete:
            self.maineq.delete(supr=True)
        elif key == Qt.Key_Return:
            self.maineq.eqsel.select_bigger_usubeq()
        elif key == Qt.Key_Space:
            self.maineq.insert_from_panel(r'\,')
        elif key == Qt.Key_Apostrophe:
            self.maineq.insert_from_panel(r'\prime')

    def on_key_pressed_ctrl(self, event):
        key = event.key()
        if key == Qt.Key_B:
            pass
        elif key == Qt.Key_F:
            pass

    def on_key_pressed_alt(self, event):
        key = event.key()
        if key == Qt.Key_B:
            self.maineq.eqsel.select_prev_neighbour()
        elif key == Qt.Key_F:
            self.maineq.eqsel.select_next_neighbour()
        elif key == Qt.Key_T:
            self.maineq.transpose_neighbours()

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            super().dragEnterEvent(event)

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            url = event.mimeData().urls()[0]
            self.maineq.open_eq(str(url.toLocalFile()))
            event.acceptProposedAction()
        else:
            super().dropEvent(event)
