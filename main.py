import re
import sys
import argparse

identifiers = '[_a-zA-Z][_a-zA-Z]*'

integers = '[0-9][0-9]*'


operations={'=':'ASSIGN',
            '+':'ADD',
            '-':'SUB',
            '*':'MUL',
            '/':'DIV',
            '%':'MOD',
            '(':'left_paranthesis',
            ')':'right_paranthesis',
            ';':'delimiter',
            '{':'left_curly',
            '}':'right_curly',
            '>':"GREATER_THAN",
            '<':"LESS_THAN",
            '>=':'GREATER_EQUAL',
            '<=':"LESS_THAN_EQUAL_TO",
            '==':'EQUALITY_OPERATOR',
            '!=':'NOT_EQUAL',
            '!':"EXCLAMATION"}
keywords = {'int_one':'INT1',
            'int_two':'INT2',
            'int_four':'INT4',
            'int_eight':'INT8',
            'or':'ELSE',
            'if_satisfied':'IF_SATISFIED',
            'void':'VOID',
            'return':'RETURN',
            'when':'WHEN',
            'main':'MAIN',
            'end':'END'}
delimiter=';'
parser_array=[]

parser = argparse.ArgumentParser(description='A test program.')
parser.add_argument("file", help="Prints the supplied argument.")
args = parser.parse_args()

with open(args.file, 'r') as file:
    while True:
        next_char=file.read(1)
        if next_char=='':
            break
        if next_char in [' ','\r','\n','\t']:
            continue
        currToken=next_char
        if re.fullmatch(identifiers,currToken):
            token_type='IDENTIFIER'
            while re.fullmatch(identifiers,currToken) is not None:
                next_char=file.read(1)
                if next_char=='':
                    break
                currToken+=next_char
            if next_char=='':
                parser_array.append((currToken,token_type))
                break
            else:
                parser_array.append((currToken[:-1], token_type))
                if re.fullmatch(integers,next_char):
                    print('Error: The identifier or keyword {} cannot contain numbers{}'.format(currToken[:-1],next_char))
                    sys.exit()
                if next_char in operations.keys():
                    token_type=operations[next_char]
                    parser_array.append((next_char,token_type))
        elif re.fullmatch(integers,currToken):
            token_type='INTEGER'
            while re.fullmatch(integers,currToken) is not None:
                next_char=file.read(1)
                if next_char=='':
                    break
                currToken+=next_char
            if next_char=='':
                parser_array.append((currToken,token_type))
                break
            else:
                parser_array.append((currToken[:-1], token_type))
                if re.fullmatch(identifiers,next_char):
                    print('Error: The integer {} cannot contain letter {}'.format(currToken[:-1],next_char))
                    sys.exit()
                if next_char in operations.keys():
                    token_type=operations[next_char]
                    parser_array.append((next_char,token_type))
        elif currToken in operations.keys():
            token_type = operations[next_char]
            parser_array.append((next_char, token_type))

for i in range(len(parser_array)):
    if parser_array[i][1]=='IDENTIFIER':
        if parser_array[i][0] in keywords.keys():
            parser_array[i]=(parser_array[i][0],keywords[parser_array[i][0]])
        else:
            if len(parser_array[i][0])<6 or len(parser_array[i][0])>8:
                print('Error: The length of the variable: {} is {}, which not meet the requirements'.format(parser_array[i][0],len(parser_array[i][0])))
                sys.exit()

i = 0
while i < len(parser_array):
    if parser_array[i][0] == "=" and parser_array[i+1][0] == "=":
        parser_array.pop(i+1)
        parser_array[i] = ("==", operations['=='])
    elif parser_array[i][0] == ">" and parser_array[i+1][0] == "=":
        parser_array.pop(i + 1)
        parser_array[i] = (">=", operations['>='])
    elif parser_array[i][0] == "<" and parser_array[i+1][0] == "=":
        parser_array.pop(i + 1)
        parser_array[i] = ("<=", operations['<='])
    elif parser_array[i][0] == "!" and parser_array[i+1][0] == "=":
        parser_array.pop(i + 1)
        parser_array[i] = ("!=", operations['!='])
    else:
        i +=1

