import re
from func import *

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

    # This will check if a token has datatype declaration
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

    # This will look for an operator
    elif isOperator(word):
        classification = isOperator(word)
        tokens.append([classification, word, Line_no])

    # This will look for integer items and cast them as a number
    elif isPunctuator(word):
        classification = isPunctuator(word)
        tokens.append([classification, word, Line_no])

def write_output():
    with open("output.txt", "w") as file:
        for token in tokens:
            file.write(f"[{token[0]}, {token[1]}, {token[2]}]\n")

