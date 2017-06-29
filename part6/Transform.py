from tree import *

tIDENT = tree("IDENT", ["ID "])

tOPplus = tree("OP", ["PLUS "])
tOPminus = tree("OP", ["MINUS "])
tOPmulti = tree("OP", ["MULTI "])
tOPdivi = tree("OP", ["DIV "])
tOPge = tree("OP", ["GREATEQUAL "])
tOPle = tree("OP", ["LESSEQUAL "])
tOPe = tree("OP", ["EQUAL "])
tOPl = tree("OP", ["LESS "])
tOPg = tree("OP", ["GREAT "])
tOPand = tree("OP", ["AND "])
tOPor = tree("OP", ["OR "])

tINITI = tree("INIT", ["INTLIT ", tIDENT])
tINITS = tree("INIT", ["STRINGLIT ", tIDENT])
tINITB = tree("INIT", ["BOOLLIT ", tIDENT])


t1 = tree("ASSIGNMENT", [tINITI])
t2 = tree("ASSIGNMENT", [tINITB])
t3 = tree("ASSIGNMENT", [tINITS])
t4 = tree("ASSIGNMENT", [tIDENT, tree("EXPRESSION", [tree("PRIMARY", [tIDENT]), tOPmulti, tree("PRIMARY", [tIDENT]),
                                    tOPplus, tree("PRIMARY", ["MINUS ", "INTLIT "]), tOPmulti, tree("PRIMARY", ["INTLIT "]),
                                    tOPplus, tree("PRIMARY", [tree("EXPRESSION", [tree("PRIMARY", [tree("PRIMARY", [tIDENT]), tOPmulti, tree("PRIMARY", [tIDENT])])])])])])
t5 = tree("ASSIGNMENT", [tIDENT, tree("EXPRESSION", [tree("PRIMARY", ["MINUS ", tIDENT]), tOPdivi, tree("PRIMARY", [tIDENT]),
                                    tOPplus, tree("PRIMARY", ["INTLIT "]), tOPdivi, tree("PRIMARY", ["INTLIT "]),
                                    tOPplus, tree("PRIMARY", [tree("EXPRESSION", [tree("PRIMARY", ["MINUS ", tIDENT]), tOPdivi, tree("PRIMARY", [tIDENT])])])])])
t6 = tree("ASSIGNMENT", [tIDENT, tree("EXPRESSION", [tree("PRIMARY", [tIDENT]), tOPand, tree("PRIMARY", [tIDENT]),
                                    tOPor, tree("PRIMARY", ["BOOLLIT "]), tOPand, tree("PRIMARY", ["BOOLLIT "]),
                                    tOPor, tree("PRIMARY", [tree("EXPRESSION", [tree("PRIMARY", ["BOOLLIT "]), tOPand, tree("PRIMARY", ["BOOLLIT "])])])])])
t7 = tree("ASSIGNMENT", [tIDENT, tree("EXPRESSION", [tree("PRIMARY", [tIDENT]), tOPor, tree("PRIMARY", [tIDENT]),
                                    tOPor, tree("PRIMARY", ["BOOLLIT "]), tOPor, tree("PRIMARY", ["BOOLLIT "]),
                                    tOPor, tree("PRIMARY", [tree("EXPRESSION", [tree("PRIMARY", [tIDENT]), tOPor, tree("PRIMARY", [tIDENT])])])])])
t8 = tree("ASSIGNMENT", [tIDENT, tree("EXPRESSION", [tree("PRIMARY", ["NOT ", tIDENT]), tOPor, tree("PRIMARY", ["NOT ", "BOOLLIT "]),
                                    tOPor, tree("PRIMARY", [tree("EXPRESSION", [tree("PRIMARY", ["NOT ", "BOOLLIT "])])])])])
t9 = tree("ASSIGNMENT", [tIDENT, tree("EXPRESSION", [tree("PRIMARY", [tIDENT]), tOPle, tree("PRIMARY", ["MINUS", tIDENT]),
                                    tOPe, tree("PRIMARY", ["INTLIT "]), tOPle, tree("PRIMARY", ["INTLIT "]),
                                    tOPe, tree("PRIMARY", [tree("EXPRESSION", [tree("PRIMARY", ["INTLIT "]), tOPle, tree("PRIMARY", ["INTLIT "])])])])])
