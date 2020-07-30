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
> The main use of parenthesis throughout the text to help the reader understand
> the sentences and their scope, not to provide additional information.

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

An *equation* is represented by a **list** and any equation primitive is an
element of that list.

*Subequations* are always **sublists**.

Since an equation must always be valid, when an operator is introduced and the 
user has not yet specified one or more of its parameters, they are set to the
special symbol *VOID*, which is represented by a small square when displayed.

To give special properties to symbols, 0-args operators are considered in the
implementation, but they are considered symbols in this formalism.

### Format
Visual Equation uses a flat list of primitives to represent an equation. The
format is similar to Polish Notation:

> An operator always precedes its parameters.

To describe the format of an subequation, consider the action **extend a list
L with subequation S**.

Consider a list L and subequation S. To extend L with S,

*   If S is a symbol, append S to L.
*   If S is a block:
    1.  Append the lop-S to L, then
    2.  Extend L with the parameters of lop-S, one after another.

This is a recursive definition that makes sense because subequations are
finite.

> **Example**:
>
> Here is equation of previous examples in the implementation format:
>
> `[Sum, 1, Prod, 2, 3]`

If you are having troubles understanding the format, maybe it can help to
read about Polish Notation somewhere (like Wikipedia).

### Python types correspondence

*Elements* of the list representing an equation are (exclusively) *primitives* 
of the equation.

*Subequations* of an equation are **slices** of a list. In python notation, if 
`L` is a list, a subequation of L can always be expressed as `L[a:b]`,
0 <= a < b <= len(L). Note that python syntax was used, so `L[b]` is
excluded in `L[a:b]`.

Symbols are represented as **strings** (+) that match their LaTeX code.

Operators are represented by instances of a **class Op**, which properties are:

*   The number of arguments it has.
*   A string indicating its LaTeX code and the position of its arguments.
*   A string that is usually empty but can be used to indicate a special 
    property of an operator. (++)

> **Note**:
>
> In the future an operator may include a list of tags.

Since equations must always be valid, when an operator is introduced and the
user has not yet specified one or more of its parameters, undefined parameters
are set to the symbol **VOID**, which is represented by a small square when 
displayed.

## Building rules

The following definitions specify the terminology used to prohibit certain
subequations to be built.

Building rules are defined by the **auxiliary** property. An element which is
not a block have intrinsically this property or not. Blocks inherit this
property from its lop.

> **Note*:
>
> The auxiliary property has only the same meaning for symbols and blocks.

Depending on its type, an elements with the auxiliary property is referred as:

*   Auxiliary symbol
*   Auxiliary operator (auxop)
*   Auxiliary arguments (auxarg)
*   Auxiliary block (auxarg)

**Rule**: An auxiliary subequation is allowed to be the parameter of an
auxiliary argument that explicitly allows it.

**Rule**: A Non-Auxiliary subequations is allowed to be an equation or a
parameters of a non-auxiliary argument.

A **marker** is an auxiliary symbol.

**Rule**: A marker has no representation in a displayed equation (they are
only used for programming convenience).

A **dummy argument** is an auxiliary argument which parameter is restricted to
be a marker. Different dummy arguments will specify in its definition which
specific marks can be its parameter.

> **Remarks**:
>
>1. Markers can only be accepted in a dummy args or non-dummy auxargs.
>1. Auxblocks can only be accepted in non-dummy auxargs.

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

A subequation S of an equation E is selectable if:
 
*   S is a usubeq, and
*   S has no usupeq which is a subeq of a parameter of a non-user arg.

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
 
*   It is a binary operator, and
*   It is a non-user op, and
*   Its first argument is a non-user arg, and
*   Its second argument is dummy and accepts a marker called **POG**.

### User subequations definitions and rules

**Rule**: A symbol that is not a user symbol is a marker.

> Property:
>
> If a non-user symbol has no representation in a displayed equation.

A **0-ulevel usubeq of a subeq S** is:
 
*   If S is a usubeq, S.
*   Elif S is a symbol, it does not exist.
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

The **representative** of a faithful subequation FS is the 0-ulevel usubeq of
FS.

> Properties:
>
>1. A usubeq is always a faithful subeq.
>1. The representative of a usubeq US is US.
>1. A faithful subeq can have any number of N-ulevel usubeqs for N > 0,
>   including not having anyone.

A **faithful operator** is an operator FOP such that:

*   It is a uop, or
*   If it has N args, N-1 args are dummy.

> **Properties**:
>
>1. If FS is a faithful subeq and FS is the parameter of an arg of a faithful
>   op FO, the FO-block is faithful.
>1. Let FNUOP be a faithful non-user op. A FNUOP-block is a faithful subeq if,
>   and only if, one parameter of FSO is a faithful subeq.
>1. If NFO is a non-faithful op, a NFO-block can be faithful or non-faithful.

**Rule**: A non-faithful op must be an auxop.

> **Properties**:
>
> A non-auxiliary block is faithful.

## Juxtaposing subequations
Visual Equation uses some operators named juxts to display subequations
contiguously. That typically means that subequations are being multiplied, but
that can have other uses or interpretations such as to represent a number with
more than one digit. To connect several subequations together, chains of juxts
are used.

### Types of juxts

There are common properties of **juxt** ops. If an operator is a juxt:
 
