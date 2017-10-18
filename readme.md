# 2-SATpolySolver
В файле datainput.py лежит строковая переменная data, внутри которой можно задавать формулу. Коммит 7bdba35 тоже содержит решение задачи, но! для нормальной работы надо переопределить нормальную функцию lex.lex, чтобы она могла скушать другой лексер:

Добавить новый аргумент lexerInput:
def lex(module=None, object=None, debug=False, optimize=False, lextab='lextab',
        reflags=int(re.VERBOSE), nowarn=False, outputdir=None, debuglog=None, errorlog=None, lexerInput=None): 

И поменять строки инициализаци лексера:

    if isinstance(lexerInput, Lexer):
        lexobj = lexerInput
    else:
        lexobj = Lexer()
        
Грамматика сейчас ambiguous, но проблем пока что не замечено. Она позволяет проставлять скобочки везде, где хочется.

data = '''(~p \/ q) /\ (~q \/ r) /\ ((~r \/ (~(s)))) /\ (p)'''


Выводится сначала исходная КНФ, где каждая строчка - новый Conjunct.
Далее начинается итеративное насыщение типа каждый с каждым. На каждом шаге выводится новый набор Conjunct'ов.
