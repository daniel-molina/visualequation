# The formalism behind Visual Equation

Version: 1.2

Here you can read most of definitions and rules used in Visual Equation code.
It is basically a bunch of definitions interconnected. It really looks like
a math book. There are also conclusions and theorems-like stuff, but (as usual)
they all have common sense, being definitions the key points. They allow to
classify and name the different elements needed by a this program. It allows to
be organised when writing code comments, deciding the name of identifiers and
writing documentation. However, final user manual will avoid many definitions 
used here to make the reading simpler.
 
This text is intended to be only as formal as needed to avoid ambiguity, but
relationships become complex and at the end this is the central reference for
any other documentation, so being self-contained and rigorous is important.

If you have corrections, good ideas or better names for definitions, feel free
to share them.

> **Disclaimer**: *Definitions are being changed and extended as it is
> required by new features, so it is possible that some of the code
> nomenclature is not up to date.*

> **Notes**:
>
> The main use of parenthesis throughout the text is to help the reader
> understand sentences and their scope. Information inside them should be
> always redundant for the meticulous reader, but probably a helping hand
> even for an ideal reader when pers knows that parenthesis are being used that
> way.
>
> Every number below is an integer. Expressions such as N > 0 refer to
> integers greater than 0.

## Formalism of an equation

### Introduction
Most of definitions included in other sections do not relay on the actual
implementation of an equation, so I found better to keep the formalism agnostic
with respect to the implementation. This documents mainly deals with the
formalism, but there is also a section on the implementation which relates
both.

### Meta-properties of equation elements
Equation are elements, probably consisting of other elements.

This formalism is designed to give elements certain, let us say,
meta-properties. As in formal logic, there is a limit of abstraction in which
it is not possible to define things without appealing intuitive human 
notions/usual language constructions such as membership, identity and so on. As
a consequence, these meta-definitions are more a statement of the words of the
English language that will be used to refer to certain ideas than well-posed
definitions.

#### Identity, equality an properties

*   Every element is **unique** and is allowed to have a unique *proper noun*.
    One element that is **not the same** element than other can never have the
    same proper noun.
*   There can be elements **equal** to others. If two elements are not equal,
    it is said that they are **different**.
*   Every element can be referred by a **property** it has, which is
    probably shared by other elements. When specifying an element by a
    property, nothing is said about any other properties that the element
    holds if those properties cannot be deduced from the original property.
    Definitions below will provide a **definiendum** to refer to an element
    satisfying certain properties. E.g.: an "equation" will have the property
    of being a subequation which has no superequations. There can be many
    equations, some of them with different properties, but all of them can be
    referred as "equations".

#### Identity and equation edition    

*   Element can **replace** other elements or being **inserted** elsewhere.
    They will continue being the same elements but in another **position**. If
    the second element does not replace a third element, it is **deleted** so
    it does not exist anymore.
*   If an element of an element is replaced, the second element will not be the
    same element anymore.

#### How to refer equation elements

Brackets in this section means that they will be replaced by a particular
expression in practice.

