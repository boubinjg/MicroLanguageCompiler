.data
dummyj: .word 0
dummyi: .word 0
dummye: .word 0
True: .asciiz "True"
False: .asciiz "False"
.text
#LESS THAN
li $t0, 1
li $t1, 2
bge $t0, $t1, Labele
li $t2, 1
sw $t2, dummye
j Labelf
Labele:
li $t2, 0
sw $t2, dummye
Labelf:
#LESS THAN
li $t0, 3
li $t1, 4
bge $t0, $t1, Labeli
li $t2, 1
sw $t2, dummyi
j Labelj
Labeli:
li $t2, 0
sw $t2, dummyi
Labelj:

lw $t1, dummyi
lw $t2, dummye
or $t0, $t1, $t2
sw $t0, dummyj

lw $t0, dummyj
li $t1, 1
bne $t1, $t0, Labelk
li $v0, 4
la $a0 True
syscall
j Labell
Labelk:
li $v0, 4
la $a0, False
syscall
Labell:
