"""
Jayson Boubin, Jason Katsaros, Gregory Pataky
CSE474, Group 8
"""

import re

class tree:
    """
    Tree class, where a tree is a label
    with zero or more trees as children
    """
    
    def __init__(self, label, children = None):
        """
        Tree constructor
        """
        self.label = label
        self.children = children if children != None else []

    def __str__(self):
        """
        Translate to newick string
        """
        
        if not self.children:
            return str(self.label) + ";"
        else:
            # Note: str(e)[:-1] cuts the semicolon off of children
            return "(" + ",".join(str(e)[:-1] for e in self.children) \
                    + ")" + str(self.label) + ";"

    def __repr__(self):
        return "Tree: " + str(self)

    def __len__(self):
        """
        Return number of nodes in teee
        """
        if not self.children:
            return 1
        else:
            count = 1
            for tree in self.children:
                count += len(tree)
            return count

    def isLeaf(self):
        """
        Return true/false indicating whether
        the tree is a leaf
        """
        return len(self.children) == 0

class LexerError(Exception):
    """
    Exception to be thrown when the lexer encounters a bad token.
    """
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return str(self.msg)

class ParserException(Exception):
    """
    Exception class for parse_newick
    """
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg

# Parse_newick Should raise the following ParserException errors when appropriate:
# * Terminating semi-colon missing. <
# * Expected label missing. <
# * Missing command or ) where expected. <
# (You may add others as you see fit.)
# - All other errors will essentially be caught by the checkers in T
#
# Spacing should not matter: "(a,b)c;", and " ( a  ,  b ) c; " should result in idential
# trees.

def lexer(s):
    """
    A simple tokenizer for the Newick language.
    Returns simple strings, with no line or column information.
    """

    # Remove whitespace
    s = re.sub('\s', '', s)
    
    i = 0
    # Need to use an indefinite loop here because we manually increment i
    while i < len(s):
        if re.match('\s', s[i]):
            continue

        found = None
        # Changed to a tuple to ensure order preference
        for regex in ('\(', '\)', '\,', ';', '\w+'):
            found = re.match(regex, s[i:])
            if found:
                i += found.end(0)
                yield found.group(0)
                # this is necessary to continue correctly to the next input
                break
        
        if not found:
            msg = "Bad token at character " + str(i)
            raise LexerError(msg)
    
    yield '$' # ensures there is always a token after the last node label

def parse_newick(s):
    """
    Take a newick string and return the corresponding tree object.
    """
    
    lex = lexer(s)
    return T(next(lex), lex)

def T(current, lex):
    """
    This is the start Grammar procedure
    """
    
    err_msg = "Parsing Error: Terminating semi-colon missing."
    
    completeTree = S(current, lex)
    
    # Catches errors where there is no next(G) (i.e. eaten in S)
    try:
        final = next(lex)
    except Exception:
        raise ParserException(err_msg)
    # Meant to catch '$' or any other invalid ending character
    if final != ';':
        raise ParserException(err_msg)
    
    return completeTree
        
def S(current, lex, children = None, prev = ""):
    """
    This recursively creates trees. It was awful to write because of the
    warning written below. This got messy.

    current = current token
    lex = token generator (lexer)
    children = list of child nodes
    prev = previous token (for errors)
    """

    err_msg_1 = "Expected label missing."
    err_msg_2 = "Missing command or ) where expected."
    
    # WARNING: You CANNOT make children default to [] because then each
    # call to the function has children point to the same list
    children = children if children != None else []
    
    if current == '(':
        children.append(S(next(lex), lex, [], current))
        return S(next(lex), lex, children, current)
    # if at a comma, there should have been a tree returned before it [len(children) > 0]
    # Comma should not come right after ')' (we are forcing a label on all nodes as per guidelines)
    # Comma can't come first in stirng (when prev = '')
    if current == ',':
        if prev not in {'', ')'} and len(children) > 0:
            children.append(S(next(lex), lex, [], current))
            return S(next(lex), lex, children, current)
        else:
            # there was a missing label before comma
            raise ParserException(err_msg_1)
    if current == ')':
        if prev == ')':
            raise ParserException(err_msg_1)
        if prev == '':
            raise ParserException(err_msg_2)
        return S(next(lex), lex, children, current)
    if re.match('\w+', current):
        return tree(current, children)
    
    # If no cases matched, then there is an error somewhere
    # The prev parameter allows the function to know what was expected
    # based on what came before, so a better error message can be tailored
    # to the situation
    raise ParserException(err_msg_1) if prev == ')' else ParserException(err_msg_2)
