import re

variable_pattern = r'[a-zA-Z][a-zA-Z0-9_]*[a-zA-Z0-9]*'

def word_break(source_code):
    tokens = []
    i = 0
    while i < len(source_code):
        char = source_code[i]

        if i == 0 and not re.match(variable_pattern, source_code[i:]):
            raise ValueError(f"Invalid variable name")

        if re.match(variable_pattern, source_code[i:]):
            match = re.match(variable_pattern, source_code[i:])
            if match is None:
                tokens.append(None)
                i += 1
                continue
            else:
                token_value = match.group(0)
                tokens.append(token_value)
                i += len(token_value)

        elif char.isdigit():
            # Number
            token = char
            i += 1
            while i < len(source_code) and (source_code[i].isdigit() or source_code[i] == "."):
                token += source_code[i]
                i += 1
            tokens.append(token)

        elif char in "+-*/&|:,'":
            # Operators
            token = char
            i += 1
            if i < len(source_code) and source_code[i] == char:
                token += char
                i += 1
            tokens.append(token)

        elif char == "=":
            # Check for ==
            token = char
            i += 1
            if i < len(source_code) and source_code[i] == "=":
                token += char
                i += 1
                tokens.append(token)
            else:
                tokens.append(char)

        elif char in "(){}<>!":
            # Check for various operators
            token = char
            i += 1
            if i < len(source_code) and source_code[i] == "=":
                token += source_code[i]
                i += 1
            tokens.append(token)

        elif char.isspace():
            # Whitespace
            i += 1

        elif char == "\n":
            # Newline
            tokens.append(char)
            i += 1

        elif char == "\r":
            # Carriage return
            tokens.append(char)
            i += 1

        elif char == "\t":
            # Tab
            tokens.append(char)
            i += 1

        else:
            raise ValueError(f"Invalid character: {char}")

    return tokens

def read_input():
    source_code = input("Enter your Python source code:\n")
    return source_code

def main():
    input_code = read_input()

    try:
        tokens = word_break(input_code)
    except ValueError as e:
        print(e)
        return

    print("Tokens:")
    for token_value in tokens:
        print(f"{token_value}")

if __name__ == "__main__":
    main()
