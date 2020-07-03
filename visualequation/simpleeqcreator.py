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

from collections import namedtuple

from . import eqqueries
from .symbols import utils

"""Module to create raw equations by adding new citizens."""


class SimpleEqCreator:
    """Create an equation by adding subequations to the right.

    It is possible to initialize the equation during construction. Else,
    it will be initialized with the first call to extend.
    """
    def __init__(self, subeq=None):
        if subeq is None:
            # There is an element in self.log for each subeq introduced by
            #   the user, in order.
            # If correspondent subeq was not a JUXT-ublock, each element is a
            #   NonJuxtUblockEntry, else, it is a JuxtUblockEntry.
            self.log = []
            self.eq = [utils.NEWARG]
        else:
            self._init(subeq)

    # Notation:
    #   idx  -> InDeX of some element in originally inserted subequation.
    #   fnje -> index of First Non-Juxt Element of subeq in current Equation
    #   lcjs -> index of Last Citizen of original juxt-ublock Subeq in itself
    #   weel -> Was current Equation Extended later?

    JuxtLog = namedtuple('JuxtLog', 'fnje len lcjs')
    NonJuxtLog = namedtuple('NonJuxtLog', 'fnje len')

    def get_idx(self, idx, subeq_entry=-1):
        """Return the index of an element of an introduced subeq in the eq.

        :idx: It is the index of the element in subeq.
        :subeq_entry: It specifies the subeq you are referring.

        Note that :subeq_entry: 0 refers to subequation which initialized the
        equation. It can be a negative number, which can be useful, for
        example, if you just know how many calls to extend were done from the
        moment in which the subequation in which you are interested was
        introduced.
        """
        if isinstance(self.log[subeq_entry], self.NonJuxtLog) \
                or idx >= self.log[subeq_entry].lcjs:
            return self.log[subeq_entry].fnje + idx
        else:
            return self.log[subeq_entry].fnje - 1 + idx

    def _init(self, subeq):
        if subeq[0] == utils.JUXT:
            fnje = 1
            lcjs = eqqueries.last_citizen(subeq, 1)
            self.log.append(self.JuxtLog(fnje, len(subeq), lcjs))
        else:
            fnje = 0
            self.log.append(self.NonJuxtLog(fnje, len(subeq)))
        self.eq = list(subeq)
        return fnje

    def _update(self, subeq):
        """Extend current equation with subeq and changecurrent the internal state.

        If subeq is not a JUXT-ublock, insert_from_panel it to the right as a citizen.
        Else, insert_from_panel any citizen of subeq as citizens of current equation.
        """
        # Add new log data
        if subeq[0] == utils.JUXT:
            fnje = len(self.eq) + 2
            lcjs = eqqueries.last_citizen(subeq, 1)
            self.log.append(self.JuxtLog(fnje, len(subeq), lcjs))
        else:
            fnje = len(self.eq) + 1
            self.log.append(self.NonJuxtLog(fnje, len(subeq)))

        # Extend equation and correct previous log data
        if isinstance(self.log[-2], self.NonJuxtLog):
            self.eq.insert(self.log[-2].fnje, utils.JUXT)
            self.log[-2].fnje += 1
        else:
            self.eq.insert(self.log[-2].lcjs, utils.JUXT)
            self.log[-2].lcjs += 1
        self.eq.extend(subeq)

        return fnje

    def extend(self, subeq):
        """Extend current equation, or initialize it.

        Return the index of the first element of subeq in the equation if it is
        an usubeq. Else, return the index of the first citizen of subeq in
        current equation. Note that these indices can be invalid after next
        uses of this method. Use self.get_idx in those cases.

        If the equation was not initialized, first call to extend will
        initialize the original equation equal to subeq.

        Behaviour for calls when equation has been already initialized:
            *   If current equation is not a JUXT-ublock, new equation will be
                a JUXT-ublock such that:

                *   First citizen is the original equation.
                *   If subeq is not a JUXT-ublock, subeq will be the second
                    citizen of the new equation.
                    Else, any citizen of subeq will be a citizen of the new
                    equation after the current equation, respecting the
                    order they have in subeq.
            *   Else:

                *   If subeq is not a JUXT-ublock, it will be added as a
                    citizen after the last citizen of the current equation.
                *   Else, any citizen of subeq will be added in order after the
                    last citizen of current equation.
        """
        if not self.log:
            # eq not initialized by the user
            return self._init(subeq)
        else:
            return self._update(subeq)

    def get_eq(self):
        return list(self.eq)