def get_next_token():
    if len(parser_array)==0:
        return None
    token=parser_array.pop(0)
    return token


def stmt(indent):
    print(' '*indent,'<stmt>')
    next_token=get_next_token()
    token_type=next_token[1]
    if token_type in ['INT1','INT2','INT4','INT8']:
        parser_array.insert(0,next_token)
        declaration_stmt(indent+4)
    elif token_type=='IDENTIFIER':
        parser_array.insert(0, next_token)
        assignment_stmt(indent+4)
    elif token_type=='IF_SATISFIED':
        parser_array.insert(0, next_token)
        if_satisfied_stmt(indent+4)
    elif token_type=='WHEN':
        parser_array.insert(0, next_token)
        when_stmt(indent+4)
    else:
        print('Error: in stmt')
        sys.exit()
    print(' '*indent,'</stmt>')


def when_stmt(indent):
    print(' ' * indent, '<when_stmt>')
    next_token = get_next_token()
    assert next_token[1] == keywords['when']
    print(' ' * (indent + 4), next_token[0])
    next_token = get_next_token()
    if next_token is None or next_token[1] != operations['(']:
        print('Error: in when_stmt')
        sys.exit()
    print(' ' * (indent + 4), next_token[0])
    bool_expr(indent + 4)
    next_token = get_next_token()
    if next_token is None or next_token[1] != operations[')']:
        print('Error: in when_stmt')
        sys.exit()
    print(' ' * (indent + 4), next_token[0])
    next_token = get_next_token()
    if next_token is None or next_token[1] != operations['{']:
        print('Error: in when_stmt')
        sys.exit()
    print(' ' * (indent + 4), next_token[0])
    next_token = get_next_token()
    while next_token is not None and next_token[1] != operations['}']:
        parser_array.insert(0, next_token)
        stmt(indent + 4)
        next_token = get_next_token()
    if next_token is None:
        print('Error: in when_stmt')
        sys.exit()
    print(' ' * (indent + 4), next_token[0])
    print(' ' * indent, '</when_stmt>')

def if_satisfied_stmt(indent):
    print(' ' * indent, '<if_satisfied_stmt>')
    next_token = get_next_token()
    assert next_token[1] == keywords['if_satisfied']
    print(' ' * (indent + 4), next_token[0])
    next_token = get_next_token()
    if next_token is None or next_token[1] != operations['(']:
        print('Error: in if_satisfied_stmt')
        sys.exit()
    print(' ' * (indent + 4), next_token[0])
    bool_expr(indent+4)
    next_token=get_next_token()
    if next_token is None or next_token[1]!=operations[')']:
        print('Error: in if_satisfied_stmt')
        sys.exit()
    print(' ' * (indent + 4), next_token[0])
    next_token = get_next_token()
    if next_token is None or next_token[1]!=operations['{']:
        print('Error: in if_satisfied_stmt')
        sys.exit()
    print(' ' * (indent + 4), next_token[0])
    next_token=get_next_token()
    while next_token is not None and  next_token[1]!=operations['}']:
        parser_array.insert(0,next_token)
        stmt(indent+4)
        next_token=get_next_token()
    if next_token is None:
        print('Error: in if_satisfied_stmt')
        sys.exit()
    print(' ' * (indent + 4), next_token[0])
    next_token=get_next_token()
    if next_token is not None and next_token[1]==keywords['or']:
        print(' ' * (indent + 4), next_token[0])
        next_token = get_next_token()
        if next_token is None or next_token[1]!=operations['{']:
            print('Error: in if_satisfied_stmt')
            sys.exit()
        print(' ' * (indent + 4), next_token[0])
        next_token = get_next_token()
        while next_token is not None and next_token[1] != operations['}']:
            parser_array.insert(0, next_token)
            stmt(indent + 4)
            next_token = get_next_token()
        if next_token is None:
            print('Error: in if_satisfied_stmt')
            sys.exit()
        print(' ' * (indent + 4), next_token[0])
    elif next_token is not None:
        parser_array.insert(0,next_token)
    print(' ' * indent, '</if_satisfied_stmt>')



