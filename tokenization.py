import re                                 

tokens = []                              
with open("output.txt", "r") as file:
    content = file.readlines()

values = []
for line in content:
    parts = line.strip().split(',')
    if parts:
        value= parts[0].strip()
        values.append(value)

# Loop through each source code word
for word in values:
    
    # This will check if a token has datatype decleration
    if word in ['str', 'int', 'bool']: 
        tokens.append(['DATATYPE', word])
        
    # This will look for an identifier which would be just a word
    elif re.match("[a-z]", word) or re.match("[A-Z]", word):
        tokens.append(['IDENTIFIER', word])
    
    # This will look for an operator
    elif word in '*-/+%=':
        tokens.append(['OPERATOR', word])
    # This will look for integer items and cast them as a number
    elif re.match(".[0-9]", word):
        if word[len(word) - 1] == ';': 
            tokens.append(["INTEGER", word[:-1]])
            tokens.append(['END_STATEMENT', ';'])
        else: 
            tokens.append(["INTEGER", word])

print(tokens) # Outputs the token array