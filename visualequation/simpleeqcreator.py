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
from copy import deepcopy

from . import eqqueries
from .symbols import utils

"""Module to create raw equations by adding new citizens."""


class SimpleEqCreator:
    """Create an equation by adding subequations to the right.

    It is possible to initialize the equation during construction. Else,
    it will be initialized with the first call to extend.

    If equation is not initialized, it is equal to VOID.

    If equation is only initialized, it is equal to initial eq.

    Else, it is a JUXT-block including any inserted subeq which is not a
    JUXT-block as a juxted. Juxteds of an inserted JUXT-block are integrated
    as juxteds of the whole eq.

    .. note::
        If a TJUXT-block is passed, it is integrated as a single juxted. In
        particular, the TJUXT op will be present in the whole eq. Of course,
        you should not insert more than one TJUXT-block to be consistent with
        visual equation conventions.
    """

    LogEntry = namedtuple('LogEntry', 'was_jb pos')

    def __init__(self, subeq=None):
        self.log = []
        self.eq = utils.void()
        if subeq is not None:
            self._init(subeq)

    def get_idx(self, subeq_idx, subeq_entry=-1):
        """Return the index of in composed eq by specifying the index of the
        element in a inserted subeq and which inserted subeq you refer.

        .. note::
            If inserted subeq was a JUXT-block, you must not pass *subeq_idx*
            in ([], [0]) since the original juxt was probably discarded and
            only one juxt op is present as the lop of the composed eq (This
            paragraph does not apply to TJUXT-blocks.)
        """
        if self.log[subeq_entry].pos < 0:
            return subeq_idx[:]
        if not self.log[subeq_entry].was_jb:
            return [self.log[subeq_entry].pos] + subeq_idx
        return [self.log[subeq_entry].pos + subeq_idx[0] - 1] + subeq_idx[1:]

    def _init(self, subeq):
        self.eq[:] = deepcopy(subeq)
        if len(subeq) > 1 and subeq[0] == utils.JUXT:
            self.log[:] = [self.LogEntry(True, 1)]
            return [1]
        else:
            # Let us use a special value for position in this case
            # It will be overwritten in next call to extend
            self.log[:] = [self.LogEntry(False, -1)]
            return []

    def _update(self, subeq):
        """Extend current equation with subeq and update the log.

        It supposes that eq has been already initialized.
        """
        # Marginal case: Set initial eq as a juxted if it was not a JUXT-block
        # self.eq will have only one juxted after this block, but it will have
        # at least 2 when this function returns
        if self.eq[0] != utils.JUXT:
            self.eq[:] = [utils.JUXT, deepcopy(self.eq)]
            self.log[:] = [self.LogEntry(False, 1)]

        # Add new subeq
        next_juxted_pos = len(self.eq)
        if len(subeq) > 1 and subeq[0] == utils.JUXT:
            self.log.append(self.LogEntry(True, next_juxted_pos))
            self.eq[:] += deepcopy(subeq[1:])
        else:
            self.log.append(self.LogEntry(False, next_juxted_pos))
            self.eq.append(deepcopy(subeq))
        return [next_juxted_pos]

    def append(self, subeq, include_voids=True):
        """Extend current equation, or initialize it.

        Return:

            *   If *include_voids* is False and subeq is a VOID, -1.
            *   Elif *subeq* was not a JUXT-block subeq, the index in eq of
                *subeq*.
            *   Else, the index of the first juxted of *subeq*.

        If the equation was not initialized, first call to this method will
        initialize the original equation to subeq.

        .. note::
            Returned values are reliable unless:

                *   It was the returned value by the first call to this
                    method, and
                *   A non juxt-block subeq was inserted in that first call, and
                *   The instance of this class was not initialized using the
                    constructor, and
                *   At least one more call to this method has been done from
                    that first call.
            In the specified case, originally returned value would be [] and
            after the second call previously inserted subequation will be in
            [1]. You can: 1. Relay on the mentioned behavior or 2. Call method
            get_idx (with *subeq_entry* equal to 0) to obtain the correct
            value.
        """
        if not include_voids and subeq == utils.void():
            return -1

        if not self.log:
            # eq not yet initialized
            return self._init(subeq)
        else:
            return self._update(subeq)

    def extend(self, subeq_list, include_voids=True):
        """Given a list of subeqs, append all of them.

        Return the number of inserted subeqs.
        """
        n_inserted_subeqs = 0
        for s in subeq_list:
            if include_voids or s != utils.void():
                self.append(s)
                n_inserted_subeqs += 1
        return n_inserted_subeqs

    def get_eq(self):
        return deepcopy(self.eq)

    def n_inserted_subeqs(self):
        return len(self.log)

    def n_juxteds(self):
        """Return number of juxteds.

        Marginal cases:

            *   Non-initialized eq: return 0.
            *   Equation was just initialized (by ctor or not) with a
                non-JUXT-block subeq: return 1.
        """
        if not self.log:
            return 0
        if self.eq[0] != utils.JUXT:
            return 1
        return len(self.eq) - 1
