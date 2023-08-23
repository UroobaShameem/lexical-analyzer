
def word_break(source_code,Line):
    tokens = []
    Line = 1
    i = 0
    while i < len(source_code):
        char = source_code[i]

        if char.isalpha() or char == "_":
            # Identifier
            token = char
            i += 1
            while i < len(source_code) and (source_code[i].isalnum() or source_code[i] == "_"):
                token += source_code[i]
                i += 1
            tokens.append((token,Line))

        elif char.isdigit():
            # Number
            token = char
            i += 1
            while i < len(source_code) and (source_code[i].isdigit() or source_code[i] == "."):
                token += source_code[i]
                i += 1
            tokens.append((token,Line))

        elif char in "+-*/&|:,'":
            # Operators
            token = char
            i += 1
            if i < len(source_code) and source_code[i] == char:
                token += char
                i += 1
            tokens.append((token,Line))

        elif char == "=":
            # Check for ==
            token = char
            i += 1
            if i < len(source_code) and source_code[i] == "=":
                token += char
                i += 1
                tokens.append((token,Line))
            else:
                tokens.append((token,Line))
        elif char == "+":
            # Check for ++ and +=
            token = char
            i += 1
            if i < len(source_code) and source_code[i] == "+" or source_code[i] == "=":
                token += char
                i += 1
                tokens.append((token,Line))
            else:
                tokens.append((token,Line))

        elif char in "(){}<>!":
            # Check for various operators
            token = char
            i += 1
            if i < len(source_code) and source_code[i] == "=":
                token += source_code[i]
                i += 1
            tokens.append((token,Line))

        elif char.isspace():
            # Whitespace
            i += 1

        elif char == "\n":
            # Newline
            tokens.append((token,Line))
            i += 1
            Line +=1
 
        elif char == "\r":
            # Carriage return
            tokens.append((token,Line))
            i += 1

        elif char == "\t":
            # Tab
            tokens.append((token,Line))
            i += 1
        
        elif char == "#":
            # Single-line comment
            i += 1
            while i < len(source_code) and source_code[i] != "\n":
                i += 1
            # Move to the next line
            Line += 1

        else:
            raise ValueError(f"Invalid character: {char}")

    return tokens


