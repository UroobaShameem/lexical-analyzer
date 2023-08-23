from word_break import word_break
from tokenization import *


def input():
    with open("input.txt", "r") as source_file:
        source_code = source_file.read()
    return source_code

def output():
    tokens = word_break(input(),0)
    with open("words.txt", "a") as output_file:
        for token_value,Line in tokens:
            output_file.write(f"{token_value}, {Line}\n")

def main():
    input()
    output()
    write_output()

if __name__ == "__main__":
    main()
