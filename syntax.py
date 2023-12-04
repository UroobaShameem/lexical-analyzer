# Define an empty array to store the class parts and values
t = []

# Open the tokens.txt file for reading
with open('tokens.txt', 'r') as file:
    # Iterate through each line in the file
    for line in file:
        # Split each line into parts using a comma as the separator
        parts = line.strip().split(', ')
        if len(parts) >= 3:  # Make sure there are at least three parts
            # Remove the opening square bracket "[" from the first part
            class_part = parts[0].lstrip('[')
            # Get the second and third parts as value_part and line
            value_part = parts[1]
            line_part = parts[2]
            # Append the class part, value part, and line to the array
            t.append({'cp': class_part, 'vp': value_part, 'line': line_part})

def S0(t, i):
    if (t[i]['cp'] in ["while", "if", "static", "DT", "fun", "ID", "class"]):
        i, logic = S(t, i)
        return i, logic

    return i, False

def S(t, i):
    if (t[i]['cp'] in ["while", "if", "ID"]):
        i, logic = while_(t, i)
        return i, logic

    if (t[i]['cp'] in ["abstract", "static", "class", "DT", "fun"]):
        i, logic = S2(t, i)
        return i, logic

    return i, False

def S2(t, i):
    if t[i]['cp'] == "abstract":
        i += 1 
        if (t[i]['cp'] in ["class", "fun"]):
            i, logic = anew(t, i)
            return i, logic

    elif t[i]['cp'] == "class":
        i, logic = class_def(t, i)
        return i, logic

    elif t[i]['cp'] == "DT":
        i, logic = fdec(t, i)
        return i, logic

    elif t[i]['cp'] == "fun":
        i, logic = fun_st(t, i)
        return i, logic
    
    elif t[i]['cp'] == "static":
        i += 1  # Move to the next token
        if t[i]['cp'] == "fun":
            i, logic = snew(t, i)
            return i, logic

    return i, False

def anew(tokens, i):
    if tokens[i]['cp'] == "fun":
        i += 1  # Move to the next token
        if tokens[i]['cp'] == "abstract":
            i += 1  # Move to the next token
            if tokens[i]['cp'] in ["class", "fun"]:
                i, logic = anew(tokens, i)
                return i, logic

            elif tokens[i]['cp'] == "class":
                i, logic = class_def(tokens, i)
                return i, logic

            elif tokens[i]['cp'] == "DT":
                i, logic = fdec(tokens, i)
                return i, logic

            elif tokens[i]['cp'] == "fun":
                i, logic = fun_st(tokens, i)
                return i, logic

            elif tokens[i]['cp'] == "static":
                i += 1  # Move to the next token
                if tokens[i]['cp'] == "fun":
                    i, logic = snew(tokens, i)
                    return i, logic

    return i, False

def fdec(tokens, i):
    if tokens[i]['cp'] == "DT":
        i += 1  # Move to the next token
        if tokens[i]['cp'] == "ID":
            i += 1  # Move to the next token
            if tokens[i]['cp'] in ["=", ";"]:
                i, logic = init(tokens, i)
                return i, logic
    return i, False

def snew(tokens, i):
    if tokens[i]['cp'] == "fun":
        i, logic = fun_st(tokens, i)
        return i, logic

    if tokens[i]['cp'] == "DT":
        i, logic = fdec(tokens, i)
        return i, logic

    return i, False

def init(tokens, i):
    if tokens[i]['cp'] in ["=", ";"]:
        i, logic = initE(tokens, i)
        return i, logic
    return i, False

def initE(tokens, i): 
    if tokens[i]['cp'] == "ID":  # ID <new>
        i, logic = new(tokens, i)
        return i, logic
    
    elif tokens[i]['cp'] in ["self", "super"]:  # <TS> ID <LHP> <tdash> <edash>
        i, logic = TS(tokens, i)
        if tokens[i]['cp'] == "ID":
            i += 1
            if tokens[i]['cp'] in ["[", "(", "{", "."]:
                i, logic = lhp(tokens, i)
                if tokens[i]['cp'] == "MDM":
                    i, logic = tdash(tokens, i)
                    if tokens[i]['cp'] == "PM":
                        i, logic = edash(tokens, i)
        return i, logic
    
    elif tokens[i]['cp'] in ["int", "float", "char", "string"]:  # <const> <tdash> <edash>
        if tokens[i]['cp'] == "MDM":
            i, logic = tdash(tokens, i)
            if tokens[i]['cp'] == "PM":
                i, logic = edash(tokens, i)
        return i, logic
    
    elif tokens[i]['cp'] == "!":  # !<F> <TDASH> <EDASH>
        i += 1
        if tokens[i]['cp'] in ["self", "super", "int", "float", "char", "string", "(", "!", "ID"]:
            i, logic = F(tokens, i)
            if tokens[i]['cp'] == "MDM":
                i, logic = tdash(tokens, i)
                if tokens[i]['cp'] == "PM":
                    i, logic = edash(tokens, i)
        return i, logic
    
    elif tokens[i]['cp'] == "(":  # (<E>) <TDASH> <EDASH> 
        i += 1
        if tokens[i]['cp'] in ["self", "super", "int", "float", "char", "string", "(", "!", "ID"]:
            i, logic = E(tokens, i)
            if tokens[i]['cp'] == ")":  
                i += 1
                if tokens[i]['cp'] == "MDM":
                    i, logic = tdash(tokens, i)
                    if tokens[i]['cp'] == "PM":
                        i, logic = edash(tokens, i)
        return i, logic
    
    return i, False

