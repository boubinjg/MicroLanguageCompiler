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
        """Initialization Test"""
        L = ["begin", "read(x);", "end"]
        vars = {"x"}
        t, H, f = runTest(L)
#        self.assertTrue(set(H.keys()) == vars)
        s = "(BEGIN,(((INTLIT,(ID)IDENT)INIT)ASSIGNMENT)STATEMENT_LIST,END)PROGRAM;"
        self.assertTrue(sameShape(t,parse_newick(s)))
        
    def test02(self):
        """Initialization Test"""
        L = ["begin", "bool y;", "end"]
        vars = {"y"}
        t,H,f = runTest(L)
 #       self.assertTrue(set(H.keys()) == vars)

        s = "(BEGIN,(((BOOLLIT,(ID)IDENT)INIT)ASSIGNMENT)STATEMENT_LIST,END)PROGRAM;"
        self.assertTrue(sameShape(t,parse_newick(s)))
        

    def test03(self):
        """Initialization Test"""
        L = ["begin", "string c;", "end"]
        vars = {"c"}
        t,H,f = runTest(L)
  #      t,H = runTest(L)
  #      self.assertTrue(set(H.keys()) == vars)

        s = "(BEGIN,(((STRINGLIT,(ID)IDENT)INIT)ASSIGNMENT)STATEMENT_LIST,END)PROGRAM;"
        self.assertTrue(sameShape(t,parse_newick(s)))
        
    def test04(self):
        """Multiplication test"""
        L = ["begin", "z := x*y + -4*5 + (x*y);", "end"]
        vars = {"x", "y", "z"}
        t,H,f = runTest(L)
   #     t,H = runTest(L)
   #     self.assertTrue(set(H.keys()) == vars)

        s ="(BEGIN,(((ID)IDENT,(((ID)IDENT)PRIMARY,(MULTI)OP,((ID)IDENT)PRIMARY,(PLUS)OP,(MINUS,INTLIT)PRIMARY,(MULTI)OP,(INTLIT)PRIMARY,(PLUS)OP,(((((ID)IDENT)PRIMARY,(MULTI)OP,((ID)IDENT)PRIMARY)PRIMARY)EXPRESSION)PRIMARY)EXPRESSION)ASSIGNMENT)STATEMENT_LIST,END)PROGRAM;"
        self.assertTrue(sameShape(t,parse_newick(s)))

        
    def test05(self):
        """Division test"""
        L = ["begin", "z := -x/y + 4/5 + (-x/y);", "end"]
        vars = {"x", "y", "z"}
        t,H,f = runTest(L)
    #    t,H = runTest(L)
    #    self.assertTrue(set(H.keys()) == vars)

        s = "(BEGIN,(((ID)IDENT,((MINUS,(ID)IDENT)PRIMARY,(DIV)OP,((ID)IDENT)PRIMARY,(PLUS)OP,(INTLIT)PRIMARY,(DIV)OP,(INTLIT)PRIMARY,(PLUS)OP,(((MINUS,(ID)IDENT)PRIMARY,(DIV)OP,((ID)IDENT)PRIMARY)EXPRESSION)PRIMARY)EXPRESSION)ASSIGNMENT)STATEMENT_LIST,END)PROGRAM;"
        self.assertTrue(sameShape(t,parse_newick(s)))

        
    def test06(self):
        """And test"""
        L = ["begin", "z := x and y or True and False or (True and False);", "end"]
        vars = {"x", "y", "z"}
        t,H,f = runTest(L)
     #   t,H = runTest(L)
     #   self.assertTrue(set(H.keys()) == vars)

        s = "(BEGIN,(((ID)IDENT,(((ID)IDENT)PRIMARY,(AND)OP,((ID)IDENT)PRIMARY,(OR)OP,(BOOLLIT)PRIMARY,(AND)OP,(BOOLLIT)PRIMARY,(OR)OP,(((BOOLLIT)PRIMARY,(AND)OP,(BOOLLIT)PRIMARY)EXPRESSION)PRIMARY)EXPRESSION)ASSIGNMENT)STATEMENT_LIST,END)PROGRAM;"
        self.assertTrue(sameShape(t,parse_newick(s)))

        
    def test07(self):
        """Or test"""
        L = ["begin", "z := x or y or True or False or (x or y);", "end"]
        vars = {"x", "y", "z"}
        t,H,f = runTest(L)
      #  t,H = runTest(L)
      #  self.assertTrue(set(H.keys()) == vars)

        s = "(BEGIN,(((ID)IDENT,(((ID)IDENT)PRIMARY,(OR)OP,((ID)IDENT)PRIMARY,(OR)OP,(BOOLLIT)PRIMARY,(OR)OP,(BOOLLIT)PRIMARY,(OR)OP,((((ID)IDENT)PRIMARY,(OR)OP,((ID)IDENT)PRIMARY)EXPRESSION)PRIMARY)EXPRESSION)ASSIGNMENT)STATEMENT_LIST,END)PROGRAM;"
        self.assertTrue(sameShape(t,parse_newick(s)))

        
    def test08(self):
        """Not test"""
        L = ["begin", "z := not x or not True or (not True);", "end"]
        vars = {"x"}
        t,H,f = runTest(L)
