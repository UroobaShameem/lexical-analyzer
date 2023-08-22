import re      
from func import *                          

# array to store token values
tokens = []         

# read input from output.txt where words stored  
with open("output.txt", "r") as file:
    content = file.readlines()

#get only first part from each line
value_p = {}
for line in content:
    #separate on basis of ,
    parts = line.strip().split(',')
    if len(parts) >=2:
        Line_no= parts[1].strip()
        value= parts[0].strip()
        value_p[value]= Line_no
        #store line_no
        
# Loop through each source code word
for word in value_p.keys():
    
    # This will check if a token has datatype decleration
    if isDataType(word): 
        tokens.append(['DATATYPE', word, Line_no])
        
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