def OE(tokens, i):
    if tokens[i]['cp'] in ["self", "super", "ID", "(", "!", "int", "float", "TF", "char"]:
        i += 1
        return i, True  # Successfully parsed an expression
    else:
        return i, False  # Expression not recognized
    
def oedash(tokens, i):
    if tokens[i]['cp'] == "||":
        i += 1
        if tokens[i]['cp'] in ["self", "super", "int", "float", "char", "string", "(", "!", "ID"]:
            i, logic = AE(tokens, i)
            return i, logic
    return i, False

def aedash(tokens, i):
    if tokens[i]['cp'] == "&&":
        i += 1
        if tokens[i]['cp'] in ["self", "super", "int", "float", "char", "string", "(", "!", "ID"]:
            i, logic = RE(tokens, i)
            return i, logic
    return i, False

def redash(tokens, i):
    if tokens[i]['cp'] == "ROP":
        i += 1
        if tokens[i]['cp'] in ["self", "super", "int", "float", "char", "string", "(", "!", "ID"]:
            i, logic = E(tokens, i)
            return i, logic
    return i, False

def edash(tokens, i):
    if tokens[i]['cp'] == "PM":
        i += 1
        if tokens[i]['cp'] in ["self", "super", "int", "float", "char", "string", "(", "!", "ID"]:
            i, logic = T(tokens, i)
            return i, logic
    return i, False

def tdash(tokens, i):
    if tokens[i]['cp'] == "MDM":
        i += 1
        if tokens[i]['cp'] in ["self", "super", "int", "float", "char", "string", "(", "!", "ID"]:
            i, logic = F(tokens, i)
            return i, logic
    return i, False

def AE(tokens, i):
    if tokens[i]['cp'] in ["self", "super", "int", "float", "char", "string", "(", "!", "ID"]:
        i, logic = RE(tokens, i)
        if tokens[i]['cp'] == "||":
            i, logic = aedash(tokens, i)
        return i, logic
    return i, False

def RE(tokens, i):
    if tokens[i]['cp'] in ["self", "super", "int", "float", "char", "string", "(", "!", "ID"]:
        i, logic = E(tokens, i)
        if tokens[i]['cp'] == "ROP":
            i, logic = redash(tokens, i)
        return i, logic
    return i, False

def E(tokens, i):
    if tokens[i]['cp'] in ["self", "super", "int", "float", "char", "string", "(", "!", "ID"]:
        i, logic = T(tokens, i)
        if tokens[i]['cp'] == "PM":
            i, logic = edash(tokens, i)
        return i, logic
    return i, False

def T(tokens, i):
    if tokens[i]['cp'] in ["self", "super", "int", "float", "char", "string", "(", "!", "ID"]:
        i, logic = F(tokens, i)
        if tokens[i]['cp'] == "MDM":
            i, logic = tdash(tokens, i)
        return i, logic
    return i, False

def F(tokens, i):
    if tokens[i]['cp'] in ["self", "super"]: #"int", "float", "char", "string", "(", "!", "ID"]:
        i, logic = TS(tokens, i)
        if tokens[i]['cp'] == "ID":
            i +=1
            if tokens[i]['cp'] in ["{", "[", "(",".", "=", "assign_op","inc_dec", "mdm", "pm",
                                "rop","logical_op", ",",";",")", "}", "]"]:
                i, logic = lhp(tokens, i)
                return i, logic
    return i, False

def new(tokens, i):
    if tokens[i]['cp'] in ["=", ";"]:  # <init>
        i, logic = init(tokens, i)
        return i, logic

    elif tokens[i]['cp'] in ["[", "(", "{", "."]:  # <lhp> <tdash> <edash>
        i, logic = lhp(tokens, i)
        if tokens[i]['cp'] == "MDM":
            i, logic = tdash(tokens, i)
            if tokens[i]['cp'] == "PM":
                i, logic = edash(tokens, i)
                return i, logic
    return i, False

def TS(tokens, i):
    if tokens[i]['cp'] == "self" or tokens[i]['cp'] == "super":
        i += 1
        if tokens[i]['cp'] == ".":
            i += 1
    return i, False

def lhp(tokens,i):
    if tokens[i]['cp'] == "[":
        i, logic = array(tokens, i)
        return i, logic
    
    elif tokens[i]['cp'] == "(":
        i, logic = argument(tokens, i)
        return i, logic
    
    elif tokens[i]['cp'] == "{":
        i, logic = dict_(tokens, i)
        return i, logic
    
    elif tokens[i]['cp'] == ".":
        i, logic = lhp1(tokens, i)
        return i, logic

    return i, False