#        t,H = runTest(L)
       # self.assertTrue(set(H.keys()) == vars)

        s = "(BEGIN,(((ID)IDENT,((NOT,(ID)IDENT)PRIMARY,(OR)OP,(NOT,BOOLLIT)PRIMARY,(OR)OP,(((NOT,BOOLLIT)PRIMARY)EXPRESSION)PRIMARY)EXPRESSION)ASSIGNMENT)STATEMENT_LIST,END)PROGRAM;"
        self.assertTrue(sameShape(t,parse_newick(s)))

        
    def test09(self):
        """Less than or equal to test"""
        L = ["begin", "z := x <= -y == 4 <= 5 == (4 <= 5);", "end"]
        vars = {"x", "y", "z"}
        t,H,f = runTest(L)
 #       t,H = runTest(L)
#        self.assertTrue(set(H.keys()) == vars)

        s = "(BEGIN,(((ID)IDENT,(((ID)IDENT)PRIMARY,(LESSEQUAL)OP,(MINU,(ID)IDENT)PRIMARY,(EQUAL)OP,(INTLIT)PRIMARY,(LESSEQUAL)OP,(INTLIT)PRIMARY,(EQUAL)OP,(((INTLIT)PRIMARY,(LESSEQUAL)OP,(INTLIT)PRIMARY)EXPRESSION)PRIMARY)EXPRESSION)ASSIGNMENT)STATEMENT_LIST,END)PROGRAM;"
        self.assertTrue(sameShape(t,parse_newick(s)))



    def test10(self):
        """Greater than or equal to test"""
        L = ["begin", "z := x>= y and 4 >= -5 and (x>= y);", "end"]
        vars = {"x", "y", "z"}
        t,H,f = runTest(L)
  #      t,H = runTest(L)
 #       self.assertTrue(set(H.keys()) == vars)

        s = "(BEGIN,(((ID)IDENT,(((ID)IDENT)PRIMARY,(GREATEQUAL)OP,((ID)IDENT)PRIMARY,(AND)OP,(INTLIT)PRIMARY,(GREATEQUAL)OP,(MINUS,INTLIT)PRIMARY,(AND)OP,((((ID)IDENT)PRIMARY,(GREATEQUAL)OP,((ID)IDENT)PRIMARY)EXPRESSION)PRIMARY)EXPRESSION)ASSIGNMENT)STATEMENT_LIST,END)PROGRAM;"
        self.assertTrue(sameShape(t,parse_newick(s)))        

    def test11(self):
        """Equal test"""
        L = ["begin", "z := x==y or 5==4 or (5==4);" "end"]
        vars = {"x", "y", "z"}
        t,H,f = runTest(L)
    #    t,H = runTest(L)
   #     self.assertTrue(set(H.keys()) == vars)

        s = "(BEGIN,(((ID)IDENT,(((ID)IDENT)PRIMARY,(EQUAL)OP,((ID)IDENT)PRIMARY,(OR)OP,(INTLIT)PRIMARY,(EQUAL)OP,(INTLIT)PRIMARY,(OR)OP,(((INTLIT)PRIMARY,(EQUAL)OP,(INTLIT)PRIMARY)EXPRESSION)PRIMARY)EXPRESSION)ASSIGNMENT)STATEMENT_LIST,END)PROGRAM;"
        self.assertTrue(sameShape(t,parse_newick(s)))

        
    def test12(self):
        """Less than test"""
        L = ["begin", "z := -x<y == 4<5 == (4<5);" "end"]
        vars = {"x", "y", "z"}
        t,H,f = runTest(L)
     #   t,H = runTest(L)
    #    self.assertTrue(set(H.keys()) == vars)

        s = "(BEGIN,(((ID)IDENT,((MINUS,(ID)IDENT)PRIMARY,(LESS)OP,((ID)IDENT)PRIMARY,(EQUAL)OP,(INTLIT)PRIMARY,(LESS)OP,(INTLIT)PRIMARY,(EQUAL)OP,(((INTLIT)PRIMARY,(LESS)OP,(INTLIT)PRIMARY)EXPRESSION)PRIMARY)EXPRESSION)ASSIGNMENT)STATEMENT_LIST,END)PROGRAM;"
        self.assertTrue(sameShape(t,parse_newick(s)))

        
    def test13(self):
        """Greater than test"""
        L = ["begin", "z := x>y and 5>-4 and (x>y);", "end"];
        vars = {"x", "y", "z"}
        t,H,f = runTest(L)
      #  t,H = runTest(L)
     #   self.assertTrue(set(H.keys()) == vars)

        s = "(BEGIN,(((ID)IDENT,(((ID)IDENT)PRIMARY,(GREAT)OP,((ID)IDENT)PRIMARY,(AND)OP,(INTLIT)PRIMARY,(GREAT)OP,(MINUS,INTLIT)PRIMARY,(AND)OP,((((ID)IDENT)PRIMARY,(GREAT)OP,((ID)IDENT)PRIMARY)EXPRESSION)PRIMARY)EXPRESSION)ASSIGNMENT)STATEMENT_LIST,END)PROGRAM;"
        self.assertTrue(sameShape(t,parse_newick(s)))
        
    def test14(self):
        """String test"""
