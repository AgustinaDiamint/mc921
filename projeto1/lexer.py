import ply.lex as lex


class UCLexer:
    """ A lexer for the uC language. After building it, set the
        input text with input(), and call token() to get new
        tokens.
    """

    def __init__(self, error_func, debug=False, debuglog=None):
        """ Create a new Lexer.
            An error function. Will be called with an error
            message, line and column as arguments, in case of
            an error during lexing.
        """
        self.error_func = error_func
        self.filename = ""

        # Keeps track of the last token returned from self.token()
        self.last_token = None

    def build(self, **kwargs):
        """ Builds the lexer from the specification. Must be
            called after the lexer object is created.

            This method exists separately, because the PLY
            manual warns against calling lex.lex inside __init__
        """
        self.lexer = lex.lex(object=self, **kwargs)

    def reset_lineno(self):
        """ Resets the internal line number counter of the lexer.
        """
        self.lexer.lineno = 1

    def input(self, text):
        self.lexer.input(text)

    def token(self):
        self.last_token = self.lexer.token()
        return self.last_token

    def find_tok_column(self, token):
        """ Find the column of the token in its line.
        """
        last_cr = self.lexer.lexdata.rfind("\n", 0, token.lexpos)
        return token.lexpos - last_cr

    # Internal auxiliary methods
    def _error(self, msg, token):
        location = self._make_tok_location(token)
        self.error_func(msg, location[0], location[1])
        self.lexer.skip(1)

    def _make_tok_location(self, token):
        return (token.lineno, self.find_tok_column(token))

    # Reserved keywords
    keywords = (
        "ASSERT",
        "BREAK",
        "CHAR",
        "ELSE",
        "FLOAT",
        "FOR",
        "IF",
        "INT",
        "PRINT",
        "READ",
        "RETURN",
        "VOID",
        "WHILE",
    )

    keyword_map = {}
    for keyword in keywords:
        keyword_map[keyword.lower()] = keyword

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

    constants = ("ICONST", "FCONST", "CCONST")

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
        "UNMATCHEDQUOTE",
        "ERROR",
        "CCOMMENT",
        "CPPCOMMENT",
        "UNTERMCOMMENT",
        "COMMA",
    )

    tokens = keywords + operators + constants + assigments + others

    # Regexes

    def t_CCOMMENT(self, t):
        r"/\*(.|\n)*?\*/"
        t.lexer.lineno += t.value.count("\n")

    def t_UNTERMCOMMENT(self, t):
        r"/\*(.|\n)*"
        print("%d: Unterminated Comment" % t.lexer.lineno)

    def t_STRING_LITERAL(self, t):
        r"\"(.|\n)*?\""
        return t

    def t_UNMATCHEDQUOTE(self, t):
        r"\"(.|\n)*"
        print("%d: Unmatched Quote " % t.lexer.lineno)

    def t_CPPCOMMENT(self, t):
        r"//.*"
        pass

    t_ICONST = r"[0-9]+"
    t_FCONST = r"([0-9]+\.[0-9]*)|([0-9]*\.[0-9]+)"
    t_CCONST = r"[a-zA-Z]"

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

    def t_COMMA(self, t):
        r","
        return t

    def t_ID(self, t):
        r"[a-zA-Z_][a-zA-Z_0-9]*"
        t.type = self.keyword_map.get(t.value, "ID")  # Check for reserved words
        return t

    # Ignored characters
    t_ignore = r" "

    def t_newline(self, t):
        r"\n+"
        t.lexer.lineno += t.value.count("\n")

    def t_error(self, t):
        msg = "Illegal character '%s'" % t.value[0]
        self._error(msg, t)

    # Scanner (used only for test)ß
    def scan(self, data):
        self.lexer.input(data)
        while True:
            tok = self.lexer.token()
            if not tok:
                break
            print(tok)


if __name__ == "__main__":

    import sys

    def print_error(msg, x, y):
        print("Lexical error: %s at %d:%d" % (msg, x, y))

    m = UCLexer(print_error)
    m.build()  # Build the lexer
    m.scan(open(sys.argv[1]).read())  # print tokens
