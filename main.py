from word_break import word_break
from tokenization import *


def input():
    with open("input.txt", "r") as source_file:
        source_code = source_file.read()
    return source_code

def output():
    code= input()
    tokens = word_break(code)
    with open("words.txt", "a") as output_file:
        for token_value,Line_no in tokens:
            output_file.write(f"{token_value}, {Line_no}\n")

def write_output():
    LA = tokenize(output())
    with open("output.txt", "w") as file:
        for token in LA:
            file.write(f"[{token[0]}, {token[1]}, {token[2]}]\n")


def main():
    input()
    output()
    write_output()

if __name__ == "__main__":
    main()
