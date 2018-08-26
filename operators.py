class BinaryOperator:
    def __init__(self, latex_code):
        self.latex_code = latex_code

    def __call__(self, s0, s1):
        return self.latex_code.format(s0, s1)

class UnaryOperator:
    def __init__(self, latex_code):
        self.latex_code = latex_code

    def __call__(self, s0):
        return self.latex_code.format(s0)

class Symbol:
    def __init__(self, latex_code):
        self.latex_code = latex_code

    def __call__(self):
        return self.latex_code

# Latin letters
LOWER_LATIN = [
'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o',
'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
]

UPPER_LATIN = [
'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O',
'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
]

# Numbers
NUMBERS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

#TODO: Accepts only latin, represented by other thing than CDot
#Text = UnaryOperator(r'\text{%s}')

LATIN_NUMBERS = LOWER_LATIN + UPPER_LATIN + NUMBERS

# Greek Letters lowercase
Alpha = Symbol(r'\alpha ')
Beta = Symbol(r'\beta ')
Gamma = Symbol(r'\gamma ')
Digamma = Symbol(r'\digamma ')
Delta = Symbol(r'\delta ')
Epsilon = Symbol(r'\epsilon ')
Zeta = Symbol(r'\zeta ')
Eta = Symbol(r'\eta ')
Theta = Symbol(r'\theta ')
Iota = Symbol(r'\iota ')
Kappa = Symbol(r'\kappa ')
Lambda = Symbol(r'\lambda ')
Mu = Symbol(r'\mu ')
Nu = Symbol(r'\nu ')
Xi = Symbol(r'\xi ')
Pi = Symbol(r'\pi ')
Rho = Symbol(r'\rho ')
Sigma = Symbol(r'\sigma ')
Tau = Symbol(r'\tau ')
Upsilon = Symbol(r'\upsilon ')
Phi = Symbol(r'\phi ')
Chi = Symbol(r'\chi ')
Psi = Symbol(r'\psi ')
Omega = Symbol(r'\omega ')

LOWER_GREEK = [
Alpha,
Beta,
Gamma,
Digamma,
Delta,
Epsilon,
Zeta,
Eta,
Theta,
Iota,
Kappa,
Lambda,
Mu,
Nu,
Xi,
Pi,
Rho,
Sigma,
Tau,
Upsilon,
Phi,
Chi,
Psi,
Omega,
]

# Greek Letters Uppercase
UpperGamma = Symbol(r'\Gamma ')
UpperDelta = Symbol(r'\Delta ')
UpperTheta = Symbol(r'\Theta ')
UpperLambda = Symbol(r'\Lambda ')
UpperXi = Symbol(r'\Xi ')
UpperPi = Symbol(r'\Pi ')
UpperSigma = Symbol(r'\Sigma ')
UpperUpsilon = Symbol(r'\Upsilon ')
UpperPhi = Symbol(r'\Phi ')
UpperPsi = Symbol(r'\Psi ')
UpperOmega = Symbol(r'\Omega ')

UPPER_GREEK = [
UpperGamma,
UpperDelta,
UpperTheta,
UpperLambda,
UpperXi,
UpperPi,
UpperSigma,
UpperUpsilon,
UpperPhi,
UpperPsi,
UpperOmega,
]

# Greek letters variants
VarEpsilon = Symbol(r'\varepsilon ')
VarTheta = Symbol(r'\vartheta ')
VarKappa = Symbol(r'\varkappa ')
VarRho = Symbol(r'\varrho ')
VarSigma = Symbol(r'\varsigma ')
VarPhi = Symbol(r'\varphi ')
VarPi = Symbol(r'\varpi ')

VAR_GREEK = [
VarEpsilon,
VarTheta,
VarKappa,
VarRho,
VarSigma,
VarPhi,
VarPi,
]

# Hebrew
Aleph = Symbol(r'\aleph ')
Beth = Symbol(r'\beth ')
Daleth = Symbol(r'\daleth ')
Gimel = Symbol(r'\gimel ')

HEBREW = [
Aleph,
Beth,
Daleth,
Gimel,
]

GREEK_HEBREW = LOWER_GREEK + UPPER_GREEK + VAR_GREEK + HEBREW

