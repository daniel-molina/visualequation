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

from .symbols import utils
from . import eqtools

class Alice:
    def __init__(self):
        self.name = "Alice"
        self.op = utils.Op(1, r'\textcolor{{magenta}}' 
                           + r'{{\left\lmoustache{{{0}}}\right\rgroup}}')
        self.pos = 0
        self.right = True

    def turn_left(self):
        self.right = False
        self.op = utils.Op(1, r'\textcolor{{magenta}}'
                           + r'{{\left\lgroup{{{0}}}\right\rmoustache}}')

    def turn_right(self):
        self.right = True
        self.op = utils.Op(1, r'\textcolor{{magenta}}' 
                           + r'{{\left\lmoustache{{{0}}}\right\rgroup}}')

    def move(self, eq):
        # Force to be inside the equation before updating
        if self.pos > len(eq) - 1:
            self.pos = len(eq) - 1
            # Simulate a fall
            self.right = False
            self.op = utils.Op(1, r'\textcolor{{brown}}'
                               + r'{{\left\lgroup{{{0}}}\right\lmoustache}}')
            return
        # Get a moving value
        val = random.randint(-1, 1)
        # Correct direction if necessary
        if val < 0 and self.right:
            self.turn_left()
        elif val > 0 and not self.right:
            self.turn_right()
        else:
            self.pos += val 
        # Boundary conditions
        if self.pos < 0:
            self.pos = len(eq) - 1 + self.pos
        elif self.pos > len(eq) - 1:
            self.pos = self.pos - len(eq) + 1
        # Avoid intermediate JUXTs
        if eqtools.is_intermediate_JUXT(eq, self.pos):
            cond = True
            while cond:
                self.pos += 1 if self.right else -1
                cond = eqtools.is_intermediate_JUXT(eq, self.pos)

class Game:
    """
    By the moment there is only one game. In the future we will have to improve
    the interface.
    """
    active = False

    def __init__(self):
        self.ghost = Alice()

    @classmethod
    def activate(cls, state):
        cls.active = state

    def update(self, eq):
        # Keep to the minimum return when no game is played
        if not Game.active:
            return

        self.ghost.move(eq)
        assert 0 <= self.ghost.pos <= (len(eq) - 1)
        eq.insert(self.ghost.pos, self.ghost.op)

