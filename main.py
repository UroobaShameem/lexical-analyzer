from word_break import word_break


def input():
    with open("input.txt", "r") as source_file:
        source_code = source_file.read()
    return source_code

def output():
    tokens = word_break(input())
    with open("output.txt", "a") as output_file:
        for token_value in tokens:
            output_file.write(f"Token Value: {token_value}\n")

def main():
    input_code = input()

    try:
        tokens = word_break(input_code)
    except ValueError as e:
        print(e)
        return

    output()

    # Store the tokens in an array
    token_array = tokens
    print("Token Array:", token_array)

if __name__ == "__main__":
    main()
