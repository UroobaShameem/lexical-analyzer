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

def S0(tokens, i):
    print("s0")
    if tokens[i]['cp'] in ["while", "if", "static", "DT", "fun", "ID", "class","$"]:
        i, logic = S(tokens, i)
        return i, logic

    return i, False

def S(tokens, i):
    print("s")
    if tokens[i]['cp'] in ["while", "return","if","ID"]:
        i, logic = SST(tokens, i)
        if tokens[i]['cp'] in ["DT","fun","abstract","class"]:
            i, logic = S(tokens, i)
            return i, logic

    if tokens[i]['cp'] in ["abstract", "static", "class", "DT", "fun"]:
        i, logic = S2(tokens, i)
        return i, logic
    
    if tokens[i]['cp'] == "$":
        i, logic = last(tokens, i)
        return i, logic

    return i, False

def S2(tokens, i):
    print("s2")
    if tokens[i]['cp'] == "abstract":
        i += 1 
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

def anew(tokens, i):
    print("anew")
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
    print("fdec")
    if tokens[i]['cp'] == "DT":
        i += 1  # Move to the next token
        if tokens[i]['cp'] == "ID":
            i += 1  # Move to the next token
            if tokens[i]['cp'] in ["ASSIGN_OP", ";", ",", "{", "["]:
                print("x")
                i, logic = declaration(tokens, i)
                return i, logic
    return i, False

def declaration(tokens, i):
    print("declaration")
    if tokens[i]['cp'] in ["ASSIGN_OP", ";", ","]:
        i, logic = dec(tokens, i)
        return i, logic
    
    elif tokens[i]['cp'] == "[":
        i, logic = arr_dec(tokens, i)
        return i, logic
    
    elif tokens[i]['cp'] == "{":
        i, logic = dict_(tokens, i)
        return i, logic
    
    return i, False

def snew(tokens, i):
    print("snew")
    if tokens[i]['cp'] == "fun":
        i, logic = fun_st(tokens, i)
        return i, logic

    if tokens[i]['cp'] == "DT":
        i, logic = fdec(tokens, i)
        return i, logic

    return i, False

#VARIABLE DECLARATION

def dec(tokens, i):
    print("dec")
    if tokens[i]['cp'] in ["ASSIGN_OP", ";",","]:  
        i, logic = init(tokens, i)
        return i, logic
    return i, False

def lst(tokens, i):
    print("lst")
    if tokens[i]['cp'] == ";":  
        i +=1
        i, logic = last(tokens, i)
        return i, logic
    
    elif tokens[i]['cp'] == ",":
       i +=1
       if tokens[i]['cp'] == "ID":  
            i +=1
            if tokens[i]['cp'] in ["ASSIGN_OP", ";",","]:  
                i, logic = init(tokens, i)
                return i, logic
    return i, False

def init(tokens, i):
    print("init")
    if tokens[i]['cp'] == "ASSIGN_OP":
        i+=1 
        if tokens[i]['cp'] in ["self", "super", "int", "float", "char", "string", "(", "!", "ID"]:
            i, logic = initE(tokens, i)
            return i, logic
        
    elif tokens[i]['cp'] in [",", ";"]:  
        i, logic = lst(tokens, i)
        return i, logic
    return i, False


def initE(tokens, i): 
    print("init e")
    if tokens[i]['cp'] == "ID":  
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
    
    elif tokens[i]['cp'] in ["int", "float", "char", "string"]: 
        i +=1
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

# EXPRESSION
def OE(tokens, i):
    print("oe")
    if tokens[i]['cp'] in ["self", "super", "ID", "(", "!", "int", "float", "TF", "char", ")", "}","LOGICAL_OP", "$"]:
        i, logic = AE(tokens, i)
        return i, logic  

    return i, False  
    
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
        if tokens[i]['cp'] in ["self", "super", "int", "float", "char", "string", "(", "!", "ID", "ROP"]:
            i, logic = T(tokens, i)
            return i, logic
    return i, False

def tdash(tokens, i):
    if tokens[i]['cp'] == "MDM":
        i += 1
        if tokens[i]['cp'] in ["self", "super", "int", "float", "char", "string", "(", "!", "ID","ROP","PM","MDM"]:
            i, logic = F(tokens, i)
            return i, logic
    return i, False

