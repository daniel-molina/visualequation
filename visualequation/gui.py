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

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from . import commons
from .symbolstab import TabWidget
# from . import game
from .clipboard import ClipBoard
from .eqdisplay import DisplayedEq
from .errors import ShowError
from .uiactions import UIActions
from .uidialogs import UIDialogs
from .uimisc import UIMisc


class MyScrollBar(QScrollBar):
    """
    Class to set focus in equation when moving the scroll bars.
    It also moves the equation correctly when inserting new elements.
    """

    def __init__(self, orientation, parent=None):
        super().__init__(orientation, parent)
        self.equation = None
        self.prev_max = None

    def mouseReleaseEvent(self, event):
        QScrollBar.mouseReleaseEvent(self, event)
        self.equation.setFocus()

    def setFocusTo(self, widget):
        self.equation = widget

    def sliderChange(self, change):
        QScrollBar.sliderChange(self, change)
        # Do not use/set prev_max vertically
        if change == QAbstractSlider.SliderRangeChange and \
                self.orientation() == Qt.Horizontal:
            if self.prev_max is not None:
                self.setValue(self.value() + self.maximum() - self.prev_max)
            self.prev_max = self.maximum()


class MyScrollArea(QScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.vbar = MyScrollBar(Qt.Vertical, self)
        self.hbar = MyScrollBar(Qt.Horizontal, self)
        self.setVerticalScrollBar(self.vbar)
        self.setHorizontalScrollBar(self.hbar)

    def setWidget(self, widget):
        QScrollArea.setWidget(self, widget)
        self.vbar.setFocusTo(widget)
        self.hbar.setFocusTo(widget)


class MainWindow(QMainWindow):
    def __init__(self, tempdir, args):
        super().__init__()
        self.args = args
        self.tempdir = tempdir
        self.clipboard = ClipBoard()
        self.deq = DisplayedEq(self, debug=args.debug)
        self.scrollarea = MyScrollArea(self)
        self.tabs = TabWidget(self)
        ShowError.default_parent = self
        self.init_center_widget()
        self.uid = UIDialogs(self)
        self.uimisc = UIMisc(self)
        self.uiactions = UIActions(self)
        self.statusBar()
        self.init_menu()
        for action in self.uiactions:
            self.addAction(action)

        self.setWindowTitle('Visual Equation')
        self.setWindowIcon(QIcon(commons.ICON))
        self.resize(900, 600)

    def init_center_widget(self):
        # Create central widget
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()
        # Create the equation
        self.deq.setAlignment(Qt.AlignCenter)
        self.scrollarea.setWidget(self.deq)
        self.scrollarea.setWidgetResizable(True)
        # Create the symbols TabWidget
        self.tabs.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        # Add everything to the central widget
        layout.addWidget(self.scrollarea)
        layout.addWidget(self.tabs)
        central_widget.setLayout(layout)
        self.deq.setFocus()

    def init_menu(self):
        # Old commentary:
        # Not using mnemonics (&) for the menubar because the focus is lost
        # and equation cannot continue being edited.
        menubar = self.menuBar()
        menubar.setNativeMenuBar(False)
        file_menu = menubar.addMenu(_('File'))
        file_menu.addAction(self.uiactions.get("New equation"))
        file_menu.addAction(self.uiactions.get("Open equation"))
        file_menu.addAction(self.uiactions.get("Export equation"))
        file_menu.addSeparator()
        file_menu.addAction(self.uiactions.get("Exit"))
        edit_menu = menubar.addMenu(_('Edit'))
        edit_menu.addAction(self.uiactions.get("Undo (local)"))
        edit_menu.addAction(self.uiactions.get("Redo (local)"))
        edit_menu.addSeparator()
        edit_menu.addAction(self.uiactions.get("Cut"))
        edit_menu.addAction(self.uiactions.get("Copy"))
        edit_menu.addAction(self.uiactions.get("Paste"))
        edit_menu.addSeparator()
        edit_menu.addAction(self.uiactions.get("Edit Latex block"))
        edit_menu.addSeparator()
        edit_menu.addAction(self.uiactions.get("Select all"))
        view_menu = menubar.addMenu(_('View'))
        view_menu.addAction(self.uiactions.get("Zoom in"))
        view_menu.addAction(self.uiactions.get("Zoom out"))
        view_menu.addSeparator()
        view_menu.addAction(self.uiactions.get("LaTeX code..."))
        game_menu = menubar.addMenu(_('Games'))
        # game_menu.addAction(activate_game_act)
        help_menu = menubar.addMenu(_('Help'))
        help_menu.addAction(self.uiactions.get("Help"))
        help_menu.addAction(self.uiactions.get("About"))
        help_menu.addAction(self.uiactions.get("About Qt"))
