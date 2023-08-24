from word_break import word_break
from tokenization import tokenize

def read_input():
    with open("input.txt", "r") as source_file:
        source_code = source_file.read()
    return source_code

def write_output(output_tokens):
    with open("output.txt", "w") as file:
        for token in output_tokens:
            file.write(f"[{token[0]}, {token[1]}, {token[2]}]\n")

def main():
    source_code = read_input()
    tokens = word_break(source_code)

    with open("words.txt", "a") as output_file:
        for token_value, Line_no in tokens:
            output_file.write(f"{token_value}, {Line_no}\n")

    LA = tokenize(tokens)
    write_output(LA)

if __name__ == "__main__":
    main()
