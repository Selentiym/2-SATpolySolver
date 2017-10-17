# -----------------------------------------------------------------------------
# calc.py
#
# A simple calculator with variables -- all in one file.
# -----------------------------------------------------------------------------
myLiterals = {
   '0': 'FALSE',
   'F': 'FALSE',
   '1': 'TRUE',
   'T': 'TRUE'
}
tokens = [
    'NAME', 'LITERAL',
    'AND', 'OR', 'NOT',
    'LPAREN', 'RPAREN'
] + list(myLiterals.values())

# Tokens

t_AND = r'\\\/'
t_OR = r'\/\\'
t_NOT = r'~'
t_LPAREN = r'\('
t_RPAREN = r'\)'


def t_LITERAL(t):
    r'(' + '|'.join(myLiterals.keys()) + ')'
    try:
        t.type = myLiterals.get(t.value)
    except KeyError:
        print("Invalid literal %s", t.value)
        t.value = 0
    return t


# Ignored characters
t_ignore = " \t"


def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


# Build the lexer
import ply.lex as lex

lexer = lex.lex()

import sys
sys.exit()

# Parsing rules

# precedence = (
#     ('left', 'PLUS', 'MINUS'),
#     ('left', 'TIMES', 'DIVIDE'),
#     ('right', 'UMINUS'),
# )

# dictionary of names
names = {}


def p_statement_assign(t):
    'statement : NAME EQUALS expression'
    names[t[1]] = t[3]


def p_statement_expr(t):
    'statement : expression'
    print(t[1])


def p_expression_binop(t):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression'''
    if t[2] == '+':
        t[0] = t[1] + t[3]
    elif t[2] == '-':
        t[0] = t[1] - t[3]
    elif t[2] == '*':
        t[0] = t[1] * t[3]
    elif t[2] == '/':
        t[0] = t[1] / t[3]


def p_expression_uminus(t):
    'expression : MINUS expression %prec UMINUS'
    t[0] = -t[2]


def p_expression_group(t):
    'expression : LPAREN expression RPAREN'
    t[0] = t[2]


def p_expression_number(t):
    'expression : NUMBER'
    t[0] = t[1]


def p_expression_name(t):
    'expression : NAME'
    try:
        t[0] = names[t[1]]
    except LookupError:
        print("Undefined name '%s'" % t[1])
        t[0] = 0


def p_error(t):
    print("Syntax error at '%s'" % t.value)


import ply.yacc as yacc

parser = yacc.yacc()

while True:
    try:
        s = input('calc > ')  # Use raw_input on Python 2
    except EOFError:
        break
    parser.parse(s)