import re
import os

lex = []
n = 0

# Semantic Start
s = -1
scopeTable = []
class_Table = []
data_Items = []
scope_stack = []
scope_stack.append(-1)


# Main Table Class

class Class_Table():
    def __init__(self, Name, Type, AM, Cat, parent, Type_M):
        self.Name = Name
        self.Type = Type
        self.AM = AM
        self.Cat = Cat
        self.parent = parent
        self.Type_M = Type_M
        self.class_DT = []

    def lookup_Class_DT(self, Name, Acess_M, Type_M):
        v = next((j for j in self.class_DT if j.Name == Name), "")
        if (v == ""):
            return "Not Present"
        else:
            return v.Type, v.Type_M, v.Acess_M

    def Insert_Class_DT(self, Name, Type, Acess_M, Type_M):
        if (lookup_Class_Table(Name) == "Not Present"):
            # print("Line 30 : ", Name, Type, Acess_M, Type_M)
            self.Class_Table.append(class_DT(Name, Type, Acess_M, Type_M))
            return True
        else:
            return False


# Data Table Class
class class_DT():
    def __init__(self, Name, Type, Acess_M, Type_M, Class_Name):
        self.Name = Name
        self.Type = Type
        self.Acess_M = Acess_M
        self.Type_M = Type_M
        self.Class_Name = Class_Name


# lookup Class Main Table
def lookup_Class_Table(Name):
    v = next((j for j in class_Table if j.Name == Name), "")
    if (v == ""):
        return "Not Present"
    else:
        return v.Type


# lookup Function Table
# def lookup_Scope_Table(Name, scope):
#         print("Name is", Name, "Scope is",scope)
#         v = next((j for j in ScopeTable if j.Name != Name and j.scope == scope) ,"")
#         if (v == ""):
#             return "Not Present"
#         else:
#             return v.Type


# Lookup Class Data
def lookup_Class_Data(Name, Class_Name):
    # moiz
    # z = next((j for j in class_Table if j.parent == Name) ,"")
    # print("name is",Name)
    # if(z==""):
    #     par = Name
    #     print("par is",par)
    # else:
    #     return z.Type
    #
    for x in range(class_Table.__len__()):
        x = class_Table[x].parent

    par = x

    v = next((j for j in data_Items if j.Name == Name and (j.Class_Name == Class_Name or j.Class_Name == par)), "")
    if (v == ""):
        # print("v is",Name)
        return "Not Present"
    else:
        return v.Type


# v = next((j for j in class_DT if j.Name == Class_Name) ,"")
# if (v == ""):
#     return "Not Present"
# else:

#     return v.lookup_Class_DT(Name , "" , "")


# Insert Class MainTable
def Insert_Class_Table(Name, Type, AM, Cat, parent, Type_M):
    if (lookup_Class_Table(Name) == "Not Present"):
        # print("Name: ", Name, " Type: ", Type, " Parent: ",parent, " Type Mod: ", Type_M)
        # print("before")
        # print("Insert Class Name")
        class_Table.append(Class_Table(Name, Type, AM, Cat, parent, Type_M))

        return True
    else:
        # print("RE Class1 Declaration Error!")

        return False


# Insert Class Data
def Insert_Class_Data(Name, Type, Acess_M, Type_M, Class_Name):
    # v = next((j for j in class_Table if j.Name == Class_Name) ,"")

    if (lookup_Class_Data(Name, Class_Name) == "Not Present"):
        # print("Insert Class data before")
        # print("Line 99 : ", Name ,Type , Acess_M  , Type_M, Class_Name)
        data_Items.append(class_DT(Name, Type, Acess_M, Type_M, Class_Name))
        # print("Insert Class data after")
        return True
    else:
        # return v.Insert_class_DT(Name , Type , Acess_M  , Type_M)
        return False


class ScopeTable():
    def __init__(self, Name, Type, scope):
        self.Name = Name
        self.Type = Type
        self.scope = scope


def lookup_Scope_Table(Name):
    old = []
    old = scope_stack.copy()
    i = len(scope_stack) - 1
    # print("i before lookup is : ",i)
    # print("LOOKED UP !!! ",Name)
    # for z in range(scopeTable.__len__()):
    #     print(scopeTable[z].Name,scopeTable[z].Type,scopeTable[z].scope)

    while (old[i] != -1):
        v = next((j for j in scopeTable if j.Name == Name), "")
        # print(i,"'s Prev. Reading is : ",old[i])
        # print(v)
        i -= 1
    # print("V is : ",v)
    if (v == ""):
        return "Not Present"
    else:
        old.pop()
        return v.Type
        # print("value of i after lookup : ",i)


def Create_Scopee():
    global s
    s += 1
    # print("length is", len(scope_stack)-1)
    scope_stack.append(s)

    # return s


def Destroy_Scope():
    scope_stack.pop()


def Insert_Scope_Table(Name, Type, scope):
    # print("Name is ", Name , "scope is" , scope)
    if (lookup_Scope_Table(Name) == "Not Present"):
        scopeTable.append(ScopeTable(Name, Type, scope))
        return True
    else:
        # print("Undeclared Error")
        return False
        # return [False, lex[i][2], lex[i][1]]

    # Semantic End


tok = {
    'class_p': '',
    'value_p': '',
    'Line_No': 0
}


def tok_set(class_p, value_p, Line_No):
    global n
    lex.append([])
    lex[n].append(class_p)
    lex[n].append(value_p)
    lex[n].append(Line_No)
    n += 1


def WriteInFile():
    with open("token.txt", "a") as file:
        file.write(str(tok) + "\n")


def isStrConst(text):
    String = re.match("([0-9]*[a-zA-Z]*[-+@*=%\\\!~#&|_<>,./?;:\'\"]$)", text)
    if String:
        return True
    else:
        return False


def isID(text):
    ID = re.match("([a-zA-Z]+$)|([a-zA-Z]+_[a-zA-Z]+$)", text)
    if ID:
        return True
    else:
        return False


def isChar(text):
    Char = re.match("(\\\[bnort]$|[bnort]$)|(\\\[\'\"\\\]$)|([-+@*=%!~#&|_<>,./?;:]$)", text)
    if Char:
        return True
    else:
        return False


def isInt(text):
    Integer = re.match("([+|-][0-9]+$)|([0-9]+$)", text)
    if Integer:
        return True
    else:
        return False


def isFloat(text):
    Float = re.match("([+|-][0-9]*\\.[0-9]+$)|([0-9]*\\.[0-9]+$)", text)
    if Float:
        return True
    else:
        return False


def isOpr(text):
    pm = {"+", "-"}
    mdm = {"*", "/", "%"}
    uop = {"++", "--"}
    aop = {"=", "+=", "-=", "*=", "/=", "%="}
    lop = {"&&", "||", "!"}
    rop = {"<", ">", "<=", ">=", "==", "!="}
    sop = {"<<", ">>"}
    if text in pm:
        return "PM"
    elif text in mdm:
        return "MDM"
    elif text in uop:
        return "inc_dec"
    elif text in aop:
        return "AOP"
    elif text in lop:
        return "LOP"
    elif text in sop:
        return "SOP"
    elif text in rop:
        return "ROP"
    else:
        return False


def isPunc(text):
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
        '::': '::'
    }
    for key in pun:
        if key == text:
            return pun[key]

    return None


def isKeyWord(text):
    kw = {
        'int': 'DT',
        'float': 'DT',
        'char': 'DT',
        'String': 'DT',
        'bool': 'DT',
        'for': 'for',
        'do': 'do',
        'while': 'while',
        'if': 'if',
        'else': 'else',
        'switch': 'switch',
        'case': 'case',
        'break': 'break',
        'continue': 'continue',
        'default': 'default',
        'return': 'return',
        'void': 'void',
        'true': 'bool-constant',
        'false': 'bool-constant',
        'class': 'class',
        'virtual': 'virtual',
        'static': 'static',
        'main': 'main',
        'public': 'AM',
        'private': 'AM',
        'protected': 'AM',
        'base': 'base',
        'array': 'array',
        'list': 'list',
        # OOP
        'interface': 'interface',
        'extends': 'extends',
        'implements': 'implements',
        'new': 'new',
        'sealed': 'sealed',
        'abstract': 'abstract',
        'general': 'general',
        'try': 'try',
        'catch': 'catch',
        'import': 'import',
        'this': 'this',
        'super': 'super',
    }
    for key in kw:
        if key == text:
            return kw[key]

    return None


def word_break(word, Line_No):
    if isID(word):
        kw = isKeyWord(word)
        if (kw != None):
            tok['class_p'] = kw
            tok['value_p'] = word
            tok['Line_No'] = Line_No
            tok_set(kw, word, Line_No)
            WriteInFile()
        else:
            tok['class_p'] = "ID"
            tok['value_p'] = word
            tok['Line_No'] = Line_No
            tok_set("ID", word, Line_No)
            WriteInFile()
    elif isInt(word):
        tok['class_p'] = "int"
        tok['value_p'] = word
        tok['Line_No'] = Line_No
        tok_set("int", word, Line_No)
        WriteInFile()
    elif isFloat(word):
        tok['class_p'] = "Float"
        tok['value_p'] = word
        tok['Line_No'] = Line_No
        tok_set("Float", word, Line_No)
        WriteInFile()
    elif isPunc(word):
        value = isPunc(word)
        tok['class_p'] = value
        tok['value_p'] = word
        tok['Line_No'] = Line_No
        tok_set(value, word, Line_No)
        WriteInFile()
    elif isOpr(word):
        value = isOpr(word)
        if value is not None:
            tok['class_p'] = value
            tok['value_p'] = word
            tok['Line_No'] = Line_No
            tok_set(value, word, Line_No)
            WriteInFile()
    else:
        tok['class_p'] = "Lexical Error"
        tok['value_p'] = word
        tok['Line_No'] = Line_No
        tok_set("Invalid Lexeme", word, Line_No)
        WriteInFile()


def opr(text):
    op = {'+', '-', '*', '/', '=', ':', '<', '>', "%", '!', '&', '|'}
    if text in op:
        return True
    else:
        return False


def ID(text):
    ID = re.match("([a-zA-Z]+$)|_$|[0-9]$", text)
    if ID:
        return True
    else:
        return False


def digit(text):
    Integer = re.match("([0-9]$)", text)
    if Integer:
        return True
    else:
        return False


def pun(text):
    pun = {".", ",", ":", ";", "(", ")", "{", "}", "[", "]"}
    if text in pun:
        return True
    else:
        return False


def chr(text):
    Char = {"\\", "\r", "\b", "\t", "@"}
    if text in Char:
        return True
    else:
        return False


# Lex Start
def LA():
    comment = ''
    char = ''
    comments = ''
    string = False
    point = False
    wb = False
    word = ''
    Line_No = 1
    with open("input.txt", "r") as file:
        # with open("E:\Compiler Construction\input.txt" , "r") as file:
        while True:
            if wb == False:
                char = file.read(1)  # read by character

            if digit(char):
                while True:
                    word = word + char
                    char = file.read(1)
                    if char == "." and point == False:
                        point = True
                    elif char == ID(char):
                        word = word + char
                    elif not digit(char) and not ID(char):
                        word_break(word, Line_No)
                        word = ''
                        wb = True
                        point = False
                        break
            elif ID(char):
                while True:
                    word = word + char
                    char = file.read(1)
                    if not ID(char):
                        word_break(word, Line_No)
                        word = ''
                        wb = True
                        break
            elif char == "#":
                while (char != "\n"):
                    char = file.read(1)
                    comments = comments + char
                # print("single line: ",comments)
                comments = ''
                wb = False
            elif char == "\\":
                # print("character")
                char = file.read(1)
                if (char == "#"):
                    while True:
                        char = file.read(1)
                        if char == '\\':
                            char = file.read(1)
                            if (char == "#"):
                                word = ''
                                wb = False
                                break
                        else:
                            comments = comments + char
                # print("Multi Line : ",comments)
                comments = ''
            elif opr(char):
                word = word + char
                char = file.read(1)
                if word == "-" and char == ">":
                    word = word + char
                    word_break(word, Line_No)
                    word = ''
                    wb = False
                elif not opr(char):
                    word_break(word, Line_No)
                    word = ''
                    wb = True
                elif char == word or char == "=":
                    word = word + char
                    word_break(word, Line_No)
                    word = ''
                    wb = False
            elif pun(char):
                if char == ".":
                    word = word + char
                    char = file.read(1)
                    if digit(char):
                        word = word + char
                        while True:
                            char = file.read(1)
                            if digit(char) or ID(char):
                                word = word + char
                            else:
                                word_break(word, Line_No)
                                word = ''
                                wb = True
                                break
                    else:
                        word_break(word, Line_No)
                        word = ''
                        wb = True
                else:
                    word = word + char
                    word_break(word, Line_No)
                    word = ''
                    wb = False

            elif char == "\"":
                while True:
                    char = file.read(1)
                    if char == '\"':
                        tok['class_p'] = "String"
                        tok['value_p'] = word
                        tok['Line_No'] = Line_No
                        tok_set("String", word, Line_No)
                        WriteInFile()
                        word = ''
                        wb = False
                        break
                    elif char == '\n':
                        tok['class_p'] = "Invalid Lexeme"
                        tok['value_p'] = word
                        tok['Line_No'] = Line_No
                        tok_set("Invalid Lexeme", word, Line_No)
                        WriteInFile()
                        word = ''
                        wb = False
                        string = True
                        break
                    else:
                        word = word + char
            elif char == "\'":
                comment = comment + char
                for i in range(1, 4):
                    char = file.read(1)
                    if char == '\'':
                        comment = comment + char
                        print("Comment : ", comment)
                        if comment == "''":
                            char = file.read(1)
                            if char == "'":
                                while True:
                                    char = file.read(1)
                                    if char == '\n':
                                        Line_No = Line_No + 1
                                    if char == "'":
                                        char = file.read(1)
                                        if char == "'":
                                            char = file.read(1)
                                            if char == "'":
                                                comment = ''
                                                char = file.read(1)
                                                wb = True
                                                break
                                    elif char == None:

                                        break
                            else:
                                wb = True

                        if (comment != ''):
                            tok['class_p'] = "Char"
                            tok['value_p'] = word
                            tok['Line_No'] = Line_No
                            tok_set("Char", word, Line_No)
                            WriteInFile()
                            word = ''
                            wb = False
                            string = True
                            break
                        else:
                            string = True
                            break
                    elif char == '\n':
                        tok['class_p'] = "Invalid Lexeme"
                        tok['value_p'] = word
                        tok['Line_No'] = Line_No
                        tok_set("Invalid Lexeme", word, Line_No)
                        WriteInFile()
                        word = ''
                        wb = False
                        string = True
                        break
                    else:
                        comment = ''
                        word = word + char
                if string == False:
                    word_break(word, Line_No)
                    word = ''
                    wb = False
                comment = ''

            elif chr(char):
                while True:
                    word = word + char
                    char = file.read(1)
                    if not chr(char):
                        word_break(word, Line_No)
                        word = ''
                        wb = True
                        break

            if char == '\0' or char == ' ':
                wb = False

            if char == '\n':
                Line_No += 1
                wb = False

            if not char:
                break
        tok['class_p'] = "$"
        tok['value_p'] = "$"
        tok['Line_No'] = Line_No
        tok_set("$", "$", Line_No)
        WriteInFile()


