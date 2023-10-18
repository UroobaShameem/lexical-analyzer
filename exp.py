def OE(tokens, i):
    if tokens[i] in ["self", "super","int", "float", "char","string","(", "!", "ID"]:
        i, logic = last(tokens,i)
        
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