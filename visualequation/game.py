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
from .symbols import symbols
from . import eqtools

def f(expr):
    return utils.Op(1, r'\textcolor{{magenta}}{{' + expr + '}} {0}')

ALICE_CONSTRUCTS = [
    f(r'e^{{-i\pi}}'),
    f(r'G\frac{{Mm}}{{r^2}}'),
    f(r'\int e^{{x^2}}\,dx'),
    f(r'\frac{{ab+bc}}{{bd}}'),
    f(r'\frac{{ac}}{{bd}}'),
    f(r'ax^2+bx^2+c'),
    f(r'\frac{{1}}{{N}}\sum_{{i=1}}^N x_i'),
    f(r'\frac{{-b\pm\sqrt{{b^2-4ac}}}}{{2a}}'),
    f(r'\sqrt{{(x_2-x_1)^2-(y_2-y_1)^2}}'),
    f(r'\frac{{y_2-y}}{{x_2-x_1}}'),
    f(r'(x-h)^2+(y-k)^2'),
    f(r'\frac{{4}}{{3}}\pi r^3'),
    f(r'\frac{{1}}{{3}}b^2 h'),
    f(r'\frac{{1}}{{3}}\pi r^2 h'),
    f(r'\pi r^2 h'),
    f(r'(a\cdot c) b - (a\cdot b) c'),
]

ALICE_CONSTRUCTS += [f(i.expr) for i in symbols.LOWER_GREEK]
ALICE_CONSTRUCTS += [f(i.expr) for i in symbols.UPPER_GREEK]
ALICE_CONSTRUCTS += [f(i.expr) for i in symbols.VAR_GREEK]

class Alice:
    def __init__(self):
        self.name = "Alice"
        self.op = utils.Op(1, r'\textcolor{{magenta}}' 
                           + r'{{\left\lmoustache{{{0}}}\right\rgroup}}')
        self.pos = 0
        self.right = True
        #self.try_constructs = 0

    def cycle(self, pos, eq):
        if pos < 0:
            return self.cycle(len(eq) + pos, eq)
        elif pos > len(eq) - 1:
            return self.cycle(pos - len(eq), eq)
        else:
            return pos

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
        if val == 0:
            self.op = random.choice(ALICE_CONSTRUCTS)
            #self.op = ALICE_CONSTRUCTS[self.try_constructs]
            #self.try_constructs += 1
        elif val < 0 and self.right:
            self.turn_left()
        elif val > 0 and not self.right:
            self.turn_right()
        else:
            self.pos = self.cycle(self.pos + val, eq) 
        # Avoid all kind of JUXTs: it is disgusting when Alice is very big
        if eq[self.pos] == utils.JUXT:
            cond = True
            while cond:
                self.pos = self.cycle(self.pos + 1 if self.right else -1, eq)
                cond = eq[self.pos] == utils.JUXT
        # Avoid first argument of index operators: \sideset is picky
        if self.pos != 0 \
           and hasattr(eq[self.pos - 1], 'type_') \
           and eq[self.pos - 1].type_ in ('index', 'opindex'):
            self.pos = self.cycle(self.pos + 1 if self.right else -1, eq)


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

