import re

def isID(x):
    ID = re.match(r'[a-zA-Z_]\w*', x)
    if ID:
        return x
    return None

def isKeyword(x):
    keyword_list = {
        'var': 'var',
        'int': 'DataType',
        'float': 'DataType',
        'string': 'DataType',
        'bool': 'DataType',
        'true': 'TF',
        'false': 'TF',
        'if': 'if',
        'else': 'else',
        'while': 'while',
        'fun': 'fun',
        'back': 'back',
        'class': 'class',
        'init': 'init',
        'self': 'self',
        'enter': 'EP',
        'print': 'EP',
        'del' : 'del',
        'super': 'super',
        'add': 'add',
        'remove': 'remove',
        'virtual': 'virtual',
        'override': 'override',
        'static': 'static',
    }
    lower_x = x.lower()
    if lower_x in keyword_list:
        return keyword_list[lower_x]
    return None

def isChar(x):
    char = re.match(r"'(?:\\.|[^\\'])'", x)
    if char:
        return x
    return None

def isInt(x):
    Integer = re.match("([+|-][0-9]+$)|([0-9]+$)", x)
    if Integer:
        return x
    return None
    
def isFloat(x):
    Float = re.match("([+|-][0-9]*\\.[0-9]+$)|([0-9]*\\.[0-9]+$)", x)
    if Float:
        return x
    return None

def isString(x):
    String = re.match(r'"(?:[^"\\]|\\.)*"', x)
    if String:
        return x
    return None


def isOperator(x):
    pm = {"+", "-"}
    mdm = {"*", "/", "%"}
    inc_dec = {"++", "--"}
    assign = {"=", "+=", "-=", "*=", "/=", "%="}
    logical = {"&", "|", "!"}
    relational = {"<", ">", "<=", ">=", "==", "!="}

    if x in pm:
        return "PM"
    elif x in mdm:
        return "MDM"
    elif x in inc_dec:
        return "INC_DEC_OP"
    elif x in assign:
        return "ASSIGN_OP"
    elif x in logical:
        return "LOGICAL_OP"
    elif x in relational:
        return "RELATIONAL_OP"
    return None

def isPunctuator(x):
    pun = {
        '.': '.',
        ',': ',',
        '{': '{',
        '}': '}',
        '(': '(',
        ')': ')',
        '[': '[',
        ']': ']',
        ';': ';',
        ':': ':',
    }
    if x in pun:
        return pun[x]
    return None