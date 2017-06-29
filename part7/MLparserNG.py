# Michelle Kojs, Jayson Boubin, John Crabill
# Part 3 - CP 6

"""
Grammar:
    <program> -> begin <statement_list> end
    <statement_list> -> <statement> { , <statement> }
    <statement> -> <assign>; | read(<id_list>); | write(<expr_list>); | while <bool1>  begin <statement_list> end | if <bool1> then begin <statement_list> end { else begin <statement_list> end}
    <assign> -> <ident> := <expression> | <init>
    <init> -> INTLIT <ident> | BOOLLIT <ident> | STRINGLIT <ident>
    <id_list> -> <ident> {, <ident> }
    <expr_list> -> <expression> {, <expression>}
    <expression> -> <bool1> | STRINGLIT
    <ident> -> ID
    <bool1> -> <switch> {<logop> <switch>} | lambda
    <switch> -> <exp2> <switch'> <exp2>
    <switch'> -> <= | >= | == | != | < | > | lambda
    <exp2> -> <expr2'> {<op> <expr2'>} | lambda
    <exp2'> -> <primary> {<op2> <primary>} | lambda
    <op> -> + | -
    <op2> -> * | / | %
    <logop> -> or | and
    <primary> -> (<bool1>) | <ident> | INTLIT | BOOLLIT | MINUS <ident> | MINUS INTLIT | not BOOLLIT | not <ident> | MINUS <BOOL1> | NOT <BOOL1>

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
    # <statement_list> -> <statement>; { <statement; } 
    children = []
    while (True):
        current, child = STATEMENT(current, G)
        children.append(child)
        if (current.name == "STOP"):
            break;
        if (current.name in {"BEGIN", "END"}):
            break;
    return current, tree("STATEMENT_LIST", children)

def STATEMENT(current, G):
    # <statement> -> <assign>; | read(id_list); | write(expr_list); | while<bool1> begin <statement_list> end | if <bool1> then begin <statement_list> end {else begin <statement_list> end}
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
        current, child = BOOL1(next(G), G)
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
        current, child = BOOL1(next(G), G)
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
    else:
        current, child = ASSIGN(current, G)
        children.append(child)
        if current.name != 'SEMICOLON':
            raise ParserError("Syntax error: Missing ; in STATEMENT_LIST")
        return next(G), tree("STATEMENT", children)

def ASSIGN(current, G):
    # <assign> -> <ident> := <expression> | <init>
    children = []
    if (current.name in {"STRTYPE", "INTTYPE", "BOOLTYPE"}):
        current, child = INIT(current, G)
        children.append(child)
    else:
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

    if (current.name == "INTTYPE"):
        children.append(tree("INTTYPE"))
        current, child = IDENT(next(G), G, "int")
    elif (current.name == "BOOLTYPE"):
        children.append(tree("BOOLTYPE"))
        current, child = IDENT(next(G), G, "bool")
    elif (current.name == "STRTYPE"):
        children.append(tree("STRTYPE"))
        current, child = IDENT(next(G), G, "string")
    else:
        raise ParserError("Syntax error: invalid type")
    children.append(child)

    return current, tree("INIT", children)

def ID_LIST(current, G):
    # <id_list> -> <ident> {, <ident>}
    children = []
    while (True):
        current, child = IDENT(current, G, "int")
        children.append(child)
        if current.name != 'COMMA':
            break;
        current = next(G)

    return current, tree("ID_LIST", children)

def EXPR_LIST(current, G):
    # <expr_list> -> <expression> {, <expression>}
    children = []
    while (True):
        current, child = EXPRESSION(current, G)
        children.append(child)
        if current.name != 'COMMA':
            break;
        current = next(G)
    return current, tree("EXPR_LIST", children)

def EXPRESSION(current, G):
    # <expression> -> <bool1> | STRINGLIT
    global count
    children = []
    if current.name == "STRINGLIT":
        count = count + 1
        children.append(tree("STRINGLIT"))
        valLitTable.append([count, current.pattern, "string"])
        return next(G), tree("EXPRESSION", children)
    elif current.name in {"LPAREN", "ID", "INTLIT", "BOOLLIT", "MINUS", "NOT"}:
        current, child = BOOL1(current, G)
        children.append(child)
        return current, tree("EXPRESSION", children)
    raise ParserError("invalid in EXPRESSION")

def PRIMARY(current, G):
    #<primary> -> (<bool1>) | <ident> | INTLIT | BOOLLIT | MINUS <ident> | MINUS INTLIT | not BOOLLIT | not <ident>
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
        current, child = BOOL1(next(G), G)
        children.append(child)
        if current.name != 'RPAREN':
            raise ParserError("Syntax error: not a matching parenthesis")
        return next(G), tree("PRIMARY", children)
    elif current.name == "MINUS":
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
        else:
            current, child = BOOL1(current, G)
            children.append(child)
            return current, tree("PRIMARY", children)
        raise ParserError("Syntax error: invalid negate expression")
    elif current.name == "NOT":
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
        else: 
            current, child = BOOL1(current, G)
            children.append(child)
            return current, tree("PRIMARY", children)
        raise ParserError("Syntax Error: invalid not and boollit expression")
    else:
        current, child = IDENT(current, G, None)
        children.append(child)
        return current, tree("PRIMARY", children)

def IDENT(current, G, typeOfVar):
    # <ident> -> ID
    global count
    children = []
    location = []
    inTable = False   
    if current.name == "ID":
        count = count + 1
        if not symbolTable == []: 
            for rec in symbolTable:
                if rec[0] == current.pattern:
                    rec[1].append(count)
                    inTable = True
        if not inTable:
            if typeOfVar != None:
                symbolTable.append([current.pattern, [count], False, typeOfVar, False])
            else:
                symbolTable.append([current.pattern, [count], False, typeOfVar, False])
        children.append(tree("ID"))
        return next(G), tree("IDENT", children)
    raise ParserError("Syntax error: not an identifier")

def BOOL1(current, G):
    # <bool1> -> <switch> {<logop> <switch>} | lambda
    children = []
    if current.name in {"LPAREN", "ID", "INTLIT", "BOOLLIT", "MINUS", "NOT"}: 
        current, child = SWITCH(current, G)
        children.append(child)
        while True:
            if current.name in {"OR", "AND"}:
                current, child = LOGOP(current, G)
                children.append(child)
                current, child = SWITCH(current, G)
                children.append(child)
            else: 
                break
        return current, tree("BOOL1", children)
    else:
        return current, None
    raise ParserError("syntax error: invalid in bool1")
 
def SWITCH(current, G):
    # <switch> -> <exp2> <switch'> <exp2>
    children = []
    if current.name in {"LPAREN", "ID", "INTLIT", "BOOLLIT", "MINUS", "NOT"}:
        current, child = EXP2(current, G)
        children.append(child)
        if current.name in {"LESSEQUAL", "GREATEQUAL", "EQUAL", "NOTEQUAL", "LESS", "GREAT"}:
            current, child = SWITCHPRIME(current, G)
            children.append(child)
            if current.name in {"LPAREN", "ID", "INTLIT", "BOOLLIT", "MINUS", "NOT"}:
                current, child = EXP2(current, G)
                children.append(child)
            else:
                raise ParserError("syntax error in switch")
        return current, tree("SWITCH", children)
    raise ParserError("Syntax error: in switch?")

def SWITCHPRIME(current, G):
    # <switch'> -> <= | >= | == | != | < | > | lambda
    children = []
    if current.name == "LESSEQUAL":
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
    else:
        return next(G), None

def EXP2(current, G):
    # <exp2> -> <expr2'> {<op> <expr2'>} | lambda
    children = []
    if current.name in {"LPAREN", "ID", "INTLIT", "BOOLLIT", "MINUS", "NOT"}:
         current, child = EXP2PRIME(current, G)
         children.append(child)
         while True:
             if current.name in {"PLUS", "MINUS"}:
                 current, child = OP(current, G)
                 children.append(child)
                 current, child = EXP2PRIME(current, G)
                 children.append(child)
             else:
                 break
         return current, tree("EXP2", children)
    else:
         return current, None
    raise ParserError("Syntax error in exp2")

def EXP2PRIME(current, G): 
    # <exp2'> -> <primary> {<op2> <primary>} | lambda
    children = []
    if current.name in {"LPAREN", "ID", "INTLIT", "BOOLLIT", "MINUS", "NOT"}:
        current, child = PRIMARY(current, G)
        children.append(child)
        while True:
            if current.name in {"MULTI", "DIV", "MOD"}:
                current, child = OP2(current,G)
                children.append(child)
                current, child = PRIMARY(current, G)
                children.append(child)
            else:
                break
        return current, tree("EXP2PRIME", children)
    else:
        return current, None

def LOGOP(current, G):
    # <logop> -> or | and
    children = []
    if current.name == "OR":
        return next(G), tree("OR")
    elif current.name == "AND":
        return next(G), tree("AND")
    raise ParserError("Syntax error: incorrect syntax no logical operator")

def OP(current, G):
    # <op> -> + | - 
    children = []
    if current.name == "PLUS":       
        return next(G), tree("PLUS")
    elif current.name == "MINUS":
        return next(G), tree("MINUS")
    raise ParserError("Syntax error: incorrect syntax, no logical/arithop operator")
 
def OP2(current,G):
    # <op2> -> * | / | %
    children = []
    if current.name == "MULTI":
        return next(G), tree("MULTI")
    elif current.name == "DIV":
        return next(G), tree("DIV")
    elif current.name == "MOD":
        return next(G), tree("MOD")
    raise ParserError("Syntax Error: Not multi, div, or mod operator")