The statement **\[Certain element\] is a d** (e.g, "\[Certain element\] is a
juxt" or "\[Certain element\] is an equation") asserts that mentioned element
satisfies the **properties** stated in the **definiens** of **definiendum** d.

The expression **an element PN** gives the **proper noun** PN (noun PN will be 
different in each case) to an arbitrary and unspecified element without
restriction of the properties that the element must hold.

**A p PN \[...\]** gives the proper noun PN (noun PN will be different in
each case and usually will be formed with the initials of the particular d
of the sentence) to a generic and unspecified arbitrary element with (at
least) the properties stated in the definiens of p. Proper nouns must be
uppercase.

The statement **A d \[...\]** (e.g. "a subeq \[...\]" or "an image \[...\]") 
refers the rest of the sentence to an arbitrary element which satisfies the
definiens of p without giving the element a proper noun. It will be done when
it is not needed to refer to that (unique) element again.

#### Tuples

A **tuple** is used to group several elements together. It has a given
number of elements and all of this elements has as an ordinal associated
which **order** them as elements of the tuple. Tuples are not considered as 
elements of the theory, but a general tool used temporally in next section 
(particular tuples will be referred as blocks). However, tuples definitions
below will be extensively used.

In general, tuple elements will never be considered recursively unless
explicitly allowed for a **definiendum**. It is, an **element of a tuple** 
cannot be the tuple itself and, if an **element E of a tuple** T is also a 
tuple, an element of E will not be considered an element of T.

However, the following definitions can be used:

A (or the) **0-level element of a tuple** T is T.

A **L-level element of a tuple** T, L > 0, is a **(L-1)-level subequation of**
a tuple which is an element of T.

That is a recursive definition that finishes when N becomes 0 and the preceding
definition applies.

> **Property**: A N-level element of a tuple T is an element of T if, and only
> if, N is 1.

A **any-level element of a tuple** T is a N-element of T, N >= 0.

A **strict element of a tuple** T is a any-level element of T which is not T.

The **nesting level** (**level**) **of a N-level tuple of another tuple** is
the (non-negative) value N. 

The **maximum nesting level** (**max level**) M of a tuple T is the integer M
such that no (M+1)-level elements of T exist.

### Elements of an equation
There are four main types of elements:

*   Symbols
*   Operators
*   Arguments
*   Blocks

If one element is of one main type, it cannot be of any other main type.

**Symbols** are elements that make sense by themselves. For example, 
digits or Greek letters.

**Operators** (**ops**) are elements which require other elements in certain
order to make sense.

> **Example**:
>
> Operators can be used to represent fractions. Fraction can be seen as
> operators because they need an element acting as numerator of the fraction
> and another element acting as the denominator. The order of requiring
> elements is important to distinguish which is the role of each one.

**Blocks** are tuples with N+1 elements, N > 0, satisfying:

*   The leading element is an operator which needs N parameters. It is called
    the **leading operator** (**lop**) of the block.
*   The rest of elements are the elements needed by the leading operator. The
    ordinal of each of this elements in the block is the same than the ordinal
    which identifies its role in the associated leading operator. ("Needed
    elements" by an operator are formalised below.)

> **Note**: A particular type of block, *juxt-blocks*, will be used to
> represent several subequations contiguously (e.g., digits of a number,
> supposing each digit is represented by a subequation). They are described in
> another section.

A **x-block** is a block which has x as leading operator. If x is a proper
noun, it refers to the (unique) block which has x as lop.

**lop-B** is the leading operator of a block B.

A **parameter** (**par** or **param**) **of an operator** is one of the
elements required by the operator. A parameter must be a symbol or a block.

A **lop-B-par** is a parameter of operator lop-B.

A **OP-par** is a generic par of a operator OP not associated to a particular
block.

**Arguments** are abstract elements that are not represented when a equation is
written down. They can be seen as the placeholders of the parameters needed by
an operator. An argument is always associated to an ordinal and to operators
with certain properties like the number of arguments it has and certain role 
(e.g.: the first argument of a operator representing a square root). It can be 
argued that arguments can be avoided in this formalism and just talk in terms 
of properties of an operator. Due to its central role, it has been decided to 
consider them as elements too.
 
The number of arguments of an operator OP is the **arity** of OP.

It is said that a parameter is **associated to** an argument of an operator.

A **lop-B-arg** is an argument of operator lop-B.

A **N-arg(s) operator** is an operator with N argument(s). A **unary op** is a
1-arg op. A **binary op** is an 2-args op. A **ternary** op is a 3-args op.

The **ordinal of the argument of a N-arg(s) operator**, N > 0, indicates
univocally an argument of an operator. Arguments of operator OP will be
referred as "the first argument of OP", "the second argument of OP", and so on.

The **ordinal of a parameter** is the ordinal of its associated argument.

An **OP-arg** is a generic arg of a operator OP not associated to a particular
block.

A **primitive element** (**primitive**) is a symbol or an operator.  

A **subequation** (**subeq**) is a symbol or a block.

An **equation** (**eq**) is a subequation which is not a parameter.

> **Properties:**:
>
>1. A subequation is not always an equation but an equation is always a
> subequation.


> **Note**: *Whenever possible the term subequation will be preferred in the
> following definitions because it is more general. However, in the code some
> concepts defined here may be usually associated to equations instead of
> subeqs.*

### Basic subequation definitions

> **Properties**:
>
>1. A **any-level primitive of a subequation S** is:
>
>*  If S is a symbol, S.
>*  If S is a block, the leading operator of S or a **any-level primitive of**
>   a lop-S-par.
>
>1. A (or the) **0-level subequation of another subequation S** is S.
>
>1. A **N-level subequation of another subequation S**, N > 0, is:
>
>*   If S is a symbol, it does not exist.
>*   If S is a block, a **(N-1)-level subequation of a** S-par.

A **subequation of another subequation S** is a A **any-level subequation of 
S**.

> **Note**: Previous definition relaxes the expression "element of a tuple"
> specified above for elements of a tuple if elements are any-level
> subequations of the tuple.
>
> The "any-level" is still mandatory for elements which are not subequations.

> **Properties**:
>
>1. There always exist at least a subeq of a subequation S (S itself).
>
>1. There can be more than one N-level subeqs of a subequation S.

> **Example**:
>
> Consider the following equation:
>
>    `(Sum, 1, (Prod, 3, 2))`
>
> All its subequations are:
>
>    level 0: `(Sum, 1, (Prod, 3, 2))`
>    level 1: `1`
>    level 1: `(Prod, 3, 2)`
>    level 2: `3`
>    level 2: `2`
>
> Note that in functional notation, equation of the example would be
>
> `Sum(1, Prod(3, 2))`
>
> or in a more common notation
>
> `1 + (3 * 2)`


A subequation S **contains** or **has** a subequation SUB if SUB is a subeq
of S.

> **Property** (probably the most used in visual equation):
>
> There is a natural map between every any-level primitive of a subequation S
> and every subequation SB of S:
>
>*  For a any-level symbol SY of S, SY.
>*  For a any-level operator OP of S, the block B which has OP as lop-B.

A **N-level superequation SP of a subequation SB in a subequation S**, SB being
a subequation of S and N > 0, is a subeq such that:

*   SP is a subequation of S, and
*   SB is a N-level subequation of SP.

The **nesting level**, or simply the **level**, of a N-level superequation of
a subequation in another subequation is the (strictly positive) value N.

A **superquation** (**supeq**) of a subeq SB in a subequation S is a N-level
superquation of SB in S for any N > 0.

A subequation SB **has a superequation** SP in subequation S if SP is a
superequation of SB in S.

> **Note**: *When it is said **A supeq of SB**, it is understood that it refers
> to a supeq of SB in equation to which SB belongs (the biggest scenario). 
> Equivalently, **SB has a supeq** means that SB has a supeq in equation to
> which SB belongs.*

> **Note**:
>
> Intentionally, **0-level superequations** are not defined.
> Informally, that means:
>
> `subeq of S <= S`
> `supeq of S (in P) > S`

> **Properties**:
>
>1. At least, one supeq of SB in S exists if SB is not S (that supeq is S).
>1. A N-level supeq of SB in S does not exist or it is unique.
>1. If two subeqs have the same level with respect to a common supeq, then they
>   have the same level with respect to any common supeq.

>  **Example:**
>
>These are the supeqs of subequation `3` of previous example:
>
>*  level 1:    `(Prod, 3, 2)`
>*  level 2:    `(Sum, 1, (Prod, 3, 2))`

> **Properties and remarks**:
>
>1. To be finite, an equation requires that some of the elements of some of
>   its blocks are symbols.
>1. A subeq of an equation is always the whole equation, the parameter of some
>   operator of the equation or an element of a juxt-block.
>1. Subequations contain other subequations only **completely**, meaning that, 
>   if subequation S contains subequation T, every any-level element of T is an
>   any-level element of S. In other words, subeqs do not partially overlap.
>1. A parameter of a subequation S cannot be S (nor equal since only finite
>   subequations are considered).
>1. One parameter of an operator OP cannot be a subequation of other
>   parameter of OP.
>1. A subequation does not need another subequation to make sense, even if the 
>   concept of subeq SB of a subeq S is defined and in that case SB requires S.
>1. Superequations always are referred to a subequation SB in certain
>   subequation S; when S is not specified, the whole equation E to which
>   SB belongs is supposed to have that role.
>1. A block B always contains, at least, one operator (the leading operator,
>   lop-B).
>1. The leading operator of a block B is a privileged any-level operator of B
>   because:
>
>   *   lop-B and its parameters define B completely.
>   *   It is not an any-level op of any any-level parameter of B.

## Selection rules

A subequation that can be selected means, in the implementation, that they
can be highlighted or the cursor/caret can be placed to the left of the subeq.

In the current implementation, only a subset of all this machinery is currently
being used in VE. In fact, the only current reason to use selection rules is to
avoid selecting contiguous subequations redundantly.

In general, there are many reasons to avoid the user to select some
subequations:

1.  They can be artifacts that have no meaning to the user.
1.  It can be redundant to select certain blocks.
1.  The user may ask explicitly not to select a subeq.
1.  There can be LaTeX limitations to select a subequation.
1.  That subequation cannot be edited with the same flexibility than
    typical subequations because that has consequences that current code
    cannot manage.
1.  Other cases?

The next definitions specify the terminology used to prohibit certain
subequations of an equation to be selected.

> **Note**:
> 
> It can be tricky to correctly use the language to indicate that an element
> has a property because it is an element of another element but not by itself.
> In particular, an element *equal* to that one may not have that property, or
> the element itself may not have that property after an equation edition (if
> the element survives).
>
> The chosen solution is to define selectivity as a property of a subequation 
> *of an equation* because when the equation is fixed selectivity rules can be
> consistent. It could be helpful to the reader to think that being
> selectable is a property of subequations "in" an equation to emphasize the
> dependence on the equation.

### The user property

A symbol, operator or argument can hold the **user property**.

A block B has the user property if lop-B has the user property.

A subequation is **potentially selectable** if it has the user property.

**Rule**: Every symbol holds the user property.

Depending on its type, an element with the user property is referred as:

*   User operator (uop)
*   User arguments (uarg)
*   User block (ublock)

"User symbol" is avoided due to previous rule.

Any other term preceded by "user" and their abbreviations beginning with "u" 
indicates that, in addition, they are user elements. In particular, they are
considered usubeqs, usupeqs, X-ublocks, upars, lop-X-upars.

> **Examples**:
>
> When it is considered a X-ublock, it is supposed that it is a usubeq. As a
> consequence, X is necessarily a uop since ublocks can only be uop-blocks.
>
> Let X be a unique op. Then, X-block is the block defined by X, which is
> unique since X is unique. If we knew that X is a uop, we can write
> X-ublock. However, if X was not really a uop, writing X-ublock would be a
> nonsense or it may be possible to say that element X-ublock does not exist
> even if X exists. Since the intention of this formalism is to be helpful,
> those cases are of no interest.

> **Remarks**:
>
>1. B is a ublock if, and only if, lop-B is a uop.
>1. Strict subequations of a block B can be usubeqs or not, regardless of
>   whether B is a ublock.

### Definition of a selectable subequation

> **Note**: This section includes some rules that will allow that at least one
> subeq of an equation will be selectable.

A **selectable subequation** (**selsubeq**) of an equation E is a subequation
SS of E such that:
 
*   SS is a usubeq, and
*   SS has no usupeq which is a subeq of a parameter associated to a non-user
    arg.

> **Properties**:
>
>1. The whole equation is selectable if, and only of, it is a usubeq.
>1. A selectable subequation is a usubeq. The opposite is not (always) true.
>1. If a usubeq US of E is not selectable, no subeq of US is selectable.
>1. Let US be a usubeq of equation E. If every usupeq of US different than E is
>   the param of uarg, US is selectable.
>1. Let US be a usubeq of equation E which has at least one supeq which is
>   the parameter of a non-user arg. Let P be the N-level supeq of S which is
>   a parameter of a non-user arg with bigger N. Let U be the N-level usubeq
>   of P with lower N. Then: 1) U is selectable. 2) usupeqs of U are selectable
>   and they and their supeqs are not parameters of non-user args. 3) Strict
>   subeqs of U are not selectable. 4) US is selectable if, and only if, US
>   is U.

