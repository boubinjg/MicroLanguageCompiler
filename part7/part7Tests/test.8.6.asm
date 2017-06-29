.data
dummyh: .word 0
dummyd: .word 0
True: .asciiz "True"
False: .asciiz "False"
.text

li $t0, 5
li $t1, 5
bne $t0, $t1, Labelc
li $t2, 0
sw $t2, dummyd
j Labeld
Labelc:
li $t2, 1
sw $t2, dummyd
Labeld:

lw $t0, dummyd
li $t1, 1
bne $t1, $t0, Labele
li $v0, 4
la $a0 True
syscall
j Labelf
Labele:
li $v0, 4
la $a0, False
syscall
Labelf:

li $t0, 10
li $t1, 5
bne $t0, $t1, Labeli
li $t2, 0
sw $t2, dummyh
j Labelj
Labeli:
li $t2, 1
sw $t2, dummyh
Labelj:

lw $t0, dummyh
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
