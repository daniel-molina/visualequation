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
Module to get information from equations and subequations.

Equation format:

Symbols: [symb]
Blocks:  [lop, par1, par2, ..., parn]

Example: [JUXT, ["2"], ["x"], [FRAC, ["c"], ["d"]]]

.. note::
    This module was coded to manage filters. However, they are not allowed.
    You could drop support for them in the future at this module-level.
    Note that there can be still GOP-blocks inside GOP-blocks.
"""
from .symbols import utils

def subeq2latex(subeq):
    """Return latex code of a subeq."""
    if len(subeq) > 1:
        return subeq[0](map(subeq2latex, subeq[1:]))
    elif isinstance(subeq[0], str):
        return subeq[0]
    else:
        return subeq[0].latex_code


def get(idx, eq):
    """Get a reference to eq element given its index.

    (If you modify the return value, *eq* is modified.)
    """
    req = eq
    for pos in idx:
        req = req[pos]
    return req


def isb(subeq, idx=None):
    """Return if an equation element is a block."""
    elem = subeq if idx is None else get(idx, subeq)
    return isinstance(elem, list) and len(elem) > 1


def parord(idx):
    """Return the ordinal (starting from 1) of the parameter of an operator.

    If *idx* is [], return -2.
    Elif *idx* points to a lop, return -1.
    """
    if not idx:
        return -2
    if not idx[-1]:
        return -1
    return idx[-1]


def supeq(idx, eq=None, retsub=False):
    """Return supeq ref or its index.

    If *idx* is [], -2 is returned.
    If *idx* is a lop, -1 is returned.
    """
    if not idx:
        return -2
    if not idx[-1]:
        return -1
    return get(idx[:-1], eq) if retsub else idx[:-1]


def islop(idx):
    """Return if an index points to a lop."""
    return idx != [] and idx[-1] == 0


def outlop(idx, eq=None, retsub=False):
    """Return a leading operator ref (or its index) by specifying one of its
    parameters.

    If *idx* is [], return -2.
    Elif *idx* points to a lop, return -1.
    """
    if not idx:
        return -2
    if not idx[-1]:
        return -1
    ridx = list(idx)
    ridx[-1] = 0
    return get(ridx, eq) if retsub else ridx


def inlop(idx, eq, retsub=False):
    """Return a leading operator ref (or its index) given the lop-block.

    If *idx* points to a symbol, return -3.
    Elif *idx* points to a lop, return -1.
    """
    if islop(idx):
        return -1

    lopblock = get(idx, eq)
    if len(lopblock) == 1:
        return -3

    return lopblock[0] if retsub else idx + [0]


def nthpar(n, idx, eq, retsub=False):
    """Return the n-th parameter of a block/op or its index.

    If you want the last parameter, pass n == -1.

    Value *idx* must point to a op or block.
    In the second case, lop-block will be considered as the parameter's op.

    If *idx* points to a symbol, -3 is returned.
    Elif the operator does not have enough args, -1 is returned.
    Elif *n* is 0, -5 is returned.
    """
    if not n:
        return -5

    if islop(idx):
        sup_idx = idx[:-1]
    else:
        sup_idx = idx[:]
    sup = get(sup_idx, eq)
    op = sup[0]

    last_par_ord = len(sup) - 1
    if n > last_par_ord:
        return -1

    if n == -1:
        n = last_par_ord

    return get(sup_idx + [n], eq) if retsub else sup_idx + [n]


def npars(subeq, idx=None):
    """Return the actual number of parameters.

    This function matters specially for juxts-blocks. Else, it must be equal to
    lop-subeq.n_args.

    If an operator is passed or referred, -3 is returned (an operator is not
    enough to know the actual number of parameters of a juxt).

    If a symbol is passed or referred, -1 is returned.
    """
    s = subeq if idx is None else get(idx, subeq)
    if not isinstance(s, list):
        return -3
    nelems = len(s)
    return nelems - 1 if nelems > 1 else -1


def prevpar(idx, eq=None, retsub=False):
    """Return prev co-parameter ref or its index.

    If idx is [], return -2.
    Elif idx points to first param or lop, return -1.
    """
    if not idx:
        return -2
    if idx[-1] <= 1:
        # Cases: lop or first param
        return -1
    ridx = idx[:]
    ridx[-1] -= 1
    return get(ridx, eq) if retsub else ridx


def nextpar(idx, eq, retsub=False):
    """Return next co-parameter ref or its index.

    If idx is [], return -2.
    Elif it is a last param or lop, return -1.
    """
    if not idx:
        return -2

    block = get(idx, eq)
    if idx[-1] in (len(block) - 1, 0):
        return -1

    ridx = idx[:]
    ridx[-1] += 1
    return block[ridx[-1]] if retsub else ridx

def relpar(idx, subeq, n=1, retsub=False):
    """Get a co-parameter ref or its index.

    Return -1 if requested parameter does not exist or -2 if idx is [].
    """
    if not idx:
        return -2
    sup = supeq(idx, subeq, True)
    ord = idx[-1] + n
    if 0 < ord < len(sup):
        return sup[ord] if retsub else idx[:-1] + [ord]
    else:
        return -1

def isjuxtblock(subeq, idx=None):
    """Return whether an element is a juxt-block (included temporal)."""
    s = subeq if idx is None else get(idx, subeq)
    if not isinstance(s, list) or len(s) == 1:
        return False
    return s[0] in (utils.JUXT, utils.TJUXT)


def isjuxted(idx, eq):
    """Return whether a subeq is a juxted. If a supeq exist, you can use
    isjuxtblock instead."""
    if not idx:
        return False
    return isjuxtblock(eq, idx[:-1])

def isgoppar(idx, eq):
    """Return whether a subeq is a GOP-par.

    .. note::
        This function says nothing about being selectable. Use selectivity
        function to check selectivity in a safe way.
    """
    if not idx:
        return False
    if supeq(idx, eq, True)[0] == utils.GOP:
        return True
    return False

def isusubeq(subeq, idx=None):
    """Return whether an element is a usubeq.

    .. note::
        An operator is NOT an usubeq.

    It supposes that symbols are usubeqs.
    """
    s = subeq if idx is None else get(idx, subeq)
    # Note: no using islop because by default a subeq is passed, not an index
    if not isinstance(s, list):
        return False
    return len(s) == 1 or s[0] not in utils.NONUOPS


def urepr(idx, eq, retsub=False):
    """Return the urepr of a subeq or its index.

    If *idx* points to an op, -1 is returned.

    It supposes that symbols are usubeqs and non-user ops have only one arg.

    *eq* can be a subeq since user representation does not depend on eq. If you
    do that and *retsub* is False, remember to join a complementary index to
    the left of the output if you want it to refer to a superequation of *eq*.
    """
    elem = get(idx, eq)
    if not isinstance(elem, list):
        return -1
    opidx = idx[:]
    while len(elem) > 1:
        if elem[0] not in utils.NONUOPS:
            return elem if retsub else opidx
        opidx.append(1)
        elem = elem[1]
    return elem if retsub else opidx


def biggest_supeq_with_urepr(idx, eq, retsub=False):
    """Get ref of biggest subeq which has pointed usubeq as urepr or index.

    If pointed subeq is not a usubeq, -1 is returned.
    If no supeq has pointed usubeq as urepr, return -3
    (include case idx == [] and eq being an usubeq).
    """
    eqref = eq
    candidate = -3
    for lev, pos in enumerate(idx):
        if isusubeq(eqref):
            candidate = None
        elif not isinstance(candidate, list):
            candidate = eqref if retsub else idx[:lev]
        eqref = eqref[pos]

    if not isusubeq(eqref):
        return -1
    return -3 if candidate is None else candidate


def level(idx):
    """Return the nesting level of a subeq of an equation.

    If *idx* does not point to a subeq, -1 is returned.
    """
    if islop(idx):
        return -1
    return len(idx)


def ulevel(idx, eq):
    """Return the nesting ulevel of a usubeq of an equation.

    If *idx* does not point to a usubeq, -1 is returned.
    """
    eqref = eq
    ulev = 0
    for pos in idx:
        if isusubeq(eqref):
            ulev += 1
        eqref = eqref[pos]
    if not isusubeq(eqref):
        return -1
    return ulev


def selectivity(idx, eq):
    """Give information on selectivity of a subequation.

    Return  2 if subequation is SELECTABLE and is not a GOP-block urepr.
    Return  1 if subequation is SELECTABLE and is a GOP-block urepr.
    Return  0 if subequation is NOT SELECTABLE, GOP-block strict SUBEQ
                            and it is not the GOP-block urepr.
    Return -1 if subequation is NOT SELECTABLE and not GOP-block strict SUBEQ.

    .. note::
        A subequation is selectable if, and only if, return value is positive.

    .. note::
        To know that return value is 0 is not enough to know if subeq is a
        usubeq. Since this function informs about selectivity, it is not
        considered important to inform about the user property itself.

    .. note::
        If return value is -1, there exists at least one selectable strict
        subeq of pointed subeq, its urepr.

    .. note::
        In current implementation of VE, GOP-blocks are the only subeqs which
        are not usubeqs and GOP-blocks cannot be the parameter of a GOP. As a
        consequence, if -1 is returned it means (in current implementation)
        that subeq is a GOP-block and its parameter is selectable.
    """
    eqref = eq
    is_gopblock_strict_subeq = False
    for lev, par_ord in enumerate(idx):
        if is_gopblock_strict_subeq and eqref[0] not in utils.NONUOPS:
            return 0
        if eqref[0] == utils.GOP:
            is_gopblock_strict_subeq = True
        eqref = eqref[par_ord]

    if eqref[0] in utils.NONUOPS:
        return 0 if is_gopblock_strict_subeq else -1
    else:
        return 1 if is_gopblock_strict_subeq else 2


def mate(idx, eq, right, ulevel_diff=0, retsub=False):
    """Return the mate to the left and a ulevel difference.

    If it is a last mate and right is True or it is a first mate and right is,
    False, -1 is returned.

    Parameter *ulevel_diff* indicate the ulevel of the mates as an offset:
    Supposing that subeq pointed by *idx* is a N-ulevel peer and the intention
    is to find its M-ulevel mate to the right or left for M > N,
    *ulevel_diff* must be M - N.

    .. note::
        If first call to this function is done with *ulevel_diff* equal to 0,
        then a next call using the correspondent second output value is a valid
        call to look for mates to the right or left.

    .. note::
        It just translates the algorithm described in HACKING.
    """
    sidx = idx[:]
    uld = ulevel_diff

    # Find common usupeq
    while True:
        supidx = supeq(sidx)
        if supidx == -2:
            return -1, None
        pord = parord(sidx)
        sidx = supidx
        s = get(sidx, eq)
        uld += 1 if isusubeq(s) else 0
        if (right and pord != npars(s)) or (not right and pord != 1):
            break

    # Find mate
    pord += 1 if right else -1
    while True:
        uld -= 1 if isusubeq(eq, sidx) else 0
        sidx = nthpar(pord, sidx, eq)
        lop_s = inlop(sidx, eq, True)
        if not uld or lop_s == -3 or lop_s == utils.GOP:
            return urepr(sidx, eq, retsub), uld
        # -1 is a flag value accepted by nthpar
        pord = 1 if right else -1


def boundary_mate(eq, ulevel, last=False, retsub=False):
    """Return reference to the first or last *N*-ulevel mate of eq, or idx."""
    eqref = eq
    ridx = []
    ul = -1
    while isinstance(eqref, list):
        if len(eqref) == 1:
            break
        if eqref[0] == utils.GOP:
            retval = urepr([], eqref[1], retsub)
            return retval if retsub else ridx + [1] + retval
        if isusubeq(eqref):
            ul += 1
            if ul == ulevel:
                break
        ridx.append(len(eqref) - 1 if last else 1)
        eqref = eqref[ridx[-1]]

    return eqref if retsub else ridx


def boundary_symbol(subeq, idx=None, last=False, strict=True, retsub=False):
    """Return reference to the first or last symbol of a subeq, or its index.

    If *strict* is False and the boundary symbol is not selectable, it will
    return the urepr of the GOP with biggest level.

    If *strict* is False, and pointed subeq has not a selectable urepr, -1 is
    returned.

    .. note::
        If *strict* is False, you "want" to pass the full equation as *subeq*
        to guarantee a meaningful result.
    """
    ridx = [] if idx is None else idx[:]
    flag = selectivity(ridx, subeq)
    if not strict:
        if flag == 0:
            return -1
        if flag == 1:
            return get(ridx, subeq) if retsub else ridx

    # From this point we know that sref is not a strict subeq of a GOP-block
    sref = get(ridx, subeq)
    while True:
        if len(sref) == 1:
            break
        if not strict and sref[0] == utils.GOP:
            retval = urepr([], sref[1], retsub)
            return retval if retsub else ridx + [1] + retval
        ridx.append(len(sref) - 1 if last else 1)
        sref = sref[ridx[-1]]

    return sref if retsub else ridx