> **Note**:
>
> Previous properties are much more simple by using the definitions below.

A **generalized symbol** (**gsymb**) is a symbol or a parameter associated to a
non-user argument.

> **Note**: Currently there are no user arguments in VE, probably for good, so
> every gsymb is a symbol in VE. However, this formalism allows them. (They
> may be used in the future and the theory has been already written).

### User subequations definitions and rules

A **0-ulevel usubeq of a subeq S** is:
 
*   If S is a usubeq, S.
*   Elif S is a symbol, it does not exist.
*   Else (S is a block), a **0-ulevel** usubeq of a S-par**.

A **N-ulevel usubeq of a subeq S**, N > 0, is:

*   If S is a symbol, it does not exist.
*   Elif S is a ublock, a **(N-1)-ulevel usubeq of a S-par**.
*   Else (S is a block), a **N-ulevel usubeq of a S-par**.

That is a recursive definition that finishes when N becomes 0 and the preceding
definition applies.

The **user nesting level** (**ulevel**) of a N-ulevel usubeq of a subeq is the
(non-negative) value N.

> **Property**:
>
> If two usubeqs has the same ulevel with respect to a common supeq, then they
> have the same ulevel with respect to any common supeq.

> **Remark**:
>
> The N-level usubeq of S is the N-level subeq of S, which in addition is
> asserted to be a usubeq (see example above for a similar situation). In
> general, supposing that that usubeq has sense, is different than the N-ulevel
> usubeq of S.

