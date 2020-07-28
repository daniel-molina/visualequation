# The formalism behind Visual Equation

Below you can read most of definitions and rules used in Visual Equation code.
There are a lot of definitions, but I hope they are intuitive. It is intended
to be only as rigorous as needed to avoid ambiguity, but relationships become
complex and some technicalities must be used.

> **Disclaimer**: *Definitions have being changed and extended as it has been
> required by new features, it is possible that some of the code notation has
> not been updated yet.*

## Formalism of an equation

### Introduction
Most of definitions included in other sections do not relay on the actual
implementation of an equation (a python list), so I found better to keep the 
formalism agnostic with respect to the implementation.

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
There are three main classes of elements:

*   Symbols
*   Operators
*   Blocks

**Symbols** are elements that make sense by themselves. For example, digits or 
Greek letters.

**Operators** (**ops**) are elements which require other elements to make
sense. For example, a fraction, which needs a numerator and a denominator.

Elements that complete an operator are called **arguments** (**args**). They
are symbols or blocks.

A **OP-arg** is an argument of operator OP, being OP a proper or a common noun.

A **N-arg(s) operator** is an operator with N arguments. A **unary op** is a
1-arg op. A **binary** op is an 2-args op. A **ternary** op is a 3-args op.

The **ordinal of the argument of a N-arg(s) operator** is the positive
integer (from 1 to N) that identifies an argument of an operator. Arguments
of O will be referred as "the first argument of O", "the second argument of O",
and so on.

**Blocks** are tuples with N+1 elements, N > 0, composed by:

*   The leading element, which is an operator of arity N. It is called the
    **leading operator** of the block.
*   The rest of elements are the arguments of the leading operator in the same
    order than its associated ordinal.

A **X-block** is a block which has X as leading operator, being X a proper or
a common noun.

**lop-B** is the leading operator a block B, being X a proper noun or a common
noun.

A **lop-B-arg** is an argument of operator lop-B, being B a proper or common
noun.

A **subequation** (**subeq**) is a symbol or a block.

An **equation** (**eq**) is a subequation which is not the argument of an
operator.

> **Property**:
>
> A subequation is not always an equation but an equation is always a
> subequation.

> **Note**: *Whenever possible the term subequation will be preferred in the
> following definitions. However, in the code some concepts defined will be 
> usually referred to equations.*

### Basic subequation definitions
A **0-level subequation of another subequation S** is S.

A **N-level subequation of another subequation S**, N being a positive
integer, is:

*   If S is a symbol, it does not exist.
*   If S is a block B, a **(N-1)-level subequation of a B-arg**.

This is a recursive definition that finishes when the nesting level is 0 and 
previous definition applies.

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

A **primitive** or **primitive element** of a subequation S is:

*   If S is a symbol, S.
*   If S is a block, the leading operator of S or a **primitive** of an S-arg.

A **symbol of a subequation S** is a primitive of S which is a symbol.

An **operator of a subequation S** is a primitive of S which is an op.

A subequation S **contains** or **has** a subequation SUB if SUB is a subeq
of S.

> **Property** (probably the most used in visual equation):
>
> There is a natural map between any primitive of a subequation S and every
> subequation SB of S:
>
>*  If the primitive is a symbol A -> A.
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

>  **Example:**
>
>These are the supeqs of subequation `3` of previous example:
>
>*  level 1:    `(Prod, 3, 2)`
>*  level 2:    `(Sum, 1, (Prod, 3, 2))`

> **Properties and remarks**:
>
>1. To be finite, an equation requires that some of the arguments of some of
>   its operators are symbols.
>1. A subeq of an equation is always the whole equation or an argument of some
>   operator of the equation.
>1. Subequations contain other subequations only **completely**, meaning that, 
>   if subequation S contains subequation T, every element of T is an element 
>   of S. In other words, they do not partially overlap.
>1. An argument of a subequation S cannot be S (nor equal since only finite
>   subequations are considered).
>1. One argument of an operator O cannot be a subequation of other argument of
>   O.
>1. A subequation do not need another subequation to make sense, even if the 
>   concept of subeq SB of a subeq S is defined and in that case SB requires S.
>1. Superequations always are referred to a subequation SB in certain
>   subequation S, when it is not specified, the whole equation E to which
>   S belongs is supposed to have that role.
>1. A block always contains, at least, one operator (the leading operator).
>1. The leading operator is a privileged operator in a block because:
>
>   *   It and its arguments define completely the block.
>   *   It is not part of the argument of any other operator of the block.

## Implementation of an equation in Visual Equation
 
### Basic ideas

An *equation* is represented by a **list** and any equation primitive is an
element of that list.

*Subequations* are always **sublists**.

Since an equation must always be valid, when an operator is introduced and the 
user has not yet specified one or more arguments, they are set to the special 
symbol *NEWARG*, which is represented by a small square when displayed.