def AE(tokens, i):
    print("ae")
    if tokens[i]['cp'] in ["self", "super", "int", "float", "char", "string", "(", "!", "ID"]:
        i, logic = RE(tokens, i)
        if tokens[i]['cp'] == "||":
            i, logic = aedash(tokens, i)
        return i, logic
    return i, False

def RE(tokens, i):
    print("re")
    if tokens[i]['cp'] in ["self", "super", "int", "float", "char", "string", "(", "!", "ID"]:
        i, logic = E(tokens, i)
        if tokens[i]['cp'] == "ROP":
            i, logic = redash(tokens, i)
        return i, logic
    return i, False

def E(tokens, i):
    print("e")
    if tokens[i]['cp'] in ["self", "super", "int", "float", "char", "string", "(", "!", "ID", "ROP"]:
        i, logic = T(tokens, i)
        if tokens[i]['cp'] == "PM":
            i, logic = edash(tokens, i)
        return i, logic
    return i, False

def T(tokens, i):
    print("t")
    if tokens[i]['cp'] in ["self", "super", "int", "float", "char", "string", "(", "!", "ID", "ROP","PM"]:
        i, logic = F(tokens, i)
        if tokens[i]['cp'] == "MDM":
            i, logic = tdash(tokens, i)
        return i, logic
    return i, False

def F(tokens, i):
    print("f")
    if tokens[i]['cp'] in ["self", "super""int", "float", "char", "string", "(", "!", "ID", "ROP", "PM", "MDM"]:
        i, logic = TS(tokens, i)
    if tokens[i]['cp'] == "ID":
        print("f id")
        i +=1
        if tokens[i]['cp'] in ["{", "[", "(",".", "ASSIGN_OP","inc_dec", "MDM", "PM",
                                "ROP","LOGICAL_OP", ",",";",")", "}", "]"]:
            i, logic = lhp(tokens, i)
            return i, logic
    return i, False

def new(tokens, i):
    if tokens[i]['cp'] in ["ASSIGN_OP", ";"]:  # <init>
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
    print("ts")
    if tokens[i]['cp'] == "self" or tokens[i]['cp'] == "super":
        i += 1
        if tokens[i]['cp'] == ".":
            i += 1
    return i, False

def lhp(tokens,i):
    print("lhp")
    if tokens[i]['cp'] == "[":
        i, logic = array(tokens, i)
        return i, logic
    
    elif tokens[i]['cp'] == "(":
        i +=1
        i, logic = argument(tokens, i)
        if tokens[i]['cp'] == ")":
            i +=1
            if tokens[i]['cp'] in ["ASSIGN_OP", "ROP", 
                                "INC_DEC_OP", "MDM", "PM", "LOGICAL_OP",
                                ",",  ")", "}","]"]:
                i, logic = lhp3(tokens, i)
            return i, logic
    
    elif tokens[i]['cp'] == "{":
        i, logic = dict_(tokens, i)
        return i, logic
    
    elif tokens[i]['cp'] == ".":
        i, logic = lhp1(tokens, i)
        return i, logic
    
    elif tokens[i]['cp'] == ";":
        i, logic = last(tokens, i)
        return i, logic
    
    return i, False

def lhp1(tokens,i):
    if tokens[i]['cp'] == ".":
        i +=1
        if tokens[i]['cp'] == "ID":
            i +=1
            if tokens[i]['cp'] in ["{", "[", "(", ".", "ASSIGN_OP", "ROP", 
                                "INC_DEC_OP", "MDM", "PM", "LOGICAL_OP",
                                ",", ";", ")", "}","]"]:
                i, logic = lhp(tokens, i)
                return i, logic

    return i, False

def lhp3(tokens,i):
    if tokens[i]['cp'] == ".":
        i, logic = lhp1(tokens, i)
        return i, logic
    
    return i, False

# VAR OBJ ASSIGNMENT
def assign_st(tokens, i):
    print("assign st")
    if tokens[i]['cp'] == "ID":
        if tokens[i]['cp'] in ["ASSIGN_OP", "ROP"]:
            i, logic = assign_op(tokens, i)
            if tokens[i]['cp'] in ["self", "super", "int", "float", "char", "string", "(", "!", "ID"]:
                i, logic = asg(tokens, i)
                return i, logic
    return i, False