The **N-ulevel usupeq** USP of a subequation SB in a subequation S and
other related terms can be defined as expected.

### Faithful subequations and operators

A **faithful subequation** is a subequation that has one, and only one,
0-ulevel usubeq.

The **user representative** (**urepr**) of a faithful subequation FS is the
0-ulevel usubeq of FS.

> Properties:
>
>1. Every symbol is faithful.
>1. A usubeq is always a faithful subeq.
>1. The urepr of a usubeq US is US.
>1. A faithful subeq can have any number of N-ulevel usubeqs for N > 0,
>   including not having anyone.

A **faithful operator** is an operator such that:

*   It is a uop, or
*   It has one arg.

A **filter** is a faithful op which is not a user op and has one user arg.

> **Note**: Filters are currently not used in VE.

> **Properties**:
>
>1. If FS is a faithful subeq and FS is the parameter of an arg of a faithful
>   op FO, the FO-block is faithful.
>1. Let FNUOP be a faithful non-user op. A FNUOP-block is a faithful subeq if,
>   and only if, the only FNUOP-par is a faithful subeq.
>1. If NFO is a non-faithful op, a NFO-par can be faithful or non-faithful.

## Contiguous subequations

Visual Equation uses some operators named **juxts** to display contiguous or 
juxtaposed subequations. That typically means that subequations are being
multiplied, but that can have other uses or interpretations such as to 
represent a number with more than one digit. To connect several subequations 
together, a juxt with the required number of arguments is used. Juxts
arguments holds the user property. TODO: Use the prevalent definition structure
 for definition of juxts.