To give special properties to symbols, 0-args operators are considered.

### Format
Visual Equation uses a flat list of primitives to represent an equation. The
format is equivalent to Polish Notation:

> An operator always precedes its arguments.

To describe the format of an subequation, consider the action **extend a list
L with subequation S**.

Consider a list L and subequation S. To extend L with S,

*   If S is a symbol, append S to L.
*   If S is a block:
    1.  Append the lop-S to L, then
    2.  Extend L with the arguments of lop-S, one after another.

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
> The code is intended to work with operators with 0 arguments so
> they can be used to represent symbols which have some special
> property.
> In the future that may be generalized, e.g. by using a list of tags.

Since equations must always be valid, when an operator is introduced and the
user has not yet specified one or more of its arguments, undefined arguments
are set to the special symbol NEWARG, which is represented by a small square
when displayed.

## Selecting subequations

There are reasons to avoid the user to select some subequations:

1.  They can be artifacts that have no meaning to the user.
1.  It can be redundant to select certain blocks.
1.  The user can ask explicitly not to select a subeq.
1.  There can be LaTeX limitations to select a subequation.
1.  That subequation cannot be edited with the same flexibility than
    typical subequations because that has consequences that current code
    cannot manage.
1.  Other cases?

> **Note**:
> 
> It can be tricky to correctly use the language to indicate that an element
> has a property because it is an element of another element but no by itself
> since an element *equal* to that one may not have that property or the
> element itself may not have that property after an equation edition in which
> the element survives.
>
> With that objective in mind, several terms which specify the reasons for an
> element to be selectable have been defined.

### Effectively selectable subequations

A subequation S of an equation E is **effectively selectable** if S is
guaranteed to be selectable if E is not modified.

**Rule**: At least one subeq of an equation must be effectively selectable.

### User subequations

A **user subequation** (**usubeq**) is a subeq S that can be selected unless a 
superequation of S does not allow S to be selected.

> **Remark**:
>
>1. Strict subequations of a subequation can be usubeqs or not.
>1. A effectively selectable subequation is a usubeq. The opposite is not
>   (always) true.

Any subequation term preceded by a "user" and abbreviations by a
juxtaposed "u" is a user subequation. Abbreviations would be usupeq, usupeq, 
X-ublock, uarg, lop-X-uarg (last two should be avoided to avoid confusing
a casual reader).

> **Example**:
>
> (A) X-ublock is block a B which lop-B is (a) X and B is an ublock.

A **mark** M is a symbol that is not an usubeq.

> **Property**:
> 
> A mark must have a usupeq.

### Selectable arguments

An operator OP **has a selectable argument** (**has a selarg**) with
ordinal OR if OP does not impose any selectivity conditions on any subequation
that is used as its OR-th argument.

An operator **has a non-selectable argument** (**has a nonselarg**) with
ordinal OR if OP impose that any subequation S that is used as its OR-th
argument cannot be selected (but it does not impose any conditions on
strict subequations of S).

> **Note**:
>
> It has been preferred the term selectable argument instead of "user
> argument" to emphasize that *user property* is a characteristic of a
> subequation while a *selectable property* is a characteristic that a
> subequation inherits because of its superequations.

### Operators and selectivity

A **rugose operator** (**rugop**) is an operator OP such that an OP-block is a
usubeq.

A **slippery operator** (**slipop**) is an operator OP such that an OP-block is
not a usubeq.

A **sticky operator** is a slipop such that any N-level subeq of OP-block,
N > 1, is not allowed to be selected (independently of being an usubeq).

The idea of a sticky operator is to prohibit any strict subequation of its
argument from being selected.

> **Note**:
>
> For practical reasons, the only sticky operator of visual equation is a
> binary operator called *GOP* (which comes from grouping op), but a unary
> operator would be more elegant if there were no programing advantages.

**GOP** is a binary sticky operator such that the argument allowed to be
selected is the first one and the second one is a mark called POG.

## Juxtaposing subequations
Visual Equation uses some operators named juxts to display subequations
contiguously. That typically means that subequations are being multiplied, but
that can have other uses or interpretations such as to represent a number with
more than one digit. To connect several subequations with the same selectivity
rules, chains of juxts are used.

### Juxts

A **juxt** is a binary op such that:

*   Its second argument is not allowed to be selected, and
*   It does not impose restrictions on the selectivity of strict subeqs of its
    second argument.
*   Its second argument must be a juxt-block or a mark.

A **descendant juxt** (**djuxt**) DJ is a juxt of an equation or non-juxt-block
Q such that:

*   The position of the DJ-block is the second argument of another juxt of Q.

### Parent and descendant juxts

A **parent juxt** (**pjuxt**) PJ is a juxt of an equation or non-juxt-block Q
such that:
 
