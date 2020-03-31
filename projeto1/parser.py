import ply.yacc as yacc
from lexer import UCLexer


class UCParser:
    def __init__(self, error_func):
        self.start = "program"
        self.error_func = error_func
        self.lexer = UCLexer(error_func)
        self.lexer.build()

        self.tokens = self.lexer.tokens
        self.parser = yacc.yacc(module=self)

    def p_empty(self, p):
        """empty : """
        p[0] = None

    def p_program(self, p):
        """ program  : global_declaration_list
        """
        p[0] = ("program", p[1])

    def p_global_declaration_list(self, p):
        """ global_declaration_list : global_declaration
                                    | global_declaration_list global_declaration
        """
        p[0] = [p[1]] if len(p) == 2 else p[1] + [p[2]]

    def p_global_declaration(self, p):
        """global_declaration : function_definition
                              | declaration 
        """
        p[0] = p[1]

    def p_function_defnition(self, p):
        """ function_definition : type_specifier_opt declarator declaration_list_opt compound_statement """
        p[0] = ( p[1], p[2], p[3], p[4])

    def p_type_specifier(self, p):
        """ type_specifier : VOID
                           | CHAR
                           | INT
                           | FLOAT
        """
        p[0] = p[1]

    def p_type_specifier_opt(self, p):
        """type_specifier_opt : type_specifier
                             | empty
        """
        p[0] = p[1]

    def p_declarator(self, p):
        """ declarator : pointer direct_declarator
                        | direct_declarator
        """
        p[0] = [p[1]] if len(p) == 2 else p[1] + [p[2]]

    def p_pointer(self, p):
        """ pointer : TIMES pointer_opt
        """
        p[0] = (p[1], p[2])

    def p_pointer_opt(self, p):
        """pointer_opt : pointer
                      | empty
        """
        p[0] = p[1]

    def p_direct_declarator(self, p):
        """ direct_declarator : ID
                      | LPAREN declarator RPAREN
                      | direct_declarator LBRACE constant_exp_opt RBRACE
                      | direct_declarator LPAREN parameter_list RPAREN
                      | direct_declarator LPAREN identifier_list_opt RPAREN
        """
        if len(p) == 2:
            p[0] = p[1]
        elif len(p) == 4:
            p[0] = p[2]
        else:
            p[0] = (p[1], p[3])

    def p_constant_expression(self, p):
        """ constant_expression : expr """
        p[0] = p[1]

    def p_constant_exp_opt(self, p):
        """ constant_exp_opt : constant_expression
                            | empty
        """
        p[0] = p[1]

    def p_identifier_list(self, p):
        """ identifier_list : identifier_list ID
                            | ID
        """
        p[0] = [p[1]] if len(p) == 2 else p[1] + [p[2]]

    def p_identifier_list_opt(self, p):
        """ identifier_list_opt : identifier_list
                                | empty
        """
        p[0] = p[1]

    def p_expr(self, p):
        """
        expr :  cast_expression
                | expr PLUS expr
                | expr MINUS expr
                | expr TIMES expr
                | expr DIVIDE expr
                | expr EQUALS expr
                | expr MOD expr
                | expr GT expr
                | expr GET expr
                | expr LT expr
                | expr LET expr
                | expr DIFF expr
                | expr AND expr
                | expr OR expr
        """
        p[0] = p[1] if len(p) == 2 else (p[2], p[1], p[3])

    def p_cast_expression(self, p):
        """
        cast_expression : unary_expression
                    | LPAREN type_specifier RPAREN cast_expression
        """
        p[0] = p[1] if len(p) == 2 else (p[2], p[4])

    def p_unary_expression(self, p):
        """
        unary_expression : postfix_expression
                        | PP unary_expression
                        | MM unary_expression
                        | unary_operator cast_expression
        """
        p[0] = p[1] if len(p) == 2 else (p[1], p[2])

    def p_postfix_expression(self, p):
        """
        postfix_expression : primary_expression
                            | postfix_expression LBRACE expression RBRACE
                            | postfix_expression LPAREN assignment_expression_opt RPAREN
                            | postfix_expression PP
                            | postfix_expression MM
        """
        if len(p) == 2:
            p[0] = p[1]
        elif len(p) == 5:
            p[0] = (p[1], [3])
        else:
            p[0] = (p[1], p[2])

    def p_primary_expression(self, p):
        """
        primary_expression : ID
                            | constant
                            | STRING_LITERAL
                            | LPAREN expression RPAREN
        """
        p[0] = p[1] if len(p) == 2 else p[2]


    def p_constant(self, p):
        """ constant : ICONST
                    | FCONST
        """
        p[0] = p[1]

    def p_expression(self, p):
        """ expression : assignment_expression
                        | expression COMMA assignment_expression
        """
        p[0] = p[1] if len(p) == 2 else (p[1], p[2])

    def p_expression_opt(self, p):
        """ expression_opt : expression
                            | empty
        """
        p[0] = p[1]

    def p_assignment_expression(self, p):
        """assignment_expression : expr
                            | unary_expression assignment_operator assignment_expression
        """
        p[0] = p[1] if len(p) == 2 else (p[1], p[2], p[3])

    def p_assignment_expression_opt(self, p):
        """ assignment_expression_opt : assignment_expression
                                        | empty
        """
        p[0] = p[1]

    def p_argument_expression(self, p):
        """argument_expression : assignment_expression
                            | argument_expression COMMA assignment_expression
        """
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = (p[1], p[3])

    def p_assignment_operator(self, p):
        """ assignment_operator : ASSIGN
                                | TASSIGN
                                | DASSIGN
                                | MODASSIGN
                                | PASSIGN
                                | MINASSIGN
        """
        p[0] =  p[1]

    def p_unary_operator(self, p):
        """unary_operator : AND
                    | TIMES
                    | PLUS
                    | MINUS
                    | NOT
        """
        p[0] = ("unary operator", p[1])

    def p_parameter_list(self, p):
        """parameter_list : parameter_declaration
                        | parameter_list COMMA parameter_declaration
        """
        p[0] = p[1] if len(p) == 2 else (p[1], p[3])

    def p_parameter_declaration(self, p):
        """ parameter_declaration : type_specifier declarator
        """
        p[0] = (p[1], p[2])

    def p_declaration(self, p):

        """declaration : type_specifier init_declarator_list_opt SEMI 
        """
        p[0] = (p[1], p[2])

    def p_declaration_list(self, p):
        """ declaration_list : declaration
                    | declaration_list declaration
        """
        p[0] = [p[1]] if len(p) == 2 else p[1] + [p[2]]

    def p_declaration_list_opt(self, p):
        """ declaration_list_opt : declaration_list
                                | empty
        """
        p[0] = p[1]

    def p_init_declarator(self, p):
        """init_declarator : declarator
                            | declarator ASSIGN initializer
        """
        p[0] = p[1] if len(p) == 2 else (p[1], p[3])
    
    def p_init_declarator_list(self, p):
        """ init_declarator_list : init_declarator
                                | init_declarator_list COMMA init_declarator
        """
        p[0] = [p[1]] if len(p) == 2 else p[1] + [p[2]]
    
    def p_init_declarator_list_opt(self,p):
        """ init_declarator_list_opt : init_declarator_list
                                    | empty
        """
        p[0] = p[1]


    def p_initializer(self, p):
        """initializer : assignment_expression
                    | LBRACK initializer_list RBRACK
                    | LBRACK initializer_list COMMA RBRACK
        """
        p[0] = p[1] if len(p) == 2 else p[3]

    def p_initializer_list(self, p):
        """ initializer_list : initializer
                    | initializer_list COMMA initializer
        """
        p[0] = p[1] if len(p) == 2 else p[1] + [p[3]]

    def p_compound_statement(self, p):
        """compound_statement : LBRACK declaration_list_opt statement_list_opt RBRACK
        """
        p[0] = (p[2], p[3])

    def p_statement(self, p):
        """
        statement : expression_statement
                | compound_statement
                | selection_statement
                | iteration_statement
                | jump_statement
                | assert_statement
                | print_statement
                | read_statement
        """
        p[0] = p[1]

    def p_expression_statement(self, p):
        """
        expression_statement : expression_opt SEMI
        """
        p[0] = p[1]

    def p_selection_statement(self, p):
        """    selection_statement : IF LPAREN expression RPAREN statement
                                    | IF LPAREN expression RPAREN statement ELSE statement
        """
        p[0] = ("IF", p[3], p[4]) if len(p) == 5 else ("IF", p[3], p[5], "else", p[7])

    def p_iteration_statement(self, p):
        """    iteration_statement : WHILE LPAREN expression RPAREN statement
                                    | FOR LPAREN expression_opt SEMI expression_opt SEMI expression_opt RPAREN statement
        """
        if len(p) == 6:
            p[0] = ("WHILE", p[3], p[5])
        else:
            p[0] = ("FOR", p[3], p[5], p[7], p[9])

    def p_jump_statement(self, p):
        """jump_statement : BREAK SEMI
                        | RETURN expression_opt SEMI
        """
        p[0] = (p[1], p[2])

    def p_assert_statement(self, p):
        """ assert_statement : ASSERT expr SEMI """
        p[0] = ("assert", p[1])

    def p_print_statement(self, p):
        """ print_statement : PRINT LPAREN expr RPAREN SEMI 
        """
        p[0] = ("print", p[3])

    def p_read_statement(self, p):
        """read_statement : READ LPAREN argument_expression RPAREN SEMI"""
        p[0] = ("READ", p[2])

    def p_statement_list(self, p):
        """ statement_list : statement_list statement
                    | statement
        """
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[2]]

    def p_statement_list_opt(self, p):
        """ statement_list_opt : statement_list
                                | empty
        """
        p[0] = p[1]

    def p_assign_statement(self, p):
        """ statement : ID ASSIGN expr
        """
        p[0] = ("assign", p[1], p[3])

    def p_compound_expr(self, p):
        """ expr : LPAREN expr RPAREN
        """
        p[0] = p[2]
    
    precedence = (
    ('left', 'PLUS'),
    ('left', 'MINUS'),
    ('left', 'TIMES'),
    ('left', 'DIVIDE')
    )

if __name__ == "__main__":

    import sys

    def print_error(msg, x, y):
        print("Lexical error: %s at %d:%d" % (msg, x, y))

    parser = UCParser(print_error)
    parser.parser.parse(open(sys.argv[1]).read())  # print tokens