t10 = tree("ASSIGNMENT", [tIDENT, tree("EXPRESSION", [tree("PRIMARY", [tIDENT]), tOPge, tree("PRIMARY", [tIDENT]),
                                    tOPand, tree("PRIMARY", ["INTLIT "]), tOPge, tree("PRIMARY", ["MINUS ", "INTLIT "]),
                                    tOPand, tree("PRIMARY", [tree("EXPRESSION", [tree("PRIMARY", [tIDENT]), tOPge, tree("PRIMARY", [tIDENT])])])])])
t11 = tree("ASSIGNMENT", [tIDENT, tree("EXPRESSION", [tree("PRIMARY", [tIDENT]), tOPe, tree("PRIMARY", [tIDENT]),
                                    tOPor, tree("PRIMARY", ["INTLIT "]), tOPe, tree("PRIMARY", ["INTLIT "]),
                                    tOPor , tree("PRIMARY", [tree("EXPRESSION", [tree("PRIMARY", ["INTLIT "]), tOPe, tree("PRIMARY", ["INTLIT "])])])])])
t12 = tree("ASSIGNMENT", [tIDENT, tree("EXPRESSION", [tree("PRIMARY", ["MINUS ", tIDENT]), tOPl, tree("PRIMARY", [tIDENT]),
                                    tOPe, tree("PRIMARY", ["INTLIT "]), tOPl, tree("PRIMARY", ["INTLIT "]),
                                    tOPe, tree("PRIMARY", [tree("EXPRESSION", [tree("PRIMARY", ["INTLIT "]), tOPl, tree("PRIMARY", ["INTLIT "])])])])])
t13 = tree("ASSIGNMENT", [tIDENT, tree("EXPRESSION", [tree("PRIMARY", [tIDENT]), tOPg, tree("PRIMARY", [tIDENT]),
                                    tOPand, tree("PRIMARY", ["INTLIT "]), tOPg, tree("PRIMARY", ["MINUS ","INTLIT "]),
                                    tOPand, tree("PRIMARY", [tree("EXPRESSION", [tree("PRIMARY", [tIDENT]), tOPg, tree("PRIMARY", [tIDENT])])])])])
t14 = tree("ASSIGNMENT", [tIDENT, tree("EXPRESSION", ["STRINGLIT "])])
t15 = tree("ASSIGNMENT", [tIDENT, tree("EXPRESSION", ["STRINGLIT "])])

t16 = tree("EXPR_LIST", [tree("EXPRESSION", [tree("PRIMARY", ["MINUS ", tIDENT]), tOPmulti, tree("PRIMARY", [tIDENT])]),
                        tree("EXPRESSION", [tree("PRIMARY", ["INTLIT "]), tOPmulti, tree("PRIMARY", ["INTLIT "]),
                        tOPmulti, tree("PRIMARY", [tree("EXPRESSION", [tree("PRIMARY", [tIDENT]), tOPmulti, tree("PRIMARY", [tIDENT])])])])])
t17 = tree("EXPR_LIST", [tree("EXPRESSION", [tree("PRIMARY", [tIDENT]), tOPdivi, tree("PRIMARY", [tIDENT])]),
                        tree("EXPRESSION", [tree("PRIMARY", ["MINUS", "INTLIT "]), tOPdivi, tree("PRIMARY", ["INTLIT "]),
                        tOPdivi, tree("PRIMARY", [tree("EXPRESSION", [tree("PRIMARY", [tIDENT]), tOPdivi, tree("PRIMARY", [tIDENT])])])])])
t18 = tree("EXPR_LIST", [tree("EXPRESSION", [tree("PRIMARY", [tIDENT]), tOPand, tree("PRIMARY", [tIDENT])]),
                         tree("EXPRESSION", [tree("PRIMARY", ["BOOLLIT "]), tOPand, tree("PRIMARY", ["BOOLLIT "])])])
