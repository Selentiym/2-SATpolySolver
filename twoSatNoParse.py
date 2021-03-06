# -----------------------------------------------------------------------------
#
# -----------------------------------------------------------------------------


from typing import Set, Generic, TypeVar
# from ply.lex import lex as mainFunc, Lexer
import ply.lex as lex
from pprint import pprint

T = TypeVar('T')
elements = {}


def checkSatByConjunctsSet(cs):
    saveLen = cs.__len__()
    breakAll = False
    sat = 0
    while breakAll ^ True:
        sat += 1
        print("Saturation nmber ",sat)
        cop = cs.copy()
        i = 0
        for conj1 in cop:
            i += 1
            j = 0
            for conj2 in cop:
                j += 1
                if i <= j:
                    continue
                newConj = conj1.resolve(conj2)  # type: Conjunct
                if newConj is not None:
                    cs.add(newConj)
                    print("Derived: ", newConj)
        singleOnly = set()
        tempCopy = cs.copy()
        for conj in tempCopy:
            if conj.isTrivial():
                cs.remove(conj)
            else:
                if conj.variables.__len__() == 1:
                    cpEl = conj.variables.pop()
                    conj.variables.add(cpEl)
                    singleOnly.add(cpEl)

        del tempCopy
        for el1 in singleOnly:
            if breakAll:
                break
            for el2 in singleOnly:
                if el1.isNegation(el2):
                    print("False derived! The conjuncts are:")
                    for conj in cs:
                        print(conj)
                    return False

        newLen = cs.__len__()
        if newLen == saveLen:
            print("2-CNF is satisfiable:")
            for conj in cs:
                print(conj)
            return True
        saveLen = newLen


def elementToString(name: str, negation: bool):
    return str(negation)+name


def getElementInstance(name: str, negation: bool):
    global elements
    el = elements.get(elementToString(name,negation),None)
    if el is None:
        el = Element(name, negation)
    return el


class Element(Generic[T]):
    def __init__(self, name: str, negation: bool):
        self.negation = negation
        self.name = name

    def negate(self):
        self.negation ^= True

    def isNegation(self, el: T):
        return (self.name == el.name) & (self.negation ^ el.negation)

    def __hash__(self):
        return hash(self.__str__())

    def __str__(self):
        return elementToString(self.name,self.negation)

    def __eq__(self, other):
        return (self.name == other.name) & (self.negation == other.negation)


class Conjunct(Generic[T]):
    def __init__(self):
        self.variables = set()  # type: Set[Element]

    def addElement(self, el):
        tempSet = set()
        tempSet.add(el)
        self.addElements(tempSet)

    def addElements(self, elements: Set[Element]):
        self.variables = self.variables | elements
        # pprint(self)

    def resolve(self, second: T):
        for el1 in self.variables:
            for el2 in second.variables:
                if el1.isNegation(el2):
                    rez = Conjunct()
                    temp = self.variables.copy()
                    temp.remove(el1)
                    rez.addElements(temp)
                    temp = second.variables.copy()
                    temp.remove(el2)
                    rez.addElements(temp)
                    rez.simplify()
                    return rez
        return None

    def isTrivial(self):
        self.simplify()
        return self.variables.__len__() == 0

    def __hash__(self):
        rez = 0
        for v in self.variables:
            rez += v.__hash__()
        return rez

    def __str__(self):
        return self.print()

    def __eq__(self, other):
        return self.__hash__() == other.__hash__()

    def simplify(self):
        v = self.variables.copy()
        # if we have a 2-CNF there are at most 4 operations
        i = 0
        for var1 in v:
            i += 1
            j = 0
            for var2 in v:
                j += 1
                if i <= j:
                    continue
                if var1.isNegation(var2):
                    self.variables.discard(var1)
                    self.variables.discard(var2)

    def print(self):
        text = '('
        toAdd = ''
        for el in self.variables:
            text += toAdd
            if el.negation:
                text += '~'
            text += el.name
            toAdd = '\\/'
        text += ')'
        return text


