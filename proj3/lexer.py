import re
import sys

class LexerError(Exception):
    """
    Exception to be thrown when the lexer encounters a bad token.
    """
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return str(self.msg)

class Token:
    """
    A class for storing token information.
    The variable instances for a token object are:
    * t_class: The token class.
    * name: The name of the token.
    * pattern: The specific pattern of the token
    * line: The line containing the token
    * line_num: The line number (numbered from 1)
    * col: The column number (numbered from 0)
    """

    def __init__(self, t_class, name, pattern, line, line_num, col):
        """
        Constructor
        """
        self.t_class = t_class
        self.name = name
        self.pattern = pattern
        self.line = line
        self.line_num = int(line_num)
        self.col = int(col)

    def __str__(self):
        """
        Defines behavior of the str function on the Token class.
        Prints as a tupple all information except self.line.
        """
        return str((self.t_class, self.name, self.pattern, self.line_num, self.col))

    def __repr__(self):
        """
        Defines the behaviour of the repr() function
        on the Token class.
        """
        return "Token: " + str(self)

    def __eq__(self, other):
        """
        Defines behaviour of the == operator on the Token class
        """
        return self.t_class == other.t_class and self.name == other.name and \
               self.pattern == other.pattern and self.line == other.line and \
               self.line_num == other.line_num and self.col == other.col
               

def lexer(source_file, token_file):
    """
    Input:
    * source_file: file containing the content to be tokenized
    * token_file: token file (see assignment specifications for format)
    Output:
    * A generator that will iteratively return token objects corresponding to the tokens
      of source_file, throwing a LexerError if it hits a bad token.
    """
    re_list = [] # List to hold the regular expressions from the token file
    token_hash = {} # Dictionary with key as reqular expression mapping to class and name of token
 
    # Read in data from token file & save in re_list & token_hash
    tokenFp = open(token_file)

    for line in tokenFp: # Save class, name, pattern in token_hash

        A = re.split("\s+", line.rstrip()) # split the line by spaces
        re_list.append(A[2]) # A[2] is the regular expression, save in this list for future use in matching
        token_hash[A[2]] = (A[0], A[1]) # Use regular expression as key, A[0] is class and A[1] is name

    tokenFp.close()
     
    # Initialize row & column variables
    row = 1
    col = 0

    # Read in source file
    sourceFp = open(source_file)

    for line in sourceFp:

        line = line.rstrip() # Delete trailing whitespace from each line
        line = re.sub("#(.|\s)*$", "", line) # See if line contains a comment and remove
        col = len(line) - len(line.lstrip()) # Delete leading whitespace from each line & save column number of first nonspace

        while(col < len(line)-1): # Loop through whole line

            matched = None # Boolean used to determine if bad token occurs
            
            for expr in re_list: # Loop through re_list and see if any regular expressions match line (greedy)

                matchObj = re.match(expr, line[col:])

                if (matchObj):
                    yield Token(token_hash[expr][0], token_hash[expr][1], matchObj.group(1), line, row, col) # Create token (class, name, pattern, line, row, column)
                    col = col + len(matchObj.group(1)) # Update column number to be past the recent match
                    col = len(line) - len(line[col:].lstrip()) # Strip leading spaces
                    matched = True # Set matched to true, found a valid token!

            if not matched: # If matched is None, then no valid token or comment was found, send error message
               errorMsg = "Bad token (line %d, column %d): %s" %(row, col, line[col:])
               raise LexerError(errorMsg)
               sourceFp.close()

        row = row + 1 # Finished searching line, update row
    sourceFp.close() # Close file
    yield Token('STOP', 'STOP', 'STOP', -1, -1, -1)