# Lex End

i = 0


# Syntax Start
def Syntax_Ana():
    def Start():
        global i
        if (lex[i][0] == "main" or lex[i][0] == "if" or lex[i][0] == "AM" or lex[i][0] == "while" or lex[i][
            0] == "switch" or lex[i][0] == "for" or lex[i][0] == " continue" or lex[i][0] == "break" or lex[i][
            0] == "class" or lex[i][0] == "inc_dec" or lex[i][0] == "ID" or lex[i][0] == "DT" or lex[i][
            0] == "return" or lex[i][0] == "$"):
            # print("hello from MST")
            am = []
            if (MST()[0]):
                if (Main()[0]):
                    return [True, lex[i][2], lex[i][1]]
            elif (AM(am)[0]):
                if (lex[i][0] == "static" or lex[i][0] == "virtual" or lex[i][0] == "const" or lex[i][0] == "$"):
                    i += 1
                    # AcessMod = lex[i][0]
                    if (Func_dec()[0]):
                        return [True, lex[i][2], lex[i][1]]
                elif (lex[i][0] == "sealed" or lex[i][0] == "general" or lex[i][0] == "abstract" or lex[i][0] == "$"):
                    # Categogy = lex[i][0]
                    cat = []
                    cat.append(lex[i][1])
                    i += 1
                    # print(lex[i][0])
                    if (Class(am[0], cat[0])[0]):
                        return [True, lex[i][2], lex[i][1]]
                return [True, lex[i][2], lex[i][1]]
        return [False, lex[i][2], lex[i][1]]
        # print("INVALID SYNTAX")

    # def C_def():        #
    #     global i
    #     if(lex[i][0] == "class" or lex[i][0] == "$"):
    #         if(lex[i][0] == "class"):
    #             if(Class()[0]):
    #                 return [True, lex[i][2], lex[i][1]]
    #         elif(lex[i][0] == "$"):
    #             return [True, lex[i][2], lex[i][1]]
    #     return [False, lex[i][2], lex[i][1]]

    
    # M_1 (Follow Set of Main)
    def M_1():
        global i
        if (lex[i][0] == "("):
            i += 1
            if (lex[i][0] == ")"):
                i += 1
                return [True, lex[i][2], lex[i][1]]
        elif (lex[i][0] == "$" or lex[i][0] == "}"):
            return [True, lex[i][2], lex[i][1]]
        return [False, lex[i][2], lex[i][1]]

    # Body (Non-terminal of Main, If, E_List, While)
    def Body():
        global i
        if (lex[i][0] == "{"):
            if (lex[i][0] == "{"):
                Create_Scopee()
                i += 1
                # print("next")
                if (MST()[0]):
                    # functions_Items.append(class_DT(Name ,Type , Acess_M  , Type_M, Class_Name))
                    if (lex[i][0] == "}"):
                        Destroy_Scope()

                        i += 1
                        return [True, lex[i][2], lex[i][1]]
        return [False, lex[i][2], lex[i][1]]

    # Body (Non-terminal of Main, If, E_List, While)
    def Func_Body():
        global i
        if (lex[i][0] == "{"):
            if (lex[i][0] == "{"):
                # Create_Scopee()
                i += 1
                # print("next")
                if (MST()[0]):
                    # functions_Items.append(class_DT(Name ,Type , Acess_M  , Type_M, Class_Name))
                    if (lex[i][0] == "}"):
                        Destroy_Scope()
                        i += 1
                        return [True, lex[i][2], lex[i][1]]
        return [False, lex[i][2], lex[i][1]]

    # MST (Non-Terminal of Start)
    def MST():
        global i
        if (lex[i][0] == "if" or lex[i][0] == "while" or lex[i][0] == "switch" or lex[i][0] == "for" or lex[i][
            0] == "continue" or lex[i][0] == "break" or lex[i][0] == "class" or lex[i][0] == "inc_dec" or lex[i][
            0] == "ID" or lex[i][0] == "DT" or lex[i][0] == "return" or lex[i][0] == "main" or lex[i][0] == "}" or
                lex[i][0] == "case" or lex[i][0] == "$" or lex[i][0] == "default"):
            if (lex[i][0] == "if" or lex[i][0] == "while" or lex[i][0] == "switch" or lex[i][0] == "for" or lex[i][
                0] == "continue" or lex[i][0] == "break" or lex[i][0] == "class" or lex[i][0] == "inc_dec" or lex[i][
                0] == "ID" or lex[i][0] == "DT" or lex[i][0] == "return"):
                if (SSTF()[0]):
                    if (MST()[0]):
                        return [True, lex[i][2], lex[i][1]]
            elif (lex[i][0] == "$" or lex[i][0] == "main" or lex[i][0] == "}" or lex[i][0] == "case" or lex[i][
                0] == "default"):
                return [True, lex[i][2], lex[i][1]]
        return [False, lex[i][2], lex[i][1]]

    # SSTF (non-terminal of MST)
    def SSTF():
        global i
        if (lex[i][0] == "main" or lex[i][0] == "if" or lex[i][0] == "while" or lex[i][0] == "switch" or lex[i][
            0] == "for" or lex[i][0] == "continue" or lex[i][0] == "break" or lex[i][0] == "class" or lex[i][
            0] == "inc_dec" or lex[i][0] == "ID" or lex[i][0] == "DT" or lex[i][0] == "return"):
            if (SST()[0]):
                return [True, lex[i][2], lex[i][1]]
            if (Return()[0]):
                return [True, lex[i][2], lex[i][1]]
                # elif(lex[i][0] == "class"):
            #     if(Class()[0]):          #
            #         return [True, lex[i][2], lex[i][1]]
        return [False, lex[i][2], lex[i][1]]

    # SST (non-terminal of SSTF)
    def SST():
        global i
        # lex[i][0] == "static" or
        if (lex[i][0] == "main" or lex[i][0] == "if" or lex[i][0] == "while" or lex[i][0] == "return" or lex[i][
            0] == "switch" or lex[i][0] == "for" or lex[i][0] == "continue" or lex[i][0] == "break" or lex[i][
            0] == "$" or lex[i][0] == "inc_dec" or lex[i][0] == "ID" or lex[i][0] == "DT" or lex[i][0] == "static" or
                lex[i][0] == "virtual" or lex[i][0] == "const"):
            if (lex[i][0] == "if"):
                if (If()[0]):
                    return [True, lex[i][2], lex[i][1]]

            elif (lex[i][0] == "while"):
                if (While()[0]):
                    return [True, lex[i][2], lex[i][1]]

            elif (lex[i][0] == "switch"):
                if (Switch()[0]):
                    return [True, lex[i][2], lex[i][1]]

            elif (lex[i][0] == "for"):
                if (For()[0]):
                    return [True, lex[i][2], lex[i][1]]

            elif (lex[i][0] == "static" or lex[i][0] == "virtual" or lex[i][0] == "const"):
                # print("next")
                if (Func_dec()[0]):
                    return [True, lex[i][2], lex[i][1]]

            elif (lex[i][0] == "continue"):
                if (Continue()[0]):
                    return [True, lex[i][2], lex[i][1]]

            elif (lex[i][0] == "break"):
                if (Break()[0]):
                    return [True, lex[i][2], lex[i][1]]

            # elif(lex[i][0] =="class"):    #
            #     if(Class()[0]):
            #         return [True, lex[i][2], lex[i][1]]

            elif (lex[i][0] == "inc_dec"):
                if (Inc_dec_1()[0]):
                    return [True, lex[i][2], lex[i][1]]

            elif (lex[i][0] == "ID"):
                N = lex[i][1]
                i += 1
                # print("check")
                if (S_List(N)[0]):
                    return [True, lex[i][2], lex[i][1]]

            elif (lex[i][0] == "DT"):
                dt = lex[i][1]
                i += 1
                if (lex[i][0] == "ID"):
                    N = lex[i][1]
                    i += 1
                    if (S_List_2(dt, N)[0]):
                        return [True, lex[i][2], lex[i][1]]
            elif (lex[i][0] == "$"):
                return [True, lex[i][2], lex[i][1]]
        return [False, lex[i][2], lex[i][1]]

    # If (Non-Terminal of SST, E_List)
    def If():
        global i
        if (lex[i][0] == "if"):
            if (lex[i][0] == "if"):
                i += 1
                if (lex[i][0] == "("):
                    i += 1
                    if (OE()[0]):
                        if (lex[i][0] == ")"):
                            i += 1
                            if (Body()[0]):
                                if (Else()[0]):
                                    return [True, lex[i][2], lex[i][1]]
        return [False, lex[i][2], lex[i][1]]

    # OE (Non-Terminal of If, While, Switch, Switch_body, Cond_1, Cond_2, Cond_3_1, S_List, S3_List, P_List, T, T1, T2, Array, Init_4, Init_6, D_List, Obj_Array, O_Init_3, Obj_List, Return)
    def OE():
        global i
        if (lex[i][0] == "ID" or lex[i][0] == "inc_dec" or lex[i][0] == "int" or lex[i][0] == "Float" or lex[i][
            0] == "String" or lex[i][0] == "Char" or lex[i][0] == "bool_const" or lex[i][0] == "(" or lex[i][
            0] == "!" or lex[i][0] == ";"):  # or lex[i][0]==":" ):
            if (AE()[0]):
                # print("next")
                if (OE_()[0]):
                    return [True, lex[i][2], lex[i][1]]
        return [False, lex[i][2], lex[i][1]]

    # AE (Non-Terminal of OE)
    def AE():
        global i
        if (lex[i][0] == "ID" or lex[i][0] == "inc_dec" or lex[i][0] == "int" or lex[i][0] == "Float" or lex[i][
            0] == "String" or lex[i][0] == "Char" or lex[i][0] == "bool_const" or lex[i][0] == "(" or lex[i][
            0] == "!" or lex[i][0] == ";"):  # or lex[i][0]==":"):
            if (ROP()[0]):
                if (AE_()[0]):
                    return [True, lex[i][2], lex[i][1]]
        return [False, lex[i][2], lex[i][1]]

    # ROP (Non-Terminal of AE)
    def ROP():
        global i
        if (lex[i][0] == "ID" or lex[i][0] == "inc_dec" or lex[i][0] == "int" or lex[i][0] == "Float" or lex[i][
            0] == "String" or lex[i][0] == "Char" or lex[i][0] == "bool_const" or lex[i][0] == "(" or lex[i][
            0] == "!" or lex[i][0] == ";"):  # or lex[i][0]==":"):
            if (PM()[0]):
                if (ROP_()[0]):
                    return [True, lex[i][2], lex[i][1]]
        return [False, lex[i][2], lex[i][1]]

    # PM (Non-Terminal of ROP)
    def PM():
        global i
        if (lex[i][0] == "ID" or lex[i][0] == "inc_dec" or lex[i][0] == "int" or lex[i][0] == "Float" or lex[i][
            0] == "String" or lex[i][0] == "Char" or lex[i][0] == "bool_const" or lex[i][0] == "(" or lex[i][
            0] == "!" or lex[i][0] == ";"):  # or lex[i[0] ==":"]):
            if (MDM()[0]):
                if (PM_()[0]):
                    return [True, lex[i][2], lex[i][1]]
        return [False, lex[i][2], lex[i][1]]

    # MDM (Non-Terminal of PM)
    def MDM():
        global i
        if (lex[i][0] == "ID" or lex[i][0] == "inc_dec" or lex[i][0] == "int" or lex[i][0] == "Float" or lex[i][
            0] == "String" or lex[i][0] == "Char" or lex[i][0] == "bool_const" or lex[i][0] == "(" or lex[i][
            0] == "!" or lex[i][0] == ";"):  # or lex[i][0] ==  ":"):
            if (T()[0]):
                # print("next")
                if (MDM_()[0]):
                    return [True, lex[i][2], lex[i][1]]
        return [False, lex[i][2], lex[i][1]]

    # T (Non-Terminal of MDM)
    def T():
        global i
        if (lex[i][0] == "ID" or lex[i][0] == "inc_dec" or lex[i][0] == "int" or lex[i][0] == "Float" or lex[i][
            0] == "String" or lex[i][0] == "Char" or lex[i][0] == "bool_const" or lex[i][0] == "(" or lex[i][
            0] == "!" or lex[i][0] == ";"):
            if (lex[i][0] == "ID"):
                # t= Insert_Scope_Table(lex[i][1] , "int" , scope_stack[-1])

                t = lookup_Scope_Table(lex[i][1])
                if (t == "Not Present"):
                    if (lex[i + 1][0] == "("):
                        return [True, lex[i][2], lex[i][1]]
                    else:
                        print(lex[i][1], " is Undeclared ")
                        return [False, lex[i][2], lex[i][1]]

                i += 1
                if (T1()[0]):
                    if (T3()[0]):
                        return [True, lex[i][2], lex[i][1]]
            elif (Inc_dec_1()[0]):
                return [True, lex[i][2], lex[i][1]]
            elif (Const()[0]):
                return [True, lex[i][2], lex[i][1]]
            elif (lex[i][0] == "("):
                i += 1
                if (OE()[0]):
                    if (lex[i][0] == ")"):
                        i += 1
                        return [True, lex[i][2], lex[i][1]]
            elif (lex[i][0] == "!"):
                i += 1
                if (T1()[0]):
                    return [True, lex[i][2], lex[i][1]]
        return [False, lex[i][2], lex[i][1]]

    # T1 (Non-Terminal of T)
    def T1():
        global i  # &&,|| change to LOP
        if (lex[i][0] == "$" or lex[i][0] == "MDM" or lex[i][0] == "PM" or lex[i][0] == "ROP" or lex[i][0] == "LOP" or
                lex[i][0] == "const" or lex[i][0] == "!" or lex[i][0] == "]" or lex[i][0] == "." or lex[i][0] == "[" or
                lex[i][0] == "inc_dec" or lex[i][0] == "(" or lex[i][0] == "AOP" or lex[i][0] == "," or lex[i][
                    0] == "}" or lex[i][0] == "if" or lex[i][0] == "while" or lex[i][0] == "switch" or lex[i][
                    0] == "for" or lex[i][0] == "continue" or lex[i][0] == "break" or lex[i][0] == "class" or lex[i][
                    0] == "DT" or lex[i][0] == "ID" or lex[i][0] == "return" or lex[i][0] == "main" or lex[i][
                    0] == ")" or lex[i][0] == "case" or lex[i][0] == ":" or lex[i][0] == ";"):
            if (lex[i][0] == "["):
                i += 1
                if (OE()[0]):
                    if (lex[i][0] == "]"):
                        i += 1
                        if (T2()[0]):
                            # if(T3()):
                            return [True, lex[i][2], lex[i][1]]
            elif (lex[i][0] == "$" or lex[i][0] == "MDM" or lex[i][0] == "PM" or lex[i][0] == "ROP" or lex[i][
                0] == "&&" or lex[i][0] == "LOP" or lex[i][0] == ")" or lex[i][0] == "]" or lex[i][0] == ";" or lex[i][
                      0] == ":" or lex[i][0] == "if" or lex[i][0] == "while" or lex[i][0] == "switch" or lex[i][
                      0] == "for" or lex[i][0] == "conitnue" or lex[i][0] == "break" or lex[i][0] == "class" or lex[i][
                      0] == "inc_dec" or lex[i][0] == "ID" or lex[i][0] == "DT" or lex[i][0] == "return" or lex[i][
                      0] == "main" or lex[i][0] == "}" or lex[i][0] == "case" or lex[i][0] == "." or lex[i][0] == "[" or
                  lex[i][0] == "(" or lex[i][0] == "AOP"):
                return [True, lex[i][2], lex[i][1]]

        return [False, lex[i][2], lex[i][1]]

    # T2 (Non-Terminal of T1)
    def T2():
        global i
        if (lex[i][0] == "ID" or lex[i][0] == "[" or lex[i][0] == "(" or lex[i][0] == "inc_dec" or lex[i][0] == "MDM" or
                lex[i][0] == "PM" or lex[i][0] == "ROP" or lex[i][0] == "&&" or lex[i][0] == "LOP" or lex[i][
                    0] == "const" or lex[i][0] == "!" or lex[i][0] == "]" or lex[i][0] == "." or lex[i][0] == "[" or
                lex[i][0] == "inc_dec" or lex[i][0] == "(" or lex[i][0] == "AOP" or lex[i][0] == "," or lex[i][
                    0] == "}" or lex[i][0] == "if" or lex[i][0] == "while" or lex[i][0] == "switch" or lex[i][
                    0] == "for" or lex[i][0] == "continue" or lex[i][0] == "break" or lex[i][0] == "class" or lex[i][
                    0] == "DT" or lex[i][0] == "ID" or lex[i][0] == "return" or lex[i][0] == "main" or lex[i][
                    0] == ")" or lex[i][0] == "case" or lex[i][0] == ":" or lex[i][0] == ";"):
            if (lex[i][0] == "ID"):
                i += 1
                if (lex[i][0] == "["):
                    i += 1
                    if (OE()[0]):
                        if (lex[i][0] == "]"):
                            i += 1
                            if (T2()[0]):
                                return [True, lex[i][2], lex[i][1]]
        elif (lex[i][0] == "$" or lex[i][0] == "[" or lex[i][0] == "(" or lex[i][0] == "inc_dec" or lex[i][
            0] == "MDM" or lex[i][0] == "PM" or lex[i][0] == "ROP" or lex[i][0] == "&&" or lex[i][0] == "LOP" or lex[i][
                  0] == "const" or lex[i][0] == "!" or lex[i][0] == "]" or lex[i][0] == "." or lex[i][0] == "[" or
              lex[i][0] == "inc_dec" or lex[i][0] == "(" or lex[i][0] == "AOP" or lex[i][0] == "," or lex[i][
                  0] == "}" or lex[i][0] == "if" or lex[i][0] == "while" or lex[i][0] == "switch" or lex[i][
                  0] == "for" or lex[i][0] == "continue" or lex[i][0] == "break" or lex[i][0] == "class" or lex[i][
                  0] == "DT" or lex[i][0] == "ID" or lex[i][0] == "return" or lex[i][0] == "main" or lex[i][0] == ")" or
              lex[i][0] == "case" or lex[i][0] == ":" or lex[i][0] == ";"):
            return [True, lex[i][2], lex[i][1]]

        return [False, lex[i][2], lex[i][1]]

    # T3 (Non-Terminal of T)
    def T3():
        global i
        if (lex[i][0] == "$" or lex[i][0] == "(" or lex[i][0] == "inc_dec" or lex[i][0] == "MDM" or lex[i][0] == "PM" or
                lex[i][0] == "ROP" or lex[i][0] == "&&" or lex[i][0] == "LOP" or lex[i][0] == "const" or lex[i][
                    0] == "!" or lex[i][0] == "]" or lex[i][0] == "." or lex[i][0] == "[" or lex[i][0] == "AOP" or
                lex[i][0] == "," or lex[i][0] == "}" or lex[i][0] == "if" or lex[i][0] == "while" or lex[i][
                    0] == "switch" or lex[i][0] == "for" or lex[i][0] == "continue" or lex[i][0] == "break" or lex[i][
                    0] == "class" or lex[i][0] == "DT" or lex[i][0] == "ID" or lex[i][0] == "return" or lex[i][
                    0] == "main" or lex[i][0] == ")" or lex[i][0] == "case" or lex[i][0] == ":" or lex[i][0] == ";"):
            if (Func_call()[0]):
                return [True, lex[i][2], lex[i][1]]
            elif (Inc_dec_1()[0]):
                return [True, lex[i][2], lex[i][1]]
            elif (lex[i][0] == "$" or lex[i][0] == "MDM" or lex[i][0] == "PM" or lex[i][0] == "ROP" or lex[i][
                0] == "&&" or lex[i][0] == "LOP" or lex[i][0] == "const" or lex[i][0] == "!" or lex[i][0] == "]" or
                  lex[i][0] == "." or lex[i][0] == "[" or lex[i][0] == "inc_dec" or lex[i][0] == "(" or lex[i][
                      0] == "AOP" or lex[i][0] == "," or lex[i][0] == "}" or lex[i][0] == "if" or lex[i][
                      0] == "while" or lex[i][0] == "switch" or lex[i][0] == "for" or lex[i][0] == "continue" or lex[i][
                      0] == "break" or lex[i][0] == "class" or lex[i][0] == "DT" or lex[i][0] == "ID" or lex[i][
                      0] == "return" or lex[i][0] == "main" or lex[i][0] == ")" or lex[i][0] == "case" or lex[i][
                      0] == ":" or lex[i][0] == ";"):
                return [True, lex[i][2], lex[i][1]]

        return [False, lex[i][2], lex[i][1]]

    # Func_Call (Non-Terminal of T3, A_List)
    def Func_call():
        global i
        if (lex[i][0] == "("):
            i += 1
            if (FC_Parameter()[0]):
                if (lex[i][0] == ")"):
                    i += 1
                    if (FN_List()[0]):
                        return [True, lex[i][2], lex[i][1]]
        return [False, lex[i][2], lex[i][1]]

    # FC_Parameters (Non-Terminal of Func_Call)
    def FC_Parameter():
        global i
        if (lex[i][0] == "ID" or lex[i][0] == ")"):
            if (lex[i][0] == "ID"):
                i += 1
                if (FP_List()[0]):
                    if (FP_List_2()[0]):
                        return [True, lex[i][2], lex[i][1]]
            elif (lex[i][0] == ")"):
                return [True, lex[i][2], lex[i][1]]

        return [False, lex[i][2], lex[i][1]]

    # FP_List (Non-Terminal of FC_Parameters)
    def FP_List():
        global i
        if (lex[i][0] == "," or lex[i][0] == "(" or lex[i][0] == ")"):
            if (lex[i][0] == ","):
                i += 1
                if (lex[i][0] == "ID"):
                    i += 1
                    if (FP_List()[0]):
                        return [True, lex[i][2], lex[i][1]]
            elif (lex[i][0] == "."):
                i += 1
                if (lex[i][0] == "ID"):
                    i += 1
                    if (FP_List()[0]):
                        return [True, lex[i][2], lex[i][1]]
            elif (lex[i][0] == "$" or lex[i][0] == "(" or lex[i][0] == ")"):
                return [True, lex[i][2], lex[i][1]]

        return [False, lex[i][2], lex[i][1]]

    # FP_List_2 (Non-Terminal of FC_Parameters)
    def FP_List_2():
        global i
        if (lex[i][0] == "(" or lex[i][0] == ")"):
            if (lex[i][0] == "("):
                i += 1
                if (lex[i][0] == ")"):
                    i += 1
                    if (FP_List()[0]):
                        return [True, lex[i][2], lex[i][1]]
            elif (lex[i][0] == ")"):
                return [True, lex[i][2], lex[i][1]]
            return [False, lex[i][2], lex[i][1]]

            # FN_List (Non-Terminal of Func_Call)

    def FN_List():
        global i
        if (lex[i][0] == "." or lex[i][0] == "ROP" or lex[i][0] == "PM"):
            if (lex[i][0] == "."):
                i += 1
                if (lex[i][0] == "ID"):
                    i += 1
                    if (lex[i][0] == "("):
                        i += 1
                        if (FC_Parameter()[0]):
                            if (lex[i][0] == ")"):
                                i += 1
                                return [True, lex[i][2], lex[i][1]]

            elif (FN3_List()[0]):
                if (FN1_List()[0]):
                    return [True, lex[i][2], lex[i][1]]

        elif (lex[i][0] == "$" or lex[i][0] == "if" or lex[i][0] == "while" or lex[i][0] == "switch" or lex[i][
            0] == "for" or lex[i][0] == "continue" or lex[i][0] == "break" or lex[i][0] == "class" or lex[i][
                  0] == "inc_dec" or lex[i][0] == "ID" or lex[i][0] == "DT" or lex[i][0] == "return" or lex[i][
                  0] == "main" or lex[i][0] == "}" or lex[i][0] == "case"):
            return [True, lex[i][2], lex[i][1]]

        return [False, lex[i][2], lex[i][1]]

    # FN3_List (Non-Terminal of FN_List)
    def FN3_List():
        global i
        if (lex[i][0] == "ROP" or lex[i][0] == "PM" or lex[i][0] == "MDM"):
            i += 1
            return [True, lex[i][2], lex[i][1]]

        return [False, lex[i][2], lex[i][1]]

    # FN1_List (Non-Terminal of FN_List)
    def FN1_List():
        global i
        if (lex[i][0] == "ID" or lex[i][0] == "int" or lex[i][0] == "Float" or lex[i][0] == "String" or lex[i][
            0] == "Char" or lex[i][0] == "bool_const"):
            if (lex[i][0] == "ID"):
                i += 1
                if (FN2_List()[0]):
                    return [True, lex[i][2], lex[i][1]]
            elif (Const()[0]):
                return [True, lex[i][2], lex[i][1]]

        return [False, lex[i][2], lex[i][1]]

    # FN2_List (Non-Terminal of FN1_List)
    def FN2_List():
        global i
        if (lex[i][0] == "(" or lex[i][0] == "ROP" or lex[i][0] == "PM" or lex[i][0] == "MDM"):
            if (lex[i][0] == "("):
                if (Func_call()[0]):
                    return [True, lex[i][2], lex[i][1]]
            elif (lex[i][0] == "ROP" or lex[i][0] == "PM" or lex[i][0] == "MDM"):
                if (FN3_List()[0]):
                    if (FN1_List()[0]):
                        return [True, lex[i][2], lex[i][1]]
        elif (lex[i][0] == "$" or lex[i][0] == "if" or lex[i][0] == "while" or lex[i][0] == "switch" or lex[i][
            0] == "for" or lex[i][0] == "continue" or lex[i][0] == "break" or lex[i][0] == "class" or lex[i][
                  0] == "inc_dec" or lex[i][0] == "ID" or lex[i][0] == "DT" or lex[i][0] == "return" or lex[i][
                  0] == "main" or lex[i][0] == "}" or lex[i][0] == "case"):
            return [True, lex[i][2], lex[i][1]]

        return [False, lex[i][2], lex[i][1]]

    # Inc_Dec (Non-Terminal of T3, A_List)
    def Inc_dec():
        global i
        if (lex[i][0] == "inc_dec"):
            i += 1
            return [True, lex[i][2], lex[i][1]]

        return [False, lex[i][2], lex[i][1]]

    # Const (Non-Terminal of T, Assign, A2_List, A4_List)
    def Const():
        global i
        if (lex[i][0] == "int" or lex[i][0] == "Float" or lex[i][0] == "String" or lex[i][0] == "Char" or lex[i][
            0] == "bool_const"):
            if (lex[i][0] == "int"):
                i += 1
                return [True, lex[i][2], lex[i][1]]
            elif (lex[i][0] == "Float"):
                i += 1
                return [True, lex[i][2], lex[i][1]]
            elif (lex[i][0] == "String"):
                i += 1
                return [True, lex[i][2], lex[i][1]]
            elif (lex[i][0] == "Char"):
                i += 1
                return [True, lex[i][2], lex[i][1]]
            elif (lex[i][0] == "bool_const"):
                i += 1
                return [True, lex[i][2], lex[i][1]]
        return [False, lex[i][2], lex[i][1]]

    # MDM_ (Non-Terminal of MDM)
    def MDM_():
        global i
        # print("next")
        if (lex[i][0] == "$" or lex[i][0] == "MDM" or lex[i][0] == "PM" or lex[i][0] == "ROP" or lex[i][0] == "&&" or
                lex[i][0] == "LOP" or lex[i][0] == "const" or lex[i][0] == "!" or lex[i][0] == "]" or lex[i][
                    0] == "." or lex[i][0] == "[" or lex[i][0] == "inc_dec" or lex[i][0] == "(" or lex[i][0] == "AOP" or
                lex[i][0] == "," or lex[i][0] == "}" or lex[i][0] == "if" or lex[i][0] == "while" or lex[i][
                    0] == "switch" or lex[i][0] == "for" or lex[i][0] == "continue" or lex[i][0] == "break" or lex[i][
                    0] == "class" or lex[i][0] == "DT" or lex[i][0] == "ID" or lex[i][0] == "return" or lex[i][
                    0] == "main" or lex[i][0] == ")" or lex[i][0] == "case" or lex[i][0] == ":" or lex[i][0] == ";"):
            if (lex[i][0] == "MDM"):
                i += 1
                if (T()[0]):
                    if (MDM_()[0]):
                        return [True, lex[i][2], lex[i][1]]

            elif (lex[i][0] == "LOP" or lex[i][0] == "$" or lex[i][0] == "PM" or lex[i][0] == "ROP" or lex[i][
                0] == "&&" or lex[i][0] == "LOP" or lex[i][0] == "const" or lex[i][0] == "!" or lex[i][0] == "]" or
                  lex[i][0] == "." or lex[i][0] == "[" or lex[i][0] == "inc_dec" or lex[i][0] == "(" or lex[i][
                      0] == "AOP" or lex[i][0] == "," or lex[i][0] == "}" or lex[i][0] == "if" or lex[i][
                      0] == "while" or lex[i][0] == "switch" or lex[i][0] == "for" or lex[i][0] == "continue" or lex[i][
                      0] == "break" or lex[i][0] == "class" or lex[i][0] == "DT" or lex[i][0] == "ID" or lex[i][
                      0] == "return" or lex[i][0] == "main" or lex[i][0] == ")" or lex[i][0] == "case" or lex[i][
                      0] == ":" or lex[i][0] == ";"):
                # print("next")
                return [True, lex[i][2], lex[i][1]]

        return [False, lex[i][2], lex[i][1]]

    # PM_ (Non-Terminal of PM)
    def PM_():
        global i
        if (lex[i][0] == "$" or lex[i][0] == "PM" or lex[i][0] == "ROP" or lex[i][0] == "&&" or lex[i][0] == "LOP" or
                lex[i][0] == "const" or lex[i][0] == "!" or lex[i][0] == "]" or lex[i][0] == "." or lex[i][0] == "[" or
                lex[i][0] == "inc_dec" or lex[i][0] == "(" or lex[i][0] == "AOP" or lex[i][0] == "," or lex[i][
                    0] == "}" or lex[i][0] == "if" or lex[i][0] == "while" or lex[i][0] == "switch" or lex[i][
                    0] == "for" or lex[i][0] == "continue" or lex[i][0] == "break" or lex[i][0] == "class" or lex[i][
                    0] == "DT" or lex[i][0] == "ID" or lex[i][0] == "return" or lex[i][0] == "main" or lex[i][
                    0] == ")" or lex[i][0] == "case" or lex[i][0] == ":" or lex[i][0] == ";"):
            if (lex[i][0] == "PM"):
                i += 1
                if (MDM()[0]):
                    if (PM_()[0]):
                        return [True, lex[i][2], lex[i][1]]
            # else:
            # return [True, lex[i][2], lex[i][1]]
            elif (lex[i][0] == "$" or lex[i][0] == "ROP" or lex[i][0] == "&&" or lex[i][0] == "LOP" or lex[i][
                0] == "const" or lex[i][0] == "!" or lex[i][0] == "]" or lex[i][0] == "." or lex[i][0] == "[" or lex[i][
                      0] == "inc_dec" or lex[i][0] == "(" or lex[i][0] == "AOP" or lex[i][0] == "," or lex[i][
                      0] == "}" or lex[i][0] == "if" or lex[i][0] == "while" or lex[i][0] == "switch" or lex[i][
                      0] == "for" or lex[i][0] == "continue" or lex[i][0] == "break" or lex[i][0] == "class" or lex[i][
                      0] == "DT" or lex[i][0] == "ID" or lex[i][0] == "return" or lex[i][0] == "main" or lex[i][
                      0] == ")" or lex[i][0] == "case" or lex[i][0] == ":" or lex[i][0] == ";"):
                return [True, lex[i][2], lex[i][1]]

        return [False, lex[i][2], lex[i][1]]

    # ROP_ (Non-Terminal of ROP)
    def ROP_():
        global i
        if (lex[i][0] == "$" or lex[i][0] == "ROP" or lex[i][0] == "&&" or lex[i][0] == "LOP" or lex[i][0] == "const" or
                lex[i][0] == "!" or lex[i][0] == "]" or lex[i][0] == "." or lex[i][0] == "[" or lex[i][
                    0] == "inc_dec" or lex[i][0] == "(" or lex[i][0] == "AOP" or lex[i][0] == "," or lex[i][0] == "}" or
                lex[i][0] == "if" or lex[i][0] == "while" or lex[i][0] == "switch" or lex[i][0] == "for" or lex[i][
                    0] == "continue" or lex[i][0] == "break" or lex[i][0] == "class" or lex[i][0] == "DT" or lex[i][
                    0] == "ID" or lex[i][0] == "return" or lex[i][0] == "main" or lex[i][0] == ")" or lex[i][
                    0] == "case" or lex[i][0] == ":" or lex[i][0] == ";"):
            if (lex[i][0] == "ROP"):
                i += 1
                if (PM()[0]):
                    if (ROP_()[0]):
                        return [True, lex[i][2], lex[i][1]]
            # else:
            # return [True, lex[i][2], lex[i][1]]
            elif (lex[i][0] == "$" or lex[i][0] == "&&" or lex[i][0] == "LOP" or lex[i][0] == "const" or lex[i][
                0] == "!" or lex[i][0] == "]" or lex[i][0] == "." or lex[i][0] == "[" or lex[i][0] == "inc_dec" or
                  lex[i][0] == "(" or lex[i][0] == "AOP" or lex[i][0] == "," or lex[i][0] == "}" or lex[i][0] == "if" or
                  lex[i][0] == "while" or lex[i][0] == "switch" or lex[i][0] == "for" or lex[i][0] == "continue" or
                  lex[i][0] == "break" or lex[i][0] == "class" or lex[i][0] == "DT" or lex[i][0] == "ID" or lex[i][
                      0] == "return" or lex[i][0] == "main" or lex[i][0] == ")" or lex[i][0] == "case" or lex[i][
                      0] == ":" or lex[i][0] == ";"):
                return [True, lex[i][2], lex[i][1]]

        return [False, lex[i][2], lex[i][1]]

    # AE_ (Non-Terminal of AE)
    def AE_():
        global i
        if (lex[i][0] == "$" or lex[i][0] == "&&" or lex[i][0] == "LOP" or lex[i][0] == "const" or lex[i][0] == "!" or
                lex[i][0] == "]" or lex[i][0] == "." or lex[i][0] == "[" or lex[i][0] == "inc_dec" or lex[i][
                    0] == "(" or lex[i][0] == "AOP" or lex[i][0] == "," or lex[i][0] == "}" or lex[i][0] == "if" or
                lex[i][0] == "while" or lex[i][0] == "switch" or lex[i][0] == "for" or lex[i][0] == "continue" or
                lex[i][0] == "break" or lex[i][0] == "class" or lex[i][0] == "DT" or lex[i][0] == "ID" or lex[i][
                    0] == "return" or lex[i][0] == "main" or lex[i][0] == ")" or lex[i][0] == "case" or lex[i][
                    0] == ":" or lex[i][0] == ";"):
            if (lex[i][0] == "&&"):
                i += 1
                if (ROP()[0]):
                    if (AE_()[0]):
                        return [True, lex[i][2], lex[i][1]]
            # else:
            # return [True, lex[i][2], lex[i][1]]
            elif (lex[i][0] == "$" or lex[i][0] == "LOP" or lex[i][0] == "const" or lex[i][0] == "!" or lex[i][
                0] == "]" or lex[i][0] == "." or lex[i][0] == "[" or lex[i][0] == "inc_dec" or lex[i][0] == "(" or
                  lex[i][0] == "AOP" or lex[i][0] == "," or lex[i][0] == "}" or lex[i][0] == "if" or lex[i][
                      0] == "while" or lex[i][0] == "switch" or lex[i][0] == "for" or lex[i][0] == "continue" or lex[i][
                      0] == "break" or lex[i][0] == "class" or lex[i][0] == "DT" or lex[i][0] == "ID" or lex[i][
                      0] == "return" or lex[i][0] == "main" or lex[i][0] == ")" or lex[i][0] == "case" or lex[i][
                      0] == ":" or lex[i][0] == ";"):
                return [True, lex[i][2], lex[i][1]]

        return [False, lex[i][2], lex[i][1]]

    # OE_ (Non-Terminal of OE)
    def OE_():
        global i
        # print("next")
        if (lex[i][0] == "$" or lex[i][0] == "LOP" or lex[i][0] == "]" or lex[i][0] == "." or lex[i][0] == "[" or
                lex[i][0] == "(" or lex[i][0] == "AOP" or lex[i][0] == "," or lex[i][0] == "}" or lex[i][0] == "if" or
                lex[i][0] == "while" or lex[i][0] == "switch" or lex[i][0] == "for" or lex[i][0] == "continue" or
                lex[i][0] == "break" or lex[i][0] == "class" or lex[i][0] == "inc_dec" or lex[i][0] == "DT" or lex[i][
                    0] == "ID" or lex[i][0] == "return" or lex[i][0] == "main" or lex[i][0] == ")" or lex[i][
                    0] == "case" or lex[i][0] == ":" or lex[i][0] == ";"):
            if (lex[i][0] == "LOP"):
                # print("next")
                i += 1
                if (AE()[0]):
                    if (OE_()[0]):
                        return [True, lex[i][2], lex[i][1]]
                # else:
                # return [True, lex[i][2], lex[i][1]]
            elif (lex[i][0] == "$" or lex[i][0] == "]" or lex[i][0] == "." or lex[i][0] == "[" or lex[i][0] == "(" or
                  lex[i][0] == "AOP" or lex[i][0] == "," or lex[i][0] == "}" or lex[i][0] == "if" or lex[i][
                      0] == "while" or lex[i][0] == "switch" or lex[i][0] == "for" or lex[i][0] == "continue" or lex[i][
                      0] == "break" or lex[i][0] == "class" or lex[i][0] == "inc_dec" or lex[i][0] == "DT" or lex[i][
                      0] == "ID" or lex[i][0] == "return" or lex[i][0] == "main" or lex[i][0] == ")" or lex[i][
                      0] == "case" or lex[i][0] == ":" or lex[i][0] == ";"):
                return [True, lex[i][2], lex[i][1]]
        return [False, lex[i][2], lex[i][1]]

    # Else (Non-Terminal of IF)
    def Else():
        global i
        if (lex[i][0] == "else" or lex[i][0] == "DT" or lex[i][0] == "ID" or lex[i][0] == "inc_dec" or lex[i][
            0] == "static" or lex[i][0] == "virtual" or lex[i][0] == "const" or lex[i][0] == "class" or lex[i][
            0] == "while" or lex[i][0] == "for" or lex[i][0] == "$" or lex[i][0] == "if" or lex[i][0] == "switch" or
                lex[i][0] == "break" or lex[i][0] == "continue" or lex[i][0] == "return" or lex[i][0] == "}"):
            if (lex[i][0] == "else"):
                i += 1
                if (EList()[0]):
                    return [True, lex[i][2], lex[i][1]]
            # else:
            # return [True, lex[i][2], lex[i][1]]
            elif (lex[i][0] == "$" or lex[i][0] == "if" or lex[i][0] == "while" or lex[i][0] == "switch" or lex[i][
                0] == "for" or lex[i][0] == "continue" or lex[i][0] == "break" or lex[i][0] == "class" or lex[i][
                      0] == "inc_dec" or lex[i][0] == "ID" or lex[i][0] == "DT" or lex[i][0] == "return" or lex[i][
                      0] == "main" or lex[i][0] == "}" or lex[i][0] == "case"):
                return [True, lex[i][2], lex[i][1]]
            return [False, lex[i][2], lex[i][1]]

    # E_List (Non-Terminal of Else)
    def EList():
        global i
        if (lex[i][0] == "if" or lex[i][0] == "{"):
            if (If()[0]):
                return [True, lex[i][2], lex[i][1]]
            elif (Body()[0]):
                return [True, lex[i][2], lex[i][1]]

        return [False, lex[i][2], lex[i][1]]

    # Switch (Non-terminal of SST)
    def Switch():
        global i
        if (lex[i][0] == "switch"):
            i += 1
            if (lex[i][0] == "("):
                i += 1
                if (OE()[0]):
                    if (lex[i][0] == ")"):
                        i += 1
                        if (lex[i][0] == "{"):
                            i += 1
                            if (switch_body()[0]):
                                if (lex[i][0] == "}"):
                                    i += 1
                                    return [True, lex[i][2], lex[i][1]]
        return [False, lex[i][2], lex[i][1]]

    # Switch_Body (Non-Terminal of Switch)
    def switch_body():
        global i
        if (lex[i][0] == "case" or lex[i][0] == "default" or lex[i][0] == "}"):
            if (lex[i][0] == "case"):
                i += 1
                if (OE()[0]):
                    if (lex[i][0] == ":"):
                        i += 1
                        # if(MST()[0]):      #
                        if (MST()[0]):
                            if (switch_body1()[0]):
                                return [True, lex[i][2], lex[i][1]]
            elif (Default()[0]):
                return [True, lex[i][2], lex[i][1]]
            else:
                return [True, lex[i][2], lex[i][1]]
        return [False, lex[i][2], lex[i][1]]

    # Switch_Body_1 (Non-Terminal of Switch_Body)
    def switch_body1():
        global i
        if (lex[i][0] == "case" or lex[i][0] == "default"):
            if (lex[i][0] == "case"):
                i += 1
                if (OE()[0]):
                    if (lex[i][0] == ":"):
                        i += 1
                        # if(MST()[0]):      #
                        if (MST()[0]):
                            if (switch_body1()[0]):
                                return [True, lex[i][2], lex[i][1]]
            elif (Default()[0]):
                return [True, lex[i][2], lex[i][1]]
            # else:
            # return [True, lex[i][2], lex[i][1]]
        elif (lex[i][0] == "$" or lex[i][0] == "}"):
            return [True, lex[i][2], lex[i][1]]
        return [False, lex[i][2], lex[i][1]]

    # Default (Non-Terminal of Switch Body)
    def Default():
        global i
        if (lex[i][0] == "default"):
            i += 1
            if (lex[i][0] == ":"):
                i += 1
                # if(MST()[0]): #
                if (MST()[0]):
                    if (switch_body1()[0]):
                        return [True, lex[i][2], lex[i][1]]
        return [False, lex[i][2], lex[i][1]]

    # while (non-Terminal of SST)
    def While():
        global i
        if (lex[i][0] == "while"):
            i += 1
            if (lex[i][0] == "("):
                i += 1
                if (OE()[0]):
                    if (lex[i][0] == ")"):
                        i += 1
                        if (Body()[0]):
                            return [True, lex[i][2], lex[i][1]]
        return [False, lex[i][2], lex[i][1]]

    # For (non-Terminal of SST)
    def For():
        global i
        if (lex[i][0] == "for"):
            i += 1
            if (lex[i][0] == "("):
                i += 1
                if (cond1()[0]):
                    if (lex[i][0] == ";"):
                        i += 1
                        if (cond2()[0]):
                            if (lex[i][0] == ";"):
                                i += 1
                                if (cond3()[0]):
                                    if (lex[i][0] == ")"):
                                        i += 1
                                        if (Body()[0]):
                                            return [True, lex[i][2], lex[i][1]]
        return [False, lex[i][2], lex[i][1]]

    # Cond_1 (Non-Terminal of For)
    def cond1():
        global i
        if (lex[i][0] == "ID" or "DT"):
            if (lex[i][0] == "ID"):
                i += 1
                if (lex[i][0] == "AOP"):
                    i += 1
                    if (OE()[0]):
                        return [True, lex[i][2], lex[i][1]]
                elif (lex[i][0] == ";"):
                    # i+= 1
                    return [True, lex[i][2], lex[i][1]]

            elif (lex[i][0] == "DT"):
                i += 1
                if (lex[i][0] == "ID"):
                    i += 1
                    if (lex[i][0] == "AOP"):
                        i += 1
                        if (OE()[0]):
                            return [True, lex[i][2], lex[i][1]]
                    elif (lex[i][0] == ";"):
                        # i+= 1
                        return [True, lex[i][2], lex[i][1]]

            elif (lex[i][0] == ";"):
                # i+= 1
                return [True, lex[i][2], lex[i][1]]
        return [False, lex[i][2], lex[i][1]]

    # Cond_2 (Non-Terminal of For)
    def cond2():
        global i
        if (lex[i][0] == "ID" or lex[i][0] == "inc_dec" or lex[i][0] == "int" or lex[i][0] == "Float" or lex[i][
            0] == "String" or lex[i][0] == "Char" or lex[i][0] == "bool_const" or lex[i][0] == "(" or lex[i][0] == "!"):
            if (OE()[0]):
                return [True, lex[i][2], lex[i][1]]
        elif (lex[i][0] == ";"):
            # i+=1
            return [True, lex[i][2], lex[i][1]]

        return [False, lex[i][2], lex[i][1]]

    # Cond_3 (Non-Terminal of For)
    def cond3():
        global i
        if (lex[i][0] == "ID" or lex[i][0] == ")"):
            if (lex[i][0] == "ID"):
                i += 1
                if (Cond_3_1()[0]):
                    return [True, lex[i][2], lex[i][1]]

            elif (lex[i][0] == ")"):
                return [True, lex[i][2], lex[i][1]]

        return [False, lex[i][2], lex[i][1]]

        # Cond_3_1 (Non-Terminal of Cond_3)

    def Cond_3_1():
        global i
        if (lex[i][0] == "AOP" or lex[i][0] == "ID" or lex[i][0] == "inc_dec" or lex[i][0] == "int" or lex[i][
            0] == "Float" or lex[i][0] == "String" or lex[i][0] == "Char" or lex[i][0] == "bool_const" or lex[i][
            0] == "(" or lex[i][0] == "!"):
            if (lex[i][0] == "AOP"):
                i += 1
                if (OE()[0]):
                    return [True, lex[i][2], lex[i][1]]
            elif (lex[i][0] == "ID" or lex[i][0] == "inc_dec" or lex[i][0] == "int" or lex[i][0] == "Float" or lex[i][
                0] == "String" or lex[i][0] == "Char" or lex[i][0] == "bool_const" or lex[i][0] == "(" or lex[i][
                      0] == "!"):
                if (OE()[0]):
                    return [True, lex[i][2], lex[i][1]]
        return [False, lex[i][2], lex[i][1]]

    # Function Declaration (Non-terminal of SST)
    def Func_dec():
        global i
        # print("check")
        if (F_List_1()[0]):
            # print("check")
            if (F_List_2()[0]):
                # print("check")
                if (lex[i][0] == "("):
                    i += 1
                    # print("next")
                    P = []
                    if (FD_Parameter(P)[0]):
                        if (lex[i][0] == ")"):
                            i += 1
                            if (Body()[0]):
                                return [True, lex[i][2], lex[i][1]]
        elif (lex[i][0] == "$"):
            return [True, lex[i][2], lex[i][1]]
        return [False, lex[i][2], lex[i][1]]

    # F_List_1 (non-terminal of Func_Dec)
    def F_List_1():
        global i
        if (lex[i][0] == "static" or lex[i][0] == "virtual" or lex[i][0] == "constant"):

            if (lex[i][0] == "static"):
                i += 1
                return [True, lex[i][2], lex[i][1]]
            elif (lex[i][0] == "virtual" and i + 2 <= len(tok_set)):
                i += 1
                return [True, lex[i][2], lex[i][1]]
            elif (lex[i][0] == "const" and i + 2 <= len(tok_set)):
                i += 1
                return [True, lex[i][2], lex[i][1]]
        return [False, lex[i][2], lex[i][1]]

    # F_List_2 (Non-Terminal of Func_Dec)
    def F_List_2():
        global i
        if (lex[i][0] == "DT" or lex[i][0] == "ID"):

            if (lex[i][0] == "DT"):
                i += 1

                if (lex[i][0] == "ID"):
                    i += 1
                    return [True, lex[i][2], lex[i][1]]
            elif (lex[i][0] == "ID" and i + 2 <= len(lex)):
                i += 1
                if (lex[i][0] == "ID" and i + 2 <= len(lex)):
                    i += 1
                    return [True, lex[i][2], lex[i][1]]
        return [False, lex[i][2], lex[i][1]]

    # FD_Parameter (Non-Terminal of Func_Dec)
    def FD_Parameter(P):
        global i
        if (lex[i][0] == "DT" or lex[i][0] == "ID"):
            if (lex[i][0] == "DT"):
                dt = lex[i][1]
                i += 1
                if (lex[i][0] == "ID"):
                    N = lex[i][1]
                    t = Insert_Scope_Table(N, dt, scope_stack[-1])

                    if (t == False):
                        print("Redeclaration Error")
                        return [False, lex[i][2], lex[i][1]]

                    P.append(dt)
                    i += 1
                    if (P_List(P)[0]):
                        return [True, lex[i][2], lex[i][1]]
            if (lex[i][0] == "ID"):
                i += 1
                if (lex[i][0] == "ID"):
                    i += 1
                    if (P_List(P)[0]):
                        return [True, lex[i][2], lex[i][1]]
        return [False, lex[i][2], lex[i][1]]

    # P_List (Non-Terminal of FD_Parameter, P_List_2)
    def P_List(P):
        global i
        if (lex[i][0] == "," or lex[i][0] == "["):
            if (lex[i][0] == ","):
                i += 1
                if (P_List_2(P)[0]):
                    return [True, lex[i][2], lex[i][1]]
            if (lex[i][0] == "["):
                i += 1
                if (OE()[0]):
                    if (lex[i][0] == "]"):
                        i += 1
                        if (P_List(P)[0]):  #
                            return [True, lex[i][2], lex[i][1]]
        elif (lex[i][0] == "$" or lex[i][0] == ")"):
            return [True, lex[i][2], lex[i][1]]
        return [False, lex[i][2], lex[i][1]]

    # P_List_2 (Non-Terminal of P_List)
    def P_List_2(P):
        global i
        if (lex[i][0] == "DT" or lex[i][0] == "ID"):
            if (lex[i][0] == "DT"):
                dt = lex[i][1]
                i += 1
                if (lex[i][0] == "ID"):
                    N = lex[i][1]
                    t = Insert_Scope_Table(N, dt, scope_stack[-1])
                    if (t == False):
                        print("Redeclaration Error")
                        return [False, lex[i][2], lex[i][1]]

                    P[0] += ","
                    P[0] += dt
                    i += 1
                    if (P_List(P)[0]):
                        return [True, lex[i][2], lex[i][1]]
            elif (lex[i][0] == "ID"):
                i += 1
                if (lex[i][0] == "ID"):
                    i += 1
                    if (P_List()[0]):
                        return [True, lex[i][2], lex[i][1]]
        return [False, lex[i][2], lex[i][1]]

    # Break (non-Terminal of SST)
    def Break():
        global i
        if (lex[i][0] == "break"):
            i += 1
            return [True, lex[i][2], lex[i][1]]
        return [False, lex[i][2], lex[i][1]]

    # Continue (Non-Terminal of SST)
    def Continue():
        global i
        if (lex[i][0] == "continue"):
            i += 1
            return [True, lex[i][2], lex[i][1]]
        return [False, lex[i][2], lex[i][1]]

    # Class (Non-Terminal of SST)
    def Class(am, cat):
        global i
        if (lex[i][0] == "class" or lex[i][0] == "$"):
            if (lex[i][0] == "class"):
                # print("Stuck")
                dt = lex[i][1]
                i += 1
                if (lex[i][0] == "ID"):
                    N = lex[i][1]
                    curr_class = N
                    i += 1
                    P = lex[i + 1][1]
                    # print("parent is",P)

                    if (INH()[0]):
                        # print("Call: ",N)
                        t = Insert_Class_Table(N, dt, am, cat, P, "-")
                        if (t == False):
                            print("RE Class Declaration Error!")
                            return [False, lex[i][2], lex[i][1]]
                        if (C_List(curr_class)[0]):
                            # print("Start", lex[i][0])
                            if (Start()[0]):
                                return [True, lex[i][2], lex[i][1]]
            if (lex[i][0] == "$"):
                return [True, lex[i][2], lex[i][1]]
        return [False, lex[i][2], lex[i][1]]

    # INH (Non-Terminal of Class)
    def INH():
        global i
        if (lex[i][0] == ":"):
            if (lex[i][0] == ":"):
                i += 1
                am = []  #
                if (AM(am)[0]):
                    if (lex[i][0] == "ID"):
                        i += 1
                        return [True, lex[i][2], lex[i][1]]
                # else:         #
                #     return [True, lex[i][2], lex[i][1]]
                elif (lex[i][0] == "ID"):  #
                    i += 1
                    return [True, lex[i][2], lex[i][1]]
        elif (lex[i][0] == "$" or lex[i][0] == "{"):
            return [True, lex[i][2], lex[i][1]]
        return [False, lex[i][2], lex[i][1]]

    # AM (Non-Terminal of INH)
    def AM(am):
        global i
        if (lex[i][0] == "AM"):
            if (lex[i][0] == "AM"):
                am.append(lex[i][1])
                i += 1
                # print("Am",lex[i][0], am)
                return [True, lex[i][2], lex[i][1]]
        return [False, lex[i][2], lex[i][1]]

    # C_List (Non-Terminal of Class)
    def C_List(curr_class):
        global i
        if (lex[i][0] == "{"):
            if (lex[i][0] == "{"):
                Create_Scopee()
                i += 1
                if (Class_Body(curr_class)[0]):
                    if (lex[i][0] == "}"):
                        i += 1
                        return [True, lex[i][2], lex[i][1]]
            else:
                return [True, lex[i][2], lex[i][1]]
        return [False, lex[i][2], lex[i][1]]

    # C_Body (Non-Terminal of C_List)
    def Class_Body(curr_class):
        global i
        am = []
        if (AM(am)[0]):
            # i+=1
            if (lex[i][0] == ":"):
                i += 1
                # print("check")
                if (C_List_2(am, curr_class)[0]):
                    # int abc
                    if (Class_Body(curr_class)[0]):
                        return [True, lex[i][2], lex[i][1]]

        elif (lex[i][0] == "$" or lex[i][0] == "}"):
            return [True, lex[i][2], lex[i][1]]
        return [False, lex[i][2], lex[i][1]]

    # C_List2 (Non-Terminal of C_Body)
    def C_List_2(am, curr_class):
        global i
        if (lex[i][0] == "DT" or lex[i][0] == "ID" or lex[i][0] == "static" or lex[i][0] == "virtual" or lex[i][
            0] == "const" or lex[i][0] == "}"):
            if (lex[i][0] == "DT"):
                dt = lex[i][1]
                i += 1
                if (lex[i][0] == "ID"):
                    N = lex[i][1]
                    i += 1
                    if (C_List_3(N, dt, am, curr_class)):
                        return [True, lex[i][2], lex[i][1]]

            elif (lex[i][0] == "ID "):
                dt = lex[i][1]
                i += 1
                if (lex[i][0] == "ID"):
                    N = lex[i][1]
                    i += 1
                    if (C_List_3(N, dt, am, curr_class)):
                        return [True, lex[i][2], lex[i][1]]

            elif (lex[i][0] == "static" or lex[i][0] == "virtual" or lex[i][0] == "const"):
                i += 1
                if (Func_dec()):
                    return [True, lex[i][2], lex[i][1]]

            elif (lex[i][0] == "$" or lex[i][0] == "}" or lex[i][0] == "AM"):
                # i+=1
                return [True, lex[i][2], lex[i][1]]

        return [False, lex[i][2], lex[i][1]]

    # C_List_3 (Non-Terminal of C_List_2)
    def C_List_3(N, dt, am, curr_class):
        global i
        if (lex[i][0] == "[" or lex[i][0] == "AOP" or lex[i][0] == "," or lex[i][0] == "DT" or lex[i][0] == "ID" or
                lex[i][0] == "static" or lex[i][0] == "virtual" or lex[i][0] == "const" or lex[i][0] == "("):
            if (lex[i][0] == "[" or lex[i][0] == "AOP" or lex[i][0] == "," or lex[i][0] == "DT" or lex[i][0] == "ID"):
                t = Insert_Class_Data(N, dt, am, "-", curr_class)
                # print("series is",N ,dt , am , "-",curr_class)
                # Name ,Type , Acess_M  , Type_M, Class_Name
                if (t == False):
                    print("Redeclaration Error!")
                    return [False, lex[i][2], lex[i][1]]

                if (Dec(dt, curr_class, am, "")):
                    if (C_List_2(am, curr_class)):
                        return [True, lex[i][2], lex[i][1]]



            elif (lex[i][0] == "("):
                if (Func_dec_1(dt, N, curr_class)):
                    if (C_List_2(am, curr_class)):
                        return [True, lex[i][2], lex[i][1]]


            elif (lex[i][0] == "ID"):
                i += 1
                if (C_List_4()):
                    return [True, lex[i][2], lex[i][1]]

        elif (lex[i][0] == "$" or lex[i][0] == "}" or lex[i][0] == "AM"):
            return [True, lex[i][2], lex[i][1]]

        return [False, lex[i][2], lex[i][1]]

    # C_List_4 (Non-Terminal of C_List_3)
    def C_List_4():
        global i
        if (lex[i][0] == "[" or lex[i][0] == "AOP" or lex[i][0] == "," or lex[i][0] == "DT" or lex[i][0] == "ID" or
                lex[i][0] == "static" or lex[i][0] == "virtual" or lex[i][0] == "const" or lex[i][0] == "("):
            if (Obj_Dec()):
                if (C_List_2()[0]):
                    return [True, lex[i][2], lex[i][1]]
            elif (Func_dec_1(dt, N)[0]):
                if (Func_dec_1(dt, N)[0]):
                    return [True, lex[i][2], lex[i][1]]

        elif (lex[i][0] == "$"):
            return [True, lex[i][2], lex[i][1]]

        return [False, lex[i][2], lex[i][1]]

        # Obj_Dec (Non-Terminal of C_List_4,S_List_3)

    def Obj_Dec(N):
        global i
        if (lex[i][0] == "[" or lex[i][0] == "AOP" or lex[i][0] == ","):
            if (obj(N)[0]):
                return [True, lex[i][2], lex[i][1]]

            elif (lex[i][0] == "if" or lex[i][0] == "while" or lex[i][0] == "switch" or lex[i][0] == "for" or lex[i][
                0] == "continue" or lex[i][0] == "break" or lex[i][0] == "class" or lex[i][0] == "inc_dec" or lex[i][
                      0] == "ID" or lex[i][0] == "DT" or lex[i][0] == "return" or lex[i][0] == "main" or lex[i][
                      0] == "}" or lex[i][0] == "case"):
                return [True, lex[i][2], lex[i][1]]

        return [False, lex[i][2], lex[i][1]]

    # Obj (Non-Terminal of Obj_Dec)
    def obj(N):
        global i
        if (lex[i][0] == "[" or lex[i][0] == "AOP" or lex[i][0] == ","):
            if (lex[i][0] == "["):
                if (obj_array()[0]):
                    return [True, lex[i][2], lex[i][1]]
            elif (lex[i][0] == "AOP"):
                if (obj_1()[0]):
                    return [True, lex[i][2], lex[i][1]]
            elif (lex[i][0] == ","):
                if (obj_2()[0]):
                    return [True, lex[i][2], lex[i][1]]
            elif (lex[i][0] == "if" or lex[i][0] == "while" or lex[i][0] == "switch" or lex[i][0] == "for" or lex[i][
                0] == "continue" or lex[i][0] == "break" or lex[i][0] == "class" or lex[i][0] == "inc_dec" or lex[i][
                      0] == "ID" or lex[i][0] == "DT" or lex[i][0] == "return" or lex[i][0] == "main" or lex[i][
                      0] == "}" or lex[i][0] == "case"):
                return [True, lex[i][2], lex[i][1]]
        return [False, lex[i][2], lex[i][1]]

    # Obj_array (Non-Terminal of Obj)
    def obj_array():
        global i
        if (lex[i][0] == "["):
            if (lex[i][0] == "["):
                i += 1
                if (OE()[0]):
                    if (lex[i][0] == "]"):
                        i += 1
                        if (O_Init_1()[0]):
                            return [True, lex[i][2], lex[i][1]]
        return [False, lex[i][2], lex[i][1]]

    # O_Init_1 (Non-Terminal of Obj_Array)
    def O_Init_1():
        global i
        if (lex[i][0] == "AOP"):
            if (lex[i][0] == "AOP"):
                i += 1
                if (lex[i][0] == "{"):
                    i += 1
                    if (O_Init_2()[0]):
                        if (lex[i][0] == "}"):
                            i += 1
                            return [True, lex[i][2], lex[i][1]]

        return [False, lex[i][2], lex[i][1]]

    # O_Init_2 (Non-Terminal of O_Init_1)
    def O_Init_2():
        global i
        if (lex[i][0] == "ID" or lex[i][0] == "inc_dec" or lex[i][0] == "int" or lex[i][0] == "Float" or lex[i][
            0] == "String" or lex[i][0] == "Char" or lex[i][0] == "bool_const" or lex[i][0] == "(" or lex[i][0] == "!"):
            if (OE()[0]):
                if (O_Init_3()[0]):
                    return [True, lex[i][2], lex[i][1]]
            elif (lex[i][0] == "}"):
                return [True, lex[i][2], lex[i][1]]

        return [False, lex[i][2], lex[i][1]]

    # O_Init_3 (Non-Terminal of O_Init_2)
    def O_Init_3():
        global i
        if (lex[i][0] == "," or lex[i][0] == "$"):
            if (lex[i][0] == ","):
                i += 1
                if (OE()[0]):
                    if (O_Init_3()[0]):
                        return [True, lex[i][2], lex[i][1]]
            elif (lex[i][0] == "}" or lex[i][0] == "$"):
                return [True, lex[i][2], lex[i][1]]

        return [False, lex[i][2], lex[i][1]]

    # Obj_1 (Non-Terminal of Obj)
    def obj_1():
        global i
        if (lex[i][0] == "AOP"):
            if (lex[i][0] == "AOP"):
                i += 1
                if (lex[i][0] == "new"):
                    i += 1
                    if (obj_List()[0]):
                        return [True, lex[i][2], lex[i][1]]
                else:
                    if (obj_List()[0]):
                        return [True, lex[i][2], lex[i][1]]
        return [False, lex[i][2], lex[i][1]]

    # Obj_List (Non-Terminal of Obj_1)
    def obj_List():
        global i
        if (lex[i][0] == "ID" or lex[i][0] == "inc_dec" or lex[i][0] == "int" or lex[i][0] == "Float" or lex[i][
            0] == "String" or lex[i][0] == "Char" or lex[i][0] == "bool_const" or lex[i][0] == "(" or lex[i][0] == "!"):
            if (OE()[0]):
                return [True, lex[i][2], lex[i][1]]

        return [False, lex[i][2], lex[i][1]]

    # Obj_2 (Non-Terminal of Obj)
    def obj_2(N):
        global i
        if (lex[i][0] == "," or lex[i][0] == "$"):  # WARIHA ADDING $
            if (lex[i][0] == ","):
                i + 1
                if (lex[i][0] == "ID"):
                    N2 = lex[i][1]
                    t = Insert_Scope_Table(N2, N, scope_stack[-1])
                    if (t == False):
                        print("Redeclaration Error")
                        return [False, lex[i][2], lex[i][1]]

                    i += 1
                    if (obj_2(N)[0]):
                        return [True, lex[i][2], lex[i][1]]
            elif (lex[i][0] == "$" or lex[i][0] == "if" or lex[i][0] == "while" or lex[i][0] == "switch" or lex[i][
                0] == "for" or lex[i][0] == "continue" or lex[i][0] == "break" or lex[i][0] == "class" or lex[i][
                      0] == "inc_dec" or lex[i][0] == "ID" or lex[i][0] == "DT" or lex[i][0] == "return" or lex[i][
                      0] == "main" or lex[i][0] == "}" or lex[i][0] == "case"):
                return [True, lex[i][2], lex[i][1]]
        return [False, lex[i][2], lex[i][1]]

    # Inc_Dec_1 (non-Terminal of SST, T)
    def Inc_dec_1():
        global i
        if (lex[i][0] == "inc_dec"):
            i += 1
            if (lex[i][0] == "ID"):
                i += 1
                if (I_List()[0]):
                    return [True, lex[i][2], lex[i][1]]
            elif (lex[i][0] == ")" or lex[i][0] == "$"):
                return [True, lex[i][2], lex[i][1]]
        return [False, lex[i][2], lex[i][1]]

    # I_List (Non-Terminal of Inc_Dec_1)
    def I_List():
        global i
        if (lex[i][0] == "[" or lex[i][0] == "."):
            if (lex[i][0] == "["):
                i += 1
                if (OE()[0]):
                    if (lex[i][0] == "]"):
                        i += 1
                        if (I_List_2()[0]):
                            return [True, lex[i][2], lex[i][1]]

            elif (I_List_2()[0]):
                return [True, lex[i][2], lex[i][1]]
        elif (lex[i][0] == "$" or lex[i][0] == "if" or lex[i][0] == "while" or lex[i][0] == "switch" or lex[i][
            0] == "for" or lex[i][0] == "continue" or lex[i][0] == "break" or lex[i][0] == "class" or lex[i][
                  0] == "inc_dec" or lex[i][0] == "ID" or lex[i][0] == "DT" or lex[i][0] == "return" or lex[i][
                  0] == "main" or lex[i][0] == "}" or lex[i][0] == "case"):
            return [True, lex[i][2], lex[i][1]]
        return [False, lex[i][2], lex[i][1]]

    # I_List_2 (Non-Terminal of I_List)
    def I_List_2():
        global i
        if (lex[i][0] == "."):
            i += 1
            if (lex[i][0] == "ID"):
                i += 1
                return [True, lex[i][2], lex[i][1]]

            elif (lex[i][0] == "if" or lex[i][0] == "while" or lex[i][0] == "switch" or lex[i][0] == "for" or lex[i][
                0] == "continue" or lex[i][0] == "break" or lex[i][0] == "class" or lex[i][0] == "inc_dec" or lex[i][
                      0] == "ID" or lex[i][0] == "DT" or lex[i][0] == "return" or lex[i][0] == "main" or lex[i][
                      0] == "}" or lex[i][0] == "case"):

                return [True, lex[i][2], lex[i][1]]
        return [False, lex[i][2], lex[i][1]]

    # S_List (non-Terminal of SST)
    def S_List(N):
        global i
        if (lex[i][0] == "." or lex[i][0] == "[" or lex[i][0] == "inc_dec" or lex[i][0] == "(" or lex[i][0] == "AOP" or
                lex[i][0] == "ID" or lex[i][0] == "ROP"):
            if (S1_List()[0]):
                if (S2_List()[0]):
                    return [True, lex[i][2], lex[i][1]]
            elif (lex[i][0] == "AOP"):
                i += 1
                if (Assign()[0]):
                    return [True, lex[i][2], lex[i][1]]
            elif (lex[i][0] == "ID"):
                t = lookup_Class_Table(N)
                if (t == "Not Present"):
                    print("Class Is Not Decleared!")
                    return False
                N1 = lex[i][1]
                i += 1
                if (S_List_3(N, N1)[0]):
                    return [True, lex[i][2], lex[i][1]]

            elif (lex[i][0] == "ROP"):
                i += 1
                if (OE()[0]):
                    return [True, lex[i][2], lex[i][1]]

            # elif(lex[i][0] == "$"):
            # return [True, lex[i][2], lex[i][1]]
        return [False, lex[i][2], lex[i][1]]

    # S1_List (Non-Terminal of S_List)
    def S1_List():
        global i
        if (lex[i][0] == "." or lex[i][0] == "[" or lex[i][0] == "inc_dec" or lex[i][0] == "("):
            if (lex[i][0] == "."):
                i += 1
                if (lex[i][0] == "ID"):
                    i += 1
                    if (S3_List()[0]):
                        return [True, lex[i][2], lex[i][1]]

            elif (lex[i][0] == "["):

                i += 1
                if (OE()[0]):
                    if (lex[i][0] == "]"):
                        i += 1
                        if (S3_List()[0]):
                            return [True, lex[i][2], lex[i][1]]
            elif (lex[i][0] == "$" or lex[i][0] == "inc_dec" or lex[i][0] == "("):
                return [True, lex[i][2], lex[i][1]]
        return [False, lex[i][2], lex[i][1]]

    # S3_List (Non-Terminal of S1_List)
    def S3_List():
        global i  # (adding $)
        if (lex[i][0] == "." or lex[i][0] == "[ " or lex[i][0] == "inc_dec" or lex[i][0] == "("):
            if (lex[i][0] == "."):
                i += 1
                if (lex[i][0] == "ID"):
                    i += 1
                    if (S3_List()[0]):
                        return [True, lex[i][2], lex[i][1]]
            elif (lex[i][0] == "["):
                i += 1
                if (OE()[0]):
                    if (lex[i][0] == "]"):
                        i += 1
                        return [True, lex[i][2], lex[i][1]]
            elif (lex[i][0] == "$" or lex[i][0] == "inc_dec" or lex[i][0] == "("):
                return [True, lex[i][2], lex[i][1]]
        return [False, lex[i][2], lex[i][1]]

    # Assign (Non-Terminal of S_List)
    def Assign():
        global i
        if (lex[i][0] == "int" or lex[i][0] == "Float" or lex[i][0] == "String" or lex[i][0] == "Char" or lex[i][
            0] == "bool_const" or lex[i][0] == "ID"):
            if (Const()[0]):
                return [True, lex[i][2], lex[i][1]]
            elif (lex[i][0] == "ID"):
                i += 1
                if (A_List()[0]):
                    return [True, lex[i][2], lex[i][1]]

        return [False, lex[i][2], lex[i][1]]

    # A_List (Non-Terminal of Assign)
    def A_List():
        global i
        if (lex[i][0] == "$" or lex[i][0] == "inc_dec" or lex[i][0] == "(" or lex[i][0] == "AOP" or lex[i][0] == "PM" or
                lex[i][0] == "MDM" or lex[i][0] == "ROP"):
            if (Inc_dec()[0]):
                return [True, lex[i][2], lex[i][1]]
            elif (Func_call()[0]):
                return [True, lex[i][2], lex[i][1]]
            elif (lex[i][0] == "AOP"):
                i += 1
                if (lex[i][0] == "ID"):
                    i += 1
                    if (A1_List()[0]):
                        return [True, lex[i][2], lex[i][1]]
            elif (A3_List()[0]):
                if (A4_List()[0]):
                    return [True, lex[i][2], lex[i][1]]
            # elif(lex[i][0] == "$"):
            #   return [True, lex[i][2], lex[i][1]]
            elif (lex[i][0] == "if" or lex[i][0] == "while" or lex[i][0] == "switch" or lex[i][0] == "for" or lex[i][
                0] == "continue" or lex[i][0] == "break" or lex[i][0] == "class" or lex[i][0] == "inc_dec" or lex[i][
                      0] == "ID" or lex[i][0] == "DT" or lex[i][0] == "return" or lex[i][0] == "main" or lex[i][
                      0] == "}" or lex[i][0] == "case" or lex[i][0] == "$" or lex[i][0] == "default"):
                return [True, lex[i][2], lex[i][1]]

        return [False, lex[i][2], lex[i][1]]

    # A1_List (Non-Terminal of A_List)
    def A1_List():
        global i
        if (lex[i][0] == "AOP"):
            i += 1
            if (A2_List()[0]):
                return [True, lex[i][2], lex[i][1]]
        elif (lex[i][0] == "if" or lex[i][0] == "while" or lex[i][0] == "switch" or lex[i][0] == "for" or lex[i][
            0] == "continue" or lex[i][0] == "break" or lex[i][0] == "class" or lex[i][0] == "inc_dec" or lex[i][
                  0] == "ID" or lex[i][0] == "DT" or lex[i][0] == "return" or lex[i][0] == "main" or lex[i][0] == "}" or
              lex[i][0] == "case" or lex[i][0] == "$" or lex[i][0] == "default"):
            return [True, lex[i][2], lex[i][1]]

        return [False, lex[i][2], lex[i][1]]

    # A2_List (Non-Terminal of A1_List)
    def A2_List():
        global i
        if (lex[i][0] == "int" or lex[i][0] == "Float" or lex[i][0] == "String" or lex[i][0] == "Char" or lex[i][
            0] == "bool_const" or lex[i][0] == "ID"):
            if (lex[i][0] == "ID"):
                i += 1
                if (A1_List()[0]):  # A2 to A1_list
                    return [True, lex[i][2], lex[i][1]]
            elif (Const()[0]):
                return [True, lex[i][2], lex[i][1]]

        return [False, lex[i][2], lex[i][1]]

    # A3_List (Non-Terminal of A_List)
    def A3_List():
        global i
        if (lex[i][0] == "PM" or lex[i][0] == "MDM" or lex[i][0] == "ROP"):
            if (lex[i][0] == "PM"):
                i += 1
                return [True, lex[i][2], lex[i][1]]
            elif (lex[i][0] == "MDM"):
                i += 1
                return [True, lex[i][2], lex[i][1]]
            elif (lex[i][0] == "ROP"):
                i += 1
                return [True, lex[i][2], lex[i][1]]

        return [False, lex[i][2], lex[i][1]]

    # A4_List (Non-Terminal of A_List, A5_List)
    def A4_List():
        global i
        if (lex[i][0] == "int" or lex[i][0] == "Float" or lex[i][0] == "String" or lex[i][0] == "Char" or lex[i][
            0] == "bool_const" or lex[i][0] == "ID"):
            if (lex[i][0] == "ID"):
                i += 1
                if (A5_List()[0]):
                    return [True, lex[i][2], lex[i][1]]
            elif (Const()):
                if (A5_List()[0]):
                    return [True, lex[i][2], lex[i][1]]

        return [False, lex[i][2], lex[i][1]]

    # A5_List (Non-Terminal of A4_List)
    def A5_List():
        global i
        if (lex[i][0] == "PM" or lex[i][0] == "MDM" or lex[i][0] == "ROP"):
            if (lex[i][0] == "PM"):
                i += 1
                if (A4_List()[0]):
                    return [True, lex[i][2], lex[i][1]]
            elif (lex[i][0] == "MDM"):
                i += 1
                if (A4_List()[0]):
                    return [True, lex[i][2], lex[i][1]]
            elif (lex[i][0] == "ROP"):
                i += 1
                if (A4_List()[0]):
                    return [True, lex[i][2], lex[i][1]]
        elif (lex[i][0] == "if" or lex[i][0] == "while" or lex[i][0] == "switch" or lex[i][0] == "for" or lex[i][
            0] == "continue" or lex[i][0] == "break" or lex[i][0] == "class" or lex[i][0] == "inc_dec" or lex[i][
                  0] == "ID" or lex[i][0] == "DT" or lex[i][0] == "return" or lex[i][0] == "main" or lex[i][0] == "}" or
              lex[i][0] == "case" or lex[i][0] == "$" or lex[i][0] == "default"):
            return [True, lex[i][2], lex[i][1]]

        return [False, lex[i][2], lex[i][1]]

    # S_List_3 (Non-Terminal of S_List)
    def S_List_3(N, N1):
        global i
        if (lex[i][0] == "[" or lex[i][0] == "AOP" or lex[i][0] == "," or lex[i][0] == "if" or lex[i][0] == "while" or
                lex[i][0] == "switch" or lex[i][0] == "for" or lex[i][0] == "continue" or lex[i][0] == "break" or
                lex[i][0] == "class" or lex[i][0] == "inc_dec" or lex[i][0] == "ID" or lex[i][0] == "DT" or lex[i][
                    0] == "return" or lex[i][0] == "main" or lex[i][0] == "}" or lex[i][0] == "("):
            if (lex[i][0] == "[" or lex[i][0] == "AOP" or lex[i][0] == ","):
                t = Insert_Scope_Table(N1, N, scope_stack[-1])
                if (t == False):
                    print("Redeclaration Error")
                    return [False, lex[i][2], lex[i][1]]

                if (Obj_Dec(N)[0]):
                    return [True, lex[i][2], lex[i][1]]


            elif (lex[i][0] == "("):
                if (Func_dec_1(dt, N)[0]):
                    return [True, lex[i][2], lex[i][1]]
        elif (lex[i][0] == "$" or lex[i][0] == "if" or lex[i][0] == "while" or lex[i][0] == "switch" or lex[i][
            0] == "for" or lex[i][0] == "continue" or lex[i][0] == "break" or lex[i][0] == "class" or lex[i][
                  0] == "inc_dec" or lex[i][0] == "ID" or lex[i][0] == "DT" or lex[i][0] == "return" or lex[i][
                  0] == "main" or lex[i][0] == "}" or lex[i][0] == "case"):
            return [True, lex[i][2], lex[i][1]]

        return [False, lex[i][2], lex[i][1]]


    # S_List_2 (non-Terminal of SST)
    def S_List_2(dt, N):
        global i
        if (lex[i][0] == "[" or lex[i][0] == "AOP" or lex[i][0] == "," or lex[i][0] == "(" or lex[i][0] == "if" or
                lex[i][0] == "while" or lex[i][0] == "switch" or lex[i][0] == "for" or lex[i][0] == "continue" or
                lex[i][0] == "break" or lex[i][0] == "class" or lex[i][0] == "inc_dec" or lex[i][0] == "ID" or lex[i][
                    0] == "DT" or lex[i][0] == "return" or lex[i][0] == "main" or lex[i][0] == "}" or lex[i][
                    0] == "case" or lex[i][0] == "$" or lex[i][0] == "default"):
            if (lex[i][0] == "[" or lex[i][0] == "AOP" or lex[i][0] == ","):
                t = Insert_Scope_Table(N, dt, scope_stack[-1])
                if (t == False):
                    print("Redeclaration Error")
                    return [False, lex[i][2], lex[i][1]]
                if (Dec(dt, N, "-", "-")[0]):
                    return [True, lex[i][2], lex[i][1]]
            elif (lex[i][0] == "("):
                # if(Func_dec_1(dt,N)[0]):
                if (Func_dec_1(dt, N)[0]):
                    return [True, lex[i][2], lex[i][1]]
            elif (lex[i][0] == "if" or lex[i][0] == "while" or lex[i][0] == "switch" or lex[i][0] == "for" or lex[i][
                0] == "continue" or lex[i][0] == "break" or lex[i][0] == "class" or lex[i][0] == "inc_dec" or lex[i][
                      0] == "ID" or lex[i][0] == "DT" or lex[i][0] == "return" or lex[i][0] == "main" or lex[i][
                      0] == "}" or lex[i][0] == "case" or lex[i][0] == "$" or lex[i][0] == "default"):
                if (lex[i][0] == "$"):
                    t = Insert_Scope_Table(N, dt, scope_stack[-1])
                    if (t == False):
                        print("Redeclaration Error")
                        return [False, lex[i][2], lex[i][1]]

                    return [True, lex[i][2], lex[i][1]]

                # return [True, lex[i][2], lex[i][1]]
        return [False, lex[i][2], lex[i][1]]

    # Dec (Non-Terminal of S_List_2, C_List_3)
    def Dec(dt, curr_class, am, Type_M):
        global i
        # print("I am Declaring",lex[i][0])
        if (lex[i][0] == "[" or lex[i][0] == "AOP" or lex[i][0] == ","):
            if (Init_1(dt, curr_class, am, Type_M)[0]):
                return [True, lex[i][2], lex[i][1]]
        elif (lex[i][0] == "if" or lex[i][0] == "while" or lex[i][0] == "switch" or lex[i][0] == "for" or lex[i][
            0] == "continue" or lex[i][0] == "break" or lex[i][0] == "class" or lex[i][0] == "inc_dec" or lex[i][
                  0] == "ID" or lex[i][0] == "DT" or lex[i][0] == "return" or lex[i][0] == "main" or lex[i][0] == "}" or
              lex[i][0] == "case" or lex[i][0] == "$"):
            return [True, lex[i][2], lex[i][1]]

        return [False, lex[i][2], lex[i][1]]

    # Init_1 (Non-Terminal of Dec, Init_3)
    def Init_1(dt, curr_class, am, Type_M):
        global i
        if (lex[i][0] == "[" or lex[i][0] == "AOP" or lex[i][0] == "," or lex[i][0] == "$"):
            if (lex[i][0] == "["):
                if (array()[0]):
                    return [True, lex[i][2], lex[i][1]]

            elif (lex[i][0] == "AOP"):
                if (Init_2()[0]):
                    return [True, lex[i][2], lex[i][1]]
            elif (lex[i][0] == ","):
                if (Init_3(dt, curr_class, am, Type_M)[0]):
                    return [True, lex[i][2], lex[i][1]]
        elif (lex[i][0] == "if" or lex[i][0] == "while" or lex[i][0] == "switch" or lex[i][0] == "for" or lex[i][
            0] == "continue" or lex[i][0] == "break" or lex[i][0] == "class" or lex[i][0] == "inc_dec" or lex[i][
                  0] == "ID" or lex[i][0] == "DT" or lex[i][0] == "return" or lex[i][0] == "main" or lex[i][0] == "}" or
              lex[i][0] == "case" or lex[i][0] == "$"):
            return [True, lex[i][2], lex[i][1]]

        return [False, lex[i][2], lex[i][1]]

    # Array (Non-Terminal of Init_1)
    def array():
        global i
        if (lex[i][0] == "["):
            if (lex[i][0] == "["):
                i += 1
                if (OE()[0]):
                    if (lex[i][0] == "]"):
                        i += 1
                        if (Init_5()[0]):
                            return [True, lex[i][2], lex[i][1]]
        return [False, lex[i][2], lex[i][1]]

    # Init_5 (Non-Terminal of Array)
    def Init_5():
        global i
        if (lex[i][0] == "AOP"):
            i += 1
            if (lex[i][0] == "{"):
                i += 1
                if (Init_4()[0]):
                    if (lex[i][0] == "}"):
                        i += 1
                        return [True, lex[i][2], lex[i][1]]

            elif (lex[i][0] == "if" or lex[i][0] == "while" or lex[i][0] == "switch" or lex[i][0] == "for" or lex[i][
                0] == "continue" or lex[i][0] == "break" or lex[i][0] == "class" or lex[i][0] == "inc_dec" or lex[i][
                      0] == "ID" or lex[i][0] == "DT" or lex[i][0] == "return" or lex[i][0] == "main" or lex[i][
                      0] == "}" or lex[i][0] == "case"):
                return [True, lex[i][2], lex[i][1]]

        return [False, lex[i][2], lex[i][1]]

    # Init_4 (Non-Terminal of Init_5)
    def Init_4():
        global i
        if (lex[i][0] == "ID" or lex[i][0] == "inc_dec" or lex[i][0] == "int" or lex[i][0] == "Float" or lex[i][
            0] == "String" or lex[i][0] == "Char" or lex[i][0] == "bool_const" or lex[i][0] == "(" or lex[i][0] == "!"):
            if (OE()[0]):
                if (Init_6()[0]):
                    return [True, lex[i][2], lex[i][1]]
            elif (lex[i][0] == "}"):
                # i+=1
                return [True, lex[i][2], lex[i][1]]
        return [False, lex[i][2], lex[i][1]]

    # Init_6 (Non-Terminal of Init_4)
    def Init_6():
        global i
        if (lex[i][0] == ","):
            if (lex[i][0] == ","):
                i += 1
                if (OE()[0]):
                    if (Init_6()[0]):
                        return [True, lex[i][2], lex[i][1]]
        elif (lex[i][0] == "}" or lex[i][0] == "$"):
            # i+=1
            return [True, lex[i][2], lex[i][1]]

        return [False, lex[i][2], lex[i][1]]

    # Init_2 (Non-Terminal of Init_1)
    def Init_2():
        global i
        if (lex[i][0] == "AOP"):
            if (lex[i][0] == "AOP"):
                i += 1
                if (D_List()[0]):
                    return [True, lex[i][2], lex[i][1]]
        return [False, lex[i][2], lex[i][1]]

    # D_List (Non-Terminal of Init_2)
    def D_List():
        global i
        if (lex[i][0] == "ID" or lex[i][0] == "inc_dec" or lex[i][0] == "int" or lex[i][0] == "Float" or lex[i][
            0] == "String" or lex[i][0] == "Char" or lex[i][0] == "bool_const" or lex[i][0] == "(" or lex[i][0] == "!"):
            if (OE()[0]):
                return [True, lex[i][2], lex[i][1]]

        return [False, lex[i][2], lex[i][1]]

    # Init_3 (Non-Terminal of Init_1)
    def Init_3(dt, curr_class, am, Type_M):
        global i
        if (lex[i][0] == ","):
            i += 1
            N = lex[i][1]
            if (lex[i][0] == "ID"):
                t = Insert_Scope_Table(N, dt, scope_stack[-1])
                if (t == False):
                    print("Redeclaration Error!")
                    return [False, lex[i][2], lex[i][1]]
            else:
                t = Insert_Class_Data(N, dt, am, "+", curr_class)
                if (t == False):
                    print("Redeclaration Error!")
                    return [False, lex[i][2], lex[i][1]]

            i += 1
            if (Init_1(dt, curr_class, am, Type_M)):
                return [True, lex[i][2], lex[i][1]]

        return [False, lex[i][2], lex[i][1]]

    # Func_dec_1 (Non-Terminal of S_List_2, S_List_3)
    # def Func_dec_1(dt,N):
    def Func_dec_1(dt, N, curr_class):
        global i
        if (lex[i][0] == "("):
            Create_Scopee()
            i += 1
            P = []
            if (FD_Parameter(P)):
                if (lex[i][0] == ")"):
                    param = P[0] + "->" + dt
                    t = Insert_Class_Data(N, param, "default", "*", curr_class)
                    if (t == False):
                        print("Redeclaration Error !")
                        return [False, lex[i][2], lex[i][1]]
                    i += 1
                    if (Func_Body()):
                        return [True, lex[i][2], lex[i][1]]

        elif (lex[i][0] == "$"):
            return [True, lex[i][2], lex[i][1]]

        return [False, lex[i][2], lex[i][1]]

    # Return (Non-Terminal of SSTF)
    def Return():
        global i
        if (lex[i][0] == "return"):
            i += 1
            if (OE()[0]):
                return [True, lex[i][2], lex[i][1]]
        return [False, lex[i][2], lex[i][1]]

    # Calling Start Terminal to Find whether Parse Tree has returned True or False!
    d = Start()
    if (d[0] == True):
        print(f"sYNTAX\n Class Part (Parsed): {d[2]}")
    else:
        print(f" INVALID SYNTAX at Line Number {d[1]} \n Class Part (Unparsed): {d[2]}")

    # Syntax End


# End Code (Start)
os.system("cls")
LA()
Syntax_Ana()
# print("length of class table: ",class_Table.__len__())
print("Main Table")
for x in range(class_Table.__len__()):
    print(class_Table[x].Name, "|", class_Table[x].Type, "|", class_Table[x].AM, "|", class_Table[x].Type_M, "|",
          class_Table[x].Cat, "|", class_Table[x].parent, "|",
          data_Items[data_Items[x].Class_Name == class_Table[x].Name])

print("\n")

print('Data table')
for y in range(data_Items.__len__()):
    print(data_Items[y].Name, data_Items[y].Type, data_Items[y].Acess_M, data_Items[y].Type_M, data_Items[y].Class_Name)

print("\n")

print("Symbol Table")
for z in range(scopeTable.__len__()):
    print(scopeTable[z].Name, scopeTable[z].Type, scopeTable[z].scope)
print("\n")






