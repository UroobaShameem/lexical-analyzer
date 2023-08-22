import re

def split_words(text):
    # Define the regular expression pattern to match words
    pattern = r'''(?x)          # Verbose mode for readability
                 \s+           # Match one or more white spaces
                 |             # OR
                 [][()"']      # Match any of the specified brackets or quotes
                 |             # OR
                 (?<!\w)-      # Match a hyphen that is not preceded by a word character
                 |             # OR
                 -(?!\w)       # Match a hyphen that is not followed by a word character
                 |             # OR
                 \w+           # Match one or more word characters
                 '''

    # Use the findall() function to find all occurrences of the pattern in the text
    words = re.findall(pattern, text)

    return words

# Example sentence with various characters
# sentence = "void Class A_B_c::35"
sentence = "Int a()"
word_list = split_words(sentence)

for word in word_list:
    print(word)