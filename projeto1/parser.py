import ply.yacc as yacc
from lexer import UCLexer
import ast


def print_error(msg, x, y):
    print("Lexical error: %s at %d:%d" % (msg, x, y))


class UCParser:
    def __init__(self):
        # initial state
        self.start = "program"

        # lexer
        self.lexer = UCLexer(print_error)
        self.lexer.build()
        self.tokens = self.lexer.tokens

        self.parser = yacc.yacc(module=self, start=self.start, debug=True)

    def parse(self, input, ast_file, debug=False):
        return self.parser.parse(input, debug=debug)

    def p_empty(self, p):
        """empty : """
        p[0] = None

    def p_program(self, p):
        """ program  : global_declaration_list
        """
        p[0] = ast.Program(p[1], coord=_token_coord(self, p, 1))

    def p_global_declaration_list(self, p):
        """ global_declaration_list : global_declaration
                                    | global_declaration_list global_declaration
        """
        p[0] = [p[1]] if len(p) == 2 else p[1] + [p[2]]

    def p_global_declaration(self, p):
        """global_declaration : function_definition
                              | declaration
        """
        p[0] = ast.GlobalDecl(p[1], coord=_token_coord(self, p, 1))

    def p_function_definition(self, p):
        """ function_definition : type_specifier declarator declaration_list_opt compound_statement """
        p[0] = ast.FuncDef(p[1], p[2], p[3], p[4], coord=_token_coord(self, p, 1))

    def p_type_specifier(self, p):
        """ type_specifier : VOID
                           | CHAR
                           | INT
                           | FLOAT
        """
        p[0] = ast.Type(p[1], coord=_token_coord(self, p, 1)) if len(p) == 2 else None

    def p_declarator(self, p):
        """ declarator : pointer direct_declarator
                        | direct_declarator
        """
        p[0] = (
            p[1]
            if len(p) == 2
            else ast.PtrDecl(p[1], p[2], coord=_token_coord(self, p, 1))
        )

    def p_pointer(self, p):
        """ pointer : TIMES pointer_opt
        """
        p[0] = p[2]

    def p_pointer_opt(self, p):
        """pointer_opt : pointer
                      | empty
        """
        p[0] = p[1]

    def p_direct_declarator_1(self, p):
        """ direct_declarator : identifier
                              | LPAREN declarator RPAREN
        """
        if len(p) == 2:
            p[0] = ast.VarDecl(None, p[1], coord=_token_coord(self, p, 1))
        elif len(p) == 3:
            p[0] = p[2]
    # TODO arraydecl(type = direct_declarator)
    def p_direct_declarator_2(self, p):
        """ direct_declarator : direct_declarator LBRACK constant_expression_opt RBRACK
        """
        p[0] = ast.ArrayDecl(p[3], coord=_token_coord(self, p, 1))

    def p_direct_declarator_3(self, p):
        """ direct_declarator : direct_declarator LPAREN parameter_list RPAREN
                              | direct_declarator LPAREN identifier_list_opt RPAREN
        """
        p[0] = ast.FuncDecl(p[3], None, coord=_token_coord(self, p, 1))

    def p_constant_expression(self, p):
        """ constant_expression : expr """
        p[0] = p[1]

    def p_constant_expression_opt(self, p):
        """ constant_expression_opt : constant_expression
                                    | empty
        """
        p[0] = p[1] if len(p) == 2 else None

    def p_identifier(self, p):
        """ identifier : ID """
        p[0] = ast.ID(p[1], coord=_token_coord(self, p, 1))

    def p_identifier_list(self, p):
        """ identifier_list : identifier_list identifier
                            | identifier
        """
        p[0] = [p[1]] if len(p) == 2 else p[1] + [p[2]]

    def p_identifier_list_opt(self, p):
        """ identifier_list_opt : identifier_list
                                | empty
        """
        p[0] = p[1] if len(p) == 2 else None

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
        p[0] = (
            (p[1])
            if len(p) == 2
            else ast.BinaryOp(p[2], p[1], p[3], coord=_token_coord(self, p, 2))
        )

    def p_cast_expression(self, p):
        """
        cast_expression : unary_expression
                        | LPAREN type_specifier RPAREN cast_expression
        """
        p[0] = (
            p[1]
            if len(p) == 2
            else ast.Cast(p[2], p[4], coord=_token_coord(self, p, 2))
        )

    def p_unary_expression_1(self, p):
        """
        unary_expression : postfix_expression
                         | unary_operator cast_expression
        """
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = ast.UnaryOp(p[1], p[2], coord=_token_coord(self, p, 1))

    def p_unary_expression_2(self, p):
        """unary_expression : PP unary_expression  """
        p[0] = ast.UnaryOp(p[1], p[2], coord=_token_coord(self, p, 2))

    def p_unary_expression_3(self, p):
        """
        unary_expression : MM unary_expression
        """
        p[0] = ast.UnaryOp(p[1], p[2], coord=_token_coord(self, p, 2))

    def p_postfix_expression_1(self, p):
        """
        postfix_expression : primary_expression
                           | postfix_expression LPAREN argument_expression RPAREN
                           | postfix_expression LPAREN RPAREN

        """
        if len(p) == 2:
            p[0] = p[1]
        elif len(p) == 4:
            p[0] = ast.FuncCall(p[1], None, coord=_token_coord(self, p, 1))
        elif len(p) == 5:
            p[0] = ast.FuncCall(p[1], p[3], coord=_token_coord(self, p, 1))

    def p_postfix_expression_2(self, p):
        """
        postfix_expression : postfix_expression MM
                           | postfix_expression PP
        """
        p[0] = ast.UnaryOp("p" + p[2], p[1], coord=_token_coord(self, p, 1))

    def p_postfix_expression_3(self, p):
        """
        postfix_expression : postfix_expression LBRACK expression RBRACK
        """
        p[0] = ast.ArrayRef(p[1], p[3], coord=_token_coord(self, p, 1))

    def p_primary_expression_1(self, p):
        """
        primary_expression : identifier
        """
        p[0] = p[1]

    def p_primary_expression_2(self, p):
        """
        primary_expression : constant
        """
        p[0] = p[1]

    def p_primary_expression_3(self, p):
        """
        primary_expression : STRING_LITERAL
        """
        p[0] = ast.Constant("string", p[1], coord=_token_coord(self, p, 1))

    def p_primary_expression_4(self, p):
        """
        primary_expression : LPAREN expression RPAREN
        """
        p[0] = p[2]

    def p_constant_1(self, p):
        """ constant : ICONST
        """
        p[0] = ast.Constant("int", p[1], coord=_token_coord(self, p, 1))

    def p_constant_2(self, p):
        """ constant : FCONST
        """
        p[0] = ast.Constant("float", p[1], coord=_token_coord(self, p, 1))

    def p_expression(self, p):
        """ expression : assignment_expression
                       | assignment_expression COMMA expression
        """
        if len(p) == 2:
            p[0] = ast.ExprList([p[1]], coord=_token_coord(self, p, 1))
        else:
            if isinstance(p[1], ast.ExprList):
                p[1].expr.append(p[3])
                p[0] = ast.ExprList(p[1].expr, coord=_token_coord(self, p, 1))
            else:
                p[1] = ast.ExprList([p[1]], coord=_token_coord(self, p, 1))
                p[1].expr.append(p[3])
                p[0] = ast.ExprList(p[1].expr, coord=_token_coord(self, p, 1))

    def p_expression_opt(self, p):
        """ expression_opt : expression
                           | empty
        """
        p[0] = p[1]

    def p_assignment_expression(self, p):
        """assignment_expression : expr
                                 | unary_expression assignment_operator assignment_expression
        """
        p[0] = (
            p[1]
            if len(p) == 2
            else ast.Assignment(p[2], p[1], p[3], coord=_token_coord(self, p, 2))
        )

    def p_argument_expression(self, p):
        """argument_expression : assignment_expression
                               | argument_expression COMMA assignment_expression
        """
        if len(p) == 2:
            p[0] = ast.ExprList([p[1]], coord=_token_coord(self, p, 1))
        else:
            if isinstance(p[1], ast.ExprList):
                p[1].expr.append(p[3])
                p[0] = ast.ExprList(p[1].expr, coord=_token_coord(self, p, 1))
            else:
                p[1] = ast.ExprList([p[1]], coord=_token_coord(self, p, 1))
                p[1].expr.append(p[3])
                p[0] = ast.ExprList(p[1].expr, coord=_token_coord(self, p, 1))

    def p_assignment_operator(self, p):
        """ assignment_operator : ASSIGN
                                | TASSIGN
                                | DASSIGN
                                | MODASSIGN
                                | PASSIGN
                                | MINASSIGN
        """
        p[0] = p[1]

    def p_unary_operator(self, p):
        """unary_operator : ADDRESS
                          | TIMES
                          | PLUS
                          | MINUS
                          | NOT
        """
        p[0] = p[1]

    def p_parameter_list(self, p):
        """parameter_list : parameter_declaration
                          | parameter_list COMMA parameter_declaration
        """
        p[0] = (
            [p[1]]
            if len(p) == 2
            else ast.ParamList(p[1] + [p[3]], coord=_token_coord(self, p, 3))
        )

    def p_parameter_declaration(self, p):
        """ parameter_declaration : type_specifier declarator
        """
        p[0] = ast.FuncDecl(type=p[2], args=p[1], coord=_token_coord(self, p, 1))

    def p_declaration(self, p):
        """declaration : type_specifier init_declarator_list SEMI
        """
        p[0] = self._build_declarations(p[1], p[2])

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
        p[0] = {"decl" : p[1]} if len(p) == 2 else { "decl": p[1], "init": p[3]}

    def p_init_declarator_list(self, p):
        """ init_declarator_list : init_declarator
                                 | init_declarator_list COMMA init_declarator
        """
        p[0] = [p[1]] if len(p) == 2 else p[1] + [p[3]]

    def p_initializer(self, p):
        """initializer : assignment_expression
                       | LBRACE initializer_list RBRACE
                       | LBRACE initializer_list COMMA RBRACE
        """
        p[0] = p[1] if len(p) == 2 else p[2]

    def p_initializer_list(self, p):
        """ initializer_list : initializer
                             | initializer_list COMMA initializer
        """
        if len(p) == 2:
            p[0] = ast.InitList([p[1]], coord=_token_coord(self, p, 1))
        else:
            p[1].initializer.append(p[3])
            p[0] = ast.InitList(p[1].initializer, coord=_token_coord(self, p, 1))

    def p_compound_statement(self, p):
        """compound_statement : LBRACE declaration_list_opt statement_list_opt RBRACE
        """
        p[0] = ast.Compound(p[2], p[3], coord=_token_coord(self, p, 1))

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
        p[0] = (
            ast.If(p[3], p[5], None, coord=_token_coord(self, p, 1))
            if len(p) == 5
            else ast.If(p[3], p[5], p[7], coord=_token_coord(self, p, 1))
        )

    def p_iteration_statement(self, p):
        """    iteration_statement : WHILE LPAREN expression RPAREN statement
                                    | FOR LPAREN expression_opt SEMI expression_opt SEMI expression_opt RPAREN statement
                                    | FOR LPAREN declaration expression_opt SEMI expression_opt RPAREN statement
        """
        if len(p) == 6:
            p[0] = ast.While(p[3], p[5], coord=_token_coord(self, p, 1))
        elif len(p) == 10:
            p[0] = ast.For(p[3], p[5], p[7], p[9], coord=_token_coord(self, p, 1))
        else:
            p[0] = ast.For(p[3], p[4], p[6], p[8], coord=_token_coord(self, p, 1))

    def p_jump_statement_1(self, p):
        """
        jump_statement : BREAK SEMI
        """
        p[0] = ast.Break(coord=_token_coord(self, p, 2))

    def p_jump_statement_2(self, p):
        """
        jump_statement : RETURN expression_opt SEMI
        """
        if len(p) == 3:
            p[0] = ast.Return(None, coord=_token_coord(self, p, 1))
        else:
            p[0] = ast.Return(p[2], coord=_token_coord(self, p, 1))

    def p_assert_statement(self, p):
        """ assert_statement : ASSERT expr SEMI """
        p[0] = ast.Assert(p[2], coord=_token_coord(self, p, 2))

    def p_print_statement(self, p):
        """ print_statement : PRINT LPAREN expression_opt RPAREN SEMI
        """
        p[0] = ast.Print(p[3], coord=_token_coord(self, p, 3))

    def p_read_statement(self, p):
        """read_statement : READ LPAREN argument_expression RPAREN SEMI"""
        p[0] = ast.Read(p[3], coord=_token_coord(self, p, 2))

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
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = ast.EmptyStatement(coord=_token_coord(self, p, 0))

    def p_error(self, p):
        pass

    precedence = (
        ("left", "OR"),
        ("left", "AND"),
        ("left", "EQUALS", "DIFF"),
        ("left", "GT", "GET", "LT", "LET"),
        ("left", "PLUS", "MINUS"),
        ("left", "TIMES", "DIVIDE", "MOD"),
    )

    def _build_declarations(self, spec, decls):
        """
        Builds a list of declarations all sharing the given specifiers.
        """
        declarations = []

        for decl in decls:
            assert decl["decl"] is not None
            declaration = ast.Decl(
                name=None,
                type=decl["decl"],
                init=decl.get("init"),
                coord=decl["decl"].coord,
            )

            fixed_decl = self._fix_decl_name_type(declaration, spec)
            declarations.append(fixed_decl)

        return declarations

    def _fix_decl_name_type(self, decl, typename):
        """ Fixes a declaration. Modifies decl.
            """
        # Reach the underlying basic type
        type = decl
        while not isinstance(type, ast.VarDecl):
            type = type.type

        decl.name = type.declname

        # The typename is a list of types. If any type in this
        # list isn't an Type, it must be the only
        # type in the list.
        # If all the types are basic, they're collected in the
        # Type holder.
        for tn in typename:
            if not isinstance(tn, ast.Type):
                if len(typename) > 1:
                    self._parse_error("Invalid multiple types specified", tn.coord)
                else:
                    type.type = tn
                    return decl

        if not typename:
            # Functions default to returning int
            if not isinstance(decl.type, ast.FuncDecl):
                self._parse_error("Missing type in declaration", decl.coord)
            type.type = ast.Type(["int"], coord=decl.coord)
        else:
            # At this point, we know that typename is a list of Type
            # nodes. Concatenate all the names into a single list.
            type.type = ast.Type([typename.names[0]], coord=typename.coord)
        return decl

    def _type_modify_decl(self, decl, modifier):
        """ Tacks a type modifier on a declarator, and returns
            the modified declarator.
            Note: the declarator and modifier may be modified
        """
        modifier_head = modifier
        modifier_tail = modifier

        # The modifier may be a nested list. Reach its tail.
        while modifier_tail.type:
            modifier_tail = modifier_tail.type

        # If the decl is a basic type, just tack the modifier onto it
        if isinstance(decl, ast.VarDecl):
            modifier_tail.type = decl
            return modifier
        else:
            # Otherwise, the decl is a list of modifiers. Reach
            # its tail and splice the modifier onto the tail,
            # pointing to the underlying basic type.
            decl_tail = decl

            while not isinstance(decl_tail.type, ast.VarDecl):
                decl_tail = decl_tail.type

            modifier_tail.type = decl_tail.type
            decl_tail.type = modifier_head
            return decl


def _token_coord(self, p, token_idx):
    last_cr = p.lexer.lexdata.rfind("\n", 0, p.lexpos(token_idx))
    if last_cr < 0:
        last_cr = -1
    column = p.lexpos(token_idx) - (last_cr)
    return ast.Coord(p.lineno(token_idx), column)


if __name__ == "__main__":

    import sys

    uc_parser = UCParser()
    uc_parser.parse(open(sys.argv[1]).read(), "", debug=True)  # print tokens
