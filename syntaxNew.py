import semantics


class SyntaxAnalyzer:
    index = 0

    def start(self):
        if self.sst():
            if self.start():
                return True
        elif self.funcDef():
            print("call fun")
            if self.start():
                return True
        elif self.classDef():
            if self.start():
                return True
        if self.ts[self.index].cp in ["dt","id", "if", "switch", "for", "while", "do", "try", "incdec", "void",
                                      "class","break", "$"]:

            return True
        return False

    def sst(self):

        if self.ts[self.index].cp in ["dt", "if", "switch", "for", "while", "do", "try", "incdec", "break","id"]:


            if self.dec():
                print("decleration")
                return True
            elif self.ifElse():
                return True
            elif self.switchSt():
                return True
            elif self.forST():
                return True
            elif self.whileSt():
                return True
            elif self.dowhile():
                return True
            elif self.trySt():
                return True
            elif self.breakSt():
                return True
            elif self.ts[self.index].cp == "id":

                self.index += 1
                if self.sst2():
                    return True
            elif self.ts[self.index].cp == "incdec":
                self.index += 1
                if self.self.ts[self.index].cp == "id":
                    self.index += 1
                    if self.x():
                        return True

        return False

    def sst2(self):
        if self.ts[self.index].cp in [".", "dt", "id", "if", "switch", "for", "while", "do", "try", "incdec",
                                      "void", "class", "$", "break", "case", "default", "}",
                                      "return"]:
            if self.ts[self.index].cp == "id":
                self.index += 1
                if self.ts[self.index].cp == "=":
                    self.index += 1
                    if self.ts[self.index].cp == "new":
                        self.index += 1
                        if self.ts[self.index].cp == "id":
                            self.index += 1
                            if self.ts[self.index].cp == "(":
                                self.index += 1
                                if self.pl():
                                    if self.ts[self.index].cp == ")":
                                        self.index += 1

                                        return True
            elif self.x():
                if self.sst3():
                    return True
        return False

    def sst3(self):
        if self.ts[self.index].cp in ["(", "=", "incdec", "["]:
            if self.ts[self.index].cp == "(":
                self.index += 1
                if self.pl():
                    if self.ts[self.index].cp == ")":
                        self.index += 1
                        return True
            elif self.ts[self.index].cp == "=":
                self.index += 1
                if self.oe():
                    return True
            elif self.ts[self.index].cp == "incdec":
                self.index += 1
                return True
            elif self.ts[self.index].cp == "[":
                self.index += 1
                if self.oe():
                    if self.ts[self.index].cp == "]":
                        self.index += 1
                        if self.sst4():
                            return True
        return False

    def sst4(self):
        if self.ts[self.index].cp == "=":
            self.index += 1
            if self.oe():
                return True
        if self.ts[self.index].cp in ["=", "dt", "id", "if", "switch", "for", "while", "do", "try", "incdec",
                                      "void", "class", "$", "break", "case", "default", "}",
                                      "return"]:
            return True
        return False

    def x(self):
        if self.ts[self.index].cp == ".":
            self.index += 1
            if self.ts[self.index].cp == "id":
                self.index += 1
                if self.x():
                    return True
        elif self.ts[self.index].cp in [".", "dt", "id", "if", "switch", "for", "while", "do", "try",
                                        "incdec", "void", "class",  "$", "break", "case",
                                        "default", "}", "return", "("]:
            return True
        return False

    def pl(self):
        if self.ts[self.index].cp in ["id", "int_con", "float_con", "str_Con", "char_Con", "bool_Con", "(", "not",
                                      "void", "incdec"]:
            if self.oe():
                if self.pl2():
                    return True
        elif self.ts[self.index].cp == ")":
            return True
        return False

    def pl2(self):
        if self.ts[self.index].cp == ",":
            self.index += 1
            if self.oe():
                if self.pl2():
                    return True
        elif self.ts[self.index].cp == ")":
            return True
        return False

    def oe(self):
        if self.ts[self.index].cp in ["this", "id", "int_con", "float_con", "str_Con", "char_Con", "bool_Con", "(",
                                      "not", "void", "incdec"]:
            if self.ae():
                if self.oe2():
                    return True
        return False

    def oe2(self):
        if self.ts[self.index].cp == "or":
            self.index += 1
            if self.ae():
                if self.oe2():
                    return True
        if self.ts[self.index].cp in ["or", ",", ")", ";", "}", "]", "id", "if", "switch", "for", "while",
                                      "do", "try", "incdec", "void", "class",  "$", "break",
                                      "case", "default", "}", "return"]:
            return True
        return False

    def ae(self):
        if self.ts[self.index].cp in ["this", "id", "int_con", "float_con", "str_Con", "char_Con", "bool_Con", "(",
                                      "not", "void", "incdec"]:
            if self.re():
                if self.ae2():
                    return True
        return False

    def ae2(self):
        if self.ts[self.index].cp == "and":
            self.index += 1
            if self.re():
                if self.oe2():
                    return True
        if self.ts[self.index].cp in ["and", "or", ",", ")", ";", "}", "]", "id", "if", "switch", "for",
                                      "while", "do", "try", "incdec", "void", "class" ,
                                        "$", "break", "case", "default", "}", "return"]:
            return True
        return False

    def re(self):
        if self.ts[self.index].cp in ["this", "id", "int_con", "float_con", "str_Con", "char_Con", "bool_Con", "(",
                                      "not", "void", "incdec"]:
            if self.e():
                if self.re2():
                    return True
        return False

    def re2(self):
        if self.ts[self.index].cp == "ro":
            self.index += 1
            if self.e():
                if self.re2():
                    return True
        if self.ts[self.index].cp in ["ro", "and", "or", ",", ")", ";", "}", "]", "id", "if", "switch", "for",
                                      "while", "do", "try", "incdec", "void", "class" ,
                                        "$", "break", "case", "default", "return"]:
            return True
        return False

    def e(self):
        if self.ts[self.index].cp in ["this", "id", "int_con", "float_con", "str_Con", "char_Con", "bool_Con", "(",
                                      "not", "void", "incdec"]:
            if self.t():
                if self.e2():
                    return True
        return False

    def e2(self):
        if self.ts[self.index].cp == "pm":
            self.index += 1
            if self.t():
                if self.e2():
                    return True
        if self.ts[self.index].cp in ["pm", "ro", "and", "or", ",", ")", ";", "}", "]", "id", "if", "switch",
                                      "for", "while", "do", "try", "incdec", "void", "class" ,
                                        "$", "break", "case", "default", "}", "return"]:
            return True
        return False

    def t(self):
        if self.ts[self.index].cp in ["this", "id", "int_con", "float_con", "str_Con", "char_Con", "bool_Con", "(",
                                      "not", "void", "incdec"]:
            if self.f():
                if self.t2():
                    return True
        return False

    def t2(self):
        if self.ts[self.index].cp == "mdm":
            self.index += 1
            if self.f():
                if self.t2():
                    return True
        if self.ts[self.index].cp in ["mdm", "pm", "ro", "and", "or", ",", ")", ";", "}", "]", "id", "if", "switch",
                                      "for", "while", "do", "try", "incdec", "void", "class" ,
                                        "$", "break", "case", "default", "}", "return"]:
            return True
        return False

    def f(self):
        if self.ts[self.index].cp in ["this", "id", "int_con", "float_con", "str_Con", "char_Con", "bool_Con", "(",
                                      "not", "void", "incdec"]:
            if self.th():
                if self.ts[self.index].cp == "id":
                    self.index += 1
                    return True
            elif self.const():
                return True
            elif self.ts[self.index].cp == "(":
                self.index += 1
                if self.e():
                    if self.ts[self.index].cp == ")":
                        self.index += 1
                        return True
            elif self.ts[self.index].cp == "not":
                self.index += 1
                if self.f():
                    return True
            elif self.fnCall():
                return True
            elif self.ts[self.index].cp == "incdec":
                self.index += 1
                if self.ts[self.index].cp == "id":
                    self.index += 1
                    if self.x():
                        return True
            elif self.ts[self.index].cp == "id":
                self.index += 1
                if self.x():
                    if self.ts[self.index].cp == "incdec":
                        return True
        return False

    def th(self):
        if self.ts[self.index].cp == "this":
            self.index += 1
            if self.ts[self.index].cp == ".":
                self.index += 1
                return True
        elif self.ts[self.index].cp == "id":
            return True
        return False

    def mst(self):
        if self.sst():
            print("return sst")
            if self.mst():
                return True

        elif self.ts[self.index].cp in ["}","case","default","return","dt", "id", "if", "switch", "for", "while", "do", "try", "incdec","break",
                                      "void"]:
            print("break in mst")
            return True
        return False

    def const(self):
        if self.ts[self.index].cp in ["int_con", "float_con", "str_Con", "char_Con", "bool_Con"]:
            self.index += 1
            return True
        return False

    def ifElse(self):
        if self.ts[self.index].cp == "if":
            self.index += 1
            if self.ts[self.index].cp == "(":
                self.index += 1
                if self.oe():
                    if self.ts[self.index].cp == ")":
                        self.index += 1
                        if self.body():

                            if self.elseSt():
                                return True
        return False

    def elseSt(self):
        if self.ts[self.index].cp == "else":
            self.index += 1
            if self.body():
                return True
        if self.ts[self.index].cp in ["dt", "id", "if", "switch", "for", "while", "do", "try", "incdec",
                                      "void", "class",  "$", "break", "case", "default", "}",
                                      "return"]:
            return True
        return False

    def body(self):
        if self.ts[self.index].cp in ["dt", "id", "if", "switch", "for", "while", "do", "try", "incdec",
                                      "void", "class" ,  "$", "break", "case", "default", "{",
                                      "return"]:
            if self.sst():
                return True
            elif self.ts[self.index].cp == "{":
                self.index += 1
                if self.mst():
                    if self.ts[self.index].cp == "}":
                        self.index += 1
                        return True
        return False

    def switchSt(self):
        if self.ts[self.index].cp == "switch":
            print("switch")
            self.index += 1
            if self.ts[self.index].cp == "(":
                self.index += 1
                print("(s")
                if self.idConst():
                    print("idconst s")
                    if self.ts[self.index].cp == ")":
                        self.index += 1
                        print(")s")
                        if self.ts[self.index].cp == "{":
                            self.index += 1
                            print("{ of s")
                            if self.caseSt():
                                print("return case")
                                if self.defaultSt():
                                    if self.ts[self.index].cp == "}":
                                        self.index += 1
                                        return True
        return False

    def idConst(self):
        if self.ts[self.index].cp in ["id", "int_con", "float_con", "str_Con", "char_Con", "bool_Con"]:
            self.index += 1
            return True
        return False

    def caseSt(self):
        if self.ts[self.index].cp == "case":
            self.index += 1
            print("case def")
            if self.const():
                if self.ts[self.index].cp == ":":
                    self.index += 1
                    print(":")
                    if self.mst():
                        print("mst case")
                        if self.breakSt():
                            print("nnnnn")
                            if self.caseSt():
                                return True


        elif self.ts[self.index].cp in ["default"]:
            return True
        return False

    def breakSt(self):
        print("break def")
        if self.ts[self.index].cp == "break":
            print("breack break")
            self.index += 1

            return True
        elif self.ts[self.index].cp in ["case", "default"]:
            return True
        return False

    def defaultSt(self):
        if self.ts[self.index].cp == "default":
            self.index += 1

            if self.ts[self.index].cp == ":":
                self.index += 1
                if self.mst():
                    return True
        return False

    def forST(self):
        if self.ts[self.index].cp == "for":
            self.index += 1
            if self.ts[self.index].cp == "(":
                self.index += 1
                if self.c1():
                    if self.ts[self.index].cp == ";":
                        self.index += 1
                        if self.oe():
                            if self.ts[self.index].cp == ";":
                                self.index += 1

                                if self.incDecSt():
                                    if self.ts[self.index].cp == ")":
                                        self.index += 1
                                        if self.body():
                                            return True
        return False

    def c1(self):

        if self.ts[self.index].cp in ["dt", "id", "int_con", "float_con", "str_Con", "char_Con", "bool_Con"]:
            if self.dec():
                return True

        elif self.ts[self.index].cp == ";":
           return True
        return False

    def incDecSt(self):

        if self.ts[self.index].cp == "id":
            self.index += 1

            if self.ts[self.index].cp == "incdec":
                self.index += 1

                return True
        elif self.ts[self.index].cp == "incdec":
            self.index += 1
            if self.ts[self.index].cp == "id":
                self.index += 1
                return True
        ##elif self.ts[self.index].cp == ")":
          ##  return True
        return False

    def whileSt(self):
        if self.ts[self.index].cp == "while":
            self.index += 1
            if self.ts[self.index].cp == "(":
                self.index += 1
                if self.oe():
                    if self.ts[self.index].cp == ")":
                        self.index += 1
                        if self.body():
                            return True
        return False

    def dowhile(self):
        if self.ts[self.index].cp == "do":
            self.index += 1
            if self.ts[self.index].cp == "{":
                self.index += 1
                if self.mst():
                    if self.ts[self.index].cp == "}":
                        self.index += 1
                        if self.ts[self.index].cp == "while":
                            self.index += 1
                            if self.ts[self.index].cp == "(":
                                self.index += 1
                                if self.oe():
                                    if self.ts[self.index].cp == ")":
                                        self.index += 1
                                        return True
        return False

    def trySt(self):
        if self.ts[self.index].cp == "try":
            self.index += 1
            if self.ts[self.index].cp == "(":
                self.index +=1
                if self.oe():
                    if self.ts[self.index].cp == ")":
                        self.index += 1
                        if self.ts[self.index].cp == "{":
                            self.index += 1
                            if self.mst():
                                if self.ts[self.index].cp == "}":
                                    self.index += 1

                                    if self.catchSt():
                                        if self.finallySt():
                                            return True
        return False

    def catchSt(self):
        if self.ts[self.index].cp == "catch":
            self.index += 1
            if self.ts[self.index].cp == "{":
                self.index += 1
                if self.mst():
                    if self.ts[self.index].cp == "}":
                        self.index += 1
                        return True
        elif self.ts[self.index].cp in ["id", "if", "switch", "for", "while", "do", "try", "incdec", "void",
                                        "class" ,   "$", "break", "case", "default", "}",
                                        "return"]:
            return True
        return False

    def finallySt(self):
        if self.ts[self.index].cp == "finally":
            self.index += 1
            if self.ts[self.index].cp == "{":
                self.index += 1
                if self.mst():
                    if self.ts[self.index].cp == "}":
                        self.index += 1
                        return True
        elif self.ts[self.index].cp in ["dt", "id", "if", "switch", "for", "while", "do", "try", "incdec",
                                        "void", "class",   "$", "break", "case", "default",
                                        "}", "return"]:
            return True
        return False

    def dec(self):
        if self.ts[self.index].cp == "dt":
            tempDT = self.ts[self.index].vp
            self.index += 1
            if self.ts[self.index].cp == "id":
                tempRes = semantic.insert(semantic.classScope[-1], self.ts[self.index].vp, tempDT, [])
                if(not(tempRes["success"])):
                    print("Error at line ", str(self.ts[self.index].line), ": ", tempRes["message"])
                    return False

                self.index += 1
                print("dec")

                if self.varArr():
                    print("var arr call")

                    return True
        return False

    def varArr(self):
        if self.ts[self.index].cp in ["=", ",", "[", "dt", "id", "if", "switch", "for", "while", "do",
                                      "try", "incdec", "void", "class",   "$", "break",
                                      "case", "default", "}", "return"]:

            if self.var():
                print("var call")
                return True
            elif self.arr():
                return True
        return False

    def var(self):
        if self.ts[self.index].cp in [",","=", "dt", "id", "if", "switch", "for", "while", "do", "try", "incdec",
                                      "void", "class",   "$", "break", "case", "default", "}",
                                      "return"]:

            if self.inSt():
                print("inst")
                if self.listSt():
                    print("list call")

                    return True
        return False

    def inSt(self):
        if self.ts[self.index].cp == "=":
            self.index += 1
            if self.in2():
                return True
        elif self.ts[self.index].cp in ["dt", "id", "if", "switch", "for", "while", "do", "try", "incdec",
                                        "void", "class" ,  "$", "break", "case", "default",
                                        "}", "return","=",","]:

            return True
        return False

    def in2(self):
        if self.idConst():

            return True

        elif self.ts[self.index].cp == "=":
            self.index += 1
            if self.ts[self.index].cp == "id":
                self.index += 1
                if self.inSt():
                    return True
        return False

    def listSt(self):
        print("list defff")
        if self.ts[self.index].cp == ",":
            self.index += 1
            if self.ts[self.index].cp == "id":
                self.index += 1
                if self.inSt():
                    if self.listSt():
                        return True
        elif self.ts[self.index].cp in ["dt", "id", "if", "switch", "for", "while", "do", "try", "incdec",
                                        "void", "class", "summary",   "$", "case", "default",
                                        "}", "return", "break", ";"]:
            print("list elif")

            return True
        return False

    def arr(self):
        if self.ts[self.index].cp == "[":
            self.index += 1

            if self.idConst():
                if self.ts[self.index].cp == "]":
                    self.index += 1

                    if self.items():
                        return True
        return False
    def items(self):
        if self.ts[self.index].cp == "=":
            self.index+=1
            if self.ts[self.index].cp == "[":
                self.index += 1
                if self.itemList():
                    if self.ts[self.index].cp == "]":
                        self.index += 1
                        return True
            return False


    def itemList(self):
        if self.idConst():
            if self.itemList2():
                return True
        elif self.ts[self.index].cp == "]":
            return True
        return False

    def itemList2(self):
        if self.ts[self.index].cp == ",":
            self.index += 1
            if self.idConst():
                if self.itemList2():
                    return True
        elif self.ts[self.index].cp == "]":
            return True
        return False

    def funcDef(self):


        if self.dtVoid():

            if self.ts[self.index].cp == "id":
                self.index += 1
                if self.ts[self.index].cp == "(":
                    self.index += 1
                    if self.plid():
                        if self.ts[self.index].cp == ")":
                            self.index += 1
                            if self.ts[self.index].cp == "{":
                                self.index += 1
                                if self.mst():
                                    if self.returnSt():
                                        if self.ts[self.index].cp == "}":
                                            self.index += 1
                                            return True
                else:
                    self.index -= 2
                    # return True
        return False

    def plid(self):
        if self.dtid():
            if self.plid2():
                return True
        elif self.ts[self.index].cp == ")":
            return True
        return False

    def plid2(self):
        if self.ts[self.index].cp == ",":
            self.index += 1
            if self.dtid():
                if self.plid2():
                    return True
        elif self.ts[self.index].cp == ")":
            return True
        return False

    def dtid(self):
        if self.ts[self.index].cp == "dt":
            self.index += 1
            if self.ts[self.index].cp == "id":
                self.index += 1
                if self.enull():
                    return True
        elif self.ts[self.index].cp in ["=", ",", ")"]:
            return True
        return False

    def enull(self):
        if self.ts[self.index].cp == "=":
            self.index += 1
            if self.const():
                return True
        elif self.ts[self.index].cp in [",", ")"]:
            return True
        return False

    def returnSt(self):
        if self.ts[self.index].cp == "return":
            self.index += 1
            if self.oe():
                return True
        elif self.ts[self.index].cp == "}":
            return True
        return False

    def dtVoid(self):

        if self.ts[self.index].cp in["void","dt"]:
            print("in")
            if self.ts[self.index].cp == "dt":
                self.index += 1
            if self.ts[self.index].cp == "void":
                self.index += 1

            return True
        return False

    def classDef(self):
        if self.ts[self.index].cp == "class":
            self.index += 1
            if self.ts[self.index].cp == "id":
                tempclassName = self.ts[self.index].vp
                self.index += 1
                inhResult = self.inheritSt()
                if inhResult["success"]:
                    implResult = self.implementSt()
                    if implResult["success"]:
                        temp = semantic.insertClass(tempclassName, inhResult["list"], implResult["data"], [])

                        if(not(temp["success"])):
                            print("Error at line ", str(self.ts[self.index].line), ": ", temp["message"])
                            return False

                        semantic.createClassScope(len(semantic.cTable) - 1)
                        if self.ts[self.index].cp == "{":
                            self.index += 1
                            if self.classBody():
                                if self.ts[self.index].cp == "}":
                                    self.index += 1
                                    semantic.destroyClassScope()
                                    return True
        return False

    def inheritSt(self):
        if self.ts[self.index].cp == "id":
            self.index += 1
            tempRes = self.inlist()
            if tempRes["success"]:
                return {"success":True, "list":tempRes["list"]}
        elif self.ts[self.index].cp in ["implement", "{"]:
            return {"success":True, "list":""}
        return {"success":False}

    def inlist(self):
        if self.ts[self.index].cp == "id":
            tempInheritClass = self.ts[self.index].vp
            self.index += 1
            tempRes = self.inlist2(tempInheritClass)
            if tempRes["success"]:
                return {"success":True, "list":tempRes["list"]}
        return {"success":False, "list":tempInheritClass}

    def inlist2(self, inheritClass):
        if self.ts[self.index].cp == ",":
            self.index += 1
            if self.ts[self.index].cp == "id":
                inheritClass += "," + self.ts[self.index].vp
                self.index += 1
                tempRes = self.inlist2(inheritClass)
                if tempRes["success"]:
                    return {"success":True, "list":tempRes["list"]}
        elif self.ts[self.index].cp in ["implement", "{", ","]:
            return {"success":True, "list":inheritClass}
        return {"success":False, "list":inheritClass}

    def implementSt(self):
        if self.ts[self.index].cp == "implement":
            self.index += 1
            if self.ts[self.index].cp == "id":
                tempName = self.ts[self.index].vp
                self.index += 1
                return {"success":True, "data":tempName}
        elif self.ts[self.index].cp == "{":
            return {"success":True, "data":""}
        return {"success":False}

    def classBody(self):
        if self.ts[self.index].cp in ["am", "static", "final", "dt", "void", "class"]:
            if self.amSt():
                if self.staticSt():
                    if self.finalSt():
                        if self.funcDecClass():
                            if self.classBody():
                                return True
        elif self.ts[self.index].cp == "constructor":
            self.index += 1
            if self.ts[self.index].cp == "{":
                self.index += 1
                if self.mst():
                    if self.ts[self.index].cp == "}":
                        self.index += 1
                        if self.classBody():
                            return True
        elif self.ts[self.index].cp == "}":
            return True
        return False

    def funcDecClass(self):
        if self.ts[self.index].cp in ["dt", "void", "class"]:
            if self.funcDef():
                return True

            if self.dec():
                return True
            elif self.classDef():
                return True
        return False

    def amSt(self):
        if self.ts[self.index].cp == "am":
            self.index += 1
            return True
        elif self.ts[self.index].cp in ["static", "final", "dt", "void", "class"]:
            return True
        return False

    def staticSt(self):
        if self.ts[self.index].cp == "static":
            self.index += 1
            return True
        elif self.ts[self.index].cp in ["final", "dt", "void", "class"]:
            return True
        return False

    def finalSt(self):
        if self.ts[self.index].cp == "final":
            self.index += 1
            return True
        elif self.ts[self.index].cp in ["dt", "void", "class"]:
            return True
        return False

    def __init__(self, ts):
        self.ts = ts
        if self.start():
            if self.ts[self.index].cp == "$":
                print("No Syntax Error")
            else:
                print("Syntax Error at Line #", self.ts[self.index].line)
        else:
            print("Syntax Error at Line #", self.ts[self.index].line)

