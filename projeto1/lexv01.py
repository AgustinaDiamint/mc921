# Parte 1 do lexer

types = ['VOID', 'CHAR', 'INT', 'FLOAT']

reserved = ['FOR', 'WHILE', 'IF', 'ASSERT',
            'PRINT', 'READ', 'BREAK', 'RETURN']

operators = ['PLUS','MINUS',
             'TIMES','DIVIDE',
             'EQUALS', 'MOD',
             'GT', 'GET',
             'LT', 'LET',
             'DIFF', 'AND',
             'OR', 'PP', 'MM',
             'ADDRESS']

tokens = types + reserved + operators

#Tokens
t_VOID = r'void'
t_CHAR  = r' char'
t_INT= r'int'
t_FLOAT = r'float'

t_FOR = r'for'
t_WHILE = r'while'
t_IF = r'IF'
t_ASSERT =  r'assert'
t_PRINT = r'print'
t_READ = r'read'
t_BREAK = r'break'
t_RETURN = r'return'

t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_EQUALS = r'\=\='
t_MOD = r'\%'
t_GT = r'>'
t_GET = r'>\='
t_LT = r'<'
t_LET = r'<\='
t_DIFF = '\!\='
t_AND  = '\&\&'
t_OR = r'||'
t_PP = r'\+\+'
t_MM = r'\-\-'
t_ADDRESS = r'\&'

