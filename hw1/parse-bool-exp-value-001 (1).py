'''
This program implements a recursive descent parser for grammar
rules 5, 6, 7 below.

Implement rules 1, 2, 3, 4.

Note that the relational operators in rule 4 and the True
False literals in rule 3 require spaces.
around the operator.

Single quote marks are used to indicate terminal symbols, so
'|' means the | is a terminal symbol, while | alone is a
meta-symbol seperating different re-writing rules.

1 <bexp> → <bterm> { '|' <bterm> }
2 <bterm> → <bfact> { '&' <bfact> }
3 <bfact> → ( <bexp> ) | '~' <bfact> | ' True ' | ' False ' | <exp> <rop> <exp>
4 <rop>  ' < ' | ' > ' | ' <= ' | ' >= ' | ' == '

5 <exp> → <term>{ '+'<term> | '-'<term> }
6 <term> → <factor>{ '*'<factor> | '/'<factor> }
7 <factor> → (<exp>) | <atomic> | 'pi'

'''
import math


class ParseError(Exception): pass


# ==============================================================
# FRONT END PARSER
# ==============================================================

i = 0  # keeps track of what character we are currently reading.
err = None


# ---------------------------------------
# Parse an Expression   <exp> → <term>{+<term> | -<term>}
#
def exp():
    global i, err

    value = term()
    while True:
        if w[i] == '+':
            i += 1
            value = binary_op('+', value, term())
        elif w[i] == '-':
            i += 1
            value = binary_op('-', value, term())
        else:
            break

    return value


# ---------------------------------------
# Parse a Term   <term> → <factor>{+<factor> | -<factor>}
#
def term():
    global i, err

    value = factor()
    while True:
        if w[i] == '*':
            i += 1
            value = binary_op('*', value, factor())
        elif w[i] == '/':
            i += 1
            value = binary_op('/', value, factor())
        else:
            break
    return value


# ---------------------------------------
# Parse a Factor   <factor> → (<exp>) | <number> 
#       
def factor():
    global i, err
    value = None
    if w[i] == '(':
        i += 1  # read the next character
        value = exp()
        if w[i] == ')':
            i += 1
            return value
        else:
            print('missing )')
            raise ParseError
    elif w[i] == 'pi':
        i += 1
        return math.pi
    else:
        try:
            value = atomic(w[i])
            i += 1  # read the next character
        except ValueError:
            print('number expected')
            value = None
    if value is None:
        raise ParseError
    return value


# ==============================================================
# BACK END PARSER (ACTION RULES)
# ==============================================================

def binary_op(op, lhs, rhs):
    if op == '+':
        return lhs + rhs
    elif op == '-':
        return lhs - rhs
    elif op == '*':
        return lhs * rhs
    elif op == '/':
        return lhs / rhs
    else:
        return None


def atomic(x):
    return float(x)


def bexp():
    global i, err
    value = bterm()
    while True:
        if w[i] == '|':
            i += 1
            value = booleanvalue('|', value, bterm())
        else:
            break
    return value


def booleanvalue(op, a, b):
    if op == '|':
        if a == False and b == False:
            return False
        elif a == 'False' and b == 'False':
            return False
        else:
            return True
    if op == '&':
        if a == True and b == True:
            return True
        elif a== 'True' and b == 'True':
            return True
        else:
            return False
    if op == '~':
        if a == True or a == 'True':
            return False
        elif a == False or a == 'False':
            return True
    return False


def bterm():
    global i, err
    value = bfact()
    while True:
        if w[i] == '&':
            i += 1
            value = booleanvalue('&', value, bfact())
        else:
            break
    return value


def bfact():
    global i, err
    value = None
    if w[i] == '(':
        i += 1
        value = bexp()
        if w[i] == ')':
            i += 1
            return value
        else:
            print('missing )')
            raise ParseError
    elif w[i] == '~':
        i += 1
        value = booleanvalue('~', bfact(), value)
        return value
    elif w[i] == 'True':
        i += 1
        return True
    elif w[i] == 'False':
        i += 1
        return False
    else:
        value = exp()
        op = w[i]
        i += 1
        value = rop(value, op, exp())
        return value
    return False


def rop(lhs, op, rhs):
    if op == '<':
        return bool(lhs < rhs)
    elif op == '>':
        return bool(lhs > rhs)
    elif op == '<=':
        return bool(lhs <= rhs)
    elif op == '>=':
        return bool(lhs >= rhs)
    elif op == '==':
        return bool(lhs == rhs)
    else:
        print('operator error')
        raise ParseError
    return False


# ==============================================================
# User Interface
# ==============================================================

w = input('\nEnter expression: ')
while w != '':
    # ------------------------------
    # Split string into token list.
    #
    array = ['(', ')', '+', '-', '<', '==', '<=', '>=', '*', '/','&','|','~']
    for c in array:
        w = w.replace(c, ' ' + c + ' ')
    w = w.split()
    w.append('$')  # EOF marker

    print('\nToken Stream:     ', end='')
    for t in w:
        print(t, end='  ')
    print('\n')
    i = 0
    try:
        print('Value:           ', bexp())  # call the parser
    except:
        print('parse error')
    print()
    if w[i] != '$':
        print('Syntax error: $')
    print('read | un-read:   ', end='')
    for c in w[:i]:
        print(c, end=' ')
    print(' : ', end='')
    for c in w[i:]:
        print(c, end=' ')
    print()
    w = input('\n\nEnter expression: ')

'''
Example test run:

Enter expression: 2*(3 + 4) < 15 & 1 + 2 == 3

Token Stream:     2  *  (  3  +  4  )  <  15  &  1  +  2  ==  3  $  

Value:            True

read : un-read:   2 * ( 3 + 4 ) < 15 & 1 + 2 == 3  : $ 



Enter expression: ~ 2*(3 + 4) < 15 & 1 + 2 == 3

Token Stream:     ~  2  *  (  3  +  4  )  <  15  &  1  +  2  ==  3  $  

Value:            False

read : un-read:   ~ 2 * ( 3 + 4 ) < 15 & 1 + 2 == 3  : $ 

'''
