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

import random

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from . import symbols
from . import conversions
from . import eq

class EqLabel(QLabel):
    def __init__(self, temp_dir, parent):
        super().__init__(parent)

        self.parent = parent
        self.eq = eq.Eq(temp_dir, self.setPixmap, parent)

    def event(self, event):
        if event.type() == QEvent.KeyPress and event.key() == Qt.Key_Tab:
            self.eq.next_sel()
            # The True value prevents the event to be sent to other objects
            return True
        else:
            return QLabel.event(self, event)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.eq.next_sel()
        elif event.button() == Qt.RightButton:
            self.eq.previous_sel()
        else:
            QLabel.mousePressEvent(self, event)

    def mouseMoveEvent(self, event):
        if event.buttons() != Qt.LeftButton:
            return
        base = "eq" + str(random.randint(0, 999999))
        eq_png = conversions.eq2png(self.eq.eq, None, None, self.eq.temp_dir,
                                    os.path.join(self.eq.temp_dir,
                                                 base +'.png'),
                                    True)
        mimedata = QMimeData()
        #mimedata.setImageData(QImage(eq_png)) # does not work for web browser
        mimedata.setUrls([QUrl.fromLocalFile(eq_png)])
        drag = QDrag(self)
        drag.setPixmap(QPixmap(eq_png))
        drag.setMimeData(mimedata)
        drag.exec_()

    def keyPressEvent(self, event):
        if QApplication.keyboardModifiers() != Qt.ControlModifier:
            self.on_key_pressed_no_ctrl(event)
        else:
            self.on_key_pressed_ctrl(event)

    def on_key_pressed_no_ctrl(self, event):
        # 0-9 or A-Z or a-z exluding Ctr modifier
        try:
            code = ord(event.text())
            if (48 <= code <= 57 or 65 <= code <= 90 or 97 <= code <= 122) \
               and QApplication.keyboardModifiers() != Qt.ControlModifier:
                self.eq.insert(event.text())
        except TypeError:
            pass
        try:
            self.eq.insert(symbols.ASCII_LATEX_TRANSLATION[event.text()])
        except KeyError:
            pass
        key = event.key()
        if key == Qt.Key_Up:
            self.eq.insert_sup_substituting()
        elif key == Qt.Key_Down:
            self.eq.insert_sub_substituting()
        elif key == Qt.Key_Right:
            self.eq.next_sel()
        elif key == Qt.Key_Left:
            self.eq.previous_sel()
        elif key == Qt.Key_Backslash:
            self.eq.insert(r'\backslash')
        elif key == Qt.Key_AsciiTilde:
            self.eq.insert(r'\sim')
        elif key == Qt.Key_Backspace or key == Qt.Key_Delete:
            self.eq.remove_sel()
        elif key == Qt.Key_Space:
            self.eq.insert(r'\,')

    def on_key_pressed_ctrl(self, event):
        pass