# class MyLexer(Lexer):
#     def __init__(self):
#         Lexer.__init__(self)
#         self.conjuncts = set()
#         self.currentConjunct = None
#         self.negation = False
#         self.andNeeded = False
#         self.openedBrackets = 0
#
#     def andFound(self):
#         print("And found")
#         if self.openedBrackets == 0:
#             self.endConjunct()
#         else:
#             raise SyntaxError('And literal found when it is not needed')
#
#     def beginConjunct(self):
#         if self.openedBrackets > 0:
#             raise ValueError('Beginning a conjunct while number of opened brackets is more that zero')
#         temp = Conjunct()
#         if self.currentConjunct is not None:
#             raise IndexError('Attempt to start a new conjunct when the last one is not still closed!')
#         #self.conjuncts.append(temp)
#         self.currentConjunct = temp
#         self.begin('conjunct')
#
#     def endConjunct(self):
#         print("End conjunct")
#         if self.openedBrackets != 0:
#             raise ValueError('Trying to close a conjunct while the number of opened brackets is not 0. It is %i', self.openedBrackets)
#         if self.currentConjunct is None:
#             raise IndexError('Attempt to close a conjunct while none is opened')
#         if self.currentConjunct.isTrivial() ^ True:
#             self.conjuncts.add(self.currentConjunct)
#         self.currentConjunct = None
#         self.begin('INITIAL')
#
#     def getCurrentConjunct(self) -> Conjunct:
#         if self.currentConjunct is None:
#             raise IndexError('Attempt to obtain current conjunct while the one is not opened.')
#         return self.currentConjunct
#
#     def getNegation(self):
#         save = self.negation
#         self.negation = False
#         return save
#
#     def createElement(self, name: str):
#         return Element(name, self.getNegation())
#
#     def negate(self):
#         self.negation = self.negation ^ True


# not using literals dictionary since I need to specify types
# myLiterals = {
#    '0': 'FALSE',
#    'F': 'FALSE',
#    '1': 'TRUE',
#    'T': 'TRUE'
# }

tokens = [
    'NAME', #'LITERAL',
    'AND', 'OR', 'NOT',
    'LPAREN', 'RPAREN'
]# + list(set(myLiterals.values()))

# Tokens


t_OR = r'\\/'


def t_LPAREN(t):
    r'\('
    return t


def t_RPAREN(t):
    r'\)'
    return t


def t_AND(t):
    r'/\\'
    return t


def t_NAME(t):
    r'[a-zA-Z][a-zA-Z\d_]*'
    return t


def t_NOT(t):
    r'~'
    return t


# Ignored characters
t_ignore = " \t"


def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


# Parsing rules

lex.lex()

precedence = (
    ('left','OR'),
    ('left','AND'),
    )



def p_conjunctset_extend(p):
    'conjunctset : conjunctset AND conjunctset'
    p[0] = p[1] | p[3]
    # global saveSet
    saveSet = p[0]


def p_conjunctset_paran(p):
    'conjunctset : LPAREN conjunctset RPAREN'
    p[0] = p[2]


def p_conjunctset_create(p):
    'conjunctset : conjunct'
    s = set()
    s.add(p[1])
    p[0] = s


def p_conjunct_extend(p):
    'conjunct : conjunct OR conjunct'
    p[1].addElements(p[3].variables)
    p[0] = p[1]


def p_conjunct_create(p):
    'conjunct : element'
    conj = Conjunct()
    conj.addElement(p[1])
    p[0] = conj


def p_element_negation(p):
    "element : NOT element"
    tempEl = p[2]
    tempEl.negate()
    p[0] = tempEl


def p_element_paranthesis(p):
    'element : LPAREN element RPAREN'
    p[0] = p[2]


def p_element_create(p):
    'element : NAME'
    el = Element(p[1], False)
    p[0] = el


def p_error(p):
    print ("Syntax error at '%s'" % p.value)


import ply.yacc as yacc
parser = yacc.yacc()

#myLex = MyLexer()

#lexer = mainFunc(lexerInput=myLex)

# data = '''(~p \/ q) /\ (q \/ r) /\ (~p \/ ~r) /\ (p \/ r) /\ (~p \/ r) /\ (p \/ ~r)'''



# lex.input(data)
#
# while True:
#     tok = lex.token()  # читаем следующий токен
#     if not tok:
#         break    # закончились печеньки
#     print (tok)

from datainput import data

rez = parser.parse(data)


checkSatByConjunctsSet(rez)

#lexer.input(data)

# while True:
#     tok = lexer.token()  # читаем следующий токен
#     if not tok:
#         lexer.endConjunct()  # Нужно попробовать закрыть блок. Если не выйдет, выстрелит ошибка
#         break    # закончились печеньки
#     print (tok)
#
# print("Initial conjuncts:")
# for conj in myLex.conjuncts:
#     print(conj)
#
# checkSatByConjunctsSet(myLex.conjuncts)

# c1 = Conjunct()
# c2 = Conjunct()
# el1 = Element("q", True)
# el2 = Element("r", False)
#
# tempSet = set()
# tempSet.add(el1)
# c1.addElements(tempSet)
#
# tempSet = set()
# tempSet.add(el2)
# c2.addElements(tempSet)
#
# tempSet = set()
# tempSet.add(c1)
# tempSet.add(c2)
# checkSatByConjunctsSet(tempSet)
