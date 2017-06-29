# Michelle Kojs, Jayson Boubin, John Crabill
# Part 3 - CP 6

"""
Part 6 Grammar:
    <program> -> begin <statement_list> end
    <statement_list> -> <statement>; { , <statement>; }
    <statement> -> <assign> | read(<id_list>) | write(<expr_list>)
    <assign> -> <ident> := <expression> | <init>
    <init> -> INTLIT <ident> | BOOLLIT <ident> | STRINGLIT <ident>
    <id_list> -> <ident> {, <ident> }
    <expr_list> -> <expression> {, <expression>}
    <ident> -> ID
    <op> -> + | - | * | % | / | <= | >= | == | != | < | > | and | or | not
    <expression> -> <primary> {<op> <primary>} | STRINGLIT
    <primary> -> (<expression>) | <ident> | INTLIT | BOOLLIT | MINUS <ident> | MINUS INTLIT | not BOOLLIT | not <ident>

Part 7 Grammar:
    <program> -> begin <statement_list> end
    <statement_list> -> <statement> { , <statement> }
    <statement> -> <assign>; | read(<id_list>); | write(<expr_list>); | while <expression> begin <statement_list> end | if <expression> then begin <statement_list> end { else begin <statement_list> end}
    <assign> -> <ident> := <expression> | <init>
    <init> -> INTLIT <ident> | BOOLLIT <ident> | STRINGLIT <ident>
    <id_list> -> <ident> {, <ident> }
    <expr_list> -> <expression> {, <expression>}
    <ident> -> ID
    <op> -> + | - | * | % | / | <= | >= | == | != | < | > | and | or | not
    <expression> -> <primary> {<op> <primary>} | STRINGLIT
    <primary> -> (<expression>) | <ident> | INTLIT | BOOLLIT | MINUS <ident> | MINUS INTLIT | not BOOLLIT | not <ident>

symbolTable -> holds variables
[pattern, count[], ifInitialized, type, ifDeclared]

valLitTable -> holds intlits, boollits, and stringlits
[count, val, type]

"""
import lexer as Lex
from tree import tree

count = 0
symbolTable = []
valLitTable = []