*   PJ is a rugop, and
*   The second argument of PJ is a djuxt-block.
*   The position of the PJ-block cannot be the argument of another juxt of Q.

> Remark:
>
>1. juxts and juxt-blocks can be completely determined in a subequation.
>1. Determination of djuxts, pjuxts, djuxt-blocks and pjuxt-blocks or
>   juxt-ublocks in a subequation S can only be done if it is known that S is
>   the entire equation or S is not a juxt-block.
>1. A pjuxt-block has one pjuxt and, at least, one djuxt.
>1. A pjuxt-block is a usubeq and a djuxt-block of an equation is not a usubeq.
>1. A juxt-ublock is a pjuxt-block and a pjuxt-block is a juxt-ublock. Another
>   name for them can be an **entire juxt-block**.

### Constituent and terminal juxts

A **constituent juxt** (**cjuxt**) of a juxt-ublock JU is a juxt that is:

*   the parent juxt of JU, or
*   lop-Q, being Q the second argument of another **cjuxt** of JU.

This is a recursive definition which could be improved to be a little more
constructive.

A **terminal juxt** (**tjuxt**) of a juxt-block JB is a cjuxt of JB which
second argument is a mark.

In visual equation implementation, the mark used for the second arg of a
tjuxt is named *TXUJ* (that is the word JUXT reversed, not a typo).

A **juxted** of a juxt-block JB is a first arg of a cjuxt of a JB.

The only pjuxt and djuxt in visual equation are called *PJUXT* and *DJUXT*.

> **Remarks**:
>
>1. A juxt-block is a juxt-ublock if, and only if, it is a PJUXT-block.
>1. A *PJUXT* is always the pjuxt of a juxt-ublock.
>1. A *DJUXT* is always a djuxt of a juxt-ublock.

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
> If it is intentional that some contiguous juxtaposed subequations must be
> selectable as a whole, an structure like this would be used:
>
>   `(PJUXT, (DJUXT, A, (DJUXT, B, TXUJ)), (DJUXT, C, TXUJ))`
>
> However, the user must not worry about this internal structure.


> **Properties and remarks**:
>
>1. A juxt-ublock with N cjuxts has N juxteds.
>
>1. There can be juxts in a juxt-ublock JU that are not cjuxts of JU. In that
>   case, they are cjuxts of another juxt-ublock which is a subeq of a juxted
>   of JU.
>   Previous example was an example of that case. Another one is the following
>   equation where FRAC is a binary rugop.
>
>    `(PJUXT, (FRAC, A, (PJUXT, B, (DJUXT, C, TXUJ)), (DJUXT, X, TXUJ)))`
>
> The equation is itself a juxt-ublock with one djuxt. The first juxted is the
> ublock `(FRAC, A, (PJUXT, B, (DJUXT, C, TXUJ))`, the second juxted is the 
> symbol X, and the > third one is the symbol Y. Second argument of first 
> juxted is itself another juxt-ublock `(PJUXT, B, (DJUXT, C, TXUJ)` which 
> only has one juxt, so it is at the same time the pjuxt and tjuxt.

## Equation metrics

A **0-ulevel usubeq of a subeq S** is:
 
*   If S is a usubeq, S.
*   Else, it does not exist.

A **N-ulevel usubeq of a subeq S**, N being a positive integer, is:

*   If S is a symbol, it does not exist.
*   If S is a block B, a **(N-1)-ulevel usubeq of a B-arg**.

The **user nesting level** (**ulevel**), of a N-ulevel usubeq of a subeq is the
(non-negative) value N.

A neighbour 

A **guy from an ublock UB** is a subeq of UB such that:

*   It is not UB, and
*   It is an usubeq, and
*   It has only one usupeq in UB (UB itself).

An ublock UB **houses** guy G if G is a guy from UB.

All juxteds of a juxt-ublock appear horizontally to the user. If they were
usubeqs, the only difference between them would be the visual order in which
they appear, from left to right. That motivates the following definitions:

Guys from the same juxt-ublock are **peers**.

Guys from a same ublock which is not a juxt-ublock are **mates**.

Two subequations of an equation are **neighbours** of each other if they
        are:

        The i-th and (i+1)-th citizens of the same JUXT-ublock, or
        The i-th and (i+1)-th uargs of the same (non-JUXT) operator.

A **superequation neighbour** SUP of a subequation S in E, S a strict subeq of
E, is a subequation of E such that:

*   SUP is a neighbour of the smallest superequation of S.

Two subeqs are **pseudo-neighbours** (p-neighbours) if:

        They are neighbours and none of them is a group-block, or
        One of them is a group argument and its group-block is
                neighbour of the other, or
        Both of them are group arguments and their group-blocks are
                neighbours, or
            *

Properties:

Neighbours and superequation neighbours do not always exist.
