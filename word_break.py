import re

def word_break(source_code):
    tokens = []
    Line = 1
    i = 0

    while i < len(source_code):
        char = source_code[i]

        if char in "\n\r\t":
            # Newline, Carriage return, Tab
            #tokens.append((char, Line))
            i += 1
            if char == "\n":
                Line += 1

        elif char in "+-*/<>!=":
            # Operators
            token = char
            i += 1
            if i < len(source_code) and source_code[i] == "=":
                token += source_code[i]
                i += 1
            elif i < len(source_code) and char in "+-" and source_code[i] == char:
                token += char
                i += 1
            tokens.append((token, Line))

        elif char in "&|:,(){};":
            i += 1
            tokens.append((char, Line))

        elif char == "'":
            # Single-character or sequence enclosed in single quotes
            i += 1
            token = char

            if i < len(source_code) and source_code[i] == "\\":
                token += source_code[i]
                i += 1
                if i < len(source_code):
                    token += source_code[i]
                    i += 1
                    if token == "n":
                        token = "\n"  # Handle \n escape sequence
            else:
                if i < len(source_code):
                    token += source_code[i]
                    i += 1
            
            if i < len(source_code) and source_code[i] == "'":
                token += source_code[i]
                tokens.append((token, Line))
                i += 1
            else:
                tokens.append((token, Line))

        elif char == '"':
            # String enclosed in double quotes
            i += 1
            token = '"'
            while i < len(source_code):
                if source_code[i] == '"':
                    token += source_code[i]
                    i += 1
                    break
                elif source_code[i] == "\\" and i + 1 < len(source_code) and source_code[i + 1] == '"':
                    token += '\\"'
                    i += 2
                else:
                    token += source_code[i]
                    i += 1
            tokens.append((token, Line))

        elif char == ".":
            # Handling dot as part of a number or a separate token
            if i + 1 < len(source_code) and (source_code[i + 1].isdigit() or source_code[i + 1].isalpha()):
                token = char
                i += 1
                while i < len(source_code) and (source_code[i].isdigit() or source_code[i] == "." or source_code[i].isalpha()):
                    token += source_code[i]
                    i += 1
                tokens.append((token, Line))
            else:
                tokens.append((char, Line))
                i += 1

        elif char == "#":
            # Single-line comment
            i += 1
            while i < len(source_code) and source_code[i] != "\n":
                i += 1
            # Move to the next line
            #Line += 1
        
        elif char == "@" and i + 1 < len(source_code) and source_code[i + 1] == "@":
            # Multiline comment using "@@" at start and end
            i += 2
            while i < len(source_code) and not (source_code[i] == "@" and i + 1 < len(source_code) and source_code[i + 1] == "@"):
                if source_code[i] == "\n":
                    Line += 1
                i += 1
            if i < len(source_code):
                i += 2  # Skip over "@@"
            else:
                i += 1  # Skip over "@" to handle incomplete comment

        elif char.isspace():
            # Whitespace
            i += 1

        elif re.match(r"\w", char):
            # Alphanumeric characters
            token = char
            i += 1
            while i < len(source_code) and re.match(r"\w", source_code[i]):
                token += source_code[i]
                i += 1
            tokens.append((token, Line))

        else:
            tokens.append((char, Line))
            i += 1

    return tokens
