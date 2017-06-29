.data
dummyl: .word 0
dummyh: .word 0
dummyd: .word 0
True: .asciiz "True"
False: .asciiz "False"
.text
#GREATER THAN EQUAL
li $t0, 5
li $t1, 10
bge $t0, $t1, Labelc
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
#GREATER THAN EQUAL
li $t0, 5
li $t1, 5
bge $t0, $t1, Labeli
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
#GREATER THAN EQUAL
li $t0, 5
li $t1, 0
bge $t0, $t1, Labelo
li $t2, 0
sw $t2, dummyl
j Labelp
Labelo:
li $t2, 1
sw $t2, dummyl
Labelp:

lw $t0, dummyl
li $t1, 1
bne $t1, $t0, Labelq
li $v0, 4
la $a0 True
syscall
j Labelr
Labelq:
li $v0, 4
la $a0, False
syscall
Labelr:
