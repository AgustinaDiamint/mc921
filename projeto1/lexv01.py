types = ("VOID", "CHAR", "INT", "FLOAT")

reserved = ("FOR", "WHILE", "IF", "ASSERT", "PRINT", "READ", "BREAK", "RETURN")

operators = (
    "PLUS",
    "MINUS",
    "TIMES",
    "DIVIDE",
    "EQUALS",
    "MOD",
    "GT",
    "GET",
    "LT",
    "LET",
    "DIFF",
    "AND",
    "OR",
    "PP",
    "MM",
    "ADDRESS",
    "NOT",
)

constants = ("ICONST", "FCONST")

assigments = ("ASSIGN", "TASSIGN", "DASSIGN", "MODASSIGN", "PASSIGN", "MINASSIGN")

others = (
    "ID",
    "LPAREN",
    "RPAREN",
    "RBRACE",
    "LBRACE",
    "RBRACK",
    "LBRACK",
    "SEMI",
    "STRING_LITERAL",
    "UNMATCHEDQUOTE" "ERROR",
    "CCOMMENT",
    "CPPCOMMENT",
    "UNTERMCOMMENT",
    "COMMA",
)

tokens = types + reserved + operators + constants + assigments + others

# REGEX
# reserved words
reserved = {
    "if": "IF",
    "then": "THEN",
    "else": "ELSE",
    "for": "FOR",
    "while": "WHILE",
    "assert": "ASSERT",
    "print": "PRINT",
    "read": "READ",
    "break": "BREAK",
    "return": "RETURN",
    "void": "VOID",
    "char": "CHAR",
    "int": "INT",
    "float": "FLOAT",
}


def t_CCOMMENT(t):
    r"/\*(.|\n)*?\*/"
    t.lexer.lineno += t.value.count("\n")


def t_UNTERMCOMMENT(t):
    r"/\*(.|\n)*"
    print("%d: Unterminated Comment" % t.lexer.lineno)


def t_STRING_LITERAL(t):
    r"\"(.|\n)*?\""
    return t


def t_UNMATCHEDQUOTE(t):
    r"\"(.|\n)*"
    print("%d: Unmatched Quote " % t.lexer.lineno)


def t_CPPCOMMENT(t):
    r"//.*"
    pass


t_ICONST = r"[0-9]+"
t_FCONST = r"([0-9]+\.[0-9]*)|([0-9]*\.[0-9]+)"


t_ASSIGN = r"\="
t_TASSIGN = r"\*\="
t_DASSIGN = r"\/\="
t_MODASSIGN = r"\%\="
t_PASSIGN = r"\+\="
t_MINASSIGN = r"\-\="

t_LPAREN = r"\("
t_RPAREN = r"\)"
t_LBRACE = r"\{"
t_RBRACE = r"\}"
t_LBRACK = r"\["
t_RBRACK = r"\]"
t_SEMI = r"\;"


t_PLUS = r"\+"
t_MINUS = r"-"
t_TIMES = r"\*"
t_DIVIDE = r"/"
t_EQUALS = r"\=\="
t_MOD = r"\%"
t_GT = r">"
t_GET = r">\="
t_LT = r"<"
t_LET = r"<\="
t_DIFF = r"\!\="
t_AND = r"\&\&"
t_OR = r"\|\|"
t_PP = r"\+\+"
t_MM = r"\-\-"
t_ADDRESS = r"\&"
t_NOT = r"\!"


def t_COMMA(t):
    r","
    return t


def t_ID(t):
    r"[a-zA-Z_][a-zA-Z_0-9]*"
    t.type = reserved.get(t.value, "ID")  # Check for reserved words
    return t


# Ignored characters
t_ignore = r" \t"


def t_newline(t):
    r"\n+"
    t.lexer.lineno += t.value.count("\n")


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


# Build the lexer
from ply import lex

lexer = lex.lex()

with open("projeto1/teste1") as f:
    read_data = f.read()

# sentence = "/* comment */ int j = 3; int main () {  int i = j;int k = 3;int p = 2 * j; assert p == 2 * i;}  /* asdasdas "

# Give the lexer some input
lexer.input(read_data)

# Tokenize
while True:
    tok = lexer.token()
    if not tok:
        break  # No more input
    print(tok)
