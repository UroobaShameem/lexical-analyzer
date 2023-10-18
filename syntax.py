# Define an empty array to store the class parts
t = []

# Open the tokens.txt file for reading
with open('tokens.txt', 'r') as file:
    # Iterate through each line in the file
    for line in file:
        # Split each line into parts using a comma as the separator
        parts = line.strip().split(', ')
        if len(parts) >= 1:
            # Remove the opening square bracket "[" from the first part
            class_part = parts[0].lstrip('[')
            # Add the cleaned "class part" to the class_parts array
            t.append(class_part)


def S0(tokens, i):
    if (tokens[i] in ["while", "if", "static", "DT", "fun", "ID", "class"]):
        i, logic = S(tokens, i)  # Pass 'tokens' and 'i' to the S function
        return i, logic

    return i, False

def S(tokens, i):
    if (tokens[i] in ["while", "if", "ID"]):
        i, logic = while_(tokens, i)
        return i, logic
    
    if (tokens[i] in ["abstract", "static", "class", "DT", "fun"]):
        i, logic = S2(tokens, i)
        return i, logic
    
    return i, False

def S2(tokens, i):
    if tokens[i] == "abstract":
        i += 1  # Move to the next token
        if (tokens[i] in ["class","fun"]):
            i, logic = anew(tokens,i)
            return i, logic
    
    elif tokens[i] == "class":
        i, logic = class_def(tokens, i)
        return i, logic
    
    elif tokens[i] == "DT":
        i, logic = fdec(tokens, i)
        return i, logic
    
    elif tokens[i] == "fun":
        i, logic = fun_st(tokens, i)
        return i, logic
    
    elif tokens[i] == "static":
        i += 1  # Move to the next token
        if tokens[i]== "fun":
            i, logic = snew(tokens,i)
            return i, logic
    
    return i, False

def anew(tokens,i):
    if tokens[i] == "fun":
        i += 1  # Move to the next token
        if tokens[i] == "abstract":
            i += 1  # Move to the next token
            if (tokens[i] in ["class","fun"]):
                i, logic = anew(tokens,i)
                return i, logic
    
            elif tokens[i] == "class":
                i, logic = last(tokens, i)
                return i, logic
            
            elif tokens[i] == "DT":
                i, logic = fdec(tokens, i)
                return i, logic
            
            elif tokens[i] == "fun":
                i, logic = fun_st(tokens, i)
                return i, logic
            
            elif tokens[i] == "static":
                i += 1  # Move to the next token
                if tokens[i]== "fun":
                    i, logic = snew(tokens,i)
                    return i, logic
                
        return i, False

def fdec(tokens,i):
    if tokens[i] == "DT":
        i += 1  # Move to the next token
        if tokens[i] == "ID":
            i += 1  # Move to the next token
            if tokens[i] in ["=", ";"]:
                i, logic = init(tokens,i)
                return i, logic
    return i, False    

def snew(tokens,i):
    if tokens[i] == "fun":
        i, logic = fun_st(tokens,i)
        return i, logic
    
    if tokens[i] == "DT":
        i, logic = fdec(tokens,i)
        return i, logic
    
    return i, False

def init(tokens,i):
    if tokens[i] in ["=", ";"]:
                i, logic = initE(tokens,i)
                return i, logic
    return i, False

def initE(tokens,i): 
    if tokens[i] == "ID": #ID <new>
        i, logic = new(tokens,i)
        return i, logic
    
    elif tokens[i] in ["self", "super"]: #<TS> ID <LHP> <tdash> <edash>
            i, logic = TS(tokens,i)
            if tokens[i] == "ID":
                i += 1
                if tokens[i] in ["[", "(", "{", "."]:
                    i, logic = lhp(tokens, i)
                    if tokens[i] == "MDM":
                        i, logic = tdash(tokens, i)
                        if tokens[i] == "PM":
                            i, logic = edash(tokens, i)
                    
            return i, logic
    
    elif tokens[i] in ["int", "float", "char","string"]: #<const> <tdash> <edash>
        if tokens[i] == "MDM":
                        i, logic = tdash(tokens, i)
                        if tokens[i] == "PM":
                            i, logic = edash(tokens, i)
        return i, logic
    
    elif tokens[i] == "!":  # !<F> <TDASH> <EDASH>
            i += 1
            if tokens[i] in ["self", "super","int", "float", "char","string","(", "!", "ID"]: 
                i, logic = F(tokens,i)
                if tokens[i] == "MDM":
                        i, logic = tdash(tokens, i)
                        if tokens[i] == "PM":
                            i, logic = edash(tokens, i)
            return i, logic
    
    elif tokens[i] == "(":  # (<E>) <TDASH> <EDASH> 
            i += 1
            if tokens[i] in ["self", "super","int", "float", "char","string","(", "!", "ID"]: 
                i, logic = E(tokens,i)
                if tokens[i] == ")":  
                    i += 1
                    if tokens[i] == "MDM":
                            i, logic = tdash(tokens, i)
                            if tokens[i] == "PM":
                                i, logic = edash(tokens, i)
            return i, logic
    return i, False

