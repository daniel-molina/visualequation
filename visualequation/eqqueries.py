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
Module to transform equations to latex code and getting information from or
replacing equation blocks.
"""
from .symbols import utils
from .errors import ShowError


def subeq2latex(subeq):
    """Return latex code of a subeq."""
    if isinstance(subeq, str):
        return subeq
    elif isinstance(subeq, utils.Op):
        return subeq.latex_code
    elif isinstance(subeq, list):
        return subeq[0](map(subeq2latex, subeq[1:]))
    else:
        ShowError('Unknown equation element in subeq2latex: '
                  + repr(subeq), True)


def get(idx, eq):
    """Get a reference to eq element given its index.

    (If you modify the return value, *eq* is modified.)
    """
    req = eq
    for pos in idx:
        req = req[pos]
    return req


def set_(idx, eq, elem):
    """Overwrite an element of an equation."""
    if not idx:
        eq[:] = elem
        return

    eqref = eq
    for pos in enumerate(idx):
        if pos == len(idx) - 1:
            break
        eqref = eqref[pos]

    eqref[idx[-1]] = elem


def parord(idx):
    """Return the ordinal (starting from 1) of the parameter of an operator.

    If idx is [], return -2.
    """
    if not idx:
        return -2
    return idx[-1] + 1


def supeq(idx, eq=None, retsub=False):
    """Return supeq ref or its index.

    If idx is [], -2 is returned.
    """
    if not idx:
        return -2
    return get(idx[:-1], eq) if retsub else idx[:-1]


def lop(idx, eq=None, retsub=False):
    """Return a leading operator ref or its index.

    If idx is [], return -2.
    Elif idx points to a lop, return -1.
    """
    if not idx:
        return -2
    if not idx[-1]:
        return -1
    ridx = list(idx)
    ridx[-1] = 0
    return get(ridx, eq) if retsub else ridx


def nthpar(n, idx, eq, retsub=False):
    """Return the n-th parameter of a block/op or its index.

    If you want the last parameter, pass n == -1.

    Value *idx* must point to a op or block.
    In the second case, lop-block will be considered.

    If idx points to a symbol, -3 is returned.
    If the operator does not have enough args, -1 is returned.
    """
    elem = get(idx, eq)
    if isinstance(elem, str) or (isinstance(elem, utils.Op)
                                 and not elem.n_args):
        return -3

    ridx = list(idx)

    if isinstance(elem, list):
        elem = elem[0]

    if elem.n_args < n:
        return -1

    if n == -1:
        n = elem.n_args

    if isinstance(elem, list):
        ridx.append(n)
    else:
        ridx[-1] = n

    return get(ridx, eq) if retsub else ridx


def prevpar(idx, eq=None, retsub=False):
    """Return prev co-parameter ref or its index.

    If idx is [], return -2.
    Elif idx points to first param or lop, return -1.
    """
    if not idx:
        return -2
    # Remember that lop is in pos 0 and first param in pos 1.
    if idx[-1] <= 1:
        return -1
    ridx = list(idx)
    ridx[-1] -= 1
    return get(ridx, eq) if retsub else ridx


def nextpar(idx, eq, retsub=False):
    """Return next co-parameter ref or its index.

    If idx is [], return -2.
    Elif it is a last param or lop, return -1.
    """
    plop = lop(idx, eq, True)
    if not isinstance(plop, utils.Op):
        return plop
    if idx[-1] >= plop.n_args:
        return -1
    ridx = list(idx)
    ridx[-1] += 1
    return get(ridx, eq) if retsub else ridx


def is_juxted(idx, eq):
    """Return whether subeq pointed by idx is an arg of a JUXT."""
    return lop(idx, eq, True) == utils.JUXT


def is_juxtblock(subeq, idx=None, iseq=False):
    """Return whether a subeq is a JUXT-block."""
    if not isinstance(subeq, list):
        return False
    return (get(idx, subeq)[0] if iseq else subeq[0]) == utils.JUXT


def is_tjuxtblock(subeq, idx=None, iseq=False):
    """Return whether a subeq is a TJUXT-block."""
    if not isinstance(subeq, list):
        return False
    return (get(idx, subeq)[0] if iseq else subeq[0]) == utils.TJUXT


def is_usubeq(subeq, idx=None, iseq=False):
    """Return whether a subeq is a usubeq."""
    if not isinstance(subeq, list):
        return True
    return (get(idx, subeq)[0] if iseq else subeq[0]) not in utils.NONUOPS


def urepr(idx, eq, retsub=False):
    """Return the urepr of a subeq or its index.

    It supposes that only blocks can be non-usubeqs and in that case they have
    only one parameter.

    *eq* can be a subeq since user representation does not depend on eq. If you
    do that and *retsub* is False, remember to join the complementary index to
    the left of the output if you want it to refer to a superequation of *eq*.
    """
    elem = get(idx, eq)
    opidx = idx
    while isinstance(elem, list):
        if elem[0] not in utils.NONUOPS:
            return elem if retsub else opidx
        opidx.append(1)
        elem = elem[1]
    return elem if retsub else opidx


def level(idx):
    """Return the nesting level of a subeq of an equation."""
    return len(idx)


def ulevel(idx, eq):
    """Return the nesting ulevel of a usubeq of an equation.

    If *idx* does not point to a usubeq, -1 is returned.
    """
    if not is_usubeq(eq, idx, True):
        return -1

    eqref = eq
    ulevel = 0
    for pos in idx[:-1]:
        if is_usubeq(eqref):
            ulevel += 1
        eqref = eqref[pos]
    return ulevel


def mate(idx, eq, right, ulevel_diff=0, retsub=False):
    """Return the mate to the left and a ulevel difference.

    If it is a first mate, -1 is returned.

    Parameter *ulevel_diff* indicate the ulevel of the mates as an offset:
    Supposing that subeq pointed by *idx* is a N-ulevel peer and the intention
    is to find its M-ulevel mate to the right or left for M > N,
    *ulevel_diff* must be M - N.

    .. note::
        Let be N the ulevel of subeq pointed by *idx*. If *ulevel_diff* is
        not 0, subeq MUST be is a M-ulevel aide for every M > N.

    .. note::
        If first call to this function is done with *ulevel_diff* equal to 0,
        then a next call using the correspondent second output value is a valid
        call to look for mates to the right or left.

    .. note::
        It just translates the algorithm described in HACKING.
    """
    sidx = list(idx)
    ulev_diff = ulevel_diff

    # Find common usupeq
    while True:
        supidx = supeq(sidx)
        if supidx == -2:
            return -1, None
        pord = parord(sidx)
        sidx = supidx
        ulev_diff += 1 if is_usubeq(eq, sidx, True) else 0
        if (right and pord != lop(sidx, eq, True).n_args) \
                or (not right and pord != 1):
            break

    # Find mate
    pord += 1 if right else -1
    while True:
        ulev_diff -= 1 if is_usubeq(eq, sidx, True) else 0
        sidx = nthpar(pord, sidx, eq)
        if not ulev_diff or lop(sidx, eq, True) == utils.GOP:
            return urepr(sidx, eq, retsub), ulev_diff
        # -1 is a flag value accepted by nthpar
        pord = 1 if right else -1


def boundary_mate(eq, N, last=False, retsub=False):
    """Return the first or last *N*-ulevel mate of eq."""
    eqref = eq
    ridx = []
    ulevel = -1
    while isinstance(eqref, list):
        if eqref[0] == utils.GOP:
            retval = urepr([], eqref[1], retsub)
            return retval if retsub else ridx + [1] + retval
        if is_usubeq(eqref):
            ulevel += 1
            if ulevel == N:
                break
        ridx.append(eqref[0].n_args if last else 1)
        eqref = eqref[ridx[-1]]

    return eqref if retsub else ridx