# Math constructs
Frac = BinaryOperator(r'\frac{{{0}}}{{{1}}}')
Prime = Symbol(r"'")
Sqrt = UnaryOperator(r'\sqrt{{{0}}}')
NSqrt = BinaryOperator(r'\sqrt[{1}]{{{0}}}')
OverLine = UnaryOperator(r'\overline{{{0}}}')
UnderLine = UnaryOperator(r'\underline{{{0}}}')
WideHat = UnaryOperator(r'\widehat{{{0}}}')
WideTilde = UnaryOperator(r'\widetilde{{{0}}}')
OverRightArrow = UnaryOperator(r'\overrightarrow{{{0}}}')
OverLeftArrow = UnaryOperator(r'\overleftarrow{{{0}}}')
OverBrace1 = UnaryOperator(r'\overbrace{{{0}}}')
UnderBrace1 = UnaryOperator(r'\underbrace{{{0}}}')
OverBrace2 = BinaryOperator(r'\overbrace{{{0}}}^{{{1}}}')
UnderBrace2 = BinaryOperator(r'\underbrace{{{0}}}_{{{1}}}')

MATH_CONSTRUCTS = [
Frac,
Prime,
Sqrt,
NSqrt,
OverLine,
UnderLine,
WideHat,
WideTilde,
OverRightArrow,
OverLeftArrow,
OverBrace1,
UnderBrace1,
OverBrace2,
UnderBrace2,
]

# Delimiters
Parenthesis = UnaryOperator(r'\left({0}\right)')
Vert = UnaryOperator(r'\left|{0}\right|')
UpperVert = UnaryOperator(r'\left\|{0}\right\|')
Brackets = UnaryOperator(r'\left\{{{0}\right\}}')
Angle = UnaryOperator(r'\left\langle{0}\right\rangle')
Floor = UnaryOperator(r'\left\lfloor{0}\right\rfloor')
Ceil = UnaryOperator(r'\left\lceil{0}\right\rceil')
Slash = UnaryOperator(r'\left/{0}\right\backslash')
SqBrackets = UnaryOperator(r'\left[{0}\right]')
LCorner = UnaryOperator(r'\left\llcorner{0}\right\lrcorner')
UCorner = UnaryOperator(r'\left\ulcorner{0}\right\urcorner')

DELIMITERS = [
Parenthesis,
Vert,
UpperVert,
Brackets,
Angle,
Floor,
Ceil,
Slash,
SqBrackets,
LCorner,
UCorner,
]

# Variable-size symbols
Sum0 = Symbol(r'\sum ')
Sum1 = UnaryOperator(r'\sum_{{{0}}}')
UpperSum1 = UnaryOperator(r'\sum^{{{0}}}')
Sum2 = BinaryOperator(r'\sum_{{{0}}}^{{{1}}}')
Prod0 = Symbol(r'\prod ')
Prod1 = UnaryOperator(r'\prod_{{{0}}}')
UpperProd1 = UnaryOperator(r'\prod^{{{0}}}')
Prod2 = BinaryOperator(r'\prod_{{{0}}}^{{{1}}}')
CoProd0 = Symbol(r'\coprod ')
CoProd1 = UnaryOperator(r'\coprod_{{{0}}}')
UpperCoProd1 = UnaryOperator(r'\coprod^{{{0}}}')
CoProd2 = BinaryOperator(r'\coprod_{{{0}}}^{{{1}}}')
Int0 = Symbol(r'\int ')
Int1 = UnaryOperator(r'\int_{{{0}}}')
UpperInt1 = UnaryOperator(r'\int^{{{0}}}')
Int2 = BinaryOperator(r'\int_{{{0}}}^{{{1}}}')
OInt0 = Symbol(r'\oint ')
OInt1 = UnaryOperator(r'\oint_{{{0}}}')
UpperOInt1 = UnaryOperator(r'\oint^{{{0}}}')
OInt2 = BinaryOperator(r'\oint_{{{0}}}^{{{1}}}')
IInt0 = Symbol(r'\iint ')
IIInt0 = Symbol(r'\iiint ')
BigUPlus0 = Symbol(r'\biguplus ')
BigUPlus1 = UnaryOperator(r'\biguplus_{{{0}}}')
UpperBigUPlus1 = UnaryOperator(r'\biguplus^{{{0}}}')
BigUPlus2 = BinaryOperator(r'\biguplus_{{{0}}}^{{{1}}}')
BigCap0 = Symbol(r'\bigcap ')
BigCap1 = UnaryOperator(r'\bigcap_{{{0}}}')
UpperBigCap1 = UnaryOperator(r'\bigcap^{{{0}}}')
BigCap2 = BinaryOperator(r'\bigcap_{{{0}}}^{{{1}}}')
BigCup0 = Symbol(r'\bigcup ')
BigCup1 = UnaryOperator(r'\bigcup_{{{0}}}')
UpperBigCup1 = UnaryOperator(r'\bigcup^{{{0}}}')
BigCup2 = BinaryOperator(r'\bigcup_{{{0}}}^{{{1}}}')
BigOPlus0 = Symbol(r'\bigoplus ')
BigOPlus1 = UnaryOperator(r'\bigoplus_{{{0}}}')
UpperBigOPlus1 = UnaryOperator(r'\bigoplus^{{{0}}}')
BigOPlus2 = BinaryOperator(r'\bigoplus_{{{0}}}^{{{1}}}')
BigOTimes = Symbol(r'\bigotimes ')
BigOTimes1 = UnaryOperator(r'\bigotimes_{{{0}}}')
UpperBigOTimes1 = UnaryOperator(r'\bigotimes^{{{0}}}')
BigOTimes2 = BinaryOperator(r'\bigotimes_{{{0}}}^{{{1}}}')
BigODot0 = Symbol(r'\bigodot ')
BigODot1 = UnaryOperator(r'\bigodot_{{{0}}}')
UpperBigODot1 = UnaryOperator(r'\bigodot^{{{0}}}')
BigODot2 = BinaryOperator(r'\bigodot_{{{0}}}^{{{1}}}')
BigVee0 = Symbol(r'\bigvee ')
BigVee1 = UnaryOperator(r'\bigvee_{{{0}}}')
UpperBigVee1 = UnaryOperator(r'\bigvee^{{{0}}}')
BigVee2 = BinaryOperator(r'\bigovee_{{{0}}}^{{{1}}}')
BigWedge0 = Symbol(r'\bigwedge ')
BigWedge1 = UnaryOperator(r'\bigwedge_{{{0}}}')
UpperBigWedge1 = UnaryOperator(r'\bigwedge^{{{0}}}')
BigWedge2 = BinaryOperator(r'\bigwedge_{{{0}}}^{{{1}}}')
BigSqCup0 = Symbol(r'\bigsqcup ')
BigSqCup1 = UnaryOperator(r'\bigsqcup_{{{0}}}')
UpperBigSqCup1 = UnaryOperator(r'\bigsqcup^{{{0}}}')
BigSqCup2 = BinaryOperator(r'\bigsqcup_{{{0}}}^{{{1}}}')

VARIABLE_SIZE1 = [
Sum0,
Sum1,
UpperSum1,
Sum2,
Prod0,
Prod1,
UpperProd1,
Prod2,
CoProd0,
CoProd1,
UpperCoProd1,
CoProd2,
Int0,
Int1,
UpperInt1,
Int2,
OInt0,
OInt1,
UpperOInt1,
OInt2,
IInt0,
IIInt0,
]

VARIABLE_SIZE2 = [
BigUPlus0,
BigUPlus1,
UpperBigUPlus1,
BigUPlus2,
BigCap0,
BigCap1,
UpperBigCap1,
BigCap2,
BigCup0,
BigCup1,
UpperBigCup1,
BigCup2,
BigOPlus0,
BigOPlus1,
UpperBigOPlus1,
BigOPlus2,
BigOTimes,
BigOTimes1,
UpperBigOTimes1,
BigOTimes2,
BigODot0,
BigODot1,
UpperBigODot1,
BigODot2,
BigVee0,
BigVee1,
UpperBigVee1,
BigVee2,
BigWedge0,
BigWedge1,
UpperBigWedge1,
BigWedge2,
BigSqCup0,
BigSqCup1,
UpperBigSqCup1,
BigSqCup2,
]

