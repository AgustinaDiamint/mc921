import ply.yacc as yacc
from lexv01 import tokens


class Parser:
    def p_empty(self, p):
        """empty:"""
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
        p[0] = ("global_declaration", p[1])

    def p_function_defnition(self, p):
        """ function_definition : type_specifier_opt declarator declaration_list_opt compound_statement """
        p[0] = ("function_definition", p[1], p[2], p[3], p[4])

    def p_type_specifier(self, p):
        """ type_specifier : VOID
                           | CHAR
                           | INT
                           | FLOAT
        """
        p[0] = ("type_specifier", p[1])

    def type_specifier_opt(self, p):
        """type_specifier_opt: type_specifier
                             | empty
        """
        p[0] = p[1]

    def declaration_list(self, p):
        """ declaration_list: declaration
                            | declaration_list declaration
        """
        p[0] = [p[1]] if len(p) == 2 else p[1] + [p[2]]

    def declaration_list_opt(self, p):
        """declaration_list_opt: declaration_list
                            | empty"""
        p[0] = p[1]

    def p_declarator(self, p):
        """ declarator : pointer direct_declarator
                        | direct_declarator
        """
        p[0] = [p[1]] if len(p) == 2 else p[1] + [p[2]]

    def p_pointer(self, p):
        """ pointer : TIMES pointer_opt
        """
        p[0] = ('pointer', p[1], p[2])

    def p_pointer_opt(self, p):
        """pointer_opt: pointer
                      | empty
        """
        p[0] = p[1]

    def p_direct_declarator(self, p):
        """ direct_declarator: ID
                      | ( declarator )
                      | direct_declarator [ constant_exp_opt ]
                      | direct_declarator ( parameter_list )
                      | direct_declarator ( identifier_list_opt )
        """
        if len(p) == 2:
            p[0] = p[1]
        elif len(p) == 4:
            p[0] = p[2]
        else:
            p[0] = (p[1], p[3])

    def p_constant_expression(self, p):
        """ constant_expression : binary_expression """
        p[0] = p[1]

    def p_constant_expression_opt(self, p):
        """ constant_exp_opt : constant_expression
                            | empty
        """
        p[0] = p[1]

    def p_identifier_list(self, p):
        """ identifier_list : identifier_list ID
                            | ID
        """
        p[0] = [p[1]] if len(p) == 2 else p[1] + [p[2]]

    def identifier_list_opt(self, p):
        """ identifier_list_opt: identifier_list
                                | empty
        """
        p[0] = p[1]

    def p_binop_expr(self, p):
        """
        expr : expr PLUS expr
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
                | expr PP expr
                | expr MM expr
        """
        p[0] = (p[2], p[1], p[3])

    def p_cast_expression(self, p):
        """
        cast_expression: unary_expression
                    | ( type_specifier ) cast_expression
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
                            | postfix_expression [ expression ]
                            | postfix_expression ( assignment_expression_list_opt )
                            | postfix_expression PP
                            | postfix_expression MM
        """
        if len(p) == 2:
            p[0] = p[1]
        elif len(p) == 5:
            p[0] = (p[1],[3])
        else:
            p[0] = (p[1],p[2])

    def p_primary_expression(self, p):
        """
        primary_expression : ID
                            | constant
                            | string
                            | ( expression )
        """
        p[0] = p[1] if len(p) == 2 else p[2]
    #TODO
    # o que é char const 
    def p_constant(self, p):
        """ constant: ICONST
                    | CCONST
                    | FCONST
        """
        p[0] = p[1]

    def p_expression(self, p):
        """ expression : assignment_expression
                        | expression , assignment_expression
        """
        p[0] = p[1] if len(p) == 2 else (p[1], p[2])

    def p_expression_opt(self,p):
        """ expression_opt : expression
                            | empty
        """
        p[0] = p[1]
    def p_assignment_expression(self, p):
        """assignment_expression : binary_expression
                            | unary_expression assignment_operator assignment_expression
        """
        p[0] = p[1] if len(p) == 2 else (p[1], p[2], p[3])

    def p_assignment_expression_list(self,p):
        """ assignment_expression_list: assignment_expression_list assignment_expression
                                    | assignment_expression
        """
        p[0] = [p[1]] if len(p) == 2 else p[1] + [p[2]]
    
    def assignment_expression_list_opt(self,p):
        """ assignment_expression_list_opt: assignment_expresssion_list
                                            | empty
        """
        p[0] = p[1]

    def p_assignment_operator(self, p):
        """ assignment_operator: EQ
                                | TASSIGN
                                | DASSIGN
                                | MODASSIGN
                                | PASSIGN
                                | MINASSIGN
        """
        p[0] = ('assignment_operator', p[1])

    def p_unary_operator(self, p):
        """unary_operator : AND
                    | TIMES
                    | PLUS
                    | MINUS
                    | NOT
        """
        p[0] = ('unary operator', p[1])

    def p_parameter_list(self, p):
        """parameter_list : parameter_declaration
                        | parameter_list COMMA parameter_declaration
        """
        p[0] = p[1] if len(p) == 2 else  (p[1], p[3])

    def parameter_declaration(self, p):
        """ parameter_declaration : type_specifier declarator
        """
        p[0] = (p[1], p[2])


    def p_declaration(self, p):

        """declaration : type_specifier init_declarator_list_opt ; 
        """
        p[0] = (p[1],p[2])

    def p_declaration_list(self,p):
        """ declaration_list: declaration
                    | declaration_list declaration
        """
        p[0] = [p[1]] if len(p) == 2 else p[1] + [p[2]]
    
    def p_declaration_list_opt(self,p):
        """ declaration_list_opt : declaration_list
                                | empty
        """
        p[0] = p[1]

    def p_init_declarator(self, p):
        """init_declarator : declarator
                            | declarator EQ initializer
        """
        p[0] = p[1] if len(p) == 2 else (p[1],p[3])

    def p_init_declarator_list(self,p):
        """ init_declarator_list: init_declarator
                                    | init_declarator_list init_declarator
        """
        p[0] = p[1] if len(p) == 2 else  p[1] +[p[2]]

    def p_init_declarator_list_opt(self,p):
        """ init_declarator_list_opt: init_declarator_list
                                    | empty
        """
        p[0] = p[1] 

    def p_initializer(self, p):
        """initializer : assignment_expression
                    | LBRACK initializer_list RBRACK
                    | LBRACK initializer_list COMMA RBRACK
        """
        p[0] = p[1] if len(p) == 2 else p[3]

    def p_initializer_list(self,p):
        """ initializer_list : initializer
                    | initializer_list COMMA initializer
        """
        p[0] = p[1] if len(p) == 2 else p[1] + [p[3]]

    # TODO
    def p_compound_statement(self, p):
        """compound_statement : LBRACK declaration_list_opt {<statement>}* RBRACK
        """


    # TODO
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
    # TODO
    def p_expression_statement(self, p):
        """
        expression_statement: expression_opt ;
        """
        p[0] = p[1]

    # TODO
    def p_selection_statement(self, p):
        """    <selection_statement> ::= if ( <expression> ) <statement>
                                    | if ( <expression> ) <statement> else <statement>
        """

    # TODO
    def p_iteration_statement(self, p):
        """    <iteration_statement> ::= while ( <expression> ) <statement>
                                    | for ( {<expression>}? ; {<expression>}? ; {<expression>}? ) <statement>
        """

    # TODO
    def p_jump_statement(self, p):
        """<jump_statement> ::= break ;
                        | return {<expression>}? ;
        """

    def p_assert_statement(self, p):
        """ assert_statement: ASSERT expr SEMI """
        p[0] = ("assert", p[1])

    def p_print_statement(self, p):
        """ statement : PRINT LPAREN expr RPAREN SEMI 
        """
        p[0] = ("print", p[3])

    # TODO
    def p_read_statement(self, p):
        """<read_statement> ::= read ( {<declarator>}+ );"""

    def p_statement_list(self, p):
        """ statements : statements statement
                    | statement
        """
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = p[1] + (p[2])

    def p_assign_statement(self, p):
        """ statement : ID EQ expr
        """
        p[0] = ("assign", p[1], p[3])

    def binary_expression_cast_expression(self, p):
        """ binary_expression : cast_expression"""
        p[0] = ("bin_expression", p[1])

    def p_num_expr(self, p):
        """ expr : NUM
        """
        p[0] = ("num", p[1])

    def p_name_expr(self, p):
        """ expr : ID
        """
        p[0] = ("id", p[1])

    def p_compound_expr(self, p):
        """ expr : LPAREN expr RPAREN
        """
        p[0] = p[2]