def OE(tokens, i):
    if tokens[i] in ["self", "super", "ID", "(", "!", "int", "float", "TF", "char"]:
        i += 1
        return i, True  # Successfully parsed an expression
    else:
        return i, False  # Expression not recognized
    
def oedash(tokens,i):
    if tokens[i] == "||":
        i+=1
        if tokens[i] in ["self", "super","int", "float", "char","string","(", "!", "ID"]:
            i, logic = AE(tokens,i)
            return i, logic
    return i, False

def aedash(tokens,i):
    if tokens[i] == "&&":
        i+=1
        if tokens[i] in ["self", "super","int", "float", "char","string","(", "!", "ID"]:
            i, logic = RE(tokens,i)
            return i, logic
    return i, False

def redash(tokens,i):
    if tokens[i] == "ROP":
        i+=1
        if tokens[i] in ["self", "super","int", "float", "char","string","(", "!", "ID"]:
            i, logic = E(tokens,i)
            return i, logic
    return i, False

def edash(tokens,i):
    if tokens[i] == "PM":
        i+=1
        if tokens[i] in ["self", "super","int", "float", "char","string","(", "!", "ID"]:
            i, logic = T(tokens,i)
            return i, logic
    return i, False

def tdash(tokens,i):
    if tokens[i] == "MDM":
        i+=1
        if tokens[i] in ["self", "super","int", "float", "char","string","(", "!", "ID"]:
            i, logic = F(tokens,i)
            return i, logic
    return i, False

def AE(tokens,i):
    if tokens[i] in ["self", "super","int", "float", "char","string","(", "!", "ID"]: 
        i, logic = RE(tokens,i)
        if tokens[i] == "||":
             i, logic = aedash(tokens,i)
        return i, logic
    return i, False

def RE(tokens,i):
    if tokens[i] in ["self", "super","int", "float", "char","string","(", "!", "ID"]: 
        i, logic = E(tokens,i)
        if tokens[i] == "ROP":
             i, logic = redash(tokens,i)
        return i, logic
    return i, False

def E(tokens,i):
    if tokens[i] in ["self", "super","int", "float", "char","string","(", "!", "ID"]: 
        i, logic = T(tokens,i)
        if tokens[i] == "PM":
             i, logic = edash(tokens,i)
        return i, logic
    return i, False

def T(tokens,i):
    if tokens[i] in ["self", "super","int", "float", "char","string","(", "!", "ID"]: 
        i, logic = F(tokens,i)
        if tokens[i] == "MDM":
             i, logic = tdash(tokens,i)
        return i, logic
    return i, False

def F(tokens,i):
    if tokens[i] in ["self", "super","int", "float", "char","string","(", "!", "ID"]: 
        i, logic = last(tokens,i)
        return i, logic
    return i, False

def new(tokens,i):
    if tokens[i] in ["=", ";"]: #<init>
        i, logic = init(tokens,i)
        return i, logic
    
    elif tokens[i] in ["[", "(", "{", "."]: #<lhp> <tdash> <edash>
        i, logic = lhp(tokens, i)
        if tokens[i] == "MDM":
            i, logic = tdash(tokens, i)
            if tokens[i] == "PM":
                i, logic = edash(tokens, i)
                return i, logic
    return i, False

def TS(tokens,i):
    if tokens[i] == "self" or tokens[i] == "super":  
        i += 1
        if tokens[i] == ".":  
            i += 1
    return i, False

def lhp(tokens,i):

    return i, False

def class_def(tokens,i):

    return i, False

def fun_st(tokens,i):

    return i, False

def while_(tokens, i):
    if tokens[i] == "while":
        i += 1  # Move to the next token
        if tokens[i] == "(":
            i += 1  # Move to the next token
            if tokens[i] in ["self", "super", "ID", "(", "!", "int", "float", "TF", "char"]:
                i, logic = OE(tokens, i)
                if tokens[i] == ")":  # Check for the closing parenthesis
                    i += 1  # Move to the next token
                    if i < len(tokens) and tokens[i] == "{":  # Check for the opening curly brace
                        i += 1  # Move to the next token
                        if i < len(tokens) and tokens[i] == ";":
                            i += 1  # Move to the next token
                        elif i < len(tokens) and tokens[i] == "while"or tokens[i] == "if":
                            i, logic = SST(tokens, i)
                    # Add any additional logic specific to the while loop here
                    return i, logic
    return i, False

def SST(tokens, i):
    if tokens[i] == ";":
        i += 1  # Move to the next token
        return i, True  # Successfully parsed a statement
    else:
        return i, False  # Statement not recognized

def last(tokens,i):
    return i, True

# Execute Your Parser
index = 0
index, result = S0(t, index)

# Check Output
if result:
    print("Test Passed")
else:
    print("Test Failed")