def class_def(tokens,i):

    return i, False

def fun_st(tokens, i):
    if tokens[i]['cp'] == "fun":  
        i += 1
        if tokens[i]['cp'] == "ID":  
            i += 1
            if tokens[i]['cp'] == "(":  
                i += 1
                if tokens[i]['cp'] == "DT":
                    i, logic = parameter(tokens, i)
                    if tokens[i]['cp'] == ")":  
                        i += 1
                        if tokens[i]['cp'] == "{":  
                            i += 1
                            if tokens[i]['cp'] in ["while", "back", "if", "ID"]: 
                                i, logic = MST(tokens, i)
                                if tokens[i]['cp'] == "}":  
                                    i += 1
                return i, logic
    return i, False

def parameter(tokens, i):
    if tokens[i]['cp'] == "DT":  
        i += 1
        if tokens[i]['cp'] == "ID":  
            i += 1
            if tokens[i]['cp'] in ["=", "[", ",", ")"]: 
                i, logic = p0(tokens, i)
                if tokens[i]['cp'] in [",", ")"]: 
                    i, logic = p1(tokens, i)
                return i, logic
    return i, False

def p0(tokens, i):
    if tokens[i]['cp'] == "=":  
        i += 1
        if tokens[i]['cp'] in ["self", "super", "int", "float", "char", "string", "(", "!", "ID"]: 
            i, logic = E(tokens, i)
            if tokens[i]['cp'] in [",", ")"]: 
                i, logic = p1(tokens, i)
                return i, logic
            
    elif tokens[i]['cp'] == "[":  
        i, logic = arr_dec(tokens, i)
        return i, logic
    return i, False

def p1(tokens, i):
    if tokens[i]['cp'] == ",":  
        i += 1
        if tokens[i]['cp'] == "DT":
            i, logic = parameter(tokens, i)
            return i, logic
    return i, False

def back_st(tokens, i):
    if tokens[i]['cp'] == "back":  
        i += 1
        if tokens[i]['cp'] in ["self", "super", "ID", "(", "!", "int", "float", "TF", "char"]:
            i, logic = OE(tokens, i)
            if tokens[i]['cp'] == ";":  
                i += 1
                return i, logic
    return i, False

def while_(tokens, i):
    if tokens[i]['cp'] == "while":
        i += 1  # Move to the next token
        if tokens[i]['cp'] == "(":
            i += 1  # Move to the next token
            if tokens[i]['cp'] in ["self", "super", "ID", "(", "!", "int", "float", "TF", "char"]:
                i, logic = OE(tokens, i)
                if tokens[i]['cp'] == ")":  # Check for the closing parenthesis
                    i += 1  # Move to the next token
                    if i < len(tokens) and tokens[i]['cp'] == "{":  # Check for the opening curly brace
                        i += 1  # Move to the next token
                        if i < len(tokens) and tokens[i]['cp'] == ";":
                            i += 1  # Move to the next token
                        elif i < len(tokens) and tokens[i]['cp'] == "while" or tokens[i]['cp'] == "if":
                            i, logic = SST(tokens, i)
                    # Add any additional logic specific to the while loop here
                    return i, logic
    return i, False

def array(tokens, i):
    if tokens[i]['cp'] == "[":
        i +=1
        if tokens[i]['cp'] in ["self", "super", "int", "float", "char", "string", "(", "!", "ID"]:
            i, logic = E(tokens, i)
        if tokens[i]['cp'] == "]":
            i +=1
        if tokens[i]['cp'] in ["[",")"]:
            i, logic = array1(tokens, i)
            return i, logic
    return i, False

def array1(tokens, i):
    if tokens[i]['cp'] == "[":
        i +=1
        if tokens[i]['cp'] in ["self", "super", "int", "float", "char", "string", "(", "!", "ID"]:
            i, logic = E(tokens, i)
        if tokens[i]['cp'] == "]":
            i +=1
            return i, logic

    if tokens[i]['cp'] == ")":
        i +=1
        return i, logic
    
    return i, False

def argument(tokens, i):
    if tokens[i]['cp'] in ["self", "super", "ID", "(", "!"]:
        i, logic = OE(tokens, i)
        if tokens[i]['cp'] == ",":
            i, logic = A1(tokens, i)
            return i, logic
        
    return i, False

def A1(tokens, i):
    if tokens[i]['cp'] == ",":
        i +=1
        if tokens[i]['cp'] == "(":
            i, logic = argument(tokens, i)
        return i, logic

    return i, False

def SST(tokens, i):
    if tokens[i]['cp'] == ";":
        i += 1  # Move to the next token
        return i, True  # Successfully parsed a statement
    else:
        return i, False  # Statement not recognized

def last(tokens, i):
    return i, True

def S0_from_tokens(tokens):
    i = 0
    i, logic = S0(tokens, i)
    return i, logic

# Execute Your Parser with a list of tokens
index, result = S0_from_tokens(t)

# Check Output
if result:
    print("Test Passed")
else:
    print("Test Failed")

