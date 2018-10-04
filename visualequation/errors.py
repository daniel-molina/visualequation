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

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

class ShowError(QMessageBox):

    # It is modified in __main__.MainWindow
    default_parent = None

    def __init__(self, msg, exit_on_click, parent=None):
        if parent is None:
            super().__init__(ShowError.default_parent)
        else:
            super().__init__(parent)
        self.setText(msg)
        self.setWindowTitle("Error")
        self.setIcon(QMessageBox.Critical)
        self.exec_()
        if exit_on_click:
            raise SystemExit(msg)
