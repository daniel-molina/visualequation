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
"""
from .symbols import utils


def checkeq(eq):
    valid_msg = "OK!"
    if not isinstance(eq, list):
        return repr(eq) + " is not a list."

    if len(eq) == 1:
        if not (isinstance(eq[0], str) or isinstance(eq[0], utils.Op)):
            return repr(eq) \
                    + " has length 1 and content is not a str or op."

        if isinstance(eq[0], utils.Op) and eq[0].n_args:
            return repr(eq) + " has length 1 and content is Op with n_args " \
                              "== " + repr(eq[0].n_args) + " != 0."

    if len(eq) > 1:
        if not isinstance(eq[0], utils.Op):
            return repr(eq) + " has len " + repr(len(eq)) \
                   + " > 1 and first element is not an Op."
        if eq[0].n_args == 0 or eq[0].n_args < -1:
            return repr(eq[0]) + " is a lop with n_args == " \
                   + repr(eq[0].n_args) + " instead of -1 or N > 0."
        if eq[0].n_args > 0 and eq[0].n_args != len(eq) - 1:
            return repr(eq) + " has a lop which expects " \
                   + repr(eq[0].n_args) + " != " + repr(len(eq) - 1) \
                   + " parameters."
        if eq[0] in utils.NONUOPS and eq[0].n_args != 1:
            return repr(eq[0]) + " is a non-user Op with with " \
                   + repr(eq[0].n_args) + " args."
        if eq[0] in (utils.JUXT, utils.TJUXT) and len(eq) < 3:
            return repr(eq) + " is a juxt-block and it has only 1 juxted."

        for par in eq[1:]:
            msg = checkeq(par)
            if valid_msg != msg:
                return msg

    return valid_msg


def checkidx(idx):
    if not isinstance(idx, list):
        return "Index must be a list."
    if not all(isinstance(ele, int) for ele in idx):
        return "Not every element is an integer."
    if not all(ele >= 0 for ele in idx):
        return "Not every element is non-negative."
    try:
        first0pos = idx.index(0)
        if first0pos != len(idx) - 1:
            return "Non-last element is 0."
    except ValueError:
        pass
    return "OK!"


def check(idx, eq, onlysubeqs=True):
    """Check of integrity of a pair index-equation.

    If *onlysubeqs* is True, an index pointing to a lop is an error.
    That is the last condition checked: if that is reported, the rest is OK.
    """
    valid_message = "OK!"
    msg = checkidx(idx)
    if msg != valid_message:
        return "Wrong index: " + msg
    msg = checkeq(eq)
    if msg != valid_message:
        return "Wrong eq: " + msg

    if not idx:
        return valid_message

    eqref = eq
    for lev, pos in enumerate(idx):
        if len(eqref) == 1:
            return "Subeq in " + repr(idx[:lev]) \
                   + " is a symbol/0-args Op. It cannot be indexed."
        if pos > len(eqref) - 1:
            return "Subeq in " + repr(idx[:lev]) \
                   + " has no position " + repr(pos) + "."

        eqref = eqref[pos]

    # This must be the last condition
    if onlysubeqs and idx and not idx[-1]:
        return "Pointed element is a lop."

    return valid_message


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
    """Return the number of actual number of parameters.

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
    plop = outlop(idx, eq, True)
    if not isinstance(plop, utils.Op):
        # Cases: idx == [] and idx points to lop
        return plop
    if idx[-1] == plop.n_args:
        # Case: last param
        return -1
    ridx = idx[:]
    ridx[-1] += 1
    return get(ridx, eq) if retsub else ridx


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
    do that and *retsub* is False, remember to join the complementary index to
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
    if not isusubeq(eq, idx):
        return -1

    eqref = eq
    ulev = 0
    for pos in idx:
        if isusubeq(eqref):
            ulev += 1
        # Last pos is not used. It is assured that elem there is a usubeq.
        eqref = eqref[pos]
    return ulev


def mate(idx, eq, right, ulevel_diff=0, retsub=False):
    """Return the mate to the left and a ulevel difference.

    If it is a last mate and right is True or it is a first mate and right is,
    False, -1 is returned.

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


def boundary_mate(eq, n, last=False, retsub=False):
    """Return the first or last *N*-ulevel mate of eq."""
    eqref = eq
    ridx = []
    ulev = -1
    while isinstance(eqref, list):
        if len(eqref) == 1:
            break
        if eqref[0] == utils.GOP:
            retval = urepr([], eqref[1], retsub)
            return retval if retsub else ridx + [1] + retval
        if isusubeq(eqref):
            ulev += 1
            if ulev == n:
                break
        ridx.append(npars(eqref) if last else 1)
        eqref = eqref[ridx[-1]]

    return eqref if retsub else ridx
