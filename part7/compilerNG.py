import sys
import argparse
import MLparserNG
import NameGenerator as ng

class ParserError(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg


count = 1
GEN = ng.NameGenerator("dummy2")
labelGen = ng.NameGenerator("Label")
declaredVars = []
variablesWritten = []

def compiler(source, tokens, output):
    tree, symbolTable, intLitTable = MLparserNG.parser(source, tokens)
    PROGRAM(tree, symbolTable, intLitTable, output)

def PROGRAM(tree, symbolTable, intLitTable, output):
    outputFile = BEGIN(tree, symbolTable, output)
    IG = ng.NameGenerator("if")
    EG = ng.NameGenerator("else")
    STATEMENT_LIST(tree.children[1], symbolTable, intLitTable, output, outputFile, IG, EG)
    return;

def BEGIN(tree, symbolTable, output):
    outputFile = open(output, 'w+')
    outputFile.write(".data\n")
    outputFile.write("True: .asciiz \"True\"\n")
    outputFile.write("False: .asciiz \"False\"\n")
    variablesWritten.append("True")
    variablesWritten.append("False")
   
    for i in symbolTable:
	#bools and literals
        if (i[3] != "string"):
            outputFile.write(i[0] + ": .word 0\n")
            variablesWritten.append(i[0])
	#strings:
	#outputFile.write(i[0] + ": .space 32\n")
    outputFile.write(".text\n")
    outputFile.flush()
    return outputFile
    
def STATEMENT_LIST(tree, symbolTable, intLitTable, output, outputFile, IG, EG):
    JG = ng.NameGenerator("jump")
    NG = ng.NameGenerator("dummy")
    for child in tree.children:
        STATEMENT(child, symbolTable, intLitTable, output, outputFile, JG, NG, IG, EG)
    return

def STATEMENT(tree, symbolTable, intLitTable, output, outputFile, JG, NG, IG, EG):
    global count
    global GEN
    global labelGen
    global variablesWritten
    index = 0
    if (tree.children[0].label == "READ"):
        for readID in tree.children[1].children:
            i = 0
            while (i < len(symbolTable)):
                if (count in symbolTable[i][1]):
                    index = i
                    break
                i = i + 1
            READ(tree, symbolTable, output, symbolTable[index][0])
            symbolTable[index][2] = True
            count = count + 1
    elif (tree.children[0].label == "WRITE"):
        i = 0
        v = None
        typeOfVal = None
        val = None
        name = next(NG)
        idStr = name
        op = None
        for child in tree.children:
            if child.label == "EXPR_LIST":
                for child2 in child.children:
                    if (child2.label == "EXPRESSION"):
                        jumpName = next(labelGen)
                        jumpName2 = next(labelGen)
                        val, typeOfVal = EXPRESSION(child2, symbolTable, intLitTable, output, idStr, i, True, typeOfVal, NG, JG)
                    if (val != None):
                        if typeOfVal == "int":
                            if val.isdigit():
                                WRITEInt(tree, symbolTable, output, val)
                            else:
                                WRITEVal(tree, symbolTable, output, val)
                        elif typeOfVal == "bool":
                            if (val == "True" or val == "False"):
                                printBoolLit(tree, symbolTable, output, val, next(labelGen), next(labelGen))
                            else:
                                printBoolVar(tree, symbolTable, output, val, next(labelGen), next(labelGen))
                            writeVarAtTop(output, val)
                        elif (typeOfVal == "string"):
                            if(val[0] == "\""): 
                                assignStringLit(tree, symbolTable, output, idStr, val)
                                WRITEstring(tree, symbolTable, output, idStr)
                            else:
                                WRITEstring(tree, symbolTable, output, val)
    elif (tree.children[0].label == "ASSIGNMENT"):
        tree = tree.children[0]
        idStr = None
        v = None
        typeOfVar = None
        val = None
        name = next(NG)
        typeOfVal = None
        for child in tree.children:
            if (child.label == "EXPRESSION"):
                jumpName = next(labelGen)
                jumpName2 = next(labelGen)
                val, typeOfVal = EXPRESSION(child, symbolTable, intLitTable, output, idStr, i, False, typeOfVar, NG, JG)
            elif child.label == "IDENT":
                idStr, typeOfVar, i = IDENT(child, symbolTable, intLitTable, output, False)
                symbolTable[i][2] = True
            elif child.label == "INIT":
                typeOfVar, idStr, i = INIT(child, symbolTable, intLitTable, output, outputFile, True)
                symbolTable[i][4] = True
        if (val != None):
             if(typeOfVar == "int"):
                 if (val.isdigit()):
                     assignIntLit(tree, symbolTable, output, idStr, val)
                 else:
                     assignVariable(tree, symbolTable, output, idStr, val)
             elif(typeOfVar == "bool"):
                 if (val == "True" or val == "False"):
                     assignBoolLit(tree, symbolTable, output, idStr, val)
                 else:
                     assignBoolVar(tree, symbolTable, output, idStr, val)
             elif (typeOfVar == "string"):
                 if(val[0] == "\""):
                     assignStringLit(tree, symbolTable, output, idStr, val)
                 else:
                     assignStringVar(tree, symbolTable, output, idStr, val)
                 if (idStr not in variablesWritten):
                     outputFile = open(output, 'r')
                     contents = outputFile.readlines()
                     outputFile.close()
                     contents.insert(1, idStr+": .space 64\n")
                     outputFile = open(output, 'w+')
                     contents = "".join(contents)
                     variablesWritten.append(idStr)
                     outputFile.write(contents)
             else:
                 assignVariable(tree, symbolTable, output, idStr, val)
             symbolTable[i][2] = True
        elif (idStr != None):
             if typeOfVar == "int" or typeOfVar == "bool":
                 writeVarAtTop(output, idStr)
             else:
                 if (idStr not in variablesWritten):
                     outputFile = open(output, 'r')
                     contents = outputFile.readlines()
                     outputFile.close()
                     contents.insert(1, idStr+": .space 64\n")
                     outputFile = open(output, 'w+')
                     contents = "".join(contents)
                     variablesWritten.append(idStr)
                     outputFile.write(contents)
 
    elif (tree.children[0].label == "IF"):
        ifName = next(IG)
        elseName = next(EG)
        
        idStr = None
        v = None
        typeOfVar = None
        val = None
        name = next(NG)
        tt = None
        i = 0

        for child in tree.children:
           if child.label == "BOOL1":
               jumpName = next(labelGen)
               jumpName2 = next(labelGen)
               val, typeofVal = BOOL1(child, symbolTable, intLitTable, output, idStr, i, True, "bool", NG, JG)
               printIf(tree, symbolTable, output, val, ifName)
           elif child.label == "STATEMENT_LIST":
               STATEMENT_LIST(child, symbolTable, intLitTable, output, outputFile, IG, EG)
           elif child.label == "ELSE":
               
               printElse(tree, symbolTable, output, elseName, ifName)
               ifName = elseName

        printIfLabel(tree, symbolTable, output, ifName)
    elif (tree.children[0].label == "WHILE"):
        topLabel = next(labelGen)
        bottomLabel = next(labelGen)
        for child in tree.children:
            if child.label == "BOOL1":
                printWhileTopLabel(tree, symbolTable, output, topLabel)
                i = 0
                v = None
                typeOfVar = None
                val = None
                name = next(NG)
                idStr = name
                jumpName = next(labelGen)
                jumpName2 = next(labelGen)
                val, typeOfVar = BOOL1(child, symbolTable, intLitTable, output, idStr, i, True, "bool", NG, JG)
                if(typeOfVar != "bool"):
                    raise ParserError("Semantic Error: invalid type for condition")
                printWhile(tree, symbolTable, output, val, topLabel, bottomLabel) 
            elif child.label == "STATEMENT_LIST": 
                STATEMENT_LIST(child, symbolTable, intLitTable, output, outputFile, IG, EG)
                printWhileBottomLabel(tree, symbolTable, output, topLabel, bottomLabel)
 

def EXPRESSION(tree, symbolTable, intLitTable, output, idStr, i, write, idType, NG, JG):
    global count
    val = None
    typeOfVal = None
    for child in tree.children:
        if child.label == "BOOL1":
            val, typeOfVal = BOOL1(child, symbolTable, intLitTable, output, idStr, i, write, idType, NG, JG)
            if typeOfVal != idType and not write:
                raise ParserError("Semantic Error: Can't assign type of " + typeOfVal + " to type of " + idType)
            return val, typeOfVal
        elif child.label == "STRINGLIT":
            j = 0
            typeOfVal = "string"
            while (j < len(intLitTable)):
                if (count == intLitTable[j][0]):
                    val = intLitTable[j][1]
                    count = count + 1 
                    break
                j = j + 1
            if typeOfVal != idType and not write:
                raise ParserError("Semantic Error: Can't assign type of " + typeOfVal + " to type of " + idType)
            if (idStr not in variablesWritten):
                outputFile = open(output, 'r')
                contents = outputFile.readlines()
                outputFile.close()
                contents.insert(1, idStr+": .space 64\n")
                outputFile = open(output, 'w+')
                contents = "".join(contents)
                variablesWritten.append(idStr)
                outputFile.write(contents)

            return val, typeOfVal    
    return val, typeOfVal

def BOOL1(tree, symbolTable, intLitTable, output, idStr, i, write, idType, NG, JG):
    val = None
    typeOfVal = None
    val2 = None
    typeOfVal2 = None
    op = None

    for child in tree.children:
        if child.label == "OR":
            op = "OR"
            val2 = val
            typeOfVal2 = typeOfVal
        elif child.label == "AND":
            op = "AND"
            val2 = val
            typeOfVal2 = typeOfVal
        elif child.label == "SWITCH":
            val, typeOfVal = SWITCH(child, symbolTable, intLitTable, output, idStr, i, write, idType, NG, JG)
            if op != None:
                idStr = next(NG)
                if idType != "bool" and not write:
                    raise ParserError("Semantic Error: Can't assign result to type of " + idType)
                elif (typeOfVal != "bool" or typeOfVal2 != "bool"):
                    raise ParserError("Semantic Error: Can't use OR on variable of " + typeOfVal + " type or of " + typeOfVal2)
                if op == "OR":
                    if ((val == "True" or val == "False") and (val2 == "True" or val2 == "False")):
                        orTwoLit(tree, symbolTable, output, val2, val, idStr)
                    elif ((val == "True" or val == "False") or (val2 == "True" or val2 == "False")):
                        if (val == "True" or val == "False"):
                            orOneVar(tree, symbolTable, output, val2, val, idStr)
                        else:
                            orOneVar(tree, symbolTable, output, val, val2, idStr)
                    else:
                        orTwoVar(tree, symbolTable, output, val, val2, idStr)
                elif op == "AND":
                    if ((val == "True" or val == "False") and (val2 == "True" or val2 == "False")):
                        andTwoLit(tree, symbolTable, output, val2, val, idStr)
                    elif ((val == "True" or val == "False") or (val2 == "True" or val2 == "False")):
                        if (val == "True" or val == "False"):
                            andOneVar(tree, symbolTable, output, val2, val, idStr)
                        else:
                            andOneVar(tree, symbolTable, output, val, val2, idStr)
                    else:
                        andTwoVar(tree, symbolTable, output, val, val2, idStr)
                writeVarAtTop(output, idStr)
                val = idStr
    return val, typeOfVal

def SWITCH(tree, symbolTable, intLitTable, output, idStr, i, write, idType, NG, JG):
    val = None
    typeOfVal = None
    op = None
    valPrev = None
    valPrevType = None
    for child in tree.children: 
        if child.label == "EXP2":
            val, typeOfVal = EXP2(child, symbolTable, intLitTable, output, idStr, i, write, idType, NG, JG)
            if op != None:
               idStr = next(NG)
               jumpName = next(labelGen)
               jumpName2 = next(labelGen)
               if idType != "bool" and not write:
                   raise ParserError("Semantic Error: Can't assign boolean expression to type of " + idType)
               if op == "LESSEQUAL":
                   if (typeOfVal != "int" or valPrevType != "int"):
                       raise ParserError("Semantic Error: Can't use type of " + typeOfVal + " and type of " + valPrevType + " in less than equal expression")
                   lessThanEqual(tree, symbolTable, output, val, valPrev, idStr, jumpName, jumpName2)
                   writeVarAtTop(output, idStr)
                   val = idStr
                   valPrev = valPrev <= val
                   typeOfVal = "bool"
               elif op == "GREATEQUAL":
                   if (typeOfVal != "int" or valPrevType != "int"):
                       raise ParserError("Semantic Error: Can't use type of " +
typeOfVal + " and type of " + valPrevType + " in greater than equal expression")
                   greaterThanEqual(tree, symbolTable, output, val, valPrev, idStr, jumpName, jumpName2)
                   writeVarAtTop(output, idStr)
                   val = idStr
                   valPrev = val >= valPrev
                   typeOfVal = "bool"
               elif op == "EQUAL":
                   if (typeOfVal != "int" or valPrevType != "int"):
                       raise ParserError("Semantic Error: Can't use type of " +
typeOfVal + " and type of " + valPrevType + " in equal expression")
                   equal(tree, symbolTable, output, val, valPrev, idStr, jumpName, jumpName2)
                   writeVarAtTop(output, idStr)
                   val = idStr
                   valPrev = (valPrev == val)
                   typeOfVal = "bool"
               elif op == "NOTEQUAL":
                   if (typeOfVal != "int" or valPrevType != "int"):
                       raise ParserError("Semantic Error: Can't use type of " +
typeOfVal + " and type of " + valPrevType + " in not equal expression")
                   notEqual(tree, symbolTable, output, val, valPrev, idStr, jumpName, jumpName2)
                   writeVarAtTop(output, idStr)
                   val = idStr
                   valPrev = (valPrev != val)
                   typeOfVal = "bool"
               elif op == "LESS":
                   if (typeOfVal != "int" or valPrevType != "int"):
                       raise ParserError("Semantic Error: Can't use type of " +
typeOfVal + " and type of " + valPrevType + " in less than expression")
                   jumpName = next(labelGen)
                   jumpName2 = next(labelGen)
                   lessThan(tree, symbolTable, output, val, valPrev, idStr, jumpName, jumpName2)
                   writeVarAtTop(output, idStr)
                   valPrev = valPrev < val
                   typeOfVal = "bool"
                   val = idStr 
                   
               elif op == "GREAT": 
                   if (typeOfVal != "int" or valPrevType != "int"):
                       raise ParserError("Semantic Error: Can't use type of " +
typeOfVal + " and type of " + valPrevType + " in greater than expression")
                   greaterThan(tree, symbolTable, output, val, valPrev, idStr, jumpName, jumpName2)
                   writeVarAtTop(output, idStr)
                   val = idStr
                   valPrev = valPrev > val
                   typeOfVal = "bool"
            else:
               valPrev = val
               valPrevType = typeOfVal
        elif child.label in {"LESSEQUAL", "GREATEQUAL", "EQUAL", "NOTEQUAL", "LESS", "GREAT"}:
            op = SWITCHPRIME(child, symbolTable, intLitTable, output, idStr, i, write, idType, NG, JG)
    return val, typeOfVal

def SWITCHPRIME(child, symbolTable, intLitTable, output, idStr, i, write, idType, NG, JG):
    op = None
    if child.label == "LESSEQUAL":
        op = child.label
    elif child.label == "GREATEQUAL":
        op = child.label
    elif child.label == "EQUAL":
        op = child.label
    elif child.label == "NOTEQUAL":
        op = child.label
    elif child.label == "LESS":
        op = child.label
    elif child.label == "GREAT":
        op = child.label
    return op

def EXP2(tree, symbolTable, intLitTable, output, idStr, i, write, idType, NG, JG):
    val = None
    typeOfVal = None
    val2 = None
    typeOfVal2 = None
    op = None
    for child in tree.children:
        if child.label == "PLUS":
            op = "PLUS"
            val2 = val
            typeOfVal2 = typeOfVal
        elif child.label == "MINUS":
            op = "MINUS"
            val2 = val
            typeOfVal2 = typeOfVal
        elif child.label == "EXP2PRIME":
            val, typeOfVal = EXP2PRIME(child, symbolTable, intLitTable, output, idStr, i, write, idType, NG, JG)
            if op != None:
                idStr = next(NG)
        #        if idType != "int" and not write:
        #            raise ParserError("Semantic Error: Can't assign result to type of " + idType)
                if (typeOfVal != "int" or typeOfVal2 != "int"):
                    raise ParserError("Semantic Error: Can't use " + op + " on variable of type " + typeOfVal + " and type " + typeOfVal2)
                if (op == "PLUS"):
                    infixAdd(tree, symbolTable, output, idStr, val2, val)
                    writeVarAtTop(output, idStr)
                elif op == "MINUS":
                    infixSub(tree, symbolTable, output, idStr, val2, val)
                    writeVarAtTop(output, idStr)
                val = idStr
    return val, typeOfVal

def EXP2PRIME(tree, symbolTable, intLitTable, output, idStr, i, write, idType, NG, JG):
    val = None
    typeOfVal = None
    op = None
    val2 = None
    typeOfVal2 = None
    for child in tree.children:
        if child.label == "MULTI":
            op = "MULTI"
            val2 = val
            typeOfVal2 = typeOfVal
        elif child.label == "DIV":
            op = "DIV"
            val2 = val
            typeOfVal2 = typeOfVal
        elif child.label == "MOD":
            op = "MOD"
            val2 = val
            typeOfVal2 = typeOfVal
        elif child.label == "PRIMARY":
            val, typeOfVal = PRIMARY(child, symbolTable, intLitTable, output, idStr, i, write, idType, NG, JG)
            if op != None:
                idStr = next(NG)
        #        if idType != "int" and not write:
        #            raise ParserError("Semantic Error: Can't assign result to type of " + idType)
                if (typeOfVal != "int" or typeOfVal2 != "int"):
                    raise ParserError("Semantic Error: Can't use " + op + " on variable of type " + typeOfVal + " and type " + typeOfVal2)
                if (op == "MULTI"):
                    infixMult(tree, symbolTable, output, idStr, val2, val)
                    writeVarAtTop(output, idStr)          
                elif op == "DIV":
                    infixDiv(tree, symbolTable, output, idStr, val2, val)
                    writeVarAtTop(output, idStr)
                elif op == "MOD":
                    infixRem(tree, symbolTable, output, idStr, val2, val)
                    writeVarAtTop(output, idStr)
                val = idStr       
    return val, typeOfVal

def PRIMARY(tree, symbolTable, intLitTable, output, idStr, i, write, idType, NG, JG):
    global count
    val = None
    typeOfVal = None
    negate = False
    notT = False
    idStr = next(NG)
    init = False
    for child in tree.children:
        if child.label == "BOOL1":
            val, typeOfVal = BOOL1(child, symbolTable, intLitTable, output, idStr, i, write, idType, NG, JG) 
            if negate:
                if typeOfVal != "int":
                    raise ParserError("Semantic Error: Can't negate non integer")
                infixSub(tree, symbolTable, output, idStr, "0", val)
                writeVarAtTop(output, idStr)
                val = idStr
                idStr = next(NG)
            if notT:
                if typeOfVal != "bool":
                    raise ParserError("Semantic Error: Can't not non boolean expression")
                notVar(tree, symbolTable, output, val, idStr)
                writeVarAtTop(output, idStr)
                val = idStr
                typeOfVar = "bool"
        elif child.label == "IDENT":
            val, typeOfVal, i = IDENT(child, symbolTable, intLitTable, output, init)
            if (symbolTable[i][2] != True):
                raise ParserError("Semantic Error: Unitialized Variable")
            typeOfVar = symbolTable[i][3]
            val = symbolTable[i][0] 
            if (negate):
                infixSub(tree, symbolTable, output, idStr, "0", val)
                writeVarAtTop(output, idStr)
                val = idStr
                idStr = next(NG)
            elif (notT):
                notLit(tree, symbolTable, output, val, idStr)
                writeVarAtTop(output, idStr)
                val = idStr
                typeOfVar = "bool" 
        elif child.label == "INTLIT":
            typeOfVal = "int"
            j = 0
            while (j < len(intLitTable)):
                if count == intLitTable[j][0]:
                    val = intLitTable[j][1]
                    count = count + 1
                    break;
                j = j + 1
            if negate:
                infixSub(tree, symbolTable, output, idStr, "0", val)
                writeVarAtTop(output, idStr)
                val = idStr
                idStr = next(NG)
        elif child.label == "BOOLLIT":
            typeOfVal = "bool"
            i = 0
            while(i < len(intLitTable)):
                if count == intLitTable[i][0]:
                    val = intLitTable[i][1]
                    count = count + 1
                    break
                i = i + 1
            if notT:
                notLit(tree, symbolTable, output, val, idStr)
                writeVarAtTop(output, idStr)
                val = idStr
                typeOfVar = "bool"
        elif child.label == "MINUS":
            negate = True
        elif child.label == "NOT":
            notT = True
    return val, typeOfVal

def IDENT(tree, symbolTable, intLitTable, output, init):
    global count, declaredVars
    idStr = None
    i = 0
    while (i < len(symbolTable)):
        if (count in symbolTable[i][1]):
            idStr = symbolTable[i][0]
            count = count + 1
            break
        i = i + 1
    if (not symbolTable[i][4]):
        symbolTable[i][4] = init
    if symbolTable[i][4] != True:
        raise ParserError("Semantic Error: Variable not declared")
    
    if init:
        if idStr in declaredVars:
            raise ParserError("Semantic Error: Duplicate variable")
        declaredVars.append(idStr)

    return idStr, symbolTable[i][3], i

def INIT(tree, symbolTable, intLitTable, output, outputFile, init):
    global declaredVars
    typeOfVar = None
    idStr = None
    for child in tree.children:
        if child.label == "INTTYPE":
            typeOfVar = "int"
        elif child.label == "BOOLTYPE":
            typeOfVar = "bool"
        elif child.label == "STRTYPE":
            typeOfVar = "string"
        if child.label == "IDENT":
            idStr, typeOfVar, i = IDENT(tree, symbolTable, intLitTable, output, init)
    return typeOfVar, idStr, i

def writeVarAtTop(output, idStr):
    global variablesWritten
    if (idStr not in variablesWritten):
        outputFile = open(output, 'r')
        contents = outputFile.readlines()
        outputFile.close()
        contents.insert(1, idStr+": .word 0\n")
        outputFile = open(output, 'w+')
        contents = "".join(contents)
        variablesWritten.append(idStr)
        outputFile.write(contents)

def READ(tree, symbolTable, output, readID):
    with open(output, "a") as outputFile:
        outputFile.write("\nli $v0, 5\nsyscall\nla $t0, " + readID + "\nsw $v0, 0($t0)\n")

def WRITEVal(tree, symbolTable, output, writeId):
    with open(output,"a") as outputFile:
        outputFile.write("\nli $v0,1\nlw $a0," + writeId + "\nsyscall\n")

def WRITEInt(tree, symbolTable, output, writeId):
     with open(output,"a") as outputFile:
        outputFile.write("\nli $v0,1\nli $a0," + writeId + "\nsyscall\n")

def WRITEstring(tree, symbolTable, output, writeId):
     with open(output,"a") as outputFile:
        outputFile.write("\nla $t0 "+writeId+"\nmove $a0, $t0\nli $v0,4\nsyscall\n")

def assignIntLit(tree, symbolTable, output, ident, value):
    with open(output,"a") as outputFile:
        outputFile.write("\nli $t0,"+value+"\nla $t1,"+ident+"\nsw $t0, 0($t1)\n")

def assignVariable(tree, symbolTable, output, ident1, ident2):
    with open(output,"a") as outputFile:
        outputFile.write("\nla $t0,"+ident2+"\nla $t1,"+ident1+"\nlw $t2, 0($t0)\nsw $t2, 0($t1)\n")

def assignBoolLit(tree, symbolTable, output, ident, value):
    if(value == "False"):
        value = "0"
    else:
        value = "1"
    with open(output,"a") as outputFile:
        outputFile.write("\nli $t0,"+value+"\nla $t1,"+ident+"\nsw $t0, 0($t1)\n")

def assignBoolVar(tree, symbolTable, output, ident1, ident2):
    with open(output,"a") as outputFile:
        outputFile.write("\nla $t0,"+ident2+"\nla $t1,"+ident1+"\nlw $t2, 0($t0)\nsw $t2, 0($t1)\n")

def assignStringLit(tree, symbolTable, output, variableName, value):
    with open(output,"a") as outputFile:
        outputFile.write("\nla $s0, "+variableName+"\n")
        for char in value:
             if char in {"'"}:
                 char = "\\"+char
             outputFile.write("\nli $t0, '" + char + "'\nsb $t0, ($s0)\naddi $s0, $s0, 1\n")
   
def assignStringVar(tree, symbolTable, output, ident1, ident2):
    with open(output,"a") as outputFile:
#        outputFile.write("\nlw $s0, "+ident1+"\nsw $s0 "+ident2+"\n")
        outputFile.write("\nla $s0, "+ident1+"\nla $s1, "+ident2)
        i = 0;
        while i < 64:
            outputFile.write("\nlb $t0, ($s1)\nsb $t0, ($s0)\n")
            outputFile.write("addi $s0, $s0, 1\naddi $s1, $s1, 1\n")
            i = i + 1

#logical operators
def andTwoVar(tree, symbolTable, output, varOne, varTwo, result):
    with open(output,"a") as outputFile:
        outputFile.write("\nlw $t1, "+varOne+"\nlw $t2, "+varTwo+"\nand $t0, $t1, $t2\nsw $t0, "+result+"\n")

def andOneVar(tree, symbolTable, output, varOne, lit, result):
    if(lit == "True"):
        value = "1"
    else:
        value = "0"
    with open(output,"a") as outputFile:
        outputFile.write("\nlw $t1, "+varOne+"\nli $t2, "+value+"\nand $t0, $t1, $t2\nsw $t0, "+result+"\n")

def andTwoLit(tree, symbolTable, output, lit1, lit2, result):
    if(lit1 == "True"):
        value1 = "1"
    else:
        value1 = "0"
    if(lit2 == "True"):
        value2 = "1"
    else:
        value2 = "0"
    with open(output,"a") as outputFile:
        outputFile.write("\nli $t1, "+value1+"\nli $t2, "+value2+"\nand $t0, $t1, $t2\nsw $t0, "+result+"\n")

def orTwoVar(tree, symbolTable, output, varOne, varTwo, result):
    with open(output,"a") as outputFile:
        outputFile.write("\nlw $t1, "+varOne+"\nlw $t2, "+varTwo+"\nor $t0, $t1, $t2\nsw $t0, "+result+"\n")

def orOneVar(tree, symbolTable, output, varOne, lit, result):
    if(lit == "True"):
        value = "1"
    else:
        value = "0"
    with open(output,"a") as outputFile:
        outputFile.write("\nlw $t1, "+varOne+"\nli $t2, "+value+"\nor $t0, $t1, $t2\nsw $t0, "+result+"\n")

def orTwoLit(tree, symbolTable, output, lit1, lit2, result):
    if(lit1 == "True"):
        value1 = "1"
    else:
        value1 = "0"
    if(lit2 == "True"):
        value2 = "1"
    else:
        value2 = "0"
    with open(output,"a") as outputFile:
        outputFile.write("\nli $t1, "+value1+"\nli $t2, "+value2+"\nor $t0, $t1, $t2\nsw $t0, "+result+"\n")

def notLit(tree, symbolTable, output, lit, result):
    if(lit == "True"):
        value = "1"
    else:
        value = "0"
    with open(output,"a") as outputFile:
        outputFile.write("\nli $t1, "+value+"\nli $t2, 1\nxor $t0, $t1, $t2\nsw $t0, "+result+"\n")

def notVar(tree, sumbolTable, output, var, result):
    with open(output,"a") as outputFile:
        outputFile.write("\nlw $t1, "+var+"\nli $t2, 1\nxor $t0, $t1, $t2\nsw $t0, "+result+"\n")

#Math
def infixAdd(tree, symbolTable, output, ident1, ident2, ident3):
    with open(output,"a") as outputFile:
        if(ident2.isdigit()):
            outputFile.write("\nli $s0, "+ident2+"\nla $t1, 0($s0)\n")
        else:
            outputFile.write("\nla $s0, "+ident2+"\nlw $t1, 0($s0)\n")
        if(ident3.isdigit()):
            outputFile.write("li $s0, "+ident3+"\nla $t2, 0($s0)\n")
        else:
            outputFile.write("la $s0, "+ident3+"\nlw $t2, 0($s0)\n")

        outputFile.write("add $t0, $t1, $t2\nla $s0,"+ident1+"\nsw $t0, 0($s0)\n")
    
def infixSub(tree, symbolTable, output, ident1, ident2, ident3):
    with open(output,"a") as outputFile:
        if(ident2.isdigit()):
            outputFile.write("\nli $s0, "+ident2+"\nla $t1, 0($s0)\n")
        else:
            outputFile.write("\nla $s0, "+ident2+"\nlw $t1, 0($s0)\n")
        if(ident3.isdigit()):
            outputFile.write("li $s0, "+ident3+"\nla $t0, 0($s0)\n")
        else:
            outputFile.write("la $s0, "+ident3+"\nlw $t0, 0($s0)\n")

        outputFile.write("sub $t0, $t1, $t0\nla $s0,"+ident1+"\nsw $t0, 0($s0)\n")	

def infixMult(tree, symbolTable, output, ident1, ident2, ident3):
    with open(output,"a") as outputFile:
        if(ident2.isdigit()):
            outputFile.write("\nli $s0, "+ident2+"\nla $t1, 0($s0)\n")
        else:
            outputFile.write("\nla $s0, "+ident2+"\nlw $t1, 0($s0)\n")
        if(ident3.isdigit()):
            outputFile.write("li $s0, "+ident3+"\nla $t0, 0($s0)\n")
        else:
            outputFile.write("la $s0, "+ident3+"\nlw $t0, 0($s0)\n")

        outputFile.write("mul $t0, $t1, $t0\nla $s0,"+ident1+"\nsw $t0, 0($s0)\n")	

def infixDiv(tree, symbolTable, output, ident1, ident2, ident3):
    with open(output,"a") as outputFile:
        if(ident2.isdigit()):
            outputFile.write("\nli $s0, "+ident2+"\nla $t1, 0($s0)\n")
        else:
            outputFile.write("\nla $s0, "+ident2+"\nlw $t1, 0($s0)\n")
        if(ident3.isdigit()):
            outputFile.write("li $s0, "+ident3+"\nla $t0, 0($s0)\n")
        else:
            outputFile.write("la $s0, "+ident3+"\nlw $t0, 0($s0)\n")

        outputFile.write("div $t0, $t1, $t0\nla $s0,"+ident1+"\nsw $t0, 0($s0)\n")	

def infixRem(tree, symbolTable, output, ident1, ident2, ident3):
    with open(output,"a") as outputFile:
        if(ident2.isdigit()):
            outputFile.write("\nli $s0, "+ident2+"\nla $t1, 0($s0)\n")
        else:
            outputFile.write("\nla $s0, "+ident2+"\nlw $t1, 0($s0)\n")
        if(ident3.isdigit()):
            outputFile.write("li $s0, "+ident3+"\nla $t0, 0($s0)\n")
        else:
            outputFile.write("la $s0, "+ident3+"\nlw $t0, 0($s0)\n")

        outputFile.write("rem $t0, $t1, $t0\nla $s0,"+ident1+"\nsw $t0, 0($s0)\n")	

def equal(tree, symbolTable, output, ident1, ident2, ident3,label1, label2):
    with open(output,"a") as outputFile:
        if(ident1.isdigit()):
            outputFile.write("\nli $t0, "+ident1+"\n")
        else:
            outputFile.write("\nlw $t0, "+ident1+"\n")
        if(ident2.isdigit()):
            outputFile.write("li $t1, "+ident2+"\n")
        else:
            outputFile.write("lw $t1, "+ident2+"\n")
	
        outputFile.write("bne $t0, $t1, "+label1+"\nli $t2, 1\nsw $t2, "+ident3+"\nj "+label2)	
        outputFile.write("\n"+label1+":\nli $t2, 0\nsw $t2, "+ident3+"\n"+label2+":\n")

def notEqual(tree, symbolTable, output, ident1, ident2, ident3,label1, label2):
    with open(output,"a") as outputFile:
        if(ident1.isdigit()):
            outputFile.write("\nli $t0, "+ident1+"\n")
        else:
            outputFile.write("\nlw $t0, "+ident1+"\n")
        if(ident2.isdigit()):
            outputFile.write("li $t1, "+ident2+"\n")
        else:
            outputFile.write("lw $t1, "+ident2+"\n")
	
        outputFile.write("bne $t0, $t1, "+label1+"\nli $t2, 0\nsw $t2, "+ident3+"\nj "+label2)	
        outputFile.write("\n"+label1+":\nli $t2, 1\nsw $t2, "+ident3+"\n"+label2+":\n")
#ident1 is less than ident2
def lessThan(tree, symbolTable, output, ident1, ident2, ident3,label1, label2):
    with open(output,"a") as outputFile:
        outputFile.write("#LESS THAN")
        if(ident2.isdigit()):
            outputFile.write("\nli $t0, "+ident2+"\n")
        else:
            outputFile.write("\nlw $t0, "+ident2+"\n")
        if(ident1.isdigit()):
            outputFile.write("li $t1, "+ident1+"\n")
        else:
            outputFile.write("lw $t1, "+ident1+"\n")
	
        outputFile.write("bge $t0, $t1, "+label1+"\nli $t2, 1\nsw $t2, "+ident3+"\nj "+label2)	
        outputFile.write("\n"+label1+":\nli $t2, 0\nsw $t2, "+ident3+"\n"+label2+":\n")

def lessThanEqual(tree, symbolTable, output, ident1, ident2, ident3,label1, label2):
    with open(output,"a") as outputFile:
        outputFile.write("#LESS THAN EQUAL")
        if(ident2.isdigit()):
            outputFile.write("\nli $t0, "+ident2+"\n")
        else:
            outputFile.write("\nlw $t0, "+ident2+"\n")
        if(ident1.isdigit()):
            outputFile.write("li $t1, "+ident1+"\n")
        else:
            outputFile.write("lw $t1, "+ident1+"\n")
	 
        outputFile.write("bgt $t0, $t1, "+label1+"\nli $t2, 1\nsw $t2, "+ident3+"\nj "+label2)	
        outputFile.write("\n"+label1+":\nli $t2, 0\nsw $t2, "+ident3+"\n"+label2+":\n")

def greaterThan(tree, symbolTable, output, ident1, ident2, ident3,label1, label2):
    with open(output,"a") as outputFile:
        outputFile.write("#GREATER THAN")
        if(ident2.isdigit()):
            outputFile.write("\nli $t0, "+ident2+"\n")
        else:
            outputFile.write("\nlw $t0, "+ident2+"\n")
        if(ident1.isdigit()):
            outputFile.write("li $t1, "+ident1+"\n")
        else:
            outputFile.write("lw $t1, "+ident1+"\n")
	
        outputFile.write("bgt $t0, $t1, "+label1+"\nli $t2, 0\nsw $t2, "+ident3+"\nj "+label2)	
        outputFile.write("\n"+label1+":\nli $t2, 1\nsw $t2, "+ident3+"\n"+label2+":\n")

def greaterThanEqual(tree, symbolTable, output, ident1, ident2, ident3,label1, label2):
    with open(output,"a") as outputFile:
        outputFile.write("#GREATER THAN EQUAL")
        if(ident2.isdigit()):
            outputFile.write("\nli $t0, "+ident2+"\n")
        else:
            outputFile.write("\nlw $t0, "+ident2+"\n")
        if(ident1.isdigit()):
            outputFile.write("li $t1, "+ident1+"\n")
        else:
            outputFile.write("lw $t1, "+ident1+"\n")
	
        outputFile.write("bge $t0, $t1, "+label1+"\nli $t2, 0\nsw $t2, "+ident3+"\nj "+label2)	
        outputFile.write("\n"+label1+":\nli $t2, 1\nsw $t2, "+ident3+"\n"+label2+":\n")

#assumes variables "True" and "False" correspond to the correct values in the .data section
def printBoolVar(tree, symbolTable, output, boolean, label1, label2):
    with open(output,"a") as outputFile:
        outputFile.write("\nlw $t0, "+boolean+"\nli $t1, 1\nbne $t1, $t0, "+label1+"\n")
        outputFile.write("li $v0, 4\nla $a0 True\nsyscall\nj "+label2+"\n"+label1+":\n")
        outputFile.write("li $v0, 4\nla $a0, False\nsyscall\n"+label2+":\n")

def printBoolLit(tree, symbolTable, output, boolean, label1, label2):
    if(boolean == "True"):
        boolean = "1";
    else:
        boolean = "0";
    with open(output,"a") as outputFile:
        outputFile.write("\nli $t0, "+boolean+"\nli $t1, 1\nbne $t1, $t0, "+label1+"\n")
        outputFile.write("li $v0, 4\nla $a0 True\nsyscall\nj "+label2+"\n"+label1+":\n")
        outputFile.write("li $v0, 4\nla $a0, False\nsyscall\n"+label2+":\n")

def printIf(tree, symbolTable, output, controlVar, labelElse):
    if(controlVar == "True"):
        controlVar = "1"
    elif(controlVar == "False"):
        controlVar = "0"
    with open(output,"a") as outputFile:
        if(controlVar == "0" or controlVar == "1"):
            outputFile.write("li $t0, "+controlVar)
        else:
            outputFile.write("lw $t0, "+controlVar)
        outputFile.write("\nli $t1, 1\nbne $t0, $t1, "+labelElse+"\n")
        
def printElse(tree, symbolTable, output, labelIf, labelElse):
    with open(output, "a") as outputFile: 
        outputFile.write("j "+labelIf+"\n")
        outputFile.write(labelElse+":\n")

def printIfLabel(tree, symbolTable, output, labelIf):
    with open(output, "a") as outputFile:
        outputFile.write(labelIf+":\n")

#writes the jump after the while loop code
def printWhileLabel(tree, smbolTable, output, labelWhile, exitLabel):
    with open(output, "a") as outputFile:
        outputFile.write("\nj "+labelWhile)
        outputFile.write("\n"+exitLabel+":\n")

def printWhileBottomLabel(tree, symbolTable, output, labelWhile, exitLabel):
    with open(output, "a") as outputFile:
        outputFile.write("\nj " + labelWhile)
        outputFile.write("\n" + exitLabel + ":\n")

def printWhileTopLabel(tree, symbolTable, output, labelWhile):
    with open(output, "a") as outputFile:
        outputFile.write("\n" + labelWhile + ":\n")

def printWhile(tree, symbolTable, output, controlVar, whileLabel, exitLabel):
    if(controlVar == "True"):
        controlVar = "1" 
    elif(controlVar == "False"):
        controlVar = "0"
    with open(output, "a") as outputFile:
        if(controlVar == "0" or controlVar == "1"):
            outputFile.write("li $t0, " + controlVar)
        else:
            outputFile.write("lw $t0, "+controlVar)
        outputFile.write("\nli $t1, 1\nbne $t0, $t1, "+exitLabel)
       
if __name__ == "__main__":  # Only true if program invoked from the command line

    # Use the argparse library to parse the commandline arguments
    parser = argparse.ArgumentParser(description = "GroupX micro-language compiler")
    parser.add_argument('-t', type = str, dest = 'token_file',
                       help = "Token file", default = 'tokens.txt')
    parser.add_argument('source_file', type = str,
                        help = "Source-code file", default = 'tokens.txt')
    parser.add_argument('output_file', type = str, 
                        help = 'output file name')
    
    args = parser.parse_args()

    # Call the compiler function
    compiler(args.source_file, args.token_file, args.output_file)
