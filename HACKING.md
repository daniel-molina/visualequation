# The formalism behind Visual Equation

Below you can read most of definitions and rules used in Visual Equation code.
There are a lot of definitions, but I hope they are intuitive. It is intended
to be only as rigorous as needed to avoid ambiguity, but relationships become
complex and some technicalities must be used.

> **Disclaimer**: *Definitions have being changed and extended as it has been
> required by new features, it is possible that some of the code notation has
> not been updated yet.*

> **Note**:
>
> The main use of parenthesis throughout the text is to help the reader
> understand sentences and their scope. Information inside parenthesis should
> be always redundant for the meticulous reader.

## Formalism of an equation

### Introduction
Most of definitions included in other sections do not relay on the actual
implementation of an equation, so I found better to keep the formalism agnostic
with respect to the implementation.

### Meta-properties of equation elements
An equation is an element probably consisting of other elements.

This formalism is build to give elements the following "meta-properties":

#### Identity, equality an properties

*   Every element is **unique** and is allowed to have a unique *proper noun*.
    One element that is **not the same** element than other must have a
    different proper noun.
*   There can be elements **equal** to others and they are allowed to have a
    *common noun* that is shared between them. If two elements are not equal,
    it is said that they are **different**.
*   Every element can be referred by a **property** it has. That property is
    probably shared by other elements. When specifying an element by its
    properties, nothing is said about any other properties that the element
    has if those properties cannot be deduced from the original property.
    Definitions will give a **definiendum** to refer to an element satisfying
    certain properties.

#### Identity and equation edition    

*   An element can **replace** other element. In that case, if the first
    element existed, it continue being the same but in another **position**. If
    the second element does not replace a third element, it is **deleted** so
    it does not exist anymore.
*   If an element of an element is replaced, the second element is not the same
    element anymore.

#### How to refer equation elements

The expression **A d** or **is a d** refers to an arbitrary element which
satisfies the **definiens** of a **definiendum** d or asserts that an element
satisfies the **properties** stated in the **definiens** of **definiendum** d.

Definiendums of elements with certain properties which include elements that
are different will be lowercase.

The expression **A CN** refers to an arbitrary element with **common name** CN.
Common names will be uppercase.

The expression **A p PN** gives the proper noun PN to an arbitrary element with
the common **properties** to elements called p. Proper nouns will be uppercase.

The expression **A CN PN** gives the proper noun PN to an arbitrary element
with common name CN.

The expression **an element PN** gives the **proper noun** PN to an arbitrary 
element.

### Elements of an equation
There are four main types of elements:

*   Symbols
*   Operators
*   Arguments
*   Blocks

**Symbols** are elements that make sense by themselves. For example, digits or 
Greek letters.

**Operators** (**ops**) are elements which require other elements in certain
order to make sense. Those elements are known as **parameters**. A parameter
is a symbol or a block.

A **OP-par** is a parameter of operator OP.

> **Example**:
>
> Operator FRAC is the operator used to represent fractions. It is an operator
> because it needs an element acting as numerator of the fraction and another
> element acting as the denominator. The order is important to distinguish
> which parameter is each one.

**Arguments** are abstract elements that are not represented when a equation is
written down. They can be seen as the placeholders of the parameters needed by
an operator. An argument is always associated to an operator and operators
that are equal have equal arguments and in the same order. As a consequence, it
can be argued that they could be avoided and use instead properties of an
operator. Due to its central role, it was decided to consider them elements.
 
The number of arguments of an operator OP is the **arity** of OP.

It is said that a parameter is **associated to** an argument of an operator.

A **N-arg(s) operator** is an operator with N arguments. A **unary op** is a
1-arg op. A **binary** op is an 2-args op. A **ternary** op is a 3-args op.

The **ordinal of the argument of a N-arg(s) operator** is a positive integer
(from 1 to N) that indicates univocally an argument of an operator. Arguments
of operator OP will be referred as "the first argument of OP", "the second
argument of OP", and so on.

The **ordinal of a parameter** is the ordinal of its associated argument.

A **OP-arg** is an argument of operator OP.

**Blocks** are tuples with N+1 elements, N > 0, composed by:

*   The leading element, which is an operator of arity N. It is called the
    **leading operator** (**lop**) of the block.
*   The rest of elements are the parameters of the leading operator in order
    indicated by the ordinal of the argument associated to them.

A **X-block** is the block which has X as leading operator.

**lop-B** is the leading operator of a block B.

A **lop-B-arg** is an argument of operator lop-B.

A **lop-B-par** is a parameter of operator lop-B.

A **primitive element** or **primitive** is a symbol or an operator.  

A **subequation** (**subeq**) is a symbol or a block.

An **equation** (**eq**) is a subequation which is not the parameter of an
operator.

> **Property**:
>
> A subequation is not always an equation but an equation is always a
> subequation.

> **Note**: *Whenever possible the term subequation will be preferred in the
> following definitions. However, in the code some concepts defined will be 
> usually referred to equations instead of subeqs.*

### Basic subequation definitions
A **0-level subequation of another subequation S** is S.

A **N-level subequation of another subequation S**, N being a positive
integer, is:

*   If S is a symbol, it does not exist.
*   If S is a block B, a **(N-1)-level subequation of a B-par**.

That is a recursive definition that finishes when N becomes 0 and the preceding
definition applies.