def assign_op(tokens, i):
    print("assign op")
    if tokens[i]['cp'] in ["ASSIGN_OP", "ROP"]:
        i +=1
    return i, False
    
def asg(tokens, i):
    print("asg")
    if tokens[i]['cp'] in ["self", "super", "int", "float", "char", "string", "(", "!", "ID"]:
            i, logic = E(tokens, i)
            if tokens[i]['cp'] == ";":
                i +=1
                return i, logic

    elif tokens[i]['cp'] == "obj":  
          i, logic = obj_call(tokens, i)
          return i, logic
    return i, False

# CLASS
def class_def(tokens,i):
    print("class def")
    if tokens[i]['cp'] == "class":
        i +=1
        if tokens[i]['cp'] == "ID":
            i +=1
            if tokens[i]['cp'] in [":", "{"]:
                i, logic = inherit(tokens, i)
                if tokens[i]['cp'] == "{":
                    i +=1
                    if tokens[i]['cp'] in ["static", "abstract", "fun", "DT","}"]:
                        i, logic = class_body(tokens, i)
                        if tokens[i]['cp'] == "}":
                            i +=1
                            return i, logic
    return i, False

def inherit(tokens,i):
    print("inherit")
    if tokens[i]['cp'] == ":":
        i +=1
        if tokens[i]['cp'] == "ID":
            i +=1
    
    elif tokens[i]['cp'] == "implements":  
            i += 1
    
    return i, False

def class_body(tokens,i):
    print("class body")
    if tokens[i]['cp'] in ["static", "abstract", "fun", "DT"]:
        i, logic = SST2(tokens, i)
        if tokens[i]['cp'] in ["static", "abstract", "fun", "DT","}"]:
            i, logic = class_body(tokens, i)
            return i, logic
        
    elif tokens[i]['cp'] == "}":
            i, logic = last(tokens,i)
            return i, logic

    return i, False

def obj_call(tokens,i):
    print("obj call")
    if tokens[i]['cp'] == "obj":
        i +=1
        if tokens[i]['cp'] == "ID":
            i +=1
            if tokens[i]['cp'] == "(":
                i +=1
                if tokens[i]['cp'] in ["self", "super", "ID", "(", "!", ")"]:
                    i, logic = argument(tokens, i)
                    if tokens[i]['cp'] == ")":
                        i +=1
                        if tokens[i]['cp'] == ";":
                            i +=1
                            return i, logic

    return i, False

def interface(tokens,i):
    print("interface")
    if tokens[i]['cp'] == "interface":  
        i += 1
        if tokens[i]['cp'] == "ID":  
            i += 1
            if tokens[i]['cp'] == "{":  
                i += 1
                if tokens[i]['cp'] in ["static", "abstract", "fun", "DT","}"]:
                    i, logic = interface_body(tokens, i)
                    if tokens[i]['cp'] == "}":  
                        i += 1
                        return i, logic

    return i, False

def interface_body(tokens,i):
    print("interface body")
    if tokens[i]['cp'] in ["static", "abstract", "fun", "DT"]:
        i, logic = SST2(tokens, i)
        if tokens[i]['cp'] in ["static", "abstract", "fun", "DT","}"]:
            i, logic = interface_body(tokens, i)
            return i, logic

    return i, False

# FUNCTION
def fun_st(tokens, i):
    print("fun st")
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
                            if tokens[i]['cp'] in ["while", "return", "if", "ID","DT"]: 
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
            if tokens[i]['cp'] in ["ASSIGN_OP", "[", ",", ")"]: 
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

def return_(tokens, i):
    if tokens[i]['cp'] == "return":  
        i += 1
        if tokens[i]['cp'] in ["self", "super", "ID", "(", "!", "int", "float", "TF", "char"]:
            i, logic = OE(tokens, i)
            if tokens[i]['cp'] == ";":  
                i += 1
                return i, logic
    return i, False

