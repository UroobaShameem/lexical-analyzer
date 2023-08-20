import re

# Define regular expressions for different token types
regex_patterns = {
    'identifier': r'[a-zA-Z_]\w*',
    'number': r'\d+(\.\d+)?',
    'multi_operator': r'\+\+|--|==|<=',
    'operator': r'[\+\-\*/]',
    'parenthesis': r'[()]',
    'whitespace': r'\s+',
    'newline': r'\n',
    'carriage_return': r'\r',
    'tab': r'\t'
}

def tokenize_python_code(source_code):
    tokens = []
    
    while source_code:
        match = None
        for token_type, pattern in regex_patterns.items():
            match = re.match(pattern, source_code)
            if match:
                token_value = match.group(0)
                if token_type != 'whitespace':
                    tokens.append((token_type, token_value))
                source_code = source_code[len(token_value):]
                break
        
        if not match:
            raise ValueError(f"Invalid character: {source_code[0]}")
    
    return tokens

def read_source_code_from_user():
    source_code = input("Enter your Python source code (press Enter twice to finish):\n")
    return source_code

def main():
    input_code = read_source_code_from_user()

    try:
        tokens = tokenize_python_code(input_code)
    except ValueError as e:
        print(e)
        return

    print("Tokens:")
    for token_type, token_value in tokens:
        print(f"Token Type: {token_type}, Token Value: {token_value}")

if __name__ == "__main__":
    main()