The **nesting level**, or simply the **level**, of a N-level subequation of
another subequation is the (non-negative) value N.

A **strict subequation** of S is a subequation of S that is not S.

The **maximum nesting level M** (**max nlevel**) of a subequation S is the
the integer M such that no (M+1)-level subequations of S exist.

A **subequation of another subequation S** is a N-level subeq of any
non-negative value of N (from 0 to the max nlevel of S).

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

A **primitive** of a subequation S is:

*   If S is a symbol, S.
*   If S is a block, the leading operator of S or a **primitive** of a S-par.

A **symbol of a subequation S** is a primitive of S which is a symbol.

An **operator of a subequation S** is a primitive of S which is an op.

A subequation S **contains** or **has** a subequation SUB if SUB is a subeq
of S.

> **Property** (probably the most used in visual equation):
>
> There is a natural map between any primitive of a subequation S and every
> subequation SB of S:
>
>*  If the primitive is a symbol SY -> SY.
>*  If the primitive is an operator OP -> the block of which OP is the leading 
>   operator (the OP-block).

A **N-level superquation** SP of a subequation SB in a subequation S, SB being
a subequation of S and N a positive integer, is a subeq such that:

*   It is a subequation of S, and
*   SB is a N-level subequation of it.

The **nesting level**, or simply the **level**, of a N-level superequation of
a subequation in another subequation is the (positive) value N.

A **superquation** (**supeq**) of a subeq SB in a subequation S is a N-level
 superquation of SB in S for any positive value of N.

A subequation SB **has a superequation** SP in subequation S if SP is a
superquation of SB in S.

> **Note**: *When it is said **A supeq of SB**, it is understood that it refers
> to a supeq of SB in equation to which SB belongs (the biggest scenario). 
> Equivalently, **SB has a supeq** means that SB has a supeq in equation to
> which SB belongs.*

> **Note**:
>
> Intentionally, **0-level superequations** are not defined.
> Informally:
>
> `subeq of S <= S`
> `supeq of S (in P) > S`




> **Properties**:
>
>1. At least, one supeq of SB in S exists if SB is not S (that supeq is S).
>1. A N-level supeq of SB in S does not exist or it is unique.
>1. If two subeqs has the same level with respect to a common supeq, then they
>   have the same level with respect to any common supeq.

>  **Example:**
>
>These are the supeqs of subequation `3` of previous example:
>
>*  level 1:    `(Prod, 3, 2)`
>*  level 2:    `(Sum, 1, (Prod, 3, 2))`

> **Properties and remarks**:
>
>1. To be finite, an equation requires that some of the parameters of some of
>   its operators are symbols.
>1. A subeq of an equation is always the whole equation or a parameter of some
>   operator of the equation.
>1. Subequations contain other subequations only **completely**, meaning that, 
>   if subequation S contains subequation T, every element of T is an element 
>   of S. In other words, they do not partially overlap.
>1. An parameter of a subequation S cannot be S (nor equal since only finite
>   subequations are considered).
>1. One parameter of an operator OP cannot be a subequation of other
>   parameter of OP.
>1. A subequation do not need another subequation to make sense, even if the 
>   concept of subeq SB of a subeq S is defined and in that case SB requires S.
>1. Superequations always are referred to a subequation SB in certain
>   subequation S, when it is not specified, the whole equation E to which
>   S belongs is supposed to have that role.
>1. A block always contains, at least, one operator (the leading operator).
>1. The leading operator is a privileged operator in a block because:
>
>   *   It and its parameters define completely the block.
>   *   It is not part of the parameter of any other operator of the block.

## Implementation of an equation in Visual Equation
 
### Basic ideas

*   Symbols are 1-elem lists containing a string (list is needed to keep
    references to it).
*   Operators are objects with some properties.
*   Blocks are lists which first element is the lop and the rest are lop-pars.
*   Arguments are not represented.

Since an equation must always be valid, when an operator is introduced and the 
user has not yet specified one or more of its parameters, they are set to the
special symbol *VOID*, which is represented by a small square when displayed.

To give special properties to symbols, 0-args operators are considered in the
implementation, but they are considered symbols in this formalism.

> **Example**:
>
> Here is equation of previous examples in the implementation format:
>
> `[Sum, ["1"], [Prod, ["2"], ["3"]]]`


The **string** of a symbol is its LaTeX code.

The **class** of the object of an operator has the following properties:

*   The number of arguments it has.
*   A string indicating its LaTeX code and the position of its arguments.
*   A string that is usually empty but can be used to indicate a special 
    property of an operator. (++)

> **Note**:
>
> In the future an operator may include a list of tags.

## Building rules

Any subequation can be the parameter of any operator.

## Selection rules

There are reasons to avoid the user to select some subequations:

1.  They can be artifacts that have no meaning to the user.
1.  It can be redundant to select certain blocks.
1.  The user can ask explicitly not to select a subeq.
1.  There can be LaTeX limitations to select a subequation.
1.  That subequation cannot be edited with the same flexibility than
    typical subequations because that has consequences that current code
    cannot manage.
1.  Other cases?

The following definitions specify the terminology used to prohibit certain
subequations of an equation to be selected.

