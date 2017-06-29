.data
dummya: .word 0
True: .asciiz "True"
False: .asciiz "False"
.text
#LESS THAN
li $t0, 2
li $t1, 1
bgt $t0, $t1, Labelc
li $t2, 0
sw $t2, dummya
j Labeld
Labelc:
li $t2, 1
sw $t2, dummya
Labeld:
