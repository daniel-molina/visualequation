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

"""
Module to manage the menu of Visual Equation and the distribution of the
symbols in the above panel.
"""
import os

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from .symbols import lists
from . import commons

class TabWidget(QTabWidget):
    def __init__(self, parent, maineq):
        super().__init__(parent)

        self.maineq = maineq
        self.tabs = []
        for index, menuitemdata in enumerate(lists.MENUITEMSDATA):
            self.tabs.append(QWidget())
            icon = QIcon(os.path.join(commons.SYMBOLS_DIR,
                                      menuitemdata.tag + ".png"))
            self.setIconSize(QSize(50, 30))
            self.addTab(self.tabs[index], icon, "")
            #self.setTabToolTip(index, "Hello")
            #self.setTabWhatsThis(index, "Hello")
            layout = QGridLayout(self)
            row = 0
            column = 0
            for symb in menuitemdata.symb_l:
                label = QLabel('')
                label.setPixmap(QPixmap(os.path.join(commons.SYMBOLS_DIR,
                                                     symb.tag + ".png")))
                cmd = lambda state, code=symb.code: \
                      self.handle_click(state, code)
                label.mousePressEvent = cmd
                layout.addWidget(label, row, column)
                label.setAlignment(Qt.AlignCenter)
                column += 1
                if column > 9:
                    column = 0
                    row += 1
             
            self.tabs[index].setLayout(layout)

    def handle_click(self, event, code):
        modifiers = QApplication.keyboardModifiers()
        if modifiers == Qt.ShiftModifier:
            self.maineq.eq.insert_substituting(code)
        else:
            self.maineq.eq.insert(code)