> **Note**:
> 
> It can be tricky to correctly use the language to indicate that an element
> has a property because it is an element of another element but no by itself
> since an element *equal* to that one may not have that property or the
> element itself may not have that property after an equation edition in which
> the element survives.
>
> The chosen solution is to define selectivity as a property of a subequation 
> *of an equation* because when the equation is fixed selectivity rules can be
> consistent. It could be helpful to reader to think that being selectable is
> a property of subequations "in" an equation to emphasize the dependence on
> the equation.

### The user property

An element which is not a block have intrinsically the **user property** or
not. Blocks inherit this property from its lop.

> **Note*:
>
> The user property has only the same meaning for symbols and blocks.

Depending on its type, an elements with the user property is referred as:

*   User symbol
*   User operator (uop)
*   User arguments (uarg)
*   User block (ublock)

Any term previously defined term preceded by "user" and their abbreviations
beginning with "u" indicates that in addition they are user elements. In
particular, they are considered usubeqs, usupeqs, X-ublocks, upars, lop-X
-upars.

> **Examples**:
>
> When it is considered a X-ublock, it is supposed that it is a usubeq. As a
> consequence, X is necessarily a uop since ublocks can only be uop-blocks.
>
> Let X be a particular op. Then, X-block is the block defined by X, which is
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
*   SS has no usupeq which is a subeq of a parameter of a non-user arg.

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
> Those properties are much more simple by using the definitions below.

**GOP** is the common noun of they only (in an equality sense) operator with a
non-user argument. Characteristics of GOP:
 
*   It is a unary operator, and
*   It is a non-user op, and
*   Its argument is a non-user arg

### User subequations definitions and rules

A **0-ulevel usubeq of a subeq S** is:
 
*   If S is a usubeq, S.
*   Elif S is a symbol, it does not exist. (Today every symbol is usubeq)
*   Else (S is a block), a **0-ulevel** usubeq of a S-par**.

A **N-ulevel usubeq of a subeq S**, N being a positive integer, is:

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

### Faithful subequations and operators

A **faithful subequation** is a subequation that has one, and only one,
0-ulevel usubeq.

**Rule**: Every symbol is faithful.

The **user representative** (**urepr**) of a faithful subequation FS is the 0
-ulevel usubeq of FS.

> Properties:
>
>1. A usubeq is always a faithful subeq.
>1. The urepr of a usubeq US is US.
>1. A faithful subeq can have any number of N-ulevel usubeqs for N > 0,
>   including not having anyone.

A **faithful operator** is an operator FOP such that:

*   It is a uop, or
*   It has one arg.

A **filter** is a faithful op which is not a user op and has a user arg.

**Rule**: There are no filters in visual equation (maybe in a future (?)).

> **Properties**:
>
>1. If FS is a faithful subeq and FS is the parameter of an arg of a faithful
>   op FO, the FO-block is faithful.
>1. Let FNUOP be a faithful non-user op. A FNUOP-block is a faithful subeq if,
>   and only if, one parameter of FSO is a faithful subeq.
>1. If NFO is a non-faithful op, a NFO-block can be faithful or non-faithful.

**Rule**: Every operator of visualequation is faithful.

> **Properties**:
>
>1. Every subeq is faithful.
>
>1. The only non-user blocks are GOP-blocks.

## Juxtaposing subequations
Visual Equation uses some operators named juxts to display subequations
contiguously. That typically means that subequations are being multiplied, but
that can have other uses or interpretations such as to represent a number with
more than one digit. To connect several subequations together, a juxt with the
required number of arguments is used.

A **juxted** is a parameter of a juxt.

> **Example**:
>
> To display A B C D, being all of them symbols, the corresponding equation is
>
>   `(JUXT4, A, B, C, D)`
>
> In visual equation implementation it is not needed to specify the number
> of arguments of the juxt since it can be deduced from the length of the
> list.
>
>   `[JUXT, [A], [B], [C], [D]]`

> **Example**:
>
> If it is intentional that some contiguous juxtaposed subequations are
> selectable as a whole, an structure like this would be used:
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

A **N-ulevel peer** of an equation E, N being a positive number, is a subeq
P of US such that:

*   P is a N-ulevel usubeq of E, and
*   P is selectable.

> **Note**: That and next definitions refer to an equation because selectivity
> property is used, which require an equation to be defined.

A **N-ulevel aide** of an equation E, N being a non-negative number, is a subeq
AI of US such that:

*   AI is a M-ulevel peer of E, 0 < M < N, and
*   AI has no strict subeqs which are selectable.

A **N-ulevel mate** of an equation E, N being a non-negative number, is a subeq
MA of S such that:

*   MA is a N-ulevel peer of E, or
*   MA is a M-ulevel aide of E.

Two subeqs are **peers of each other** if they are not the same subeq and they
are N-ulevel peers of the same equation for some N.

Two subeqs are **N-mates of each other** if they are not the same subeq and
they are N-ulevel mates of the same equation.

> **Remark**:
>
> If an equation is edited, two peers/N-mates of each other of the original eq
> can become non-peers/non-N-mates of the new equation.

> **Properties**:
>
>1. A N-ulevel peer is not a M-ulevel peer for M different than N.
>1. A N-ulevel aide is a M-ulevel aide for M bigger than N.
>1. A N-ulevel peer P is a M-ulevel mate for M bigger than N if P is a symbol
>   or the representative of the parameter of a non-user arg.

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

## Equation operations

Navigation, edition and other equations-related operations are classified into
basic and advanced.