<<<<<<< HEAD
        L = ["begin", "string z := \"HELLO\";", "end"];
=======
        L = ["begin", "z := "HELLO";", "end"];
>>>>>>> 9d523a5dd66ec78ecc2f46767e17bc3f03138e77
        vars = {"z"}
        t,H,f = runTest(L)
      #  t,H = runTest(L)
     #   self.assertTrue(set(H.keys()) == vars)
        s = "(BEGIN,(((ID)IDENT,(STRINGLIT)EXPRESSION)ASSIGNMENT)STATEMENT_LIST,END)PROGRAM;"
        self.assertTrue(sameShape(t,parse_newick(s)))

    def test15(self):
        """String test without initialization"""
        L = ["begin", "z :=\"HELLO\";", "end"]
        vars = {"z"}
        t, H, f = runTest(L)
#        self.assertTrue(set(H.keys()) == vars)
        s = "(BEGIN,(((ID)IDENT,(STRINGLIT)EXPRESSION)ASSIGNMENT)STATEMENT_LIST,END)PROGRAM;"
        self.assertTrue(sameShape(t,parse_newick(s)))
     
     
    #Write statements    
    def test16(self):
        """Write with multiplication"""
        L = ["begin", "write(-x*y, 4*5*(x*y));", "end"]
        vars = {"x", "y", "z"}
        t,H,f = runTest(L)
 #       self.assertTrue(set(H.keys()) == vars)

        s = "(BEGIN,((((MINUS,(ID)IDENT)PRIMARY,(MULTI)OP,((ID)IDENT)PRIMARY)EXPRESSION,((INTLIT)PRIMARY,(MULTI)OP,(INTLIT)PRIMARY,(MULTI)OP,((((ID)IDENT)PRIMARY,(MULTI)OP,((ID)IDENT)PRIMARY)EXPRESSION)PRIMARY)EXPRESSION)EXPR_LIST)STATEMENT_LIST,END)PROGRAM;"
        self.assertTrue(sameShape(t,parse_newick(s)))
        

    def test17(self):
        """Write with division"""
        L = ["begin", "write(x/y, -4/5/(x/y));", "end"]
        vars = {"x", "y", "z"}
        t,H,f = runTest(L)
  #      t,H = runTest(L)
  #      self.assertTrue(set(H.keys()) == vars)

        s = "(BEGIN,(((((ID)IDENT)PRIMARY,(DIV)OP,((ID)IDENT)PRIMARY)EXPRESSION,((MINU,INTLIT)PRIMARY,(DIV)OP,(INTLIT)PRIMARY,(DIV)OP,((((ID)IDENT)PRIMARY,(DIV)OP,((ID)IDENT)PRIMARY)EXPRESSION)PRIMARY)EXPRESSION)EXPR_LIST)STATEMENT_LIST,END)PROGRAM;"
        self.assertTrue(sameShape(t,parse_newick(s)))
        
    def test18(self):
        """Write with and"""
        L = ["begin", "write(x and y, True and False); ", "end"]
        vars = {"x", "y"}
        t,H,f = runTest(L)
   #     t,H = runTest(L)
   #     self.assertTrue(set(H.keys()) == vars)

        s = "(BEGIN,(((((ID)IDENT)PRIMARY,(AND)OP,((ID)IDENT)PRIMARY)EXPRESSION,((BOOLLIT)PRIMARY,(AND)OP,(BOOLLIT)PRIMARY)EXPRESSION)EXPR_LIST)STATEMENT_LIST,END)PROGRAM;"
        self.assertTrue(sameShape(t,parse_newick(s)))

        
    def test19(self):
        """Write with or"""
        L = ["begin", "write(x or y, True or False or (x or y));", "end"]
        vars = {"x", "y"}
        t,H,f = runTest(L)
    #    t,H = runTest(L)
    #    self.assertTrue(set(H.keys()) == vars)

        s = "(BEGIN,(((((ID)IDENT)PRIMARY,(OR)OP,((ID)IDENT)PRIMARY,((BOOLLIT)PRIMARY,(OR)OP,(BOOLLIT)PRIMARY,(OR)OP,((((ID)IDENT)PRIMARY,(OR)OP,((ID)IDENT)PRIMARY)EXPRESSION)PRIMARY)EXPRESSION)EXPRESSION)EXPR_LIST)STATEMENT_LIST,END)PROGRAM;"
        self.assertTrue(sameShape(t,parse_newick(s)))

        
    def test20(self):
        """Write with not"""
        L = ["begin", "write(not x, not True);", "end"]
        vars = {"x"}
        t,H,f = runTest(L)
     #   t,H = runTest(L)
     #   self.assertTrue(set(H.keys()) == vars)

        s = "(BEGIN,((((NOT,(ID)IDENT)PRIMARY)EXPRESSION,((NOT,BOOLLIT)PRIMARY)EXPRESSION)EXPR_LIST)STATEMENT_LIST,END)PROGRAM;"
        self.assertTrue(sameShape(t,parse_newick(s)))

        
    def test21(self):
        """Write with lesser than or equal test"""
        L = ["begin", "write(-x <= y, 4 <= 5);", "end"]
        vars = {"x", "y"}
        t,H,f = runTest(L)
      #  t,H = runTest(L)
      #  self.assertTrue(set(H.keys()) == vars)

        s = "(BEGIN,((((MINUS,(ID)IDENT)PRIMARY,(LESSEQUAL)OP,((ID)IDENT)PRIMARY)EXPRESSION,((INTLIT)PRIMARY,(LESSEQUAL)OP,(INTLIT)PRIMARY)EXPRESSION)EXPR_LIST)STATEMENT_LIST,END)PROGRAM;"
        self.assertTrue(sameShape(t,parse_newick(s)))

        
    def test22(self):
        """Write with greater than or equal test"""
        L = ["begin", "write(x>=y, 4 >= 5);", "end"]
        vars = {"x", "y"}
        t,H,f = runTest(L)
