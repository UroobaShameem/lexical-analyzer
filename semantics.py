cTable = []
classScope = []



class ClassTable:

    def __init__(self, name, inherit, extend, link):
        self.name=name
        self.link=link
        self.inherit = inherit
        self.extend = extend


class ClassAttribTable:

    def __init__(self, name, type, link):
        self.name=name
        self.type=type
        self.link=link


def createClassScope(index):
    global cTable, classScope

    classScope.append(index)
    return len(classScope) - 1

def destroyClassScope():
    global cTable, classScope

    classScope.pop()
    return len(classScope)

def lookup(name):
    global cTable, classScope

    if(len(cTable) == 0):
        return False
    
    for tempCTable in cTable:
        if(tempCTable.name == name):
            return True

    return False


def lookupAttr(name, scope):
    global cTable, classScope

    if(len(cTable) == 0):
        return False

    try:
        tempAttrList = cTable[classScope[-1]].link
        if(len(tempAttrList) == 0):
            return False

        for tempAttr in tempAttrList:
            if(tempAttr.name == name):
                return True
    except:
        return False

    return False


def insertClass(name, inherit, extend, link):
    global cTable, classScope

    if(lookup(name)):
        return {"success":False, "message":"Class Redeclaration Error"}

    if(inherit == ""):
        inherit = None
    else:
        classList = inherit.split(",")
        for tempClass in classList:
            if(tempClass == name):
                return {"success":False, "message":"Can not inherent itself Error"}
            elif(not(lookup(tempClass))):
                return {"success":False, "message":"Class Not Found Error"}


    if(extend == ""):
        extend = None
    else:
        if(extend == name):
                return {"success":False, "message":"Can not implement itself Error"}
        elif(not(lookup(extend))):
            return {"success":False, "message":"Class Not Found Error"}


    cTable.append(ClassTable(name, inherit, extend, link))

    return {"success":True}


def insert(scope, name, type, link):
    global cTable, classScope

    if(lookupAttr(name, scope)):
        return {"success":False, "message":"Attribute Redeclaration Error"}

    cTable[scope].link.append(ClassAttribTable(name, type, link))

    return {"success":True}