A **juxted** is a parameter of a juxt.

> **Example**:
>
> Consider that JUXTN, N in the noun being a positive integer, is a juxt with N
> arguments.
>
> To display A B C D, being all of them symbols, the corresponding equation
> can be
>
>   `(JUXT4, A, B, C, D)`

> **Note**: In current VE implementation, non-last juxteds cannot be pointed to
> the right with the cursor. Rest of subeqs can.

Two juxteds are **cojuxteds** if they are juxteds of the same juxt-block.

> **Note**: In VE, there are two kind of juxts: Permanent juxts (pjuxts) and
> temporal juxts (tjuxts). Pjuxts do not hold the user property and tjuxts
> hold it.
>
> Pjuxts are the default juxts so only their juxteds are selectable.
>
> Tjuxts are created temporally if several juxteds need to be selected together
> by user request. If a pjuxt-block needs to be highlighted as a whole, it is
> replaced temporally by a tjuxt-block. A tjuxt-block is always the current
> highlighted selection. When the selection changes, the tjuxt-block is
> deleted or replaced.
>
> Juxts are edited dynamically without being noticeable by the user.

### Nested juxteds (unuseful in current implementation of VE)

A **nested juxted** is a juxted which juxt-block is itself a juxted.

Two juxteds J1 and J2 are **quasi-cojuxteds** if:

*   J2 is a juxted of a N-level supeq of J1, and
*   Every M-level supeq of J1 for 1 <= M <= N is a juxt-block.

> **Properties**:
>*  Two cojuxteds are quasi-cojuxteds.
>*  If two quasi-cojuxteds are not cojuxteds, at least one of them is a nested
>   juxted.

Current implementation of a juxt in Visual Equation uses the same operator for
every juxt with the same characteristics independently of the number of
juxteds it contains. In fact, juxts are the only operators implemented in VE
with a variable number of arguments.

