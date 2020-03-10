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
    "ERROR",
    "CCOMMENT",
    "CPPCOMMENT",
)
tokens = types + reserved + operators + constants + assigments + others
# reserved words
t_FOR = r"for"
t_WHILE = r"while"
t_IF = r"IF"
t_ASSERT = r"assert"
t_PRINT = r"print"
t_READ = r"read"
t_BREAK = r"break"
t_RETURN = r"return"
t_VOID = r"void"
t_CHAR = r" char"
t_INT = r"int"
t_FLOAT = r"float"


t_CCOMMENT = r"/\*(.|\n)*?\*/"
t_CPPCOMMENT = r"//.*"

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
t_DIFF = "\!\="
t_AND = "\&\&"
t_OR = r"\|\|"
t_PP = r"\+\+"
t_MM = r"\-\-"
t_ADDRESS = r"\&"


# Ignored characters
t_ignore = " \t"


def t_newline(t):
    r"\n+"
    t.lexer.lineno += t.value.count("\n")


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


# Build the lexer
from ply import lex

lexer = lex.lex()
lexer.input(
    "/* comment */ int j = 3; int main () {  int i = j;int k = 3;int p = 2 * j; assert p == 2 * i;}"
)
for tok in iter(lexer.token, None):
    print(tok.type + tok.value)
