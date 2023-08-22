from word_break import word_break


def input():
    with open("input.txt", "r") as source_file:
        source_code = source_file.read()
    return source_code

def output():
    tokens = word_break(input(),0)
    with open("output.txt", "a") as output_file:
        for token_value,Line in tokens:
            output_file.write(f"{token_value}, {Line}\n")

def main():
    input()
    output()

if __name__ == "__main__":
    main()