t19 = tree("EXPR_LIST", [tree("EXPRESSION", [tree("PRIMARY", [tIDENT]), tOPor, tree("PRIMARY", [tIDENT]),
                        tree("EXPRESSION", [tree("PRIMARY", ["BOOLLIT "]), tOPor, tree("PRIMARY", ["BOOLLIT "]),
                        tOPor, tree("PRIMARY", [tree("EXPRESSION", [tree("PRIMARY", [tIDENT]), tOPor, tree("PRIMARY", [tIDENT])])])])])])
t20 = tree("EXPR_LIST", [tree("EXPRESSION", [tree("PRIMARY", ["NOT ",tIDENT])]),
                         tree("EXPRESSION", [tree("PRIMARY", ["NOT ", "BOOLLIT "])])])
t21 = tree("EXPR_LIST", [tree("EXPRESSION", [tree("PRIMARY", ["MINUS ",tIDENT]),
                        tOPle, tree("PRIMARY", [tIDENT])]), tree("EXPRESSION", [tree("PRIMARY", ["INTLIT "]),
                        tOPle, tree("PRIMARY", ["INTLIT "])])])
t22 = tree("EXPR_LIST", [tree("EXPRESSION", [tree("PRIMARY", [tIDENT]),
                        tOPge, tree("PRIMARY", [tIDENT])]), tree("EXPRESSION", [tree("PRIMARY", ["INTLIT "]),
                        tOPge, tree("PRIMARY", ["INTLIT "])])])
t23 = tree("EXPR_LIST", [tree("EXPRESSION", [tree("PRIMARY", [tIDENT]), tOPe, tree("PRIMARY", [tIDENT])]),
                        tree("EXPRESSION", [tree("PRIMARY", ["INTLIT "]), tOPe, tree("PRIMARY", ["INTLIT "]),
                        tOPe, tree("PRIMARY", [tree("EXPRESSION", [tree("PRIMARY", [tIDENT]), tOPe, tree("PRIMARY", [tIDENT])])])])])
t24 = tree("EXPR_LIST", [tree("EXPRESSION", [tree("PRIMARY", [tIDENT]), tOPl, tree("PRIMARY", [tIDENT])]),
                        tree("EXPRESSION", [tree("PRIMARY", ["INTLIT "]), tOPl, tree("PRIMARY", ["MINUS ","INTLIT "])])])
t25 = tree("EXPR_LIST", [tree("EXPRESSION", [tree("PRIMARY", [tIDENT]), tOPg, tree("PRIMARY", ["MINUS ", tIDENT])]),
                         tree("EXPRESSION", [tree("PRIMARY", ["INTLIT "]), tOPg, tree("PRIMARY", ["INTLIT "])])])
t26 = tree("EXPR_LIST", [tree("EXPRESSION", [tree("PRIMARY", ["STRINGLIT "])]),
                         tree("EXPRESSION", [tree("PRIMARY", ["STRINGLIT "])])])

array1 = [t1, t2, t3, t4, t5, t6, t7, t8, t9, t10, t11, t12, t13, t14, t15]
array2 = [t16, t17, t18, t19, t20, t21, t22, t23, t24, t25, t26]

count = 1
for t in array1:
    tASS = tree("ASSIGNMENT", [t])
    tSTM = tree("STATEMENT", [tASS])
    tSTML = tree("STATEMENT_LIST", [tSTM])
    TREE = tree("PROGRAM", ["BEGIN ", tree("STATEMENT_LIST", [t]), "END "])
    print(str(count) + "   " + str(TREE))
    print("\n")
    count = count + 1

for t in array2:
    tEXRL = tree("EXPR_LIST", ["WRITE ", t])
    tSTM = tree("STATEMENT", [tEXRL])
    tSTML = tree("STATEMENT_LIST", [t])
    TREE = tree("PROGRAM", ["BEGIN ", tree("STATEMENT_LIST", [t]), "END "])
    print(str(count) + "   " + str(TREE))
    print("\n")
    count = count + 1