#        t,H = runTest(L)
       # self.assertTrue(set(H.keys()) == vars)

        s = "(BEGIN,(((((ID)IDENT)PRIMARY,(GREATEQUAL)OP,((ID)IDENT)PRIMARY)EXPRESSION,((INTLIT)PRIMARY,(GREATEQUAL)OP,(INTLIT)PRIMARY)EXPRESSION)EXPR_LIST)STATEMENT_LIST,END)PROGRAM;"   
        self.assertTrue(sameShape(t,parse_newick(s)))

        
    def test23(self):
        """Write with equal test"""
        L = ["begin", "write(x==y, 5==4 == (x==y));", "end"]
        vars = {"x", "y"}
        t,H,f = runTest(L)
 #       t,H = runTest(L)
#        self.assertTrue(set(H.keys()) == vars)

        s = "(BEGIN,(((((ID)IDENT)PRIMARY,(EQUAL)OP,((ID)IDENT)PRIMARY)EXPRESSION,((INTLIT)PRIMARY,(EQUAL)OP,(INTLIT)PRIMARY,(EQUAL)OP,((((ID)IDENT)PRIMARY,(EQUAL)OP,((ID)IDENT)PRIMARY)EXPRESSION)PRIMARY)EXPRESSION)EXPR_LIST)STATEMENT_LIST,END)PROGRAM;"
        self.assertTrue(sameShape(t,parse_newick(s)))



    def test24(self):
        """Write with less than test"""
        L = ["begin", "write(x<y, 4<-5);", "end"]
        vars = {"x", "y"}
        t,H,f = runTest(L)
  #      t,H = runTest(L)
 #       self.assertTrue(set(H.keys()) == vars)

        s = "(BEGIN,(((((ID)IDENT)PRIMARY,(LESS)OP,((ID)IDENT)PRIMARY)EXPRESSION,((INTLIT)PRIMARY,(LESS)OP,(MINUS,INTLIT)PRIMARY)EXPRESSION)EXPR_LIST)STATEMENT_LIST,END)PROGRAM;"
        self.assertTrue(sameShape(t,parse_newick(s)))        

    def test25(self):
        """Write with greater than test"""
        L = ["begin", "write(x>-y, 5>4);", "end"]
        vars = {"x", "y"}
        t,H,f = runTest(L)
   #     t,H = runTest(L)
  #      self.assertTrue(set(H.keys()) == vars)

        s = "(BEGIN,(((((ID)IDENT)PRIMARY,(GREAT)OP,(MINUS,(ID)IDENT)PRIMARY)EXPRESSION,((INTLIT)PRIMARY,(GREAT)OP,(INTLIT)PRIMARY)EXPRESSION)EXPR_LIST)STATEMENT_LIST,END)PROGRAM;"
        self.assertTrue(sameShape(t,parse_newick(s)))

    def test26(self):
        """Write with strings"""
        L = ["begin", "write(\"HELLO\", \"GOODBYE\");", "end"]
        vars = {}
        t,H,f = runTest(L)
  #      t,H = runTest(L)
  #      self.assertTrue(set(H.keys()) == vars)

        s = "(BEGIN,((((STRINGLIT)PRIMARY)EXPRESSION,((STRINGLIT)PRIMARY)EXPRESSION)EXPR_LIST)STATEMENT_LIST,END)PROGRAM;"
        self.assertTrue(sameShape(t,parse_newick(s)))
    
    
    #Tests that should crash    
    def test27(self):
        """Has a quote for inside"""
        L = ["begin", "string x := \"\"; ", "end"]
        with self.assertRaises(MLparser.ParserError):
            runTest(L)

        
    def test28(self):
        """Missing variable name"""
        L = ["begin", "bool := x and y;", "end"]
        with self.assertRaises(MLparser.ParserError):
            runTest(L)

            
    def test29(self):
        """Missing int/bool/string"""
        L = ["begin", "y;", "end"]
        with self.assertRaises(MLparser.ParserError):
            runTest(L)

        
    def test30(self):
        """Missing variable name"""
        L = ["begin", "string;", "end"]
        with self.assertRaises(MLparser.ParserError):
            runTest(L)

        
    def test31(self):
        """One too many variables"""
        L = ["begin", "z := x/x y;", "end"]
        with self.assertRaises(MLparser.ParserError):
            runTest(L)

        
    def test32(self):
        """One too many operations"""
        L = ["begin", "z := x and and y;", "end"]
        with self.assertRaises(MLparser.ParserError):
            runTest(L)


    def test33(self):
        """One too many variables with not"""
        L = ["begin", "z := not y x;", "end"]
        with self.assertRaises(MLparser.ParserError):
            runTest(L)       


    def test34(self):
        """Extra operation on end"""
        L = ["begin", "z := x <= y +;", "end"]
        with self.assertRaises(MLparser.ParserError):
            runTest(L) 


    def test35(self):
        """Additional operation at start"""
        L = ["begin", "z := + x>=y;" "end"]
        vars = {"x"}
        with self.assertRaises(MLparser.ParserError):
            runTest(L) 

        
    def test36(self):
        """Extra negative sign"""
        L = ["begin", "z := - - x==y;" "end"]
        with self.assertRaises(MLparser.ParserError):
            runTest(L)

        
    def test37(self):
        """Missing quotes around string"""
        L = ["begin", "z := HELLO;", "end"];
        with self.assertRaises(MLparser.ParserError):
            runTest(L)
            
        
    def test38(self):
        """Missing end quote"""
        L = ["begin", "z := \"Eh;", "end"];
        with self.assertRaises(MLparser.ParserError):
            runTest(L)
             
      
    def test39(self):
        """Cannot have a negative not"""
        L = ["begin", "z := not -y;" "end"]
        with self.assertRaises(MLparser.ParserError):
            runTest(L)

        
    def test40(self):
        """Missing variable name"""
        L = ["begin", "int := x*y;", "end"];
        with self.assertRaises(MLparser.ParserError):
            runTest(L)
        

def run_tests(test = None):
    suite = unittest.TestLoader().loadTestsFromTestCase(ParserTesting)
    testResult = unittest.TextTestRunner(verbosity=2).run(test if test else suite)

if __name__ == "__main__":
    run_tests()
