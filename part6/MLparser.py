# Michelle Kojs, Jayson Boubin, John Crabill
# Part 3 - CP 6

"""
Parser for the Micro-language.
Grammar:
   <program> -> begin <statement_list> end
   <statement_list> -> <statement>; { <statement; }
   <statement> -> <assign> | read( <id_list> ) | write( <expr_list> )
   <assign> -> <ident> := <expression>
   <id_list> -> <ident> {, <ident>}
   <expr_list> -> <expression> {, <expression>}
   <expression> -> <primary> {<arith_op> <primary>}
   <primary> -> (<expression>) | <ident> | INTLITERAL
   <ident> -> ID
   <arith_op> -> + | -
   
   
   
New Grammar:
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
        if current.name != 'SEMICOLON':
            raise ParserError("Syntax error: Missing ; in STATEMENT_LIST")
        current = next(G)
        if (current.name == "STOP"):
            break;
        if (current.name in {"BEGIN", "END"}):
            break;
    return current, tree("STATEMENT_LIST", children)

def STATEMENT(current, G):
#  <statement> -> <assign> | read( <id_list> ) | write( <expr_list> )
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
        return next(G), tree("STATEMENT", children)
    else:
        current, child = ASSIGN(current, G)
        children.append(child)
        return current, tree("STATEMENT", children)

def ASSIGN(current, G):
# <assign> -> <init> := <expression> | <ident> := <expression> | <init>
    children = []
    if (current.name in {"STRTYPE", "INTTYPE", "BOOLTYPE"}):
        # either init or init := expr
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
#  <id_list> -> <ident> {, <ident>}
    children = []
    while (True):
        current, child = IDENT(current, G)
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
        current, child = OP(current, G)
        children.append(child)
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
        current, child = OP(current,G)
        children.append(child)
        if current.name == "BOOLLIT":
            count = count + 1
            children.append(tree("BOOLLIT"))
            valLitTable.append([count, current.pattern, "bool"])
            return next(G), tree("PRIMARY", children)
        elif current.name == "ID":
            current, child = IDENT(current, G, None)
            children.append(child)
            return current, tree("PRIMARY", children)
        raise ParserError("Syntax Error: invalid not and boollit expression")
    else:
        current, child = IDENT(current, G, None)
        children.append(child)
        return current, tree("PRIMARY", children)

def IDENT(current, G, typeOfVar):
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
 
                    

