import re
from func import *

def tokenize(source_code):
    # array to store token values
    tokens = []

    # read input from words.txt where words stored
    with open("words.txt", "r") as file:
        lines = file.readlines()
        
    list = {}

    for line in lines:
        parts = line.strip().split(',')
        if len(parts) >= 2:
            value = parts[0].strip()
            Line_no = parts[1].strip()
        list[value] = Line_no

    # Loop through each source code word
    for word, Line_no in list.items():

        if isID(word):
            if isKeyword(word):
                classification = isKeyword(word)
                tokens.append([classification, word, Line_no])
            else:
                tokens.append(['ID', word, Line_no])

        elif isChar(word):
            tokens.append(['Char', word, Line_no])
        
        elif isString(word):
            tokens.append(['String', word, Line_no])

        elif isInt(word):
            tokens.append(['Int', word, Line_no])

        elif isFloat(word):
            tokens.append(['Float', word, Line_no])

        elif isOperator(word):
            classification = isOperator(word)
            tokens.append([classification, word, Line_no])

        elif isPunctuator(word):
            classification = isPunctuator(word)
            tokens.append([classification, word, Line_no])

        else:
            tokens.append(['Invalid Lexeme', word, Line_no])
    
    return tokens