import sys
import argparse
import MLparser
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
funcReturns = []
funcReturnVars = []
funcParamVars = []
curMeth = None;

def compiler(source, tokens, output):
    tree, symbolTable, intLitTable = MLparser.parser(source, tokens)
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
    outputFile.write("newline: .asciiz \"\\n\"\n")
    variablesWritten.append("True")
    variablesWritten.append("False")
    variablesWritten.append("newline")
    method = "";
    for i in symbolTable:
	#bools and literals
        if (i[3] == "int" or i[3] == "bool" or i[3] == "pointer"):
            outputFile.write(i[0] + ": .word 0\n")
            variablesWritten.append(i[0])
	#strings:
        if (i[3] == "string"):
            outputFile.write(i[0] + ": .space 64\n")
            variablesWritten.append(i[0])
    outputFile.write(".text\nj main\n")
    outputFile.flush()
    return outputFile
    
def STATEMENT_LIST(tree, symbolTable, intLitTable, output, outputFile, IG, EG):
    print(tree)
    JG = ng.NameGenerator("jump")
    NG = ng.NameGenerator("dummy")
    print(symbolTable)
    print(intLitTable)
    for child in tree.children:
        STATEMENT(child, symbolTable, intLitTable, output, outputFile, JG, NG, IG, EG)
    return

def STATEMENT(tree, symbolTable, intLitTable, output, outputFile, JG, NG, IG, EG):
    global count
    global GEN
    global labelGen
    global variablesWritten
    global curMeth
    global funcReturns
    global funcParamVars 

    index = 0
    print("STATEMENT")
    print(tree.children[0].label)
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
########################################################################################################
    elif (tree.children[0].label == "WRITE"):
        print("WRITE")
        print(tree)
        i = 0
        v = None
        typeOfVar = None
        val = None
        name = next(NG)
        idStr = name
        for child in tree.children:
            print("CHILD LABEL ::::::::::")
            print(child.label)
            if child.label == "EXPR_LIST":
                for child2 in child.children:
                    
                    if (child2.label == "EXPR"):
                        jumpName = next(labelGen)
                        jumpName2 = next(labelGen)
                        val, typeOfVar,  op = EXPRESSION(child2, symbolTable, intLitTable, output, idStr ,i, True, typeOfVar, name, NG, JG, jumpName, jumpName2)
                   
                    if (val != None):
                        if(typeOfVar == "int"):
                            if (op in {'GREATEQUAL', 'LESSEQUAL', 'EQUAL', 'NOTEQUAL', 'GREAT', 'LESS'}):
                                printBoolVar(tree, symbolTable, output, val, next(labelGen), next(labelGen))  
                            elif (val.isdigit()):
                                WRITEInt(tree, symbolTable, output, val)
                            else:
                                WRITEVal(tree, symbolTable, output, val)
                        #writeVarAtTop(output, val)
                        elif(typeOfVar == "bool"):
                            if (val == "True" or val == "False"):
                                printBoolLit(tree, symbolTable, output, val, next(labelGen), next(labelGen))
                            else:
                                printBoolVar(tree, symbolTable, output, val, next(labelGen), next(labelGen))
                            writeVarAtTop(output, val)
                        elif (typeOfVar == "string"):
                            
                            if(val[0] == "\""): 
                                idStr = next(NG)
                                assignStringLit(tree, symbolTable, output, idStr, val)
                                WRITEstring(tree, symbolTable, output, idStr)
                            else:
                                WRITEstring(tree, symbolTable, output, val)
                            #writeVarAtTop(output, idStr)
                            if (idStr not in variablesWritten):
                                outputFile = open(output, 'r')
                                contents = outputFile.readlines()
                                outputFile.close()
                                contents.insert(1, idStr+": .space 64\n")
                                outputFile = open(output, 'w+')
                                contents = "".join(contents)
                                variablesWritten.append(idStr)
                                outputFile.write(contents)
                                outputFile.close();
			elif (typeOfVar == "pointer"):
                            printPointer(output, val)
                        elif (idStr not in variablesWritten):
                            WRITEVal(tree, symbolTable, output, val)
                            outputFile = open(output, 'r')
                            contents = outputFile.readlines()
                            outputFile.close()
                            contents.insert(1, idStr+": .space 64\n")
                            outputFile = open(output, 'w+')
                            contents = "".join(contents)
                            variablesWritten.append(idStr)

                            outputFile.write(contents)
            else:
                print("Unknown" + child.label) 
        writeNewLine(output);
