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
symbols in the panel.
"""
import os

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from .symbols import lists
from . import commons
from .errors import ShowError
from visualequation.eqlib.ops import *
from visualequation.eqlib.subeqs import Subeq


class TabWidget(QTabWidget):
    def __init__(self, mwin):
        super().__init__(mwin)

        self.eqlabel = mwin.deq
        self.tabs = []
        for index, menuitemdata in enumerate(lists.MENUITEMSDATA):
            self.tabs.append(QWidget())
            icon_path = os.path.join(commons.ICONS_DIR,
                                     menuitemdata.name + ".png")
            if not os.path.exists(icon_path):
                ShowError("Icon " + menuitemdata.name + " not found.", True)
            icon = QIcon(icon_path)
            self.setIconSize(QSize(50, 30))
            self.addTab(self.tabs[index], icon, "")
            # self.setTabToolTip(idx, "Hello")
            # self.setTabWhatsThis(idx, "Hello")
            layout = QGridLayout(self)
            row = 0
            column = 0
            for icon in menuitemdata.icon_l:
                label = QLabel('')
                icon_path = os.path.join(commons.ICONS_DIR, icon.name + ".png")
                if not os.path.exists(icon_path):
                    ShowError("Icon " + icon.name + " not found.", True)
                label.setPixmap(QPixmap(icon_path))

                def f(state, cble=icon.callable):
                    return self.handle_click(state, cble)

                label.mousePressEvent = f
                layout.addWidget(label, row, column)
                label.setAlignment(Qt.AlignCenter)
                column += 1
                if column > 9:
                    column = 0
                    row += 1

            self.tabs[index].setLayout(layout)

    def handle_click(self, event, callable_):
        self.eqlabel.insert_from_callable(callable_)
