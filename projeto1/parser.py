class Parser:
    def p_program(self, p):
        """ program  : global_declaration_list
        """
        p[0] = Program(p[1])

    def p_global_declaration_list(self, p):
        """ global_declaration_list : global_declaration
                                    | global_declaration_list global_declaration
        """
        p[0] = [p[1]] if len(p) == 2 else p[1] + [p[2]]