# Functions
ArcCos = Symbol(r'\arccos ')
ArcSin = Symbol(r'\arcsin ')
ArcTan = Symbol(r'\arctan ')
Arg = Symbol(r'\arg ')
Cos = Symbol(r'\cos ')
CosH = Symbol(r'\cosh ')
CotH = Symbol(r'\coth ')
Csc = Symbol(r'\csc ')
Deg = Symbol(r'\deg ')
Det = Symbol(r'\det ')
Dim = Symbol(r'\dim ')
Exp = Symbol(r'\exp ')
Gcd = Symbol(r'\gcd ')
Hom = Symbol(r'\hom ')
Inf = Symbol(r'\inf ')
Ker = Symbol(r'\ker ')
Lg = Symbol(r'\lg ')
Lim = Symbol(r'\lim ')
LimInf = Symbol(r'\liminf ')
LimSup = Symbol(r'\limsup ')
Ln = Symbol(r'\ln ')
Log = Symbol(r'\log ')
Max = Symbol(r'\max ')
Min = Symbol(r'\min ')
Pr = Symbol(r'\Pr ')
Sec = Symbol(r'\sec ')
Sin = Symbol(r'\sin ')
SinH = Symbol(r'\sinh ')
Sup = Symbol(r'\sup ')
Tan = Symbol(r'\tan ')
TanH = Symbol(r'\tanh ')

FUNCTIONS = [
ArcCos,
ArcSin,
ArcTan,
Arg,
Cos,
CosH,
CotH,
Csc,
Deg,
Det,
Dim,
Exp,
Gcd,
Hom,
Inf,
Ker,
Lg,
Lim,
LimInf,
LimSup,
Ln,
Log,
Max,
Min,
Pr,
Sec,
Sin,
SinH,
Sup,
Tan,
TanH,
]

# Simple operators
Sumation = Symbol(r'+')
Negation = Symbol(r'-')
Not = Symbol(r'\neg ')
Factorial = Symbol(r'!')
Primorial = Symbol(r'\# ')
PlusMinus = Symbol(r'\pm ')
MinusPlus = Symbol(r'\mp ')
Times = Symbol(r'\times ')
Div = Symbol(r'\div ')
Ast = Symbol(r'\ast ')
Start = Symbol(r'\star ')
Dagger = Symbol(r'\dagger ')
DDagger = Symbol(r'\ddagger ')
Cap = Symbol(r'\cap ')
Cup = Symbol(r'\cup ')
UPlus = Symbol(r'\uplus ')
SqCap = Symbol(r'\sqcap ')
SqCup = Symbol(r'\sqcup ')
Vee = Symbol(r'\vee ')
Wedge = Symbol(r'\wedge ')
Cdot = Symbol(r'\cdot ')
Diamond = Symbol(r'\diamond ')
BigTriangleUp = Symbol(r'\bigtriangleup ')
BigTriangleDown = Symbol(r'\bigtriangledown ')
TriangleLeft = Symbol(r'\triangleleft ')
TriangleRight = Symbol(r'\triangleright ')
BigCirc = Symbol(r'\bigcirc ')
Bullet = Symbol(r'\bullet ')
Wr = Symbol(r'\wr ')
OPlus = Symbol(r'\oplus ')
OMinus = Symbol(r'\ominus ')
OTimes = Symbol(r'\otimes ')
OSlash = Symbol(r'\oslash ')
Circ = Symbol(r'\circ ')
SetMinus = Symbol(r'\setminus ')
Amalg = Symbol(r'\amalg ')

BASIC_OPERATORS = [
Sumation,
Negation,
Not,
Factorial,
Primorial,
PlusMinus,
MinusPlus,
Times,
Div,
Ast,
Start,
Dagger,
DDagger,
Cap,
Cup,
UPlus,
SqCap,
SqCup,
Vee,
Wedge,
Cdot,
Diamond,
BigTriangleUp,
BigTriangleDown,
TriangleLeft,
TriangleRight,
BigCirc,
Bullet,
Wr,
OPlus,
OMinus,
OTimes,
OSlash,
Circ,
SetMinus,
Amalg,
] 

