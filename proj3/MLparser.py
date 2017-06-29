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

class ParserError(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg

# to fix
#def lexer(source_file, token_file):
 #   for c in re.sub("\s+", "", s):
  #      yield c
   # yield '$'

#######################################
# Parsing code
def parser(source_file, token_file):
    """
    source_file: A program written in the ML langauge.
    returns True if the code is syntactically correct.
    Throws a ParserError otherwise.
    """
    G = Lex.lexer(source_file, token_file)
    current = PROGRAM(next(G), G)
    if (current.name == "STOP"):
        return True;
    elif (current.name != "STOP"):
        raise ParserError("Extra code after END");
        return False;
    return True;

def PROGRAM(current, G):
# <program> -> begin <statement_list> end
    while (True):
        if current.name == 'BEGIN':
            current = STATEMENT_LIST(next(G), G)
        if current.name == "STOP":
            raise ParserError("Missing END")
        if current.name == 'END':
            return next(G)
        if current.name not in {'BEGIN', 'END'}:
            raise ParserError("Parser error in PROGRAM: missing begin or end")

def STATEMENT_LIST(current, G):
#  <statement_list> -> <statement>; { <statement; }
    while (True):
        current = STATEMENT(current, G)
        if current.name != 'SEMICOLON':
            raise ParserError("Missing ; in STATEMENT_LIST")
        current = next(G)
        if (current.name == "STOP"):
            break;
        if (current.name in {"BEGIN", "END"}):
            break;
    return current

def STATEMENT(current, G):
#  <statement> -> <assign> | read( <id_list> ) | write( <expr_list> )
    if current.name == 'READ':
        current = next(G)
        if current.name != "LPAREN":
            raise ParserError("missing opening (")
        current = ID_LIST(next(G), G)
        if (current.name != "RPAREN"):
            raise ParserError("missing closing )")
        return next(G)
 #   elif current.name == 'WRITE':
    elif current.name == "WRITE":
        current = next(G)
        if current.name != "LPAREN":
            raise ParserError("missing opening (")
        current = EXPR_LIST(next(G), G)
        if (current.name != "RPAREN"):
            raise ParserError("missing closing )")
        return next(G);
    else:
        current = ASSIGN(current, G)
        return current;
    return current
   # return current

def ASSIGN(current, G):
# <assign> -> <ident> := <expression>
#   whilie (True):
    current = IDENT(current,G)
    if (current.name != "ASSIGNOP"):
        raise ParserError("invalid assignment")
    
    current = EXPRESSION(next(G),G)    
    return current

def ID_LIST(current, G):
#  <id_list> -> <ident> {, <ident>}
    while (True):
        current = IDENT(current, G)
        if current.name != 'COMMA':
            break;
        current = next(G)

    return current

def EXPR_LIST(current, G):
#  <expr_list> -> <expression> {, <expression>}
    while (True):
        current = EXPRESSION(current, G)
        if current.name != 'COMMA':
            break;
        current = next(G)
    return current

def EXPRESSION(current, G):
#  <expression> -> <primary> {<arith_op> <primary>}
    while (True):
        current = PRIMARY(current, G)
        if (current.name in {'PLUS', 'MINUS'}):
            current = ARITH_OP(current,G)
        else:
            break;
    return current

def PRIMARY(current, G):
# <primary> -> (<expression>) | <ident> | INTLITERAL
    if current.name == "INTLIT":
        return next(G)
    elif current.name == 'LPAREN':
        current = EXPRESSION(next(G), G)
        if current.name != 'RPAREN':
            raise ParserError("not a matching parenthesis")
        return next(G)
    else:
        current = IDENT(current, G)
    return current

def IDENT(current, G):
# <ident> -> ID
    if current.name == "ID":
        return next(G)
    raise ParserError("not an identifier")

def ARITH_OP(current, G):
# <arith_op> -> + | -
    if current.name in {'PLUS', 'MINUS'}:
        return next(G)
    raise ParserError("Incorrect syntax, no arithmetic operator (+ | -)")


                    

