import MLparser
import unittest

def create_file(str_list):
    with open("test.txt", "w") as fp:
        fp.write("\n".join(str_list) + "\n")

def runTest(L):
    create_file(L)
    return MLparser.parser("test.txt", "tokens.txt")

        
class ParserTester(unittest.TestCase):

    def test01(self):
        """Missing begin"""
        
        L = ["read(x);", "end"]
        with self.assertRaises(MLparser.ParserError):
            runTest(L)
    
    def test02(self):
        """Missing end"""
        
        L = ["begin", "read(x);"]
        with self.assertRaises(MLparser.ParserError):
            runTest(L)

    def test03(self):
        """Missing statement"""
        
        L = ["begin", "end"]
        with self.assertRaises(MLparser.ParserError):
            runTest(L)


    def test04(self):
        """Missing semi-colon (single statement)"""
        
        L = ["begin", "x := 5", "end"]
        with self.assertRaises(MLparser.ParserError):
            runTest(L)

    def test05(self):
        """Missing semi-colon (multiple statements)"""
        L = ["begin", "x := 5; x := 5", "end"]        
        with self.assertRaises(MLparser.ParserError):
            runTest(L)                                    

    def test06(self):
        """Missing assignop """        
        L = ["begin", "x + 5;", "end"]
        with self.assertRaises(MLparser.ParserError):
            runTest(L)

    def test07(self):
        """Bad start to statement"""
        L = ["begin", "begin;", "end"]
        with self.assertRaises(MLparser.ParserError):
            runTest(L)

    def test08(self):
        """Missing ( after read"""
        L = ["begin", "read x);", "end"]
        with self.assertRaises(MLparser.ParserError):
            runTest(L)                                    

    def test09(self):
        """Missing ) after read"""
        L = ["begin", "read (x;", "end"]
        with self.assertRaises(MLparser.ParserError):
            runTest(L)

    def test10(self):
        """Missing ( after write"""
        L = ["begin", "write x);", "end"]
        with self.assertRaises(MLparser.ParserError):
            runTest(L)                                    

    def test11(self):
        """Missing ) after write"""
        L = ["begin", "write (x;", "end"]
        with self.assertRaises(MLparser.ParserError):
            runTest(L)

    def test12(self):
        """Missing ID in id_list"""
        L = ["begin", "read(5);", "end"]
        with self.assertRaises(MLparser.ParserError):
            runTest(L)                                    

    def test13(self):
        """Bad expression 1: Missing operrand"""
        L = ["begin", "x := 5 +;", "end"]
        with self.assertRaises(MLparser.ParserError):
            runTest(L)


    def test14(self):
        """Bad expression 2: Unepxected op"""
        L = ["begin", "x := 5 + + 5;", "end"]
        with self.assertRaises(MLparser.ParserError):
            runTest(L)


    def test15(self):
        """Bad expression 3: Bad rparen"""
        L = ["begin", "x := 5 + 5);", "end"]
        with self.assertRaises(MLparser.ParserError):
            runTest(L)


    def test16(self):
        """Bad expression 4: Bad lparen"""
        L = ["begin", "x := (5 + 5;", "end"]
        with self.assertRaises(MLparser.ParserError):
            runTest(L)


    def test17(self):
        """Bad expression 6: Bad operator"""
        L = ["begin", "x := 5 x 5;", "end"]
        with self.assertRaises(MLparser.ParserError):
            runTest(L)


    def test18(self):
        """Bad expression 7: Unexpected reserved word"""
        L = ["begin", "x := 5 + read;", "end"]
        with self.assertRaises(MLparser.ParserError):
            runTest(L)

    def test19(self):
        """Multiple comma in read"""
        L = ["begin", "read(x,,y);", "end"]
        with self.assertRaises(MLparser.ParserError):
            runTest(L)            

    def test20(self):
        """Multiple comma in write"""
        L = ["begin", "write(x,,y);", "end"]
        with self.assertRaises(MLparser.ParserError):
            runTest(L)            

    def test21(self):
        """Run out of source"""
        L = ["begin", "x:="];
        with self.assertRaises(MLparser.ParserError):
            runTest(L)            

    def test22(self):
        """Unexpected primary"""
        L = ["begin", "x := read + 5;", "end"]
        with self.assertRaises(MLparser.ParserError):
            runTest(L)

    def test23(self):
        """Extra code after terminal end"""
        L = ["begin", "x := 5;", "end", "read(x)"]
        with self.assertRaises(MLparser.ParserError):
            runTest(L)                                     

    def test24(self): 
        # A reserved word begin as an ID
        L = ["begin", "x := y;", "begin := 2;", "end"]
        with self.assertRaises(MLparser.ParserError):
            runTest(L)

            
def run_tests(test = None):
    suite = unittest.TestLoader().loadTestsFromTestCase(ParserTester)
    testResult = unittest.TextTestRunner(verbosity=2).run(test if test else suite)

if __name__ == "__main__":
    run_tests()
