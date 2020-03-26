import ply.yacc as yacc
from lexv01 import tokens

class Parser:
    def p_program(self, p):
        """ program  : global_declaration_list
        """
        p[0] = ('program',p[1])

    def p_global_declaration_list(self, p):
        """ global_declaration_list : global_declaration
                                    | global_declaration_list global_declaration
        """
        p[0] = [p[1]] if len(p) == 2 else p[1] + [p[2]]
    
    def p_global_declaration(self,p):
        """global_declaration : function_definition
                              | declaration 
        """
        p[0] = ('global_declaration',p[1])

    def p_function_definition_1(self,p):
        """ function_definition : type_specifier declarator declaration compound_statement """
        p[0] = ('')
    
    def p_type_specifier(self,p):
        """ type_specifier : void
                           | char
                           | int
                           | float
        """
        p[0] = ('type_specifier',p[1])
    
    def p_declarator(self,p):
        """ declarator : identifier
                       | declarator [ constant_expression]
                       | declarator ( parameter_list )
                       | declarator ( identifier )
        """
    

    def p_constant_expression(self,p):
        """ constant_expression : binary_expression """
        p[0] = ('constant_expression', p[1])
    
    def binary_expression_cast_expression(self,p):
        """ binary_expression : cast_expression"""
        p[0] = ('bin_expression',p[1])

    def binary_expression_times(self,p):
        """ binary_expression : binary_expression TIMES binary_expression """
        p[0] = ('binary_expression', p[1]*p[3])

    def binary_expression_divide(self,p):
        """binary_expression : binary_expression DIVIDE binary_expression 
        """
        p[0] = ('binary_expression', p[1]/p[3])
     