########################################################################################################
    elif (tree.children[0].label == "ASSIGNMENT"):
        tree = tree.children[0]
        idStr = None
        v = None
        typeOfVar = None
        val = None
        name = next(NG)
        tt = None 
        print(tree)
        for child in tree.children:
            if (child.label == "EXPR"):
                jumpName = next(labelGen)
                jumpName2 = next(labelGen)
                val, tt, op = EXPRESSION(child, symbolTable, intLitTable, output, idStr,i, False, typeOfVar, name, NG, JG, jumpName, jumpName2)
            elif child.label == "IDENT":
                idStr, i, typeOfVar = IDENT(child, symbolTable, intLitTable, output, False)
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
                 if(idStr not in variablesWritten):
                     outputFile = open(output, 'r')
                     contents = outputFile.readlines()
                     outputFile.close()
                     contents.insert(1, idStr+": .space 64\n")
                     outputFile = open(output, 'w+')
                     contents = "".join(contents)
                     variablesWritten.append(idStr)
		     
                     outputFile.write(contents)
             elif typeOfVar == "pointer":
                 print("pointer in assign !!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                 assignPointerVal(tree, symbolTable, output, idStr, val)
             else:
                 assignVariable(tree, symbolTable, output, idStr, val)
             symbolTable[i][2] = True
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
           if child.label == "EXPR":
               jumpName = next(labelGen)
               jumpName2 = next(labelGen)
               val, tt, op = EXPRESSION(child, symbolTable, intLitTable, output, idStr,i, True, "bool", name, NG, JG, jumpName, jumpName2)
               print(tt)
               print("VAL::::::::::::::")
               print(val)
               if tt != "bool":
                   raise ParserError("Semantic Error: invalid type for condition")
               printIf(tree, symbolTable, output, val, ifName)
           elif child.label == "STATEMENT_LIST":
               STATEMENT_LIST(child, symbolTable, intLitTable, output, outputFile, IG, EG)
           elif child.label == "ELSE":
               printElse(tree, symbolTable, output, elseName, ifName)
               ifName = elseName

        printIfLabel(tree, symbolTable, output, ifName)
    elif (tree.children[0].label == "WHILE"):
        print(tree)
        topLabel = next(JG)
        bottomLabel = next(JG)
        
        for child in tree.children:
            print(child.label)
            if child.label == "EXPR":
                printWhileTopLabel(tree, symbolTable, output, topLabel)
                i = 0
                v = None
                typeOfVar = None
                val = None
                name = next(NG)
                idStr = name
                jumpName = next(labelGen)
                jumpName2 = next(labelGen)
                val, typeOfVar, op = EXPRESSION(child, symbolTable, intLitTable, output, idStr, i, True, "bool", name, NG, JG, jumpName, jumpName2)
                if(typeOfVar != "bool"):
                    raise ParserError("Semantic Error: invalid type for condition")
                printWhile(tree, symbolTable, output, val, topLabel, bottomLabel) 
            elif child.label == "STATEMENT_LIST": 
                STATEMENT_LIST(child, symbolTable, intLitTable, output, outputFile, IG, EG)
                printWhileBottomLabel(tree, symbolTable, output, topLabel, bottomLabel)
    elif (tree.children[0].label == "METH"):
        methName = None;
        for child in tree.children:
            
            if(child.label == "METH"):
                j = 0
                while j < len(symbolTable):
                   if count in symbolTable[j][1]:
                       methName = symbolTable[j][0]
                       count = count + 1
                       break;
                   j = j + 1
                writeMethHead(methName, output)
            elif(child.label == "METHOD"):
                methchild = child
                returnType = methchild.children[0].label;
             
                paramList = []
                for initVars in methchild.children[2].children:
                    if(initVars is not None):
                        i = 0
                        while i < len(symbolTable):
                            if(count in symbolTable[i][1]):
                                break;
                            i = i + 1
                        symbolTable[i][4] = True
                        paramList.append(symbolTable[i][0])
                        count = count + 1;
                funcParamVars.append([methName, paramList])
		#count = count - len(methchild.children[2].children)
                index = 3;
                indexMax = len(methchild.children)
               
                retName = next(NG)
                if(returnType == "STRTYPEFUNC"):
                    writeStringAtTop(output, retName)
                    funcReturnVars.append([methName, retName])
                elif(returnType != "VOIDFUNC"):
                    writeVarAtTop(output, retName) 
                    funcReturnVars.append([methName, retName])
                while(index < indexMax):
                    curMeth = methName    
                    STATEMENT(methchild.children[index], symbolTable, intLitTable, output, outputFile, JG, NG, IG, EG);
                    index+=1
           
            elif(child.label == "METHEND"):
                if(methName == "main"):
                    writeMainReturn(output)
                else:
                    writeMethReturn(methName, output)
##############################################################################################
    elif (tree.children[0].label == "FUNC"):
        j = 0
        methName = None;
        while j < len(symbolTable):
            if count in symbolTable[j][1]:
                methName = symbolTable[j][0]
                count = count + 1
                break;
            j = j + 1
      
        val = None
        typeOfVar = None
        op = None
        name = next(NG)
        idStr = name
        
        index = 0
        for func in funcParamVars:
            if(func[0] is methName):
                break;
            index = index + 1
        param = 0
        if(tree.children[2] is not None):
             for child in tree.children[2].children:
                 for newchild in child.children:
            	     val, typeOfVar, op = EXPRESSION(newchild, symbolTable, intLitTable, output, idStr, 0, True, typeOfVar, name, NG, JG, None, None)
                     paramVar = funcParamVars[index][1][param]
                     if typeOfVar == "string":
                         if val[0] == "\"":	
                             assignStringLit(tree, symbolTable, output, paramVar, val)
                         else:
                             assignStringVar(tree, symbolTable, output, paramVar, val)
                     elif typeOfVar == "int":
                         if val.isdigit():
                             assignIntLit(tree, symbolTable, output, paramVar, val)
                         else:
                             assignVariable(tree, symbolTable, output, paramVar, val)
                     elif typeOfVar == "bool":
                         if val == "True" or val == "False":
                             assignBoolLit(tree, symbolTable, output, paramVar, val)
                         else:
                             assignBoolVar(tree, symbolTable, output, paramVar, val)
                     elif typeOfVar == "pointer":
                         i = 0;
                         while i < len(symbolTable):
                             if(symbolTable[i][0] == val):
                                 break;
                             i = i + 1
                         if(symbolTable[i][3] == "int"):
                             print("ASSIGN POINTER REF 2 ######################################################")
                             assignPointerRef(tree, symbolTable, output, paramVar, val)
                         else:
                             print("ASSIGN VARIABLE 1 ######################################################")
                             assignVariable(tree, symbolTable, output, paramVar, val)
	             param = param + 1
             writeFuncCall(methName, output)
############################################################################################
    elif (tree.children[0].label == "RETURN"):
        for child in tree.children:
            
            val = None
            name = next(NG)
            idStr = name
            typeOfVar = None
            i = 0
            if child.label == "EXPR_LIST":
               for subchild in child.children:
                   if subchild.label == "EXPR":
                       val, typeOfVar, op = EXPRESSION(subchild, symbolTable, intLitTable, output, idStr, i, True, typeOfVar, name, NG, JG, None, None)
                       returnVal = None
		       i = 0
                       while i < len(funcReturnVars):
                           if curMeth in funcReturnVars[i][0]:
                               returnVal = funcReturnVars[i][1]
                               break;
                           i = i + 1
                       print(returnVal + "######################################################")
                       funcReturns.append([curMeth, val, typeOfVar])
                       
                       if(typeOfVar == "string"):
                           if(val[0] == "\""):
		                assignStringLit(tree, symbolTable, output, returnVal, val)
                           else:
                                assignStringVar(tree, symbolTable, output, val, returnVal)
                       if(typeOfVar == "int"):
                           if(val.isdigit()):
                               assignIntLit(tree, symbolTable, output, returnVal, val)
                           else: 
                               assignVariable(tree, symbolTable, output, returnVal, val)
                       if(typeOfVar == "bool"):
                           if(val == "True" or val == "False"):
                               assignBoolLit(tree, symbolTable,output, returnVal, val)
                           else:
                               assignBoolVar(tree, symbolTable,output, returnVal, val)
                       if(typeOfVar == "pointer"):
                           assignPointerVal(tree, symbolTable, output, returnVal, val)
    else:
        print("UNKNOWN")
        print(tree.children[0].label)

def EXPRESSION(tree, symbolTable, intLitTable, output, idStr, i, write, typeOfVar, name, NG, JG, jumpName, jumpName2):
    global count
    global labelGen
    global variablesWritten
    op = None
    val = None
    val2 = None
    valType = None
    idStrType = typeOfVar
    j = 0
    prevOp = None
   
    for child in tree.children:
        if (child.label == "STRINGLIT"):
            j = 0
            v = None
            typeOfVar = "string"
            while (j < len(intLitTable)):
                if (count == intLitTable[j][0]):
                    v = intLitTable[j][1]
                    count = count + 1
                    break
                j = j + 1
            return v, typeOfVar, None
        elif (child.label == "PRIMARY"):
            val2, idStr, j, op, typeOfVar, varWritten = PRIMARY(child, symbolTable, intLitTable, output, idStr, i, write, typeOfVar, op, name, NG, JG, jumpName, jumpName2) 
            if (op != None or prevOp != None):
                idStr = next(NG)
                print(idStrType)
                if (op == "PLUS" or prevOp == "PLUS"):
                    if (idStrType != "int" and idStrType != "pointer"  and not write):
                        raise ParserError("SemaAntic Error: Can't assign result of logical expression to " + idStrType + "type")
                    if (typeOfVar != "int" and typeOfVar !="pointer"):
                        raise ParserError("Semantic Error: Can't use PLUS on variable of " +typeOfVar + " type")
                    
                    if (valType != "int" and valType != "pointer"):
                        raise ParserError("Semantic Error: Can't use PLUS on variable of " +valType + " type") 
                    infixAdd(tree, symbolTable, output, idStr, val, val2, typeOfVar, valType)
                    writeVarAtTop(output, idStr)
                elif (op == "MINUS" or prevOp == "MINUS"):
                    if (idStrType != "int" and idStrType != "pointer" and not write):
                        raise ParserError("Semantic Error: Can't assign result of logical expression to " + idStrType + "type") 
                    if (typeOfVar != "int" and typeOfVar != "pointer"):
                        raise ParserError("Semantic Error: Can't use MINUS on variable of " +typeOfVar + " type")
                    if (valType != "int" and valType != "pointer"):
                        raise ParserError("Semantic Error: Can't use MINUS on variable of " +valType + " type")
                    infixSub(tree, symbolTable, output, idStr, val, val2, typeOfVar, valType)
                    writeVarAtTop(output, idStr)
                elif (op == "MULTI" or prevOp == "MULTI"):
                    if (idStrType != "int" and idStrType != "pointer" and not write):
                        raise ParserError("Semantic Error: Can't assign result of logical expression to " + idStrType + "type")
                    if (typeOfVar != "int" and typeOfVar != "pointer"):
                        raise ParserError("Semantic Error: Can't use MULTI on variable of " +typeOfVar + " type")
                    if (valType != "int" and valType != "pointer"):
                        raise ParserError("Semantic Error: Can't use MULTI on variable of " +valType + " type")
                    infixMult(tree, symbolTable, output, idStr, val, val2, typeOfVar, valType)
                    writeVarAtTop(output, idStr)
                elif (op == "DIV" or prevOp == "DIV"):
                    if (idStrType != "int" and idStrType != "pointer" and not write):
                        raise ParserError("Semantic Error: Can't assign result of logical expression to " + idStrType + "type")
                    if (typeOfVar != "int" and typeOfVar != "pointer"):
                        raise ParserError("Semantic Error: Can't use DIV on variable of " +typeOfVar + " type")
                    if (valType != "int" and valType != "pointer"):
                        raise ParserError("Semantic Error: Can't use DIV on variable of " +valType + " type")
                    infixDiv(tree, symbolTable, output, idStr, val, val2, typeOfVar, valType)
                    writeVarAtTop(output, idStr)
                elif (op == "MOD" or  prevOp == "MOD"):
                    if (idStrType != "int" and idStrType != "pointer" and not write):
                        raise ParserError("Semantic Error: Can't assign result of logical expression to " + idStrType + "type")
                    if (typeOfVar != "int" and typeOfVar != "pointer"):
                        raise ParserError("Semantic Error: Can't use MOD on variable of " +typeOfVar + " type")
                    if (valType != "int" and valType != "pointer"):
                        raise ParserError("Semantic Error: Can't use MOD on variable of " +valType + " type")
                    infixRem(tree, symbolTable, output, idStr, val, val2, typeOfVar, valType)
                    writeVarAtTop(output, idStr)
                elif (op == "LESSEQUAL" or prevOp == "LESSEQUAL"):
                    if (idStrType != "bool" and not write):
                        raise ParserError("Semantic Error: Can't assign result of boolean expression to " + idStrType + " type")
                    if (typeOfVar != "int"):
                        raise ParserError("Semantic Error: Can't perform Boolean operation on " + typeOfVar + " type")
                    if (valType != "int"):
                        raise ParserError("Semantic Error: Can't perform Boolean operation on " +valType + " type")
                    lessThanEqual(tree, symbolTable, output, val, val2, idStr, jumpName, jumpName2) 
                    jumpName = next(JG)
                    jumpName2 = next(JG)
                    
                    writeVarAtTop(output, idStr)
                    val2 = val <= val2
                    typeOfVar = "bool"

                elif (op == "GREATEQUAL" or prevOp == "GREATEQUAL"):
                    if (idStrType != "bool" and not write):
                        raise ParserError("Semantic Error: Can't assign result of boolean expression to " + idStrType + " type")
                    if (typeOfVar != "int"):
                        raise ParserError("Semantic Error: Can't perform Boolean operation on " + typeOfVar + " type")
                    if (valType != "int"):
                        raise ParserError("Semantic Error: Can't perform Boolean operation on " +valType + " type")
                    greaterThanEqual(tree, symbolTable, output, val2, val, idStr, jumpName, jumpName2)
                    jumpName = next(JG)
                    jumpName2 = next(JG)
                    writeVarAtTop(output, idStr)
                    val2 = val >= val2
                    typeOfVar = "bool"

                elif (op == "EQUAL" or prevOp == "EQUAL"):
                    if (idStrType != "bool" and not write):
                        raise ParserError("Semantic Error: Can't assign result of boolean expression to " + idStrType + " type")
                    if (typeOfVar != "int"):
                        raise ParserError("Semantic Error: Can't perform Boolean operation on " + typeOfVar + " type")
                    if (valType != "int"):
                        raise ParserError("Semantic Error: Can't perform Boolean operation on " +valType + " type")
                    equal(tree, symbolTable, output, val, val2, idStr, jumpName, jumpName2)
                    jumpName = next(JG)
                    jumpName2 = next(JG)
                    writeVarAtTop(output, idStr)

                    val2 = val == val2
                    typeOfVar = "bool"

                elif (op == "NOTEQUAL" or prevOp == "NOTEQUAL"):
                    if (idStrType != "bool" and not write):
                        raise ParserError("Semantic Error: Can't assign result of boolean expression to " + idStrType + " type")
                    if (typeOfVar != valType):
                        raise ParserError("Semantic Error: Can't perform Boolean operation on different types")
                    
                    notEqual(tree, symbolTable, output, val, val2, idStr, jumpName, jumpName2)
                    jumpName = next(JG)
                    jumpName2 = next(JG)
                    writeVarAtTop(output, idStr)

                    val2 = val != val2
                    typeOfVar = "bool"

                elif (op == "LESS" or prevOp == "LESS"):
                    jumpName = next(labelGen)
                    jumpName2 = next(labelGen)
                    if (idStrType != "bool" and not write):
                        raise ParserError("Semantic Error: Can't assign result of boolean expression to " + idStrType + " type")
                    if (typeOfVar != "int"):
                        raise ParserError("Semantic Error: Can't perform Boolean operation on " + typeOfVar + " type")
                    if (valType != "int"):
                        raise ParserError("Semantic Error: Can't perform Boolean operation on " +valType + " type")
                    lessThan(tree, symbolTable, output, val, val2, idStr, jumpName, jumpName2)

                    writeVarAtTop(output, idStr)

                    val2 = val < val2
                    typeOfVar = "bool"
                elif (op == "GREAT" or prevOp == "GREAT"):
                    jumpName = next(labelGen)
                    jumpName2 = next(labelGen)
                    if (idStrType != "bool" and not write):
                        raise ParserError("Semantic Error: Can't assign result of boolean expression to " + idStrType + " type")
                    if (typeOfVar != "int"):
                        raise ParserError("Semantic Error: Can't perform Boolean operation on " + typeOfVar + " type")
                    if (valType != "int"):
                        raise ParserError("Semantic Error: Can't perform Boolean operation on " +valType + " type")
                    greaterThan(tree, symbolTable, output, val2, val, idStr, jumpName, jumpName2) 
                    writeVarAtTop(output, idStr)             

                    val2 = val > val2
                    typeOfVar = "bool"
  
                elif (op == "AND" or prevOp == "AND"):
                    if (idStrType != "bool" and not write):
                        raise ParserError("Semantic Error: Can't assign result of boolean expression to " + idStrType + "type")
                    if (typeOfVar != "bool" or valType != "bool"):
                        raise ParserError("Semantic Error: Can't use AND on variable of " + typeOfVar + " type")
                    if ((val == "True" or val == "False") and (val2 == "True" or val2 == "False")):
                        andTwoLit(tree, symbolTable, output, val, val2, idStr)
                    elif((val == "True" or val == "False" or val2 == "True" or val2 == "False")):
                        if (val == "True" or val == "False"):
                            andOneVar(tree, symbolTable, output, val2, val, idStr)
                        else:
                            andOneVar(tree, symbolTable, output, val, val2, idStr)
                    else:
                        andTwoVar(tree, symbolTable, output, val, val2, idStr)
                    writeVarAtTop(output, idStr)
                elif (op == "OR" or prevOp == "OR"):
                    if (idStrType != "bool" and not write):
                        raise ParserError("Semantic Error: Can't assign result of boolean expression to " + idStrType + "type")
                    if (typeOfVar != "bool" or valType != "bool"):
                        raise ParserError("Semantic Error: Can't use OR on variable of " + typeOfVar + " type")
                    if ((val == "True" or val == "False") and (val2 == "True" or val2 == "False")):
                        orTwoLit(tree, symbolTable, output, val, val2, idStr)
                    elif((val == "True" or val == "False" or val2 == "True" or val2 == "False")):
                        if (val == "True" or val == "False"):
                            orOneVar(tree, symbolTable, output, val2, val, idStr)
                        else:
                            orOneVar(tree, symbolTable, output, val, val2, idStr)
                    else:
                        orTwoVar(tree, symbolTable, output, val, val2, idStr)
                    writeVarAtTop(output, idStr)
                if (write):
                    val = idStr
                    valType = typeOfVar
                    op = None
                else:
                    val = idStr
                    valType = idStrType
                    op = None
                    val2 = None
            else:
                if not write:
                    pass
                    # check this in assignment in statement?
                    #if (idStrType != typeOfVar):
                    #   raise ParserError("Semantic Error: Can't assign type of " + typeOfVar + " to " + idStrType)
                # need to check assignemnet
                
                val = val2
                valType = typeOfVar
          
                if (write):
                    idStrType = valType
        elif (child.label in {'PLUS', 'MINUS', 'MULTI', 'DIV', 'MOD', 'GREATEQUAL', 'LESSEQUAL', 'EQUAL', 'NOTEQUAL', 'GREAT', 'LESS', 'AND', 'OR', 'NOT'}):
            op = child.label
            prevOp = op
        
    return val, valType,  op

def PRIMARY(tree, symbolTable, intLitTable, output, idStr, i, write, typeOfVar, op, name, NG, JG, jumpName, jumpName2):
    global count
    global variablesWritten
   
    val = None
    v = None
    j = 0
    negate = False
    notT = False
    isFunc = False;
    varWritten = False
    methName = None
    passByValue = False
    for child in tree.children:
        name = next(NG)
        print("CHILD")
        if child is not None:
            print("NOT NONE")
        if (child is None):
            #handle this later
            print("NONE")
        elif (child.label == "EXPR"):
            idStr = name
            val, typeOfVar, op = EXPRESSION(child, symbolTable, intLitTable, output, idStr, i, write, typeOfVar, name, NG, JG, jumpName, jumpName2)
	    notVar(tree, symbolTable, output, val, val)
        elif (child.label == "IDENT"):
            if(isFunc):
                j = 0;
                while j < len(symbolTable):
                    if(count in symbolTable[j][1]):
                        methName = symbolTable[j][0]
                        count = count + 1;
                        break;
                    j = j + 1
                writeFuncCall(methName, output);
            else:
                idStr, i, typeOfVar = IDENT(child, symbolTable, intLitTable, output, False)
                if (symbolTable[i][2] != True and methName == "main"):
                    raise ParserError("Semantic Error: Unitialized variable");
                typeOfVar = symbolTable[i][3]
                val = symbolTable[i][0]
                if (negate):
                    infixSub(tree, symbolTable, output, idStr, "0", val)
	
                    writeVarAtTop(output, idStr)
                    val = idStr
                    idStr = name
                    varWritten = True
                if (notT):
                    notLit(tree, symbolTable, output, val, idStr)
                    writeVarAtTop(output, idStr)
                    val = idStr
                    typeOfVar = "bool"
                    varWritten = True
        elif (child.label == "INTLIT"):
            j = 0
            typeOfVar = "int"
            while (j < len(intLitTable)):
                if (count == intLitTable[j][0]):
                    val = intLitTable[j][1]
                    count = count + 1
                    break
                j = j + 1
            if (negate):
                infixSub(tree, symbolTable, output, idStr, "0", val)
                #writeVarAtTop(output, idStr)

                val = idStr
                idStr = name
                varWritten = True
            return val, idStr, j, op, typeOfVar, varWritten
        elif (child.label == "BOOLLIT"):
            i = 0
            typeOfVar = "bool"
            while (i < len(intLitTable)):
                if (count == intLitTable[i][0]):
                    val = intLitTable[i][1]
                    count = count + 1
                    break
                i = i + 1
            if (notT):
                if(idStr == None):
                    idStr = next(NG)
                notLit(tree, symbolTable, output, val, idStr)
                outputFile = open(output, 'r')
                contents = outputFile.readlines()
                outputFile.close()
                contents.insert(1, idStr+": .word 0\n")
                outputFile = open(output, 'w+')
                contents = "".join(contents)
                outputFile.write(contents)
                variablesWritten.append(idStr)
                outputFile.close();
                val = idStr
                typeOfVar = "bool"
                varWritten = True
            return val, idStr, j, op, typeOfVar, varWritten
        elif (child.label == "MINUS"):
            negate = True
        elif (child.label == "NOT"):
            notT = True 
        elif (child.label == "FUNC"):
            isFunc = True;
        elif (child.label == "FUNCEND"):
            isFunc = False; 
            idStr = "i"
            val = "i"
            typeOfVar = "int"
            j = 0
            while j < len(funcReturns):
                if(methName in funcReturns[j][0]):
                    #val = funcReturns[j][1]
                    #idStr = funcReturns[j][1]
                    typeOfVar = funcReturns[j][2]
		    break;
                j = j + 1
            j = 0
            while j < len(funcReturnVars):
                if(methName in funcReturnVars[j][0]):
                    val = funcReturnVars[j][1]
                    idStr = funcReturnVars[j][1]
                    #typeOfVar = funcReturns[j][2]
		    break;
                j = j + 1
        #add something below for the end function varible to make isFunc falsea
        elif child.label == "AMP":
            print("FOUND AN AMP")
            passByValue = True;
        elif child.label == "POINTER":
            passByValue = True;
        else:
            print("UNKNOWN " +child.label)
    if passByValue:
        typeOfVar = "pointer"
    return val, idStr, i, op, typeOfVar, varWritten

def IDENT(tree, symbolTable, intLitTable, output, init):
    global count, declaredVars, curMeth
    idStr = None
    i = 0
    while (i < len(symbolTable)):
        if (count in symbolTable[i][1]):
            idStr = symbolTable[i][0]
            count = count + 1
            break
        i = i + 1
    print(count)
    if (not symbolTable[i][4]):
        symbolTable[i][4] = init
    if symbolTable[i][4] != True:
        raise ParserError("Semantic Error: Variable not declared")
        
    ##########################################
    if init:
        if idStr in declaredVars:
         
            if(curMeth is not None and symbolTable[i][5] is "global"):
                idStr = idStr + curMeth;
                if(symbolTable[i][3] == "string"):
                    writeStringAtTop(output, idStr)
                else:
                    writeVarAtTop(output, idStr)
                
                #find count of next function definition
                j = 0
                nextMethCount = None;
                while j < len(symbolTable):
                    if(symbolTable[j][3].endswith("Func")):
                        definition = symbolTable[j][1][0]
                        if(nextMethCount is None and definition > count):
                            nextMethCount = definition
                        elif nextMethCount is not None and definition < nextMethCount and definition > count:
                            nextMethCount = definition
                    j = j + 1
                
                #add all elements of [i[[1] between count and nextMethCount to a new set
                j = 0; 
                newList = [];
                while j<len(symbolTable[i][1]):
                    value = symbolTable[i][1][j]
                    if(value >= count and value < nextMethCount):
                        symbolTable[i][1].remove(value)
                        newList.append(value)
                        j = j - 1
                    elif(nextMethCount is None and value >= count):
                        symbolTable[i][1].remove(value)
                        newList.append(value)
                        j = j - 1
                    j = j + 1
                
                symbolTable.append([idStr, newList, False, symbolTable[i][3], True, "local"])
            else:
                raise ParserError("Semantic Error: Duplicate variable")
        declaredVars.append(idStr)
    ###########################################
    return idStr, i, symbolTable[i][3]

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
            idStr, i, typeOfVar = IDENT(tree, symbolTable, intLitTable, output, init)
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

def writeStringAtTop(output, idStr):
    global variablesWritten
    if (idStr not in variablesWritten):
        outputFile = open(output, 'r')
        contents = outputFile.readlines()
        outputFile.close()
        contents.insert(1, idStr+": .space 64\n")
        outputFile = open(output, 'w+')
        contents = "".join(contents)
        variablesWritten.append(idStr)
        outputFile.write(contents)

def findValue(symbolTable, intLitTable):
    global count
    i = 0
    v = None
    while(i < len(symbolTable)):
        if (count in symbolTable[i][1]):
            if (symbolTable[i][2] == False):
                raise ParserError("Semantic Error: use of variable before declaration")
            v = symbolTable[i][0]
            symbolTable[i][2] = True
            break
        i = i + 1
    if v == None:
        i = 0
        while (i < len(intLitTable)):
             if (count == intLitTable[i][0]):
                 v = intLitTable[i][1]
                 break
             i = i + 1
    count = count + 1
    return v, i

def findLHS(symbolTable, intLitTable):
    global count
    i2 = 0
    v = None
    while (i2 < len(symbolTable)):
        if (count in symbolTable[i2][1]):
            # check to see if init
            if (symbolTable[i2][2] == False):
                raise ParserError("Semantic Error: Use of variable before declaration")
            v = symbolTable[i2][0]
            break
        i2 = i2 + 1
    i2 = 0
    if v == None:
        while (i2 < len(intLitTable)):
            if (count == intLitTable[i2][0]):
                v = intLitTable[i2][1]
                break
            i2 = i2 + 1
    count = count + 1
    return v, i2

def extend(tree, symbolTable, intLitTable, output, ident, v, write):
    global count
    op = 1
    while ((op < len(tree.children)) & (tree.children[op].label in {"PLUS", "MINUS"})):
        i = 0
        v2 = None
        if (tree.label == "EXPR"):
            pass
        else: 
            while (i < len(symbolTable)):
                if (count in symbolTable[i][1]):
                    if (symbolTable[i][2] == False):
                        raise ParserError("Semantic Error: use of variable before declaration")
                    v2 = symbolTable[i][0]
                    break
                i = i + 1
            if v2 == None: 
                i = 0
                while (i < len(intLitTable)):
                    if (count == intLitTable[i][0]):
                        v2 = intLitTable[i][1]
                        break
                    i = i + 1
            count = count + 1
            if (tree.children[op].label == "PLUS"):
                infixAdd(tree, symbolTable, output, ident, v, v2)
            else:
                infixSub(tree, symbolTable, output, ident, v, v2)
            if (write):
                v = "dummy"
            else:
                v = ident
            op = op + 2
            if (op >= len(tree.children)):
                break
        return

def READ(tree, symbolTable, output, readID):
    with open(output, "a") as outputFile:
        outputFile.write("\nli $v0, 5\nsyscall\nla $t0, " + readID + "\nsw $v0, 0($t0)\n")

def WRITEVal(tree, symbolTable, output, writeId):
    with open(output,"a") as outputFile:
        outputFile.write("\nli $v0,1\nlw $a0," + writeId + "\nsyscall\n")

def WRITEInt(tree, symbolTable, output, writeId):
     with open(output,"a") as outputFile:
        outputFile.write("\nli $v0,1\nli $a0," + writeId + "\nsyscall\n")
def printPointer(output, writeId):
     with open(output, "a") as outputFile:
        outputFile.write("\nli $v0,1\nlw $t0, "+writeId+"\n lw $a0, 0($t0)\nsyscall\n")

def WRITEstring(tree, symbolTable, output, writeId):
     with open(output,"a") as outputFile:
        print("WRITE STRING LIT "+writeId)
        outputFile.write("\nla $t0 "+writeId+"\nmove $a0, $t0\nli $v0,4\nsyscall\n")

def assignIntLit(tree, symbolTable, output, ident, value):
    with open(output,"a") as outputFile:
        outputFile.write("\nli $t0,"+value+"\nla $t1,"+ident+"\nsw $t0, 0($t1)\n")

def assignVariable(tree, symbolTable, output, ident1, ident2):
    with open(output,"a") as outputFile:
        outputFile.write("\nla $t0,"+ident2+"\nla $t1,"+ident1+"\nlw $t2, 0($t0)\nsw $t2, 0($t1)\n")

def assignPointerRef(tree, symbolTable, output, ident1, ident2):
    with open(output,"a") as outputFile:
        outputFile.write("\nla $t0,"+ident2+"\nla $t1,"+ident1+"\nla $t2, 0($t0)\nsw $t2, 0($t1)\n")

def assignPointerVal(tree, symbolTable, output, ident1, ident2):
    with open(output,"a") as outputFile:
        outputFile.write("\n#In AssignPointerVal()")
        if(ident2.isdigit()):
            outputFile.write("\nli $t0, "+ident2+"\nlw $t1, "+ident1)
        else:
            outputFile.write("\nlw $t0, "+ident2+"\nlw $t1, "+ident1)
        outputFile.write("\nsw $t0, 0($t1)\n")

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
        print("ASSIGN STRING LIT "+value)
        printString = ""
        outputFile.write("\nla $s0, "+variableName+"\n")
        for char in value:
            if char in {"'"}:
                char = "\\"+char
            if char not in {"\""}:
                #print(char)
                #outputFile.write("\nli $t0, '" + char + "'\nsb $t0, ($s0)\naddi $s0, $s0, 1\n")
                printString += "\nli $t0, '" + char + "'\nsb $t0, ($s0)\naddi $s0, $s0, 1\n"
        outputFile.write(printString)
def assignStringVar(tree, symbolTable, output, ident1, ident2):
    with open(output,"a") as outputFile:
        outputFile.write("\nla $s0, "+ident1+ "\nla $s1, "+ident2)
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
    print("NOTLIT")
    if(lit == "True"):
        value = "1"
    else:
        value = "0"
    with open(output,"a") as outputFile:
        outputFile.write("\nli $t1, "+value+"\nli $t2, 1\nxor $t0, $t1, $t2\nsw $t0, "+result+"\n")

def notVar(tree, sumbolTable, output, var, result):
    print("NOTVAR")
    with open(output,"a") as outputFile:
        outputFile.write("\nlw $t1, "+var+"\nli $t2, 1\nxor $t0, $t1, $t2\nsw $t0, "+result+"\n")

#Math
def infixAdd(tree, symbolTable, output, ident1, ident2, ident3, type2, type3):
    with open(output,"a") as outputFile:
        if(ident2.isdigit()):
            outputFile.write("\nli $s0, "+ident2+"\nla $t1, 0($s0)\n")
        elif(type3 == "pointer"):
            outputFile.write("\nlw $s0, "+ident2+"\nlw $t1, 0($s0)\n")
        else:
            outputFile.write("\nla $s0, "+ident2+"\nlw $t1, 0($s0)\n")
        if(ident3.isdigit()):
            outputFile.write("li $s0, "+ident3+"\nla $t2, 0($s0)\n")
        elif(type2 == "pointer"):
            outputFile.write("lw $s0, "+ident3+"\nlw $t2, 0($s0)\n")
        else:
            outputFile.write("la $s0, "+ident3+"\nlw $t2, 0($s0)\n")

        outputFile.write("add $t0, $t1, $t2\nla $s0,"+ident1+"\nsw $t0, 0($s0)\n")

def infixSub(tree, symbolTable, output, ident1, ident2, ident3, type2, type3):
    with open(output,"a") as outputFile:
        if(ident2.isdigit()):
            outputFile.write("\nli $s0, "+ident2+"\nla $t1, 0($s0)\n")
        elif(type3 == "pointer"):
            outputFile.write("\nlw $s0, "+ident2+"\nlw $t1, 0($s0)\n")
        else:
            outputFile.write("\nla $s0, "+ident2+"\nlw $t1, 0($s0)\n")
        if(ident3.isdigit()):
            outputFile.write("li $s0, "+ident3+"\nla $t2, 0($s0)\n")
        elif(type2 == "pointer"):
            outputFile.write("lw $s0, "+ident3+"\nlw $t2, 0($s0)\n")
        else:
            outputFile.write("la $s0, "+ident3+"\nlw $t2, 0($s0)\n")

        outputFile.write("sub $t0, $t1, $t2\nla $s0,"+ident1+"\nsw $t0, 0($s0)\n")

def infixMult(tree, symbolTable, output, ident1, ident2, ident3, type2, type3):
    with open(output,"a") as outputFile:
        if(ident2.isdigit()):
            outputFile.write("\nli $s0, "+ident2+"\nla $t1, 0($s0)\n")
        elif(type3 == "pointer"):
            outputFile.write("\nlw $s0, "+ident2+"\nlw $t1, 0($s0)\n")
        else:
            outputFile.write("\nla $s0, "+ident2+"\nlw $t1, 0($s0)\n")
        if(ident3.isdigit()):
            outputFile.write("li $s0, "+ident3+"\nla $t2, 0($s0)\n")
        elif(type2 == "pointer"):
            outputFile.write("lw $s0, "+ident3+"\nlw $t2, 0($s0)\n")
        else:
            outputFile.write("la $s0, "+ident3+"\nlw $t2, 0($s0)\n")

        outputFile.write("mul $t0, $t1, $t2\nla $s0,"+ident1+"\nsw $t0, 0($s0)\n")

def infixDiv(tree, symbolTable, output, ident1, ident2, ident3, type2, type3):
    with open(output,"a") as outputFile:
        if(ident2.isdigit()):
            outputFile.write("\nli $s0, "+ident2+"\nla $t1, 0($s0)\n")
        elif(type3 == "pointer"):
            outputFile.write("\nlw $s0, "+ident2+"\nlw $t1, 0($s0)\n")
        else:
            outputFile.write("\nla $s0, "+ident2+"\nlw $t1, 0($s0)\n")
        if(ident3.isdigit()):
            outputFile.write("li $s0, "+ident3+"\nla $t2, 0($s0)\n")
        elif(type2 == "pointer"):
            outputFile.write("lw $s0, "+ident3+"\nlw $t2, 0($s0)\n")
        else:
            outputFile.write("la $s0, "+ident3+"\nlw $t2, 0($s0)\n")

        outputFile.write("div $t0, $t1, $t2\nla $s0,"+ident1+"\nsw $t0, 0($s0)\n")

def infixRem(tree, symbolTable, output, ident1, ident2, ident3, type2, type3):
    with open(output,"a") as outputFile:
        if(ident2.isdigit()):
            outputFile.write("\nli $s0, "+ident2+"\nla $t1, 0($s0)\n")
        elif(type3 == "pointer"):
            outputFile.write("\nlw $s0, "+ident2+"\nlw $t1, 0($s0)\n")
        else:
            outputFile.write("\nla $s0, "+ident2+"\nlw $t1, 0($s0)\n")
        if(ident3.isdigit()):
            outputFile.write("li $s0, "+ident3+"\nla $t2, 0($s0)\n")
        elif(type2 == "pointer"):
            outputFile.write("lw $s0, "+ident3+"\nlw $t2, 0($s0)\n")
        else:
            outputFile.write("la $s0, "+ident3+"\nlw $t2, 0($s0)\n")

        outputFile.write("rem $t0, $t1, $t2\nla $s0,"+ident1+"\nsw $t0, 0($s0)\n")

def equal(tree, symbolTable, output, ident1, ident2, ident3,label1, label2):
    with open(output,"a") as outputFile:
        outputFile.write("#EQUAL")
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
	
        outputFile.write("bgt $t0, $t1, "+label1+"\nli $t2, 0\nsw $t2, "+ident3+"\nj "+label2)	
        outputFile.write("\n"+label1+":\nli $t2, 1\nsw $t2, "+ident3+"\n"+label2+":\n")

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
	 
        outputFile.write("bge $t0, $t1, "+label1+"\nli $t2, 0\nsw $t2, "+ident3+"\nj "+label2)	
        outputFile.write("\n"+label1+":\nli $t2, 1\nsw $t2, "+ident3+"\n"+label2+":\n")

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
def printWhileBottomLabel(tree, symbolTable, output, labelWhile, exitLabel):
    with open(output, "a") as outputFile:
        outputFile.write("\nj "+labelWhile)
        outputFile.write("\n"+exitLabel+":\n")

def printWhileTopLabel(tree, symbolTable, output, labelWhile):
    with open (output, "a") as outputFile:
        outputFile.write("\n"+labelWhile+":\n")

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

def writeMethHead(methName, output):
    with open(output, "a") as outputFile:
        outputFile.write("\n"+methName + ":\n")
        outputFile.write("addi $sp, $sp, -4")
        outputFile.write("\nsw $ra, 0($sp)")

def writeMethReturn(methName, output):
    with open(output, "a") as outputFile:
        outputFile.write("\nlw $s0, 0($sp)")
        outputFile.write("\naddi $sp, $sp, 4")
        outputFile.write("\njr $s0\n")

def writeMainReturn(output):
    with open(output, "a") as outputFile:
        outputFile.write("\nli $v0, 10\nsyscall\n")
def writeFuncCall(methName, output):
    with open(output, "a") as outputFile: 
        outputFile.write("\njal " +methName+"\n")
def writeNewLine(output):
    with open(output, "a") as outputFile:
        outputFile.write("li $v0,4 \nla $a0, newline\nsyscall\n")       
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