# Relation operators
LessThan = Symbol(r'<')
NLessThan = Symbol(r'\nless ')
LessThanEqual = Symbol(r'\leq ')
LessThanEqualSlant = Symbol(r'\leqslant ')
NLessThanEqual = Symbol(r'\nleq ')
NLessThanEqualSlant = Symbol(r'\nleqslant ')
Prec = Symbol(r'\prec ')
NPrec = Symbol(r'\nprec ')
PrecEqual = Symbol(r'\preceq ')
NPrecEqual = Symbol(r'\npreceq ')
LessLess = Symbol(r'\ll ')
LessLessLess = Symbol(r'\lll ')
Subset = Symbol(r'\subset ')
NSubset = Symbol(r'\not\subset ')
SubsetEqual = Symbol(r'\subseteq ')
NSubsetEqual = Symbol(r'\nsubseteq ')
SqSubset = Symbol(r'\sqsubset ')
SqSubsetEqual = Symbol(r'\sqsubseteq ')

GreaterThan = Symbol(r'>')
NGreaterThan = Symbol(r'\ngtr ')
GreaterThanEqual = Symbol(r'\geq ')
GreaterThanEqualSlant = Symbol(r'\geqslant ')
NGreaterThanEqual = Symbol(r'\ngeq ')
NGreaterThanEqualSlant = Symbol(r'\ngeqslant ')
Succ = Symbol(r'\succ ')
NSucc = Symbol(r'\nsucc ')
SuccEqual = Symbol(r'\succeq ')
NSuccEqual = Symbol(r'\nsucceq ')
GreaterGreater = Symbol(r'\gg ')
GreaterGreaterGreater = Symbol(r'\ggg ')
Supset = Symbol(r'\supset ')
NSupset = Symbol(r'\not\supset ')
SupsetEqual = Symbol(r'\supseteq ')
NSupsetEqual = Symbol(r'\nsupseteq ')
SqSupset = Symbol(r'\sqsupset ')
SqSupsetEqual = Symbol(r'\sqsupseteq ')
Equal = Symbol(r'=')
DotEqual = Symbol(r'\doteq ')
Equiv = Symbol(r'\equiv ')
Approx = Symbol(r'\approx ')
Cong = Symbol(r'\cong ')
Simeq = Symbol(r'\simeq ')
Sim = Symbol(r'\sim ')
Propto = Symbol(r'\propto ')
NotEqual = Symbol(r'\ne ')

Parallel = Symbol(r'\parallel ')
NParallel = Symbol(r'\nparallel ')
Asymp = Symbol(r'\asymp ')
Bowtie = Symbol(r'\bowtie ')
VDash = Symbol(r'\vdash ')
DashV = Symbol(r'\dashv ')
In = Symbol(r'\in ')
Ni = Symbol(r'\ni ')
NotIn = Symbol(r'\notin ')
Smile = Symbol(r'\smile ')
Frown = Symbol(r'\frown ')
Models = Symbol(r'\models ')
Perp = Symbol(r'\perp ')
Mid = Symbol(r'\mid ')


RELATIONS = [
LessThan,
NLessThan,
LessThanEqual,
LessThanEqualSlant,
NLessThanEqual,
NLessThanEqualSlant,
Prec,
NPrec,
PrecEqual,
NPrecEqual,
LessLess,
LessLessLess,
Subset,
NSubset,
SubsetEqual,
NSubsetEqual,
SqSubset,
SqSubsetEqual,
GreaterThan,
NGreaterThan,
GreaterThanEqual,
GreaterThanEqualSlant,
NGreaterThanEqual,
NGreaterThanEqualSlant,
Succ,
NSucc,
SuccEqual,
NSuccEqual,
GreaterGreater,
GreaterGreaterGreater,
Supset,
NSupset,
SupsetEqual,
NSupsetEqual,
SqSupset,
SqSupsetEqual,
Equal,
DotEqual,
Equiv,
Approx,
Cong,
Simeq,
Sim,
Propto,
NotEqual,
Parallel,
NParallel,
Asymp,
Bowtie,
VDash,
DashV,
In,
Ni,
NotIn,
Smile,
Frown,
Models,
Perp,
Mid,
]

Square = Symbol(r'\square ')

Vec = UnaryOperator(r'\vec{{{0}}}')
Edit = UnaryOperator(r'\boxed{{{0}}}')

Pow = BinaryOperator(r'{{{0}}}^{{{1}}}')
Juxt = BinaryOperator(r'{0} {1}')

Cdots = Symbol(r'\cdots ')

# Use these operators in the code, so it will be easy to change their value
# in next releases
SelArg = Cdots
NewArg = Square