def while_(tokens, i):
    print("while")
    if tokens[i]['cp'] == "while":
        i += 1  
        if tokens[i]['cp'] == "(":
            i += 1  
            if tokens[i]['cp'] in ["self", "super", "ID", "(", "!", "int", "float", "TF", "char"]:
                i, logic = OE(tokens, i)
                if tokens[i]['cp'] == ")":  
                    i += 1  
                    print(")")
                    if tokens[i]['cp'] == "{": 
                        i += 1  
                        print("{")
                        if tokens[i]['cp'] in [";" , "while", "return", "if", "ID" , "static", "abstract", "DT", "fun"]:
                            i, logic = body(tokens, i)
                        elif tokens[i]['cp'] == "}":
                            print("}")
                            i +=1
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
    print("sst")
    if tokens[i]['cp'] == ";":
        i += 1  
     
    elif tokens[i]['cp'] == "while":
        i, logic = while_(tokens, i)
        return i, logic
    
    elif tokens[i]['cp'] == "return":
        i, logic = return_(tokens, i)
        return i, logic
    
    elif tokens[i]['cp'] in ["self", "super"]:
        i, logic = create(tokens, i)
        return i, logic
    
    elif tokens[i]['cp'] == "DT":
        i, logic = fdec(tokens, i)
        return i, logic
    
    elif tokens[i]['cp'] == "ID":
        i +=1
        i, logic = initE(tokens, i)
        return i, logic
    
    elif tokens[i]['cp'] in ["int", "float","char","bool"]:
        i +=1
    
    return i, False  

def create(tokens, i):
    print("create")
    if tokens[i]['cp'] in ["self", "super"]:
        i, logic = TS(tokens, i)
        if tokens[i]['cp'] == "ID":
            i +=1
            if tokens[i]['cp'] == "ASSIGN_OP":
                i +=1
                if tokens[i]['cp'] == "ID":
                    i +=1
                    if tokens[i]['cp'] == ";":
                        i +=1
                        return i, logic
    else:
        return i, False

def SST2(tokens, i):
    print("sst 2")
    if tokens[i]['cp'] in ["static", "abstract", "fun","DT"]:
        i, logic = static(tokens, i)
        if tokens[i]['cp'] in ["abstract", "fun","DT"]:
            i, logic = SST3(tokens, i)
            return i, logic
    return i, False

def static(tokens, i):
    print("static")
    if tokens[i]['cp'] == "static":
        i +=1
        return i, True
    return i, False

def abstract(tokens, i):
    print("abstract")
    if tokens[i]['cp'] == "abstract":
        i +=1
        return i, True
    return i, False

def SST3(tokens, i):
    print("sst 3")
    if tokens[i]['cp'] in ["abstract", "fun"]:
        i, logic = abstract(tokens, i)
        if tokens[i]['cp'] == "fun":
            i, logic = fun_st(tokens, i)
            return i, logic

    elif tokens[i]['cp'] == "DT":
        i, logic = fdec(tokens, i)
        return i, logic
    return i, False

# DICTIONARY
def dict_(tokens,i):
    if tokens[i]['cp'] == "{":
        i +=1
        if tokens[i]['cp'] == "ID":
            i, logic = KVlist(tokens, i)
            if tokens[i]['cp'] == "}":
                i +=1
            return i, logic
    return i, False

def KVlist(tokens, i):
    while tokens[i]['cp'] == "ID":
        i, logic = KVpair(tokens, i)
    return i, logic 

def KVpair(tokens, i):
    print("kv pair")
    if tokens[i]['cp'] == "ID":
        i +=1
        if tokens[i]['cp'] == ":":
            i +=1
            if tokens[i]['cp'] in ["super", "self", "(", "!", "ID"]:
              i, logic = KV(tokens, i)
              return i, logic
    return i, False

def KV(tokens, i):
    print("kv")
    if tokens[i]['cp'] in ["super", "self", "(", "!", "ID"]:
        i, logic = E(tokens, i)
        return i, logic
    return i, False

# ARRAY 2D
def arr_dec(tokens,i):
    print("arr_dec")
    if tokens[i]['cp'] == "[":
        i +=1
        if tokens[i]['cp'] == "]":
            i +=1
            if tokens[i]['cp'] in [";", ",","ASSIGN_OP","["]:
                i, logic = dec2(tokens, i)
                return i, logic
            return i, False
        
