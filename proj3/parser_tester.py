import MLparser
import unittest

def create_file(str_list):
    with open("test.txt", "w") as fp:
        fp.write("\n".join(str_list) + "\n")

def runTest(L):
    create_file(L)
    return MLparser.parser("test.txt", "tokens.txt")

        
class ParserTesting(unittest.TestCase):

    def test01(self):
        """Basic statement: read"""
        L = ["begin", "read(x);", "end"]
        self.assertTrue(runTest(L))

    def test02(self):
        """Basic statement: read, multi-variable"""
        L = ["begin", "read(x,y,z);", "end"]
        self.assertTrue(runTest(L))        

    def test03(self):
        """Basic statement: write"""
        L = ["begin", "write(x);", "end"]
        self.assertTrue(runTest(L))

    def test04(self):
        """Basic statement: write, multi-variable"""
        L = ["begin", "write(x,y,z);", "end"]
        self.assertTrue(runTest(L))        

    def test05(self):
        """Compound statement: read"""
        L = ["begin", "read(x); read(x);", "end"]
        self.assertTrue(runTest(L))

    def test06(self):
        """Basic assignment"""
        L = ["begin", "x := 5;", "end"]
        self.assertTrue(runTest(L))


    def test07(self):
        """Basic assignment from variable"""
        L = ["begin", "x := y;", "end"]
        self.assertTrue(runTest(L))        

    def test08(self):
        """Assignment from expression"""
        L = ["begin", "x := 5 + 10;", "end"]
        self.assertTrue(runTest(L))

    def test09(self):
        """Assignment from compound expression"""
        L = ["begin", "x := (5 + 10)-20;", "end"]
        self.assertTrue(runTest(L))        

    def test10(self):
        """Assignmnet from expression with variables."""
        L = ["begin", "x := (y + 10)-z;", "end"]
        self.assertTrue(runTest(L))        

    def test11(self):
        """Assignment from more complex compound expression."""
        L = ["begin", "x := (5 + 10)-20-(30 + 40);", "end"]
        self.assertTrue(runTest(L))

    def test12(self):
        """Assignment from an even more complex expression."""
        L = ["begin", "x := ((1+2)-3)+((5+6-7)+8) + 9;" "end"]
        self.assertTrue(runTest(L))

    def test13(self):
        """Assignment from a deeply nested expression."""
        L = ["begin", "x := ((((((((((1+2)+2)+3)+4)+5)+6)+7)+8)+9)+10);" "end"]
        self.assertTrue(runTest(L))                

    def test14(self):
        """Writing multiple expressions."""
        L = ["begin", "write(x+y, (2-x)+y, (aa+bb)-(cc+dd));", "end"];
        self.assertTrue(runTest(L))
          

def run_tests(test = None):
    suite = unittest.TestLoader().loadTestsFromTestCase(ParserTesting)
    testResult = unittest.TextTestRunner(verbosity=2).run(test if test else suite)

if __name__ == "__main__":
    run_tests()
