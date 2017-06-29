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
"""
import lexer as Lex
from tree import tree

count = 0
symbolTable = []
intLitTable = []

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
        return t, symbolTable, intLitTable;
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
# <assign> -> <ident> := <expression>
    children = []
    current, child = IDENT(current,G)
    children.append(child)
    if (current.name != "ASSIGNOP"):
        raise ParserError("Syntax error: invalid assignment")
    
    current, child = EXPRESSION(next(G),G)
    children.append(child)
    
    return current, tree("ASSIGNMENT", children)

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
#  <expression> -> <primary> {<arith_op> <primary>}
    children = []
    while (True):
        current, child = PRIMARY(current, G)
        children.append(child)
        if (current.name in {'PLUS', 'MINUS'}):
            current, child = ARITH_OP(current,G)
            children.append(child)
        else:
            break;
    return current, tree("EXPR", children)

def PRIMARY(current, G):
# <primary> -> (<expression>) | <ident> | INTLITERAL
    global count
    children = []

    if current.name == "INTLIT":
        count = count + 1
        children.append(tree("INTLIT"))
        intLitTable.append([count, current.pattern])
        return next(G), tree("PRIMARY", children)
    elif current.name == 'LPAREN':
        current, child = EXPRESSION(next(G), G)
        children.append(child)
        if current.name != 'RPAREN':
            raise ParserError("Syntax error: not a matching parenthesis")
        return next(G), tree("PRIMARY", children)
    else:
        current, child = IDENT(current, G)
        children.append(child)
        return current, tree("PRIMARY", children)

def IDENT(current, G):
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
            symbolTable.append([current.pattern, [count], False])
        children.append(tree("ID"))
        return next(G), tree("IDENT", children)
    raise ParserError("Syntax error: not an identifier")

def ARITH_OP(current, G):
# <arith_op> -> + | -
    children = []
    if current.name == "PLUS":       
        return next(G), tree("PLUS")
    if current.name == "MINUS":
        return next(G), tree("MINUS")
    raise ParserError("Syntax error: Incorrect syntax, no arithmetic operator (+ | -)")


                    

