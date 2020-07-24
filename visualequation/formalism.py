"""The formalism behind Visual Equation.

Below you can read most of definitions and rules used in Visual Equation code.
There are a lot of definitions, but I hope they are intuitive. On the other
hand, style is more formal/rigorous than probably needed, I hope that does not
harm.

Disclaimer: Definitions have being changed and extended as it has been needed,
it is possible that some of the code notation has not been updated yet.

Formalism of an equation:

Most of definitions used in this text do not relay on the actual
implementation of the equation (a python list), so I found better to keep the
formalism agnostic with respect to the implementation.

    -   Elements (or components) of an equation can be of three different
        types:

        *   Symbols (primitive type),
        *   Operators (primitive type), and
        *   Blocks (composed type).

    -   "Symbols" are elements that make sense by themselves. For example,
        digits or greek letters.

    -   "Operators" are elements which require other elements to make
        sense. For example, a fraction, which needs a numerator and a
        denominator. Operators are usually abbreviated as "ops".

    -   "Blocks" are tuples with N+1 elements, N > 0, composed by:

        -   The leading element which is an operator of arity N. It is called
            the "leading operator" of the block.
        -   The rest of elements are called the "arguments" of the leading
            operator. Every argument of an operator has an ordinal associated:
            The first argument of the operator, the second argument...

    -   An "equation" is defined as a symbol or a block.

Rule 1:

    *   Any symbol or block being part of an equation must be a valid equation
        by itself.

Equation example:

    (Sum, 1, (Prod, 3, 2))                              (*)

In order to understand better the meaning, in functional notation, it would be

    Sum(1, Prod(3, 2))

or in a more common notation

    1 + (3 * 2)

    -   The "primitives" or "primitive elements" of an equation are:

            *   If the equation is a symbol, the equation itself, and
            *   If the equation is a block, the leading operator and the
                "primitives" of the arguments of the leading operator.
                This is a recursive definition that makes sense due to Rule 1.

    -   "Subequations of" (or "in" or "which are contained in") an equation
        are:

            *   The equation itself, and
            *   If the equation is a block, the "subequations of" every
                argument of the leading operator.
                Again, this is a recursive definition that makes sense.
        Subequations are usually abbreviated as "subeqs".

    -   An equation "contains" a subequation if the subequation is contained in
        the equation (this point may be a bit pedantic).

    -   Because subequations are equations, previously defined relations
        between subequations and equations apply also between subequations of
        an equation.

    -   "Superequations of" a subequation S in equation E are, by definition:

        *   Subequations of E such that they contain S but are different
            than S.
        Superequations are usually abbreviated as "supeqs".

Note that our definition of superequation is asymmetric with respect to the
subequation definition. Informally:

    *   Superequation > Subequation
    *   Equation >= Subequation

Examples (equation (*) was defined above):

    *   Subeqs of (*) are: 1, 3, 2, Prod(3, 2), (Sum, 1, (Prod, 3, 2)).

    *   Supeqs of subeq 3 in (*) are: Prod(3, 2), (Sum, 1, (Prod, 3, 2)).

The most used property:

    *   There is a natural map between any primitive of an equation and every
        subequation:

        *   If the primitive is a symbol -> the subequation that is that
            symbol.
        *   If the primitive is an operator -> the block of which it is the
            leading operator.

Other properties and remarks:

    *   To be finite, an equation requires that some of the arguments of some
        of its operators are symbols.
    *   A subequation of an equation is always the whole equation or an
        argument of some operator of the equation.
    *   A subequation is always a symbol or a block.
    *   Subequations can can contain other subequations only "completely",
        meaning that, if subequation S contains subequation T, every element of
        T is an element of S.
    *   An argument cannot be the whole equation.
    *   One argument of an operator cannot be a subequation of other argument
        of that operator.
    *   Superequations always are referred to a subequation of certain
        equation.
    *   If a subequation is not the whole equation, it is guaranteed that at
        least one superequation of that subequation exists (the whole
        equation).
    *   A block always contains, at least, one operator (the leading operator).
    *   The leading operator is a privileged operator in a block, because:

        *   It and its arguments define completely the block.
        *   It is not part of the argument of any other operator of the block.
    *   A block is always a subequation.

Implementation of an equation in Visual Equation (fast approach):

    -   An equation is represented by a "list" and any equation primitive is an
        element of that list.
    -   Subequations are always sublists.

Some particularities of the implementation:

    -   Since an equation must always be valid, when an operator is introduced
        and the user has not yet specified one or more arguments, they are set
        to the special symbol NEWARG, which is represented by a small square
        when displayed.

    -   To give special properties to symbols zero-arguments operators are
        considered.

Implementation of an equation in Visual Equation (longer approach):

Visual Equation uses a flat list of primitives to represent an equation. The
format is equivalent to Polish Notation:

    *   An operator always precedes its arguments.

    -   If equation is a symbol, the list just includes that symbol.

    -   Else (the equation is a block), first element of the list is the
        leading operator of the equation. Then:

        -   If the first argument of the operator is a symbol, it is the next
            element of the list. Then, continue the list continue with the
            second argument.

        -   Else, the leading operator of the first argument is the next
            element of the list. Then, the list continue with the first
            argument of that operator.

Previous rule can be applied to successive arguments. Being a recursive
definition, it is a bit hard to explain it clearly with words. Probably it is
much easy understood with a example:

Here is equation (*) used above in Visual Equation implementation:

    [Sum, 1, Prod, 2, 3]

If you are having troubles understanding the format, maybe it can help to
read about Polish Notation somewhere (like Wikipedia).

Some consequences:

    *   Elements of the list representing an equation are (exclusively)
        "primitives" of the equation.
    *   Subequations of an equation are slices of a list. In python notation,
        if L is a list, a subequation of L can always be expressed as L[a:b],
        0 <= a < b <= len(L). Note that in python, L[b] is excluded in L[a:b].

Primitive types:

    *   Symbols are represented as strings (+) that match their LaTeX code.
    *   Operators are represented by instances of a class Op, which properties
        are:

        *   The number of arguments it has.
        *   A string indicating its LaTeX code and the position of its
            arguments.
        *   A string that is usually empty but can be used to indicate a
            special property of an operator. (++)

    (+)     The code is intended to work with operators with 0 arguments so
            they can be used to represent symbols which have some special
            property.
    (++)    In the future it may be generalized, e.g. by a list of tags.

Since equations must always be valid, when an operator is introduced and the
user has not yet specified one or more of its arguments, undefined arguments
are set to the special symbol NEWARG, which is represented by a small square
when displayed.

JUXT:

Visual Equation uses a relevant binary operator (which has 2 arguments) that we
call JUXT. It is used to display subequations contiguously, which typically
means that they are being multiplied, but it can have other uses or
interpretations such as to represent a number with more than one digit.

When designing Visual Equation, it was considered several times to use
different kind of JUXTs identified by its number of arguments, but at the end
it was always decided that JUXTs with 2 arguments are easier to manage. As a
consequence, a typical equation contains a lot of JUXTs. For example, to
display "abcd", the corresponding formal equation is

(JUXT, "a", (JUXT, "b", (JUXT, "c", "d")))

(We are not going to use always the formal definition of an eq for the examples
from now on, but that one would be [JUXT, "a", JUXT, "b", JUXT, "c", "d"].)

The way to combine JUXTs to obtain the same equation is not unique, but we
consider only ordered sequences of JUXTs as in the example above. That can be
summarized with this rule:

Rule 2:

    *   Every first argument of a JUXT is never a block leaded by a JUXT.

As a consequence:

    *   The second argument of a JUXT will be a block which leading operator
        is a JUXT (a DJUXT-block, as defined below) unless that second argument
        is the last subequation being joined.

A non valid equation due to Rule 2, but which would be right if instead of
JUXT some other binary operator would be used, is:

(JUXT, (JUXT, a, b), (JUXT, c, d))  <--- Not valid equation in Visual Equation.

There is an important fact about JUXTs: they are an artifact of no interest to
the user. The user may need to select individual elements, all of them or
its own combination of them, but not something attending to the arbitrary
internal nested structure of JUXTs.

Because JUXTs are tricky at the same time as useful, we define many other
concepts to shorten the writing:

Parent JUXTs and descendant JUXTs:

    -   A "parent JUXT" of an equation is a primitive of that equation which
        is a JUXT and the subequation it naturally defines is not an argument
        of another JUXT.

    -   A "descendant JUXT" is every JUXT operator in an equation which is not
        a parent JUXT.

    -   A "terminal JUXT" is a JUXT which second argument is not a block which
        leading operator is a JUXT.

Usubeqs, ublocks, uargs and JUXT-ublocks:

    Consider an equation E:

        -   An "user block" ("ublock") of E is a block of E such that.

            *   Its leading operator is not a descendant JUXT.

        -   A "JUXT-ublock" is an ublock of E which leading operator is a
            JUXT (necessarily a parent JUXT by definition of ublock).

        -   A "DJUXT-block is a block of E which leading operator is a
            descendant JUXT.

        -   An "user subequation" ("usubeq") of E is a subequation of E such
            that:

            *   It is a symbol of E, or
            *   It is an ublock of E.

        -   An "user superequation" ("usupeq") of subequation S in E is a
            superequation of S in E such that it is an ublock of E.

        -   An "user argument" ("uarg") of E is an argument of any operator of
            E different than JUXT.

Any first argument of a JUXT and also the second argument of a terminal JUXT
are first-class elements of its JUXT-ublock. The only difference between them
is their relative position but, from the user point of view, they are not
nested (even if they are in the formalism). That fact motivates the following
definition:

    -   "Citizens" of an equation are:

        *   The first argument of a JUXT, and
        *   The second argument of a terminal JUXT.

    -   A citizen always belongs to one and only one JUXT-ublock of the
        equation.

    -   Two or more citizens are "co-citizens" if they are citizens of the
        same JUXT-ublock.

Remark 1:

    *   A JUXT is a parent JUXT and a terminal JUXT of the same JUXT-ublock at
        the same time if, equivalently:

        *   Its JUXT-ublock does not have descendant JUXTs, or
        *   The subequation it naturally defines is not the argument of
            another JUXT.

Remark 2 (important one):

    *   There can be JUXTs in a JUXT-ublock that are not parent nor descendant
        JUXTs of that JUXT-ublock, but elements of a citizen of the
        JUXT-ublock. It is, a citizen can contains an independent JUXT-ublock
        itself.

For example, consider the following equation where FRAC is a binary operator

    (JUXT, (FRAC, "a", (JUXT, "b", "c"), (JUXT, "x", "y"))).

The equation is itself a JUXT-ublock with only one descendant JUXT. The first
citizen is the ublock (FRAC, "a", (JUXT, "b", "c")), the second citizen is the
symbol "x", and the third one is the symbol "y". Second argument of first
citizen is itself an different JUXT-ublock (JUXT, "b", "c") which only has
one JUXT, so it is at the same time the parent and terminal JUXT of the
JUXT-ublock.

Corollary:

Any subequation is one and only one of these:

    *   An usubeq, or
    *   A DJUXT-block.

An usubeq of an equation E is one and only one of these:

    *   E, or
    *   A citizen of a JUXT-ublock of E
        (argument of a JUXT that are not DJUXT-blocks), or
    *   An uarg of E
        (argument of a non-JUXT operator).

Selsubeqs:

Selsubeqs deal with the idea of subequation which is selectable by the user.
There are some reasons to avoid the user to select some of them:
    *   Some subequations are artifacts that have no meaning to the user (like
        JUXT-ublocks) or selecting them would be redundant (like groups,
        not commented here).
    *   There can be LaTeX limitations to represent the selector around the
        subequation.
    *   That subequation cannot be edited with the same flexibility than
        typical subequations because in some cases it has consequences that
        current code cannot manage.
    *   Others?
Note that what a selsubeq is is something that can change with time.

Equation metrics: Neighbours and superequation neighbours:

Two subequations of an equation are "neighbours" to each other if they are:

    *   The i-th and (i+1)-th citizens of the same JUXT-ublock, or
    *   The i-th and (i+1)-th uargs of the same (non-JUXT) operator.

A "superequation neighbour" of a subequation S in E, S different than E, is
a subequation of E such that:

    *   It is a neighbour of the smallest superequation of S.

Properties:

    *   Neighbours and superequation neighbours do not always exist.
"""