def dec2(tokens,i):
    print("dec2")
    if tokens[i]['cp'] in [";", ",","ASSIGN_OP"]:
        i, logic = init1(tokens, i)
        if tokens[i]['cp'] in [";", ","]:
            i, logic = arr(tokens, i)
        return i, logic
    
    elif tokens[i]['cp'] == "[":
        i +=1
        if tokens[i]['cp'] == "]":
            i +=1
            if tokens[i]['cp'] in [";", ",","ASSIGN_OP"]:
                i, logic = init2(tokens, i)
                if tokens[i]['cp'] in [";", ","]:
                    i, logic = arr(tokens, i)
    return i, False

def init1(tokens, i):
    print("init1")
    if tokens[i]['cp'] == "=":
        i +=1
        if tokens[i]['cp'] == "[":
            i +=1
            if tokens[i]['cp'] in ["self", "super", "int", "float", "char", "string", "(", "!", "ID", "]"]:
                i, logic = exp(tokens, i)
                if tokens[i]['cp'] == "]":
                    i +=1
                    return i, logic
    return i, False

def arr(tokens, i):
    print("arr")
    if tokens[i]['cp'] == ";":
        i +=1

    elif tokens[i]['cp'] == ",":
        i +=1
        if tokens[i]['cp'] == "ID":
            i +=1
            if tokens[i]['cp'] == "[":
                i, logic = arr_dec(tokens, i)
                return i, logic
    return i, False

def init2(tokens, i):
    print("init2")
    if tokens[i]['cp'] == "ASSIGN_OP":
        i +=1
        if tokens[i]['cp'] == "[":
            i +=1
            if tokens[i]['cp'] in [";", ",","ASSIGN_OP"]:
                i, logic = init2d(tokens, i)
                if tokens[i]['cp'] == "]":
                    i +=1
                    return i, logic
    return i, False

def exp(tokens, i):
    print("exp")
    if tokens[i]['cp'] in ["super", "self", "(", "!", "ID"]:
        i, logic = E(tokens, i)
        if tokens[i]['cp'] in [",", "]"]:
            i, logic = exp1(tokens, i)
            return i, logic
    return i, False

def exp1(tokens, i):
    print("exp 1")
    if tokens[i]['cp'] == ",":
        i +=1
        if tokens[i]['cp'] in ["super", "self", "(", "!", "ID"]:
            i, logic = E(tokens, i)
            if tokens[i]['cp'] in [",", "]"]:
                i, logic = exp1(tokens, i)
                return i, logic
    return i, False

def init2d(tokens, i):
    print("init 2d")
    if tokens[i]['cp'] == "[":
        i +=1
        if tokens[i]['cp'] in ["self", "super", "int", "float", "char", "string", "(", "!", "ID", "]"]:
            i, logic = exp(tokens, i)
            if tokens[i]['cp'] == "]":
                i +=1
                if tokens[i]['cp'] == ",":
                    i, logic = init2_dash(tokens, i)
                    return i, logic
    return i, False

def init2_dash(tokens, i):
    print("init 2dash")
    if tokens[i]['cp'] == ",":
        i +=1
        if tokens[i]['cp'] in [";", ",","ASSIGN_OP"]:
            i, logic = init2d(tokens, i)
            return i, logic
    return i, False

def body(tokens,i):
    print("body")
    
    if tokens[i]['cp'] in ["while", "return","if","ID"]:
        i, logic = SST(tokens, i)
        return i, logic
    
    elif tokens[i]['cp'] in ["static", "abstract", "fun", "DT"]:
        i, logic = SST2(tokens, i)
        return i, logic

    elif tokens[i]['cp'] in ["while", "return","if","ID", "static","abstract","fun", "DT","}"]:
        i, logic = MST(tokens, i)
        return i, logic
    
    return i, False

def MST(tokens,i):
    print("mst")
    if tokens[i]['cp'] in ["while", "return","if","ID"]:
        i, logic = SST(tokens, i)
        if tokens[i]['cp'] in ["while", "return","if", "static","abstract","fun", "DT","}"]:
            i, logic = MST(tokens, i)
            return i, logic
        
    elif tokens[i]['cp'] in ["while", "return","if","ID", "static","abstract","fun", "DT","}"]:
            i, logic = SST2(tokens, i)
            return i, logic
    elif tokens[i]['cp'] == ";":  
        i +=1
        i, logic = last(tokens, i)
        return i, logic
    else: 
        pass
    return i, False

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

