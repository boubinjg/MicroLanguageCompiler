import MLparser
import unittest
from tree import parse_newick

def create_file(str_list):
    with open("test.txt", "w") as fp:
        fp.write("\n".join(str_list) + "\n")

def runTest(L):
    create_file(L)
    return MLparser.parser("test.txt", "tokens.txt")

def sameShape(r1, r2):
    """Do the trees rooted at r1 and t2 have the same topology"""
    return len(r1.children) == len(r2.children) and \
        all([sameShape(c1, c2) for c1,c2 in zip(r1.children,r2.children)])
        

class ParserTesting(unittest.TestCase):

    def test01(self):
        """Basic statement: read"""
        L = ["begin", "int x := 2;", "end"]
        vars = {"x"}
        t, H, f = runTest(L)
#        self.assertTrue(set(H.keys()) == vars)
        s = "(BEGIN,((READ,((ID)IDENT)ID_LIST)STATEMENT)STATEMENT_LIST,END)PROGRAM;"
        self.assertTrue(sameShape(t,parse_newick(s)))
        
    def test02(self):
        """Basic statement: read, multi-variable"""
        L = ["begin", "read(x,y,z);", "end"]
        vars = {"x", "y", "z"}
        t,H,f = runTest(L)
 #       self.assertTrue(set(H.keys()) == vars)

        s = "(BEGIN,((READ,((ID)IDENT,(ID)IDENT,(ID)IDENT)ID_LIST)STATEMENT)STATEMENT_LIST,END)PROGRAM;"
        self.assertTrue(sameShape(t,parse_newick(s)))
        

    def test03(self):
        """Basic statement: write"""
        L = ["begin", "write(x);", "end"]
        vars = {"x"}
        t,H,f = runTest(L)
  #      t,H = runTest(L)
  #      self.assertTrue(set(H.keys()) == vars)

        s = "(BEGIN,((WRITE,((((ID)IDENT)PRIMARY)EXPRESSION)EXPR_LIST)STATEMENT)STATEMENT_LIST,END)PROGRAM;"
        self.assertTrue(sameShape(t,parse_newick(s)))
        
    def test04(self):
        """Basic statement: write, multi-variable"""
        L = ["begin", "write(x,y,z);", "end"]
        vars = {"x", "y", "z"}
        t,H,f = runTest(L)
   #     t,H = runTest(L)
   #     self.assertTrue(set(H.keys()) == vars)

        s = "(BEGIN,((WRITE,((((ID)IDENT)PRIMARY)EXPRESSION,(((ID)IDENT)PRIMARY)EXPRESSION,(((ID)IDENT)PRIMARY)EXPRESSION)EXPR_LIST)STATEMENT)STATEMENT_LIST,END)PROGRAM;"
        self.assertTrue(sameShape(t,parse_newick(s)))

        
    def test05(self):
        """Compound statement: read"""
        L = ["begin", "read(ba); read(aa);", "end"]
        vars = {"ba", "aa"}
        t,H,f = runTest(L)
    #    t,H = runTest(L)
    #    self.assertTrue(set(H.keys()) == vars)

        s = "(BEGIN,((READ,((ID)IDENT)ID_LIST)STATEMENT,(READ,((ID)IDENT)ID_LIST)STATEMENT)STATEMENT_LIST,END)PROGRAM;"
        self.assertTrue(sameShape(t,parse_newick(s)))

        
    def test06(self):
        """Basic assignment"""
        L = ["begin", "aaa := 5;", "end"]
        vars = {"aaa"}
        t,H,f = runTest(L)
     #   t,H = runTest(L)
     #   self.assertTrue(set(H.keys()) == vars)

        s = "(BEGIN,((((ID)IDENT,((INTLIT)PRIMARY)EXPRESSION)ASSIGNMENT)STATEMENT)STATEMENT_LIST,END)PROGRAM;"
        self.assertTrue(sameShape(t,parse_newick(s)))

        
    def test07(self):
        """Basic assignment from variable"""
        L = ["begin", "x := y;", "end"]
        vars = {"x", "y"}
        t,H,f = runTest(L)
      #  t,H = runTest(L)
      #  self.assertTrue(set(H.keys()) == vars)

        s = "(BEGIN,((((ID)IDENT,(((ID)IDENT)PRIMARY)EXPRESSION)ASSIGNMENT)STATEMENT)STATEMENT_LIST,END)PROGRAM;"
        self.assertTrue(sameShape(t,parse_newick(s)))

        
    def test08(self):
        """Assignment from expression"""
        L = ["begin", "x := 5 + 10;", "end"]
        vars = {"x"}
        t,H,f = runTest(L)
#        t,H = runTest(L)
       # self.assertTrue(set(H.keys()) == vars)

        s = "(BEGIN,((((ID)IDENT,((INTLIT)PRIMARY,PLUS,(INTLIT)PRIMARY)EXPRESSION)ASSIGNMENT)STATEMENT)STATEMENT_LIST,END)PROGRAM;"
        self.assertTrue(sameShape(t,parse_newick(s)))

        
    def test09(self):
        """Assignment from compound expression"""
        L = ["begin", "x := (5 - 10) - 20;", "end"]
        vars = {"x"}
        t,H,f = runTest(L)
 #       t,H = runTest(L)
