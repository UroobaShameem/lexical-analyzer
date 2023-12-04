import re

def isID(x):
    ID = re.match(r'[a-zA-Z_]\w*', x)
    if ID:
        return x
    return None

def isKeyword(x):
    keyword_list = {
        'var': 'var',
        'int': 'DT',
        'float': 'DT',
        'string': 'DT',
        'char': 'DT',
        'bool': 'DT',
        'true': 'TF',
        'false': 'TF',
        'if': 'if',
        'else': 'else',
        'while': 'while',
        'fun': 'fun',
        'return': 'return',
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
        'interface': 'interface'
    }
    if x in keyword_list:
        return keyword_list[x]
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
    logical = {"&&", "||", "!"}
    relational = {"<", ">", "<=", ">=", "==", "!="}

    if x in pm:
        return "pm"
    elif x in mdm:
        return "mdm"
    elif x in inc_dec:
        return "inc_dec"
    elif x in assign:
        return "assign_op"
    elif x in logical:
        return "logical_op"
    elif x in relational:
        return "rop"
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