> **Note**: At least part of some operations should be presented
> in some way that a casual user is someway "forced" to know about them.
> An initial window with tips or a dropdown are possibilities.

There are two operation modes which in some cases operates differently when
the same input is sent to the program. The are:

*   Normal operation mode
*   Overwrite operation mode

### Normal mode

Characteristics:

*   Subequations are selected asymmetrically, unless selected subeq is a VOID.
*   The rounded part of the selection is called the **cursor**.
*   If the cursor is to the right of selected subeq, direction of selection is
    RDIR. If the cursor is to the left of the selected subeq, direction is
    LDIR. If a VOID is selected, direction is VDIR.
*   Insertion is done to the right of the cursor if RDIR or LDIR. If VDIR,
    insertion is really a replacement in which the VOID is substituted.
*   DEL remove the subeq to the right of the cursor, if it exists.
*   BACKSPACE remove subeq to the left of the cursor, if it exists.

If DEL or BACKSPACE do not find a juxted to delete and selection is the par of
a lop, the lop-block is flatted.

### Overwrite mode

*   Subequations are selected symmetrically. We do not use the concept of
    cursor in this mode, but it would cover the whole selection if considering 
    the equivalent mode in a graphical text editor. Direction is always called
    ODIR.
*   Insertion always substitute current selection.
*   DEL removes the selected subequation.
*   BACKSPACE removes the subeq to the left (honoring graphical texts editors
    but not readline's behaviour of replacing with a white space).
    
If DEL or BACKSPACE do not find a juxted to delete and selection is the par of
a lop, the lop-block is flatted.

### Basic operations

Basic operations must be intuitive for an user with no experience with emacs
or command-line shortcuts.

The scope of basic operations is everything that can be done only with the
mouse and cursor movement keys, RETURN, BACKSPACE, DEL and some common uses of
CONTROL, ALT and SHIFT.

> **Note**:
>
> Key bindings requiring CONTROL being selected are noted by C-x.
> Key bindings requiring ALT being selected are noted by M-x.
> Key bindings requiring CONTROL and ALT being selected are noted by M-C-x.
>
> In each particular case, instead of "x", the correspondent key which 
> completes the key binding will be used. For example, C-s if it is required
> to press CONTROL and then the S key without releasing the CONTROL key.

A limited amount of usual key bindings used in graphical applications that
collide with readline's default key bindings and/or philosophy are honored
in order to be consistent with the fact that Visual Equation is a graphical
application at the end and to help users which are used to shortcuts of
graphical environments but not those of emacs/readline. In the future it may be
possible to choose a "package" of shortcuts or even define them individually.

#### Fundamental movements
Users who do not know any key-bindings, with no previous experience 
with Visual Equation or which will not dedicate time to learn the rest of
movements will likely use these fundamental movements all the time.

Because of that, fundamental movements are intended to satisfy the following
conditions:

*   It must be possible to select any selsubeq by using them.
*   Thye must require very few keystrokes to select selsubeqs which are close 
    to current selection.
*   Navigating far away must not require too many keystrokes.
*   They must be someway reasonable so the user can learn their behaviour soon.
*   They must be a compromise between being practical and not discouraging
    a new user to use the program because they look strange.

##### LEFT (fast movement):

*   If RDIR, set LDIR.
*   Else, move to the closest symbol to the left without changing dir.
    If that symbol is not a selsubeq, select instead its usupeq of lower level.
    
**Marginal case**: If no candidate is found, select the last symbol or its
usupeq of lower lever in the case that it is not a selsubeq.

##### RIGHT (slow, exhaustive and redundant):

*   If LDIR, set RDIR.
*   Navigate equation forward, selecting selsubeqs before entering them and
    before exiting them.

#### Longer movements

> **Note**: CONTROL is preferred for "words" movements instead of ALT in basic
> commands because they are commonly used by desktop applications.

##### C-LEFT and C-RIGHT

> **Note**: The behavior does more honor to gedit and equivalent readline
> key combination than to kwrite. 

When using C-RIGHT/C-LEFT:
*   If LDIR/RDIR, direction will change to RDIR/LDIR.
*   Else, the mate to the right/left of selection is selected when
    C-RIGHT/C-LEFT is used.
    Marginal case: If selection is the last/first mate, choose the first/last
    mate.
*   Successive keystrokes of these key combinations (valid for an interleaved
    use of them) will remember the N-mate level of the selection before 
    applying the first of these key combinations.

#### Increasing and shortening selections

##### RETURN

*   Select supeq of current selection.
*   Do not change dir unless selection it was VDIR. In that case, use RDIR.

##### SHIFT-LEFT and SHIFT-RIGHT:

When using SHIFT-LEFT/SHIFT-RIGHT:
*   If selection is the representative of a non-first/non-last juxted, include
    in selection the juxted to the left/right. In the case that dir is not
    ODIR, set LDIR/RDIR.
*   If selection is already formed by several juxteds, shrink or extend the
    side matching the direction if that is LDIR or RDIR. If it is ODIR, the
    equivalent direction is determined by which was the first keystroke of the
    sequence. It is possible to change the direction in the LDIR/RDIR case
    by pressing RIGHT/LEFT.
*   If an extension is not possible (no more juxteds in the direction of
    expansion or a non-juxted is selected, select the supeq of selection and
    set LDIR/RDIR.

#### Manipulations

##### Cut (C-x)
 
Remove selected subeq and save/overwrite VE's clipboard.

##### Copy (C-c)

Save/overwrite VE's clipboard with selection.

##### Paste (C-v)

Insert VE's clipboard (in overwrite mode, selection is replaced).

##### Undo (C-z)

Undo last manipulation, if it exists.

##### Redo (C-SHIFT-z)

Redo last manipulation, if it exists.

##### Transpose forward (TAB)

Swap positions of current selection and its mate to the right, leaving original
selection selected. Exception: If LDIR, swap position with the mate the left 
instead, leaving original selection selected.

No direction is changed.

Marginal case: If there is no mate, perform a transpose backwards.

##### Transpose backward (SHIFT-TAB)

Swap positions of current selection and mate the left, leaving original
selection selected. Exception: If LDIR, swap position with the mate the right 
instead, leaving original selection selected.

No direction is changed.

Marginal case: If there is no mate, perform a transpose forward.

##### C-DEL

If selection is a juxted (or combination of them) remove all the juxted of
the same juxt-block from the cursor to the right if not ODIR. If ODIR,
remove selection and juxteds to the right.

If selection is not a juxted, it is equivalent to press DEL.

##### C-BACKSPACE

If selection is a juxted (or combination of them) remove all the juxted of
the same juxt-block from the cursor to the left if not ODIR. If ODIR, remove
juxteds to the left of selection.

If selection is not a juxted, it is equivalent to press BACKSPACE.

##### Group (SHIFT-RETURN)

Make strict usubeqs of selected block not selectable. It has no effect if
selection is a symbol.

##### Ungroup (C-SHIFT-RETURN)

Make strict usubeqs of selected block selectable. It has no effect if
selection is a symbol.

#### Shortcuts for inserting symbols and operators

> **Temporal Note**:
>
> The following key bindings are used by readline and should not be used.
>
>*  C-@, C-], C-\_, C-?
>*  M-C-\[, M-C-], M-C-?
>* M-SPACE, M-#, M-&, M-\* (requisitioned), M--, M-., M-digit, M-<, M->, M-?, 
>M-\, M-~ (requisitioned), M-\_ (requisitioned).

> **Notes**:
>
>*  Every C-x key binding of this section inserts a symbol.
>*  Every M-x key binding of this section inserts an operator with all their
>*  parameters set to VOID.
>*  Every M-C-x key binding of this section replaces selection with an operator
>   which has as first parameter the previous selection and any other it may
>   have set to VOID.
>*  Several keystrokes of the same key binding produce different
>   symbols/operators of common characteristics.

##### Functions (C-,, M-,, M-C-,)
First time is cosinus, then sinus then... The symbol version matches every 
function and the operator versions match functions which can have arguments.
##### Roots (M-%, M-C-%)
First time is a square root, next time is generic.
##### Modify subequation with a variant (M-@)
Full details to be defined.
##### Sumatory (C-+, M-+, M-C-+)
Sucesive keystrokes of the operator versions modify the number and position of
the args.
##### Productory (C-*, M-\*, M-C-\*)
Equivalent to summatory.
##### Integral (C-$, M-$, M-C-$)
Equivalent to summatory.
##### Fraction (M-/, M-C-/)
##### Equal-like symbols (C-=)
##### Multi-line equations (M-=, M-C-=) 
##### "Less than"-like symbol (C-<)
##### "Bigger than"-like symbol (C->) 
##### Pair of delimiters (M-(, M-C-()
It can be accelerated providing a character identified with the delimiter.
##### Matrices (M-), M-C-)):
###### Equation system ( M-{, M-C-{)
A digit modifies the number of equations.
###### Brace-like (C-{, M-}, M-C-})
###### Arrows (C-~)
###### Hat-like decorators of fixed size (M-\_, M-C-\_)
###### Hat-like decorators of variable size (M-\~, M-C-\~)
###### Small operators (C--)
###### Font colors (M-&, M-C-&)
###### Background colors (C-!, M-!)
###### Special text (C-., M-., M-C-.)
It is a symbol-like key biding because a windowed dialog will always appear 
and modification of the text will require a special dialog.
However, options M-. and M-C-. may be considered with care.

### Advanced operations

The intention of these command is to imitate Readline default keybindings as
much as possible. We will use Readline's command names with the following
equivalence:

*   characters -> selection and its mates
*   words -> 1-ulevel usupeq US of selection and mates of US

Main difference with equivalent clever commands is that these ones do not
consider so much direction of selection. It is recommended to avoid LDIR
when using this commands to avoid confusion.

VOID is a special character which is understood in different ways by
different commands.

If not specified, references (like mates) always refer to selection.

Old details for character <-> symbol (not sure if they are useful):

*   Symbols are unaware of equation structure, just as characters for
    Readline.
*   Mates have bounds, as words have. A word bound in Readline is a
    non-alphanumeric character. In visual equation, we consider as "word"
    bounds:

    *   The natural limits of a supeq, and
    *   VOIDs.

*   In addition, mates are nested in an equation, contrary to words in a
    line. That is indicated with ulevel of the mate. Following the
    symbolism of words, 1-ulevel mates would be words of the same
    line, 2-ulevel mates would be, for example, lines of the same page,
    3-ulevel mates pages of the same book, and so on.

Outdated, but left to rethink it if necessary:
*   If dir is -1, a numerical argument is not passed, the command accept a
    numerical argument -1 and some consequence is to operate on the opposite
    direction, then the command is applied in the opposite direction without
    any other side effect that a -1 argument would have (e.g., adding a subeq
    to the kill ring).
*   If dir is -1 and a numerical argument was passed, the effect is equivalent 
    to pass the same numerical argument multiplied by -1.

beginning-of-line (C-a)
    Select the first mate.
end-of-line (C-e)
    Select the last mate.
forward-char (C-f)
    Select mate to the right if it is not the last one. Else, do not move.
backward-char (C-b)
    Select mate to the left if it is not the first one. Else, do not move.
forward-word (M-f)
    Select last mate in supeq of selection, if it is not the same subeq. Else:
    Select last mate contained in the mate to the right RSUP of the supeq of
    selection, if RSUP exists. Else:
    Do not move.
    Successive calls to forward-word and backward-word must know the mate-
    ulevel which was applied in previous call since in general it cannot be
    deduced from final selection.
backward-word (M-b)
    Counterpart of forward-word.
clear-screen (C-l)
    Undecided.


### Advanced editions

WIP!! Non-applicable original documentation of readline can be read here until
it is finished.

#### Commands for manipulating the history

**Quick-save** means that if equation being edited was previously saved, it is
overwritten and its position in the history is not moidified. Else, it is saved
as a new "anonymous" equation as the last equation of the history.

**Save as (a new equation)** means that equation being edited is saved as a
different equation. It will be the last one of the history. It can be both
an a anonymous or named save.

save-as (C-SHIFT-s)
    Save current equation as a new equation, possibly specifying a name and
    categories in a window.
save (C-s)
    If equation being edited was never saved it is equivalent to save-as.
    Else, it overwrites saved equation with this one.
open-equation (C-o)
    This command is managed completely with a graphical interface.
    If equation being edited has modifications, it is asked if it want to be
    saved as a new equation or, if applicable, overwriting its previous entry
    in the history list. Then, choose an equation from the history with
    different search facilities and fetch it. Summary:

*   If it currently has already a place in the history:
    *   The user is asked whether discarding modifications, overwrite or save
        as a new equation.
*   Else:
    *   The user is asked whether discarding the equation or save as a new
        equation.
    
accept-line (C-j, C-m)
    This a non-windowed version of "Save as".
    Specify a name and save current equation as a new equation with that name.
    It is possible to specify a category by introducing it separated by slashes
    in the form `[category[/subcategory[/...]]/]name`. To accept the
    name press again C-j or C-m or RETURN.
    **Note**: C-j acts differently while searching in the history.
insert-comment (M-#)
    Save current equation at the end of the history list (as a new equation)
    and start editing a new empty equation. This is a fast accept-line such 
    that it does not ask for an equation name nor categories when saving.
    However, the equation will be uniquely identified anyway. With a numeric 
    argument, it is equivalent to accept-line.
save-no-window (M-C-#)
    This is a VE extension. It acts like command save (C-s).
    If equation already form part of the history, overwrite its entry. Else,
    it is equivalent to insert-comment. With a numeric argument you can specify
    a name and categories. If you are renaming an existing equation and
    you want to discard previous categories, just precede the name by a slash.
previous-history (C-p)
    save-no-window displayed equation and fetch the previous equation from the
    history list, moving back in the list. 
next-history (C-n)
    save-no-window displayed equation and fetch the next equation from the 
    history list, moving forward in the list.
beginning-of-history (M-<)
    save-no-window displayed equation and fetch to the first equation in the
    history.
end-of-history (M->)
    save-no-window displayed equation and fetch the last equation of the 
    history.
reverse-search-history (C-r)
    save-no-window current equation and search backward starting at the current
    equation and moving up through the history as necessary. This is an 
    incremental search. You can introduce part of the name, category or other 
    fields (TODO: specify). You can fetch the equation with C-j. Any
    other key combination will fetch the equation and then apply the command
    to the equation.
forward-search-history (M-C-R)
    Counter part of reverse-search-history. C-s is not used because that is a
    command with a long tradition in desktop applications to save files. If
    we allow key-bindings to be configurable, this will be one of the first
    commands supported.
    **Note**: By default, M-C-R is assigned to revert-line along with M-R in
    readline.
non-incremental-reverse-search-history (Not implemented!)
    Replace current equation by some previous equation of the history and
    discard any edition information of previous equation (so command undo will 
    not work). Equation taken is searched backward through the history starting
    at the current equation, using a non-incremental search for a string 
    supplied by the user. To accept the input, press RETURN, C-j or C-m. 
    To abort press BACKSPACE, a backward-delete-char command or an abort 
    command.
    No-Implementation note: I cannot find a way to like this command! I do not
    have any reason to implement it.
non-incremental-forward-search-history (Not implemented!)
    The counterpart of non-incremental-reverse-search-history.
yank-nth-arg (M-C-y)
    Insert  the  first argument to the previous command (usually the
    second word on the previous line) at point.  With an argument n,
    insert  the nth word from the previous command (the words in the
    previous command begin with word 0).  A  negative  argument  in‐
    serts  the  nth word from the end of the previous command.  Once
    the argument n is computed, the argument is extracted as if  the
    "!n" history expansion had been specified.
yank-last-arg (M-., M-_)
    Insert  the last argument to the previous command (the last word
    of the previous history entry).  With a numeric argument, behave
    exactly  like  yank-nth-arg.   Successive calls to yank-last-arg
    move back through the history list, inserting the last word  (or
    the  word  specified  by the argument to the first call) of each
    line in turn.  Any numeric argument supplied to these successive
    calls  determines  the direction to move through the history.  A
    negative argument switches the  direction  through  the  history
    (back or forward).  The history expansion facilities are used to
    extract the last argument, as if the "!$" history expansion  had
    been specified.



#### Commands for changing text
end-of-file (C-d)
    Exit VE if equation is a VOID.
delete-char (C-d)
    If next mate do not exist, do nothing. Else:
    Delete juxted to the right if sel is a non-last juxted of a juxt-block.
    Else:
    Move next mate, if it is not a VOID, to the right of sel as a juxted. Leave
    a VOID in the original position of the mate if it was not a juxted. Else:
    Replace next non-VOID mate, if it exists, to the mate to the left of that 
    mate, leaving a VOID in the position it was if it was not a juxted. Else:
    Do nothing.
    It saves deleted mates on the kill ring (readline do that when a
    numeric argument is passed, even if that is not documented).
    Successive calls to delete-char and backward-delete-char must know the
    mate-ulevel which was applied in previous call since in general it cannot 
    be deduced from final selection.
backward-delete-char (C-?, C-h)
    Counterpart of delete-char.
quoted-insert (C-q)
    If next input is a letter, it will introduce an associated Greek letter.
    Some capital letters have a greek version, but many cases share a latin
    symbol. To pass a negative numeric argument is equivalent to pass the
    same numeric argument but positive except for some letters which have
    a variant. In that case, it is equivalent to pass a positive numeric
    argument but the variant is used for the insertion instead.
    Not every greek letter can be inserted with this command. For those
    special cases you can use quoted-insert-extra (M-q). 
    If next input is a number, the number is introduced. (That is useful to 
    introduce several times a number. e.g, to introduce 3 ten times type: 
    M-1 0 C-q 3).
    TODO: Include TABs, SPACEs... 

Code equivalence:

> Legend:
>*  (**) means that correspondent greek letters can be obtained with another
>   key combination.
>*  (=) means that previous characters do not have a greek equivalent and
>   they map to themselves.
      
*   a, A -> alpha, A 
*   b, B -> beta, B
*   c, C -> chi, X (**)
*   d, D -> delta, Delta
*   e, E, - -> epsilon, E, varepsilon
*   f, F, - -> phi, Phi, varphi
*   g, G, - -> gamma, Gamma, digamma
*   h, H -> eta, H
*   i, I -> iota, I
*   j, J -> (=)
*   k, K, - -> kappa, K, varkappa
*   l, L -> lambda, Lambda
*   m, M -> mu, M
*   n, N -> nu, N
*   o, O -> omikron, O
*   p, P, - -> pi, Pi, varpi
*   q, Q -> (=)
*   r, R, - -> rho, P, varrho (**)
*   s, S, - -> sigma, Sigma, varsigma
*   t, T -> tau, T
*   u, U -> upsilon, Upsilon (**)
*   v, V -> (=)
*   w, W -> (=)
*   x, X -> chi, X (**)
*   y, Y -> upsilon, Upsilon (**)
*   z, Z -> zeta, Z 

quoted-insert-extra (M-C-q):
      This command supplies the missing greek letters of quoted-insert (C-q). 
      Assigned key combination is not used in readline by default.
      If next input is an alphanumeric character not listed in the list below,
      the character is considered literally. To pass a negative numeric
      argument is equivalent to pass the same numeric argument but positive 
      except for some letters which have a variant. In that case, it is
      equivalent to pass a positive numeric argument but the variant is used
      for the insertion instead.
      If next input is a number, the number is introduced.

Code equivalence:

> Legend:
>*  (**) means that correspondent greek letters can be obtained with another
>   key combination.

*   o, O -> omega, Omega
*   p, P -> rho, P, varrho (**)
*   s, S -> psi, Psi
*   t, T , - -> theta, Theta, vartheta
*   x, X -> xi, Xi

tab-insert
    See quoted-insert.
self-insert (a, b, A, 1, !, ...)
      Insert the character typed. In some cases such as ~ or SPACE, a special
      character is inserted instead (TODO: be more specific). In some cases,
      quoted-insert may be needed to insert some special symbols.
transpose-chars (C-t)
    Drag the symbol before selection forward over the first symbol of
    selection, moving selection to the next symbol. If there are no symbols
    to the right
      Drag the character before point forward over  the  character  at
      point,  moving point forward as well.  If point is at the end of
      the line, then this transposes the two characters before  point.
      Negative arguments have no effect.
transpose-words (M-t)
      Drag  the  word  before  point past the word after point, moving
      point over that word as well.  If point is at  the  end  of  the
      line, this transposes the last two words on the line.
upcase-word (M-u)
      Uppercase  the current (or following) word.  With a negative ar‐
      gument, uppercase the previous word, but do not move point.
downcase-word (M-l)
      Lowercase the current (or following) word.  With a negative  ar‐
      gument, lowercase the previous word, but do not move point.
capitalize-word (M-c)
      Capitalize the current (or following) word.  With a negative ar‐
      gument, capitalize the previous word, but do not move point.
overwrite-mode
    A similar behavior (gedit-like) can be obtained with INSERT. See above.

#### Killing and Yanking
kill-line (C-k)
      Kill the text from point to the end of the line.
backward-kill-line (C-x Rubout)
      Kill backward to the beginning of the line.
unix-line-discard (C-u)
      Kill backward from point to the  beginning  of  the  line.   The
      killed text is saved on the kill-ring.
kill-word (M-d)
      Kill from point the end of  the  current  word,  or  if  between
      words,  to  the  end  of the next word.  Word boundaries are the
      same as those used by forward-word.
backward-kill-word (M-Rubout)
      Kill the word behind point.  Word boundaries  are  the  same  as
      those used by backward-word.
unix-word-rubout (C-w)
      Kill  the  word behind point, using white space as a word bound‐
      ary.  The killed text is saved on the kill-ring.
delete-horizontal-space (M-\)
    If selection is a parameter, remove any juxted which may be
    a VOID. Else, flat the lop-block.
kill-region (Maybe we bound it even if it is not a default of readline)
    Kill the text between the point and  mark  (saved  cursor  posi‐
    tion).  This text is referred to as the region.
copy-region-as-kill (Maybe we can reserve a key combination)
    Copy the text in the region to the kill buffer.
yank (C-y)
    Yank the top of the kill ring into the buffer at point.
yank-pop (M-y)
    Rotate  the kill ring, and yank the new top.  Only works follow‐
    ing yank or yank-pop.
#### Numeric Arguments
digit-argument (M-0, M-1, ..., M--)
  Add this digit to the argument already accumulating, or start  a
  new argument. M-- starts a negative argument.

#### Completing
complete
    Not used. Using menu-complete instead with its key binding instead.
possible-completions (M-?)
    List the possible variations of the selected subequation. You can choose
    one using the cursor keys and accept it with RETURN, C-j or C-m. To
    abort, use ESC or a key binding associated to abort.
insert-completions
    Not used. M-* used to introduce productories instead.
menu-complete (C-i)
    Replace selection with a variation. Repeated execution of the command steps
    through the list of possible variations, inserting each match in turn. At
    the end of the list, the original subequation is restored. An argument of
    n moves n positions forward in the list of possible variations. A negative
    argument moves backward through the list.
    Note: C-i is used by default for complete command in readline while this
    one is unbounded.

#### Keyboard Macros
start-kbd-macro (C-c ()
      Begin saving the characters  typed  into  the  current  keyboard
      macro.
end-kbd-macro (C-c ))
      Stop saving the characters typed into the current keyboard macro
      and store the definition.
call-last-kbd-macro (C-c e)
      Re-execute the last keyboard macro defined, by making the  char‐
      acters  in  the  macro  appear  as  if  typed  at  the keyboard.
      print-last-kbd-macro () Print the last keyboard macro defined in
      a format suitable for the inputrc file.

#### Miscellaneous
re-read-init-file (C-c C-r)
      Read a configuration file.
abort (C-g, M-C-g, C-c C-g)
      Abort the current editing command. It does not ring.
do-uppercase-version (M-a, M-b, M-x, ...)
      If  the  metafied character x is lowercase, run the command that
      is bound to the corresponding uppercase character.
prefix-meta (ESC)
      Metafy the next character typed.
undo (C-_, C-c C-u)
      Incremental undo, separately remembered for each equation.
revert-line (M-r)
      Undo all changes made to this equation.  This is like executing
      the undo command enough times to return the equation to its
      initial state.
tilde-expand (M-&)
    Not used. M-& used to insert a color as described above.
set-mark (C-@, M-<space>)
      Set the mark to the point.  If a numeric argument  is  supplied,
      the mark is set to that position.
exchange-point-and-mark (C-c C-c)
      Swap  the  point  with the mark.  The current cursor position is
      set to the saved position, and the old cursor position is  saved
      as the mark.
character-search (C-])
      A character is read and point is moved to the next occurrence of
      that character.  A negative count searches for  previous  occur‐
      rences.
character-search-backward (M-C-])
      A  character  is  read and point is moved to the previous occur‐
      rence of that character.  A negative count searches  for  subse‐
      quent occurrences.
skip-csi-sequence
      Read  enough  characters to consume a multi-key sequence such as
      those defined for keys like Home and End.  Such sequences  begin
      with a Control Sequence Indicator (CSI), usually ESC-[.  If this
      sequence is bound to "\[", keys producing  such  sequences  will
      have  no  effect  unless explicitly bound to a readline command,
      instead of inserting stray characters into the  editing  buffer.
      This is unbound by default, but usually bound to ESC-[.
dump-functions
      Print  all  of the functions and their key bindings to the read‐
      line output stream.  If a numeric argument is supplied, the out‐
      put  is  formatted  in such a way that it can be made part of an
      inputrc file.
dump-variables
      Print all of the settable variables  and  their  values  to  the
      readline  output stream.  If a numeric argument is supplied, the
      output is formatted in such a way that it can be made part of an
      inputrc file.
dump-macros
      Print  all of the readline key sequences bound to macros and the
      strings they output.  If a numeric  argument  is  supplied,  the
      output is formatted in such a way that it can be made part of an
      inputrc file.
emacs-editing-mode (C-e)
      When in vi command mode, this causes a switch to  emacs  editing
      mode.
vi-editing-mode (M-C-j)
      When  in  emacs editing mode, this causes a switch to vi editing
      mode.