#        self.assertTrue(set(H.keys()) == vars)

        s = "(BEGIN,((((ID)IDENT,((((INTLIT)PRIMARY,PLUS,(INTLIT)PRIMARY)EXPRESSION)PRIMARY,MINUS,(INTLIT)PRIMARY)EXPRESSION)ASSIGNMENT)STATEMENT)STATEMENT_LIST,END)PROGRAM;"
        self.assertTrue(sameShape(t,parse_newick(s)))



    def test10(self):
        """Assignmnet from expression with variables."""
        L = ["begin", "x := (y + 10)-z;", "end"]
        vars = {"x", "y", "z"}
        t,H,f = runTest(L)
  #      t,H = runTest(L)
 #       self.assertTrue(set(H.keys()) == vars)

        s = "(BEGIN,((((ID)IDENT,(((((ID)IDENT)PRIMARY,PLUS,(INTLIT)PRIMARY)EXPRESSION)PRIMARY,MINUS,((ID)IDENT)PRIMARY)EXPRESSION)ASSIGNMENT)STATEMENT)STATEMENT_LIST,END)PROGRAM;"
        self.assertTrue(sameShape(t,parse_newick(s)))        

    def test11(self):
        """Assignment from more complex compound expression."""
        L = ["begin", "x := (5 + 10)-20-(30 + 40);", "end"]
        vars = {"x"}
        t,H,f = runTest(L)
   #     t,H = runTest(L)
  #      self.assertTrue(set(H.keys()) == vars)

        s = "(BEGIN,((((ID)IDENT,((((INTLIT)PRIMARY,PLUS,(INTLIT)PRIMARY)EXPRESSION)PRIMARY,MINUS,(INTLIT)PRIMARY,MINUS,(((INTLIT)PRIMARY,PLUS,(INTLIT)PRIMARY)EXPRESSION)PRIMARY)EXPRESSION)ASSIGNMENT)STATEMENT)STATEMENT_LIST,END)PROGRAM;"
        self.assertTrue(sameShape(t,parse_newick(s)))

    def test12(self):
        """Assignment from an even more complex expression."""
        L = ["begin", "x := ((1+2)-3)+((5+6-7)+8) + 9;" "end"]
        vars = {"x"}
        t,H,f = runTest(L)
    #    t,H = runTest(L)
   #     self.assertTrue(set(H.keys()) == vars)

        s = "(BEGIN,((((ID)IDENT,((((((INTLIT)PRIMARY,PLUS,(INTLIT)PRIMARY)EXPRESSION)PRIMARY,MINUS,(INTLIT)PRIMARY)EXPRESSION)PRIMARY,PLUS,(((((INTLIT)PRIMARY,PLUS,(INTLIT)PRIMARY,MINUS,(INTLIT)PRIMARY)EXPRESSION)PRIMARY,PLUS,(INTLIT)PRIMARY)EXPRESSION)PRIMARY,PLUS,(INTLIT)PRIMARY)EXPRESSION)ASSIGNMENT)STATEMENT)STATEMENT_LIST,END)PROGRAM;"
        self.assertTrue(sameShape(t,parse_newick(s)))

        
    def test13(self):
        """Assignment from a deeply nested expression."""
        L = ["begin", "x := ((((((((((1+2)+2)+3)+4)+5)+6)+7)+8)+9)+10);" "end"]
        vars = {"x"}
        t,H,f = runTest(L)
     #   t,H = runTest(L)
    #    self.assertTrue(set(H.keys()) == vars)

        s = "(BEGIN,((((ID)IDENT,((((((((((((((((((((((INTLIT)PRIMARY,PLUS,(INTLIT)PRIMARY)EXPRESSION)PRIMARY,PLUS,(INTLIT)PRIMARY)EXPRESSION)PRIMARY,PLUS,(INTLIT)PRIMARY)EXPRESSION)PRIMARY,PLUS,(INTLIT)PRIMARY)EXPRESSION)PRIMARY,PLUS,(INTLIT)PRIMARY)EXPRESSION)PRIMARY,PLUS,(INTLIT)PRIMARY)EXPRESSION)PRIMARY,PLUS,(INTLIT)PRIMARY)EXPRESSION)PRIMARY,PLUS,(INTLIT)PRIMARY)EXPRESSION)PRIMARY,PLUS,(INTLIT)PRIMARY)EXPRESSION)PRIMARY,PLUS,(INTLIT)PRIMARY)EXPRESSION)PRIMARY)EXPRESSION)ASSIGNMENT)STATEMENT)STATEMENT_LIST,END)PROGRAM;"
        self.assertTrue(sameShape(t,parse_newick(s)))

        
    def test14(self):
        """Writing multiple expressions."""
        L = ["begin", "write(x+y, (2-x)+y, (aa+bb)-(cc+dd));", "end"];
        vars = {"x", "y", "aa", "bb", "cc", "dd"}
        t,H,f = runTest(L)
      #  t,H = runTest(L)
     #   self.assertTrue(set(H.keys()) == vars)

        s = "(BEGIN,((WRITE,((((ID)IDENT)PRIMARY,PLUS,((ID)IDENT)PRIMARY)EXPRESSION,((((INTLIT)PRIMARY,MINUS,((ID)IDENT)PRIMARY)EXPRESSION)PRIMARY,PLUS,((ID)IDENT)PRIMARY)EXPRESSION,(((((ID)IDENT)PRIMARY,PLUS,((ID)IDENT)PRIMARY)EXPRESSION)PRIMARY,MINUS,((((ID)IDENT)PRIMARY,PLUS,((ID)IDENT)PRIMARY)EXPRESSION)PRIMARY)EXPRESSION)EXPR_LIST)STATEMENT)STATEMENT_LIST,END)PROGRAM;"
        self.assertTrue(sameShape(t,parse_newick(s)))
        
        

def run_tests(test = None):
    suite = unittest.TestLoader().loadTestsFromTestCase(ParserTesting)
    testResult = unittest.TextTestRunner(verbosity=2).run(test if test else suite)

if __name__ == "__main__":
    run_tests()