def bool_expr(indent):
    print(' ' * indent, '<bool_expr>')
    expression(indent+4)
    next_token = get_next_token()
    if next_token[1]==operations['<'] or next_token[1]==operations['<='] or next_token[1]==operations['>'] or \
            next_token[1] == operations['>='] or next_token[1]==operations['=='] or next_token[1]==operations['!=']:
        print(' ' * (indent + 4), next_token[0])
        expression(indent+4)
    else:
        print('Error: in bool_expr')
        sys.exit()
    print(' ' * indent, '</bool_expr>')

#<assignment_stmt> --> identifier '=' <expression> ';'
def assignment_stmt(indent):
    print(' ' * indent, '<assignment_stmt>')

    next_token=get_next_token()
    assert next_token[1]=='IDENTIFIER'
    print(' ' * (indent + 4), next_token[0])

    next_token = get_next_token()
    if next_token is None or next_token[1]!=operations['=']:
        print('Error: in assignment_stmt')
        sys.exit()
    print(' ' * (indent + 4), next_token[0])
    expression(indent+4)
    next_token=get_next_token()
    print(' ' * (indent + 4), next_token[0])
    print(' ' * indent, '</assignment_stmt>')




def expression(indent):
    print(' '*indent,'<expression>')
    term(indent+4)
    next_token=get_next_token()
    while next_token[1]==operations['+'] or next_token[1]==operations['-']:
        print(' '*(indent+4),next_token[0])
        term(indent+4)
        next_token = get_next_token()
    parser_array.insert(0,next_token)
    print(' '*indent,'</expression>')


def term(indent):
    print(' ' * indent, '<term>')
    factor(indent+4)
    next_token = get_next_token()
    while next_token[1]==operations['*'] or next_token[1]==operations['/'] or next_token[1]==operations['%']:
        print(' ' * (indent + 4), next_token[0])
        factor(indent+4)
        next_token = get_next_token()
    parser_array.insert(0,next_token)
    print(' ' * indent, '</term>')


def factor(indent):
    print(' ' * indent, '<factor>')
    next_token = get_next_token()
    if next_token[1]=='IDENTIFIER' or next_token[1]=='INTEGER':
        print(' '*(indent+4),next_token[0])
    elif next_token[1]==operations['(']:
        print(' ' * (indent + 4), next_token[0])
        expression(indent+4)
        next_token = get_next_token()
        if next_token[1]==operations[')']:
            print(' ' * (indent + 4), next_token[0])
        else:
            print('Error: in factor')
            sys.exit()
    else:
        print('Error: in factor')
        sys.exit()
    print(' ' * indent, '</factor>')

#<declaration_stmt> --> ( int_one | int_two | int_four | int_eight ) identifier ';'
def declaration_stmt(indent):
    print(' '*indent,'<declaration_stmt>')
    next_token = get_next_token()
    assert next_token[1] in ['INT1','INT2','INT4','INT8']
    print(' '*(indent+4),next_token[0])
    next_token = get_next_token()
    if next_token is None or next_token[1]!='IDENTIFIER':
        print('Error: in declaration_stmt')
        sys.exit()
    print(' '*(indent+4),next_token[0])
    next_token=get_next_token()
    if next_token is None or next_token[1]!=operations[';']:
        print('Error: in declaration_stmt')
        sys.exit()
    print(' ' * (indent + 4), next_token[0])
    print(' ' * indent, '</declaration_stmt>')


def program():
    print('<program>')
    next_token=get_next_token()
    if next_token is None:
        print('</Program>')
        return
    if next_token[1]!=keywords['void']:
        print('Error: Code must begin with:void main()')
        sys.exit()

    next_token=get_next_token()
    if next_token is None or next_token[1]!=keywords['main']:
        print('Error: Code must begin with:void main()')
        sys.exit()

    next_token = get_next_token()
    if next_token is None or next_token[1] != operations['(']:
        print('Error: Code must begin with:void main()')
        sys.exit()

    next_token = get_next_token()
    if next_token is None or next_token[1] != operations[')']:
        print('Error: Code must begin with:void main()')
        sys.exit()

    while len(parser_array)>1:
        stmt(4)
    next_token = get_next_token()
    if next_token is None or next_token[1] != keywords['end']:
        print('Error: Code must end with:end')
        sys.exit()
    print('</Program>')
program()