*   It is a binary op, and
*   Its first argument is an uarg, and
*   Its second argument is an auxarg which parameters must be a juxt-block or
    a mark.

Two juxts are considered in Visual Equation:

A **descendant juxt** (**djuxt**) is a juxt DJ such that

*   DJ is an non-user auxiliary operator, and
*   The second argument of PJ is restricted to be a djuxt-block or a mark.

**Rule**: Every operator that is not a djuxt must be a faithful operator.

**DJUXT** is the common noun of the djuxt considered in visual equation. The
marker accepted by its second argument has as common noun **TXUJ**.

A **parent juxt** (**pjuxt**) is a juxt PJ such that:
 
*   PJ is a user non-auxiliary operator, and
*   The second argument of PJ is restricted to be a djuxt-block.

**PJUXT** is the common noun of the pjuxt considered in visual equation.

> Remarks:
>
>1. A DJUXT-block cannot be an equation.
>1. If a subequation is a djuxt-block, it has at least one superequation.
>1. A pjuxt-block has one pjuxt and, at least, one djuxt.
>1. A pjuxt-block is a usubeq and a djuxt-block of an equation is not a usubeq.
>1. To be a pjuxt-block is equivalent to be a juxt-ublock (the second term is
>   preferred). 
>1. A pjuxt-block can be seen as an "entire" juxt-block.

### Constituent and terminal juxts

A **constituent juxt** (**cjuxt**) of a juxt-ublock JU is a juxt that is:

*   The parent juxt of JU, or
*   The leading operator of the second parameter of another **cjuxt** of JU
    if that parameter is not a marker.

A **terminal juxt** (**tjuxt**) of a juxt-block JB is a cjuxt of JB which
second argument is a marker.

> **Corollary:**
>
> A block is not faithful if, and only if, it is non-terminal djuxt-block.

> **Property**:
>
> A non-faithful subeq is a mark or non-terminal djuxt-block.

A **juxted** of a juxt-block JB is the first parameter of a cjuxt of a JB.

> **Remarks**:
>
>1. A tjuxt is a cjuxt.
>1. A tjuxt is a djuxt.

> **Example**:
>
> To display A B C D, being all of them symbols, the corresponding equation is
>
>   `(PJUXT, A, (DJUXT, B, (DJUXT, C, (DJUXT, D, TXUJ))))`
>
> In visual equation implementation:
>
>   `[PJUXT, A, DJUXT, B, DJUXT, C, D, TXUJ]`

There is an important fact about juxts: they are an artifact of no interest to
the user. The user may need to select individual elements, all of them or
its own combination of them, but not something attending to the arbitrary
nested structure of juxts.

> **Example**:
>
> If it is intentional that some contiguous juxtaposed subequations are
> selectable as a whole, an structure like this would be used:
>
>   `(PJUXT, (PJUXT, A, (DJUXT, B, TXUJ)), (DJUXT, C, TXUJ))`
>
> If A, B and C are ordinary symbols, the following are the selection
> possibilities of the previous equation:
>
>   `(A B C)`
>   `(A B) C`
>   `(A) B C`
>   `A (B) C`
>   `A B (C)`
>
> However, the user must not worry about this internal structure.
>
> **Properties and remarks**:
>
>1. A juxt-ublock with N cjuxts has N juxteds.
>1. There can be juxts in a juxt-ublock JU that are not cjuxts of JU. In that
>   case, they are cjuxts of another juxt-ublock which is a subeq of a juxted
>   of JU. Previous example was an example of that case. Another one is the 
>   following equation where FRAC is a binary rugop and a A, B, C and X are
>   ordinary symbols.
>
>    `(PJUXT, (FRAC, A, (PJUXT, B, (DJUXT, C, TXUJ)), (DJUXT, X, TXUJ)))`
>
> The equation is itself a juxt-ublock with one djuxt. The first juxted is the
> ublock `(FRAC, A, (PJUXT, B, (DJUXT, C, TXUJ))`, and the second juxted is
> the symbol X. Second argument of first juxted is itself another juxt-ublock 
> `(PJUXT, B, (DJUXT, C, TXUJ)` with two juxteds.

## Equation metrics

The following properties will be used in the definitions below:

> **Properties**:
>
>1. djuxt-blocks are (the only) non-faithful subeqs with representation when
>   the equation is displayed.
>1. A juxted is faithful.
>1. Every representative of a juxted of the same JB has the same ulevel with
>   respect to any common superequation.

A **N-ulevel peer** of an equation E, N being a positive number, is a subeq
P of US such that:

*   P is a N-ulevel usubeq of E, and
*   P is selectable.

> **Note**: That and next definitions refer to an equation because selectivity
> property is used, which require an equation to be defined.

A **N-ulevel aide** of an equation E, N being a positive number, is a subeq
AI of US such that:

*   AI is a M-ulevel peer of E, 0 < M < N, and
*   AI has no strict subeqs which are selectable.

A **N-ulevel mate** of an equation E, N being a positive number, is a subeq MA 
of S such that:

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

The **peer to the left** of another peer P is a subeq LP that results of the
following algorithm:

1.  Set SUP to the supeq of P and ORD to the ordinal of the argument of SUP-lop
    such that its parameter is P.
2. 
3.
4.