class ParserError(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg


#######################################
# Parsing code

def parser(source_file, token_file):
    """
    source_file: A program written in the ML langauge.
    returns True if the code is syntactically correct.
    Throws a ParserError otherwise.
    """
    count = 0    
    G = Lex.lexer(source_file, token_file)
    current, t  = PROGRAM(next(G), G)
    if (current.name == "STOP"):
        return t, symbolTable, valLitTable;
    elif (current.name != "STOP"):
        raise ParserError("Syntax error: Extra code after END");

def PROGRAM(current, G):
# <program> -> begin <statement_list> end
    children = []
    while (True):
        if current.name == 'BEGIN':
            children.append(tree("BEGIN"))
            current, child = STATEMENT_LIST(next(G), G)
            children.append(child)
        if current.name == "STOP":
            raise ParserError("Syntax error: Missing END")
        if current.name == 'END':
            children.append(tree("END"))
            return next(G), tree("PROGRAM", children)
        if current.name not in {'BEGIN', 'END'}:
            raise ParserError("Syntax error: in PROGRAM: missing begin or end")

def STATEMENT_LIST(current, G):
#  <statement_list> -> <statement>; { <statement; } 
    children = []
    while (True):
        current, child = STATEMENT(current, G)
        children.append(child)
     #   if current.name != 'SEMICOLON':
     #       raise ParserError("Syntax error: Missing ; in STATEMENT_LIST")
#        current = next(G)
        if (current.name == "STOP"):
            break;
        if (current.name in {"BEGIN", "END"}):
            break;
        #current = next(G)
    return current, tree("STATEMENT_LIST", children)

def STATEMENT(current, G):
#  <statement> -> <assign> | read( <id_list> ) | write( <expr_list> )
# <statement> -> <assign> | read(<id_list>) | write(<expr_list>) | while <expression> <program> | if <expression> then <program> { else <program>}

#<statement> -> <assign> | read(<id_list>) | write(<expr_list>) | while <expression> begin <statement_list> end | if <expression> then begin <statement_list> end { else begin <statement_list> end}
    children = []
    if current.name == 'READ':
        current = next(G)
        children.append(tree("READ"))
        if current.name != "LPAREN":
            raise ParserError("Syntax error: missing opening (")
        current, child = ID_LIST(next(G), G)
        children.append(child)
        if (current.name != "RPAREN"):
            raise ParserError("Syntax error: missing closing )")
        current = next(G)
        if current.name != 'SEMICOLON':
            raise ParserError("Syntax error: Missing ; in STATEMENT_LIST")
        return next(G), tree("STATEMENT", children)
    elif current.name == "WRITE":
        current = next(G)
        children.append(tree("WRITE"))
        if current.name != "LPAREN":
            raise ParserError("Syntax error: missing opening (")
        current, child = EXPR_LIST(next(G), G)
        children.append(child)
        if (current.name != "RPAREN"):
            raise ParserError("Syntax error: missing closing )")
        current = next(G)
        if current.name != 'SEMICOLON':
            raise ParserError("Syntax error: Missing ; in STATEMENT_LIST")
        return next(G), tree("STATEMENT", children)
    elif current.name == "WHILE":
        children.append(tree("WHILE"))
        current, child = EXPRESSION(next(G), G)
        children.append(child)
        if not current.name == "BEGIN":
            raise ParserError("Syntax error: missing begin in WHILE clause")
        current = next(G)
        current, child = STATEMENT_LIST(current, G)
        children.append(child)
        if not current.name == "END":
            raise ParserError("Syntax error: missing end in WHILE clause")
        return next(G), tree("STATEMENT", children)
    elif current.name == "IF":
        children.append(tree("IF"))
        current, child = EXPRESSION(next(G), G)
        children.append(child)
        if not current.name == "THEN":
            raise ParserError("Syntax error: missing then in IF Clause")
        current = next(G)
        if not current.name == "BEGIN":
            raise ParserError("Syntax error: missing begin in IF clause")
        current = next(G)
        current, child = STATEMENT_LIST(current, G)
        children.append(child)
        if not current.name == "END":
            raise ParserError("Syntax error: missing end in IF clause")
        current = next(G)
        if current.name == "ELSE":
            children.append(tree("ELSE"))
            current = next(G)
            if not current.name == "BEGIN":
                raise ParserError("Syntax error: missing begin in ELSE clause")
            current = next(G)
            current, child = STATEMENT_LIST(current, G)
            children.append(child)
            if not current.name == "END":
                raise ParserError("Syntax error: missing end in ELSE clause")
            return next(G), tree("STATEMENT", children)
        return current, tree("STATEMENT", children)
    elif current.name == "METH":
        children.append(tree("METH"))
        current, child = METHOD(next(G), G)
        children.append(child)
        if (not current.name == "METHEND"):
            raise ParserError("Syntax error: missing end of method")
        children.append(tree("METHEND"))
        return next(G), tree("STATEMENT", children)
    elif current.name == "FUNC":
        children.append(tree("FUNC"))
        current, child = IDENT(next(G), G, None)
        children.append(child)
        if current.name != "LPAREN":
            raise ParserError("Syntax error: missing opening (")
        current, child = FUNC_CHOICE(next(G), G)
        children.append(child)
        if (current.name != "RPAREN"):
            raise ParserError("Syntax error: missing closing )")
        current = next(G)
        if not current.name == "FUNCEND":
            raise ParserError("Syntax error: missing func end")
        children.append(tree("FUNCEND"))
        return next(G), tree("STATEMENT", children)
    elif current.name == "RETURN":
        children.append(tree("RETURN"))
        current, child = EXPR_LIST(next(G), G)
        children.append(child)
        if current.name != "SEMICOLON":
            raise ParserError("Syntax error: missing ; in return"  + str(current.name))
        return next(G), tree("STATEMENT", children)
    else:
        current, child = ASSIGN(current, G)
        children.append(child)
       # current = next(G)
        if current.name != 'SEMICOLON':
            raise ParserError("Syntax error: Missing ; in STATEMENT_LIST")
        return next(G), tree("STATEMENT", children)
def METHOD(current, G):
    children = []
    if (current.name == "INTTYPE"):
        children.append(tree("INTTYPEFUNC"))
        current, child = IDENT(next(G), G, "intFunc")
    elif (current.name == "BOOLTYPE"):
        children.append(tree("BOOLTYPEFUNC"))
        current, child = IDENT(next(G), G, "boolFunc")
    elif (current.name == "STRTYPE"):
        children.append(tree("STRTYPEFUNC"))
        current, child = IDENT(next(G), G, "stringFunc")
    elif (current.name == "VOID"):
        children.append(tree("VOIDFUNC"))
        current, child = IDENT(next(G), G, "voidFunc")
    else:
        raise ParserError("Syntax error: invalid type")
    children.append(child)
    if current.name != "LPAREN":
        raise ParserError("Syntax error: missing opening (")
    current, child = INIT_LIST(current, G)
    children.append(child)
    if (current.name != "RPAREN"):
        raise ParserError("Syntax error: missing closing )")
    current = next(G)
    while(True):
        if current.name == "METHEND":
            break;
        current, child = STATEMENT(current, G)
        children.append(child)
    return current, tree("METHOD", children)    

#<init_list> -> <init> {, <init>}
def INIT_LIST(current, G):
    children = []
    while (True):
        current, child = INIT(next(G), G)
        children.append(child)
        if current.name != 'COMMA':
            break;
    return current, tree("INIT_LIST", children)
	
def ASSIGN(current, G):
# <assign> -> <init> := <expression> | <ident> := <expression> | <init>
    children = []
    if (current.name in {"STRTYPE", "INTTYPE", "BOOLTYPE", "POINTTYPE"}):
        # either init or init := expr
        print ("####################### " + current.pattern)
        current, child = INIT(current, G)
        children.append(child)
    else:
        if current.name == "POINTER":
            current = next(G)
        current, child = IDENT(current,G, None)
        children.append(child)
        if (current.name != "ASSIGNOP"):
            raise ParserError("Syntax error: invalid assignment")
    
        current, child = EXPRESSION(next(G),G)
        children.append(child)
    return current, tree("ASSIGNMENT", children)

def INIT(current, G):
# <init> -> INTLIT<ident> | BOOLLLIT <ident> | STRINGLIT <ident>
    children = []
    print("++++++++++++++++++++" + current.pattern)
    if (current.name == "INTTYPE"):
        children.append(tree("INTTYPE"))
        current, child = IDENT(next(G), G, "int")
    elif (current.name == "BOOLTYPE"):
        children.append(tree("BOOLTYPE"))
        current, child = IDENT(next(G), G, "bool")
    elif (current.name == "STRTYPE"):
        children.append(tree("STRTYPE"))
        current, child = IDENT(next(G), G, "string")
    elif (current.name == "POINTTYPE"):
        children.append(tree("POINTTYPE"))
        current, child = IDENT(next(G), G, "pointer")
    elif (current.name == "RPAREN"):
        return current,None
    else:
        print(current.name)
        raise ParserError("Syntax error: invalid type")
    children.append(child)

    return current, tree("INIT", children)

def ID_LIST(current, G):
#  <id_list> -> <ident> {, <ident>}
    children = []
    while (True):
        if current.name == "AMP":
            children.append(tree("AMP"))
            current = next(G)
        current, child = IDENT(current, G, "int")
        children.append(child)
        if current.name != 'COMMA':
            break;
        current = next(G)

    return current, tree("ID_LIST", children)

def EXPR_LIST(current, G):
#  <expr_list> -> <expression> {, <expression>}
    children = []
    while (True):
        current, child = EXPRESSION(current, G)
        children.append(child)
        if current.name != 'COMMA':
            break;
        current = next(G)
    return current, tree("EXPR_LIST", children)

def EXPRESSION(current, G):
#  <expression> -> <primary> {<op> <primary>}
    global count
    children = []
    if (current.name == "STRINGLIT"):
        count = count + 1
        children.append(tree("STRINGLIT"))
        valLitTable.append([count, current.pattern, "string"])
        return next(G), tree("EXPR", children)
    while (True):
        current, child = PRIMARY(current, G)
        children.append(child)
        if (current.name in {'PLUS', 'MINUS', 'MULTI', 'DIV', 'MOD', 'GREATEQUAL', 'LESSEQUAL', 'EQUAL', 'NOTEQUAL', 'GREAT', 'LESS', 'AND', 'OR'}):
            current, child = OP(current,G)
            children.append(child)
        else:
            break;
    return current, tree("EXPR", children)

def PRIMARY(current, G):
# <primary> -> (<expression>) | <ident> | INTLITERAL | BOOLLIT | 
    global count
    children = []
    if current.name == "INTLIT":
        count = count + 1
        children.append(tree("INTLIT"))
        valLitTable.append([count, current.pattern, "int"])
        return next(G), tree("PRIMARY", children)
    elif current.name == "BOOLLIT":
        count = count + 1
        children.append(tree("BOOLLIT"))
        valLitTable.append([count, current.pattern, "bool"])
        return next(G), tree("PRIMARY", children)
    elif current.name == 'LPAREN':
        current, child = EXPRESSION(next(G), G)
        children.append(child)
        if current.name != 'RPAREN':
            raise ParserError("Syntax error: not a matching parenthesis")
        return next(G), tree("PRIMARY", children)
    elif current.name == "MINUS":
#        current, child = OP(current, G)
        children.append(tree("MINUS"))
        current = next(G)
        if current.name == "INTLIT":
            count = count + 1
            children.append(tree("INTLIT"))
            valLitTable.append([count, current.pattern, "int"])
            return next(G), tree("PRIMARY", children)
        elif current.name == "ID":
            current, child = IDENT(current, G, None)
            children.append(child)
            return current, tree("PRIMARY", children)
        raise ParserError("Syntax error: invalid negate expression")
    elif current.name == "NOT":
        #       current, child = OP(current,G)
        children.append(tree("NOT"))
        current = next(G)
        if current.name == "BOOLLIT":
            count = count + 1
            children.append(tree("BOOLLIT"))
            valLitTable.append([count, current.pattern, "bool"])
            return next(G), tree("PRIMARY", children)
        elif current.name == "ID":
            current, child = IDENT(current, G, None)
            children.append(child)
            return current, tree("PRIMARY", children)
        elif current.name == 'LPAREN':
            current, child = EXPRESSION(next(G), G)
            children.append(child)
            if current.name != 'RPAREN':
                raise ParserError("Syntax error: not a matching parenthesis")
            return next(G), tree("PRIMARY", children)
        raise ParserError("Syntax Error: invalid not and boollit expression")
    elif current.name == "AMP":
        children.append(tree("AMP"))
        current = next(G)
        if current.name == "ID":
            current, child = IDENT(current, G, None)
            children.append(child)
            return current, tree("PRIMARY", children)
        raise ParserError("Syntax Error: invalid reference expression")
    elif current.name == "POINTER":
        children.append(tree("POINTER"))
        current = next(G)
        if current.name == "ID":
            current, child = IDENT(current, G, None)
            children.append(child)
            return current, tree("PRIMARY", children)
        raise ParserError("Syntax Error: invalid pointer expression")
    elif current.name == "FUNC":
        children.append(tree("FUNC"))
        current, child = IDENT(next(G), G, None)
        children.append(child)
        if current.name != "LPAREN":
            raise ParserError("Syntax error: missing opening (")
        current, child = FUNC_CHOICE(next(G), G)
        children.append(child)
        if (current.name != "RPAREN"):
            raise ParserError("Syntax error: missing closing )")
        current = next(G)
        if not current.name == "FUNCEND":
            raise ParserError("Syntax error: missing func end")
        children.append(tree("FUNCEND"))
        return next(G), tree("PRIMARY", children)
    else:
        current, child = IDENT(current, G, None)
        children.append(child)
        return current, tree("PRIMARY", children)


def IDENT(current, G, typeOfVar):
    global count
    children = []
    location = []
    inTable = False   
    
    curFunc = "";
    #find current function if there is one    
    i = 0;

    i = count;
    found = False
    while i > 0 and not found:
        for entry in symbolTable:
            print(entry)
            if(i is entry[1][0] and entry[3].endswith("Func")):
                curFunc = entry[0]
                found = True
                break;
        i = i - 1
    print(current.name)
    if current.name == "ID":
        count = count + 1
        if not symbolTable == []: 
            for rec in symbolTable:
                if((rec[3] != None and rec[3].endswith("Func")) and rec[0] == current.pattern):
                    rec[1].append(count)
                    inTable = True;
                ####################################
                elif rec[5] is "local" and rec[0] == current.pattern+ str(curFunc):
                    rec[1].append(count)
                    inTable = True
                elif rec[5] is "global" and rec[0] == current.pattern:
                    rec[1].append(count)
                    inTable = True
        if not inTable:
            if typeOfVar != None and typeOfVar.endswith("Func"):
                ############################################
                symbolTable.append([current.pattern, [count], False, typeOfVar, False, "local"])
            elif typeOfVar != None and curFunc is "":
                symbolTable.append([current.pattern + str(curFunc), [count], False, typeOfVar, False, "global"])
            elif typeOfVar != None:
                symbolTable.append([current.pattern + str(curFunc), [count], False, typeOfVar, False, "local"])
            else:
                ###########################################
                symbolTable.append([current.pattern + str(curFunc), [count], False, typeOfVar, False, "local"])
        children.append(tree("ID"))
        return next(G), tree("IDENT", children)
    #elif current.name == "POINTER":
     ########################make this happen##################################   
    raise ParserError("Syntax error: not an identifier "+current.name)
def OP(current, G):
# <op> -> + | - | * | / | <= | >= | == | < | > | and | not | or
    children = []
    if current.name == "PLUS":       
        return next(G), tree("PLUS")
    elif current.name == "MINUS":
        return next(G), tree("MINUS")
    elif current.name == "MULTI":
        return next(G), tree("MULTI")
    elif current.name == "DIV":
        return next(G), tree("DIV")
    elif current.name == "MOD":
        return next(G), tree("MOD")
    elif current.name == "LESSEQUAL":
        return next(G), tree("LESSEQUAL")
    elif current.name == "GREATEQUAL":
        return next(G), tree("GREATEQUAL")
    elif current.name == "EQUAL":
        return next(G), tree("EQUAL")
    elif current.name == "NOTEQUAL":
        return next(G), tree("NOTEQUAL")
    elif current.name == "LESS":
        return next(G), tree("LESS")  
    elif current.name == "GREAT":
        return next(G), tree("GREAT")
    elif current.name == "AND":
        return next(G), tree("AND")
    elif current.name == "OR":
        return next(G), tree("OR")
    elif current.name == "NOT":
        return next(G), tree("NOT")
    raise ParserError("Syntax error: incorrect syntax, no logical/arithop operator")
	
def FUNC_CHOICE(current, G):
    children = []
    if current.name == "RPAREN":
        return current, None
    else:
        current, child = EXPR_LIST(current, G)
        children.append(child)
        return current, tree("FUNC_CHOICE", children)
                    