A **soft group** is a JUXT-block which is a juxted of another JUXT-block.

> **Example**:
>
> If it is intentional that some contiguous juxtaposed subequations are
> grouped as a whole, an structure like this would be used:
>
>   `(JUXT2, (JUXT2, A, B), C)`
>
> If A, B and C are user symbols, the following are the selection
> possibilities of the previous equation:
>
>   `(A B C)`
>   `(A B) C`
>   `(A) B C`
>   `A (B) C`
>   `A B (C)`
>
> Another example with a juxt-block inside a juxt-block.
>
>    `(JUXT2, (FRAC, A, (JUXT2, B, C)), X)`
>
> The equation is itself a juxt-ublock with two juxteds. The first juxted is
> the ublock `(FRAC, A, (JUXT2, B, C))`, and the second juxted is the symbol
> `X`. Second argument of the first juxted is itself another juxt-ublock with 
> two juxteds `(JUXT2, B, C)`.

## Equation metrics

> **Note**: Next definitions refer to an equation because selectivity property
> is used, which require an equation to be defined.

A **N-ulevel peer** of an equation E, N > 0, is a subeq P of US such that:

*   P is a N-ulevel usubeq of E, and
*   P is selectable.

A **N-ulevel aide** of an equation E, N >= 0, is a subeq AI of US such that:

*   AI is a M-ulevel peer of E for some 0 < M < N, and
*   AI has no strict subeqs which are selectable.

A **N-ulevel mate** of an equation E, N >= 0, is a subeq MA of S such that:

*   MA is a N-ulevel peer of E, or
*   MA is a N-ulevel aide of E.

Two subeqs are **peers of each other** if they are not the same subeq and they
are N-ulevel peers of the same equation for some N.

Two subeqs are **N-mates of each other** if they are not the same subeq and
they are N-ulevel mates of the same equation.

The **ulevel diff** of two N-mates of each other of an equation E is a 
non-negative number uld defined as:
 
*   Let one of the mates be a M1-ulevel peer of E, and
*   Let the other mate be a M2-ulevel peer of E.

Then, uld is the absolute value of M1 minus M2 (uld=abs(M1-M2)).

The **implication level** (**ilevel**) of a N-mate of E which is a M-peer of E,
is a non-negative number equal to N minus M.

> **Remark**:
>
> If an equation is edited, two peers/N-mates of each other of the original eq
> can become non-peers/non-N-mates of the new equation.

> **Properties**:
>
>1. A N-ulevel peer is not a M-ulevel peer for M different than N.
>1. A N-ulevel aide is a M-ulevel aide for M bigger than N.
>1. The ilevel of an aide is always positive.
>1. A N-ulevel peer P is a M-ulevel mate for M bigger than N if P is a symbol
>   or the representative of the parameter of a non-user arg.
>1. The ulevel-diff of two N-mates does not depend on N.
>1. Two N-mates of E are peers of each other if, and only if, their ulevel diff
>   is 0.
>1. Two N-mates of each other will be M-mates of each other for every M such
>   that M >= N - min{il1, il2}, being il1 and il2 the ilevel of the N-mates.

The **mate to the left** of another mate MA is a subeq LMA that results of the
following algorithm (it supposes that the only operator with a non-user arg is
GOP):

1.  Set S to MA.
    Set N to 0.
2.  If S has no supeq, LMA does not exist (**END**).
3.  Set ORD to the ordinal of the argument of which S is parameter.
    Set S to the supeq of S.
    If S is a usubeq, N++.
4.  If ORD == 1, go to step 2.
5.  ORD--.
6.  If S is a usubeq, N--.
    Set S to the parameter ORD of S.
    If N == 0 or S is a GOP, LMA is the representative of S (**END**).
7.  Set ORD to arity(lop-S).
    Go to step 6.

The **mate to the right** of another mate MA is a subeq RMA that results of the
following algorithm (it supposes that the only operator with a non-user arg is
GOP):

1.  Set S to MA.
    Set N to 0.
2.  If S has no supeq, RMA does not exist (**END**).
3.  Set ORD to the ordinal of the argument of which S is parameter.
    Set S to the supeq of S.
    If S is a usubeq, N++.
4.  If ORD == arity(lop-S), go to step 2.
5.  ORD++.
6.  If S is a usubeq, N--.
    Set S to the parameter ORD of S.
    If N == 0, S is a GOP or S is a symbol, RMA is the urepr of S (**END**).
7.  Set ORD to 1.
    Go to step 6.

## Implementation of an equation in Visual Equation

*   Symbols are 1-elem lists (the surrounding list is needed to keep
    references).
*   Operators are objects with some properties.
*   Blocks are lists.
*   Arguments are materialized as properties of their operators.

Because the interesting part of represented symbols is what is contained inside
the 1-elem list, the containing element is called a **pseudosymbol** and, in
the source code, they are named as the proper noun of its symbol in the source 
code.

Since an equation must always be valid, when an operator is introduced and the 
user has not yet specified one or more of its parameters, they are set to the
special symbol **PVOID**.

To give special properties to symbols, pseudosymbols are objects similar to
operators. In fact, operator class is derived from pseudosymbol class.

The class used for **pseudosymbols** has the following properties:

*   A string holding the **name** of the pseudosymbol. Must be lowercase.
    When they are represented, uppercase is used. Lowercase is preferred 
    because it has some advantages, e.g., for filenames in a random OS.
*   A string indicating its **LaTeX code**.
*   Some properties such as color, font style, etc..

To debug the code and write examples, strings are also allowed instead of
pseudosymbols, being its content its latex code or something else if it does
not need to be displayed.

The class used for **operators** has the following properties:

*   A string holding the **name** of the operator. Must be lowercase. When they
    are represented, uppercase is used. 
*   The **number of arguments** it has.
*   A string indicating its **LaTeX code** and the position of its parameters.
*   Some properties such as color, font style, selectivity of subequations,
    etc..
*   Some methods that may help, e.g., navigate with cursor keys through
    the equation.

> **Example**:
>
> Here is the equation of previous examples using the implemented format,
> using a string for pseudosymbols
>
> `[SUM, ["1"], [PROD, ["2"], ["3"]]]`
>
> where lops are supposed to be defined, for example as
>
>   `SUM = Op("sum", "{0}+{1}", 2); PROD = Op("prod", "{0}*{1}", 2)`
>
> Note that SUM and PROD are useful binary ops for examples because they are
> common operators in the real world, but in practice they are implemented
> as symbols in visual equation.
>
> First equation is shorter than the following valid code which specify the
> symbols in the standard way
>
> `[SUM, [Op("one", "1")], [PROD, [Op("two", "2")], [Op("three", "3")]]]`
>
> If symbols (or more precisely, elems contained in 1-elem lists representing
> symbols) have been previously defined similarly to SUM and PROD
>
> `[SUM, [ONE], [PROD, [TWO], [THREE]]]`

### Building rules

1.  A PVOID cannot be a juxted.
1.  A tjuxt-block must be always selected and highlighted.
1.  When selection changes from a tjuxt-block TJB, TJB is transformed into a
    pjuxt-block if it is not a juxted. If TJB is a juxted, their juxteds are
    integrated as juxted of the pjuxt-block of which TJB is juxted.

## Changelog
### 1.2
*   juxts now explicitly store the current number of arguments they have.
*   Discarding "common noun" terminology. It was strange and now it has no
    relevance because:
*   It is allowed that operators and symbols can have additional properties
    not mentioned in their definitions. That avoids the use of previously
    named "filters", e.g., for color, font style... 
*   Removed support in VE for user arguments, but still present in this
    formalism. In any case, now there is no need of a specific group op
    (previously GOP). That behaviour can be reduced to a property that any
    leading operator can have.
*   Subequations now are selected or pointed. To be selected is synonymous of
    being highlighted. Being pointed is having the cursor to the left or right.

### ~ 1.1 (never numbered)
*   Equations as nested lists.
*   Operators with the same common name are equal.
*   Distinguishing between parameters and arguments.
*   Formalised the notion of selectivity of a subeq.
*   Several ideas to formalize contiguous subeqs
    (juxt-ublocks, parent juxts, descendant juxts, terminal juxts)
*   Discarded complex operators allowing random arguments not being selectable.


### Before long_rewriting branch
*   Equations as plain lists, not nested lists.
*   Index was just an integer.
*   Difficult operations required to guess the bounds of a subeq.
