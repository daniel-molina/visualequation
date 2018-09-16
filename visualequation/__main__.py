#!/usr/bin/env python3

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

"""This is the file to execute the program."""
import sys
import tempfile
import shutil
import os

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from . import symbolstab
from . import eq
from . import symbols
from . import conversions

class MainWindow(QMainWindow):
    def __init__(self, temp_dir):
        super().__init__()
        self.temp_dir = temp_dir
        self.init_center_widget()
        self.statusBar()
        self.init_menu()

        self.setWindowTitle('Visual Equation')
        self.setGeometry(0, 0, 900, 600)

    def init_menu(self):
        exit_act = QAction('&Exit', self)
        exit_act.setShortcut('Ctrl+Q')
        exit_act.setStatusTip('Exit application')
        exit_act.triggered.connect(qApp.quit)
        open_act = QAction('&Open', self)
        open_act.setShortcut('Ctrl+O')
        open_act.setStatusTip('Open equation from image')
        open_act.triggered.connect(self.maineq.open_eq)
        save_act = QAction('&Save', self)
        save_act.setShortcut('Ctrl+S')
        save_act.setStatusTip('Save image')
        save_act.triggered.connect(self.maineq.save_eq)
        undo_act = QAction('&Undo', self)
        undo_act.setShortcut('Ctrl+Z')
        undo_act.setStatusTip('Return equation to previous state')
        undo_act.triggered.connect(self.maineq.recover_prev_eq)
        redo_act = QAction('&Redo', self)
        redo_act.setShortcut('Ctrl+Y')
        redo_act.setStatusTip('Recover next equation state')
        redo_act.triggered.connect(self.maineq.recover_next_eq)
        copy_act = QAction('&Copy', self)
        copy_act.setShortcut('Ctrl+C')
        copy_act.setStatusTip('Copy selection')
        copy_act.triggered.connect(self.maineq.sel2eqbuffer)
        def cut():
            self.maineq.sel2eqbuffer()
            self.maineq.remove_sel()
        cut_act = QAction('C&ut', self)
        cut_act.setShortcut('Ctrl+X')
        cut_act.setStatusTip('Cut selection')
        cut_act.triggered.connect(cut)
        paste_act = QAction('&Paste', self)
        paste_act.setShortcut('Ctrl+V')
        paste_act.setStatusTip('Paste previous cut or copied selection')
        paste_act.triggered.connect(self.maineq.eqbuffer2sel)
        left_insert_act = QAction('&Left insertion', self)
        left_insert_act.setShortcut('Ctrl+P')
        left_insert_act.setStatusTip('Insert blank to the left of the selection')
        left_insert_act.triggered.connect(self.maineq.left_NEWARG)

        menubar = self.menuBar()
        file_menu = menubar.addMenu('&File')
        file_menu.addAction(open_act)
        file_menu.addAction(save_act)      
        file_menu.addAction(exit_act)
        edit_menu = menubar.addMenu('&Edit')
        edit_menu.addAction(undo_act)
        edit_menu.addAction(redo_act)
        edit_menu.addAction(copy_act)
        edit_menu.addAction(cut_act)
        edit_menu.addAction(paste_act)
        edit_menu.addAction(left_insert_act)

    def init_center_widget(self):
        # Create central widget
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()
        # Create the equation
        self.maineq = eq.Eq([symbols.NEWARG], self.temp_dir, self)
        #label_pixmap = QPixmap('tests/im.png')
        #label = QLabel(self)
        #label.setPixmap(label_pixmap)
        self.maineq.setAlignment(Qt.AlignCenter)
        # Create the symbols TabWidget
        self.tabs = symbolstab.TabWidget(self, self.maineq)
        self.tabs.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        # Add everything to the central widget
        layout.addWidget(self.maineq)
        layout.addWidget(self.tabs)
        central_widget.setLayout(layout)
        self.maineq.setFocus()

def main():
    """ This the main function of the program."""    
    # Use global for app to be destructed at the end
    # http://pyqt.sourceforge.net/Docs/PyQt5/gotchas.html#crashes-on-exit
    global app 
    app = QApplication(sys.argv)

    # Prepare a temporal directory to manage all intermediate files
    temp_dirpath = tempfile.mkdtemp()

    win = MainWindow(temp_dirpath)

    win.show()

    exit_code = app.exec_()
    shutil.rmtree(temp_dirpath)
    sys.exit(exit_code)
   
if __name__ == '__main__':
    main()
