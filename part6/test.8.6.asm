.data
dummy2b: .word 0
dummy2a: .word 0
True: .asciiz "True"
False: .asciiz "False"
.text

li $t0, 5
li $t1, 5
bne $t0, $t1, Labela
li $t2, 0
sw $t2, dummy2a
j Labelb
Labela:
li $t2, 1
sw $t2, dummy2a
Labelb:

lw $t0, dummy2a
li $t1, 1
bne $t1, $t0, Labelc
li $v0, 4
la $a0 True
syscall
j Labeld
Labelc:
li $v0, 4
la $a0, False
syscall
Labeld:

li $t0, 10
li $t1, 5
bne $t0, $t1, Labele
li $t2, 0
sw $t2, dummy2b
j Labelf
Labele:
li $t2, 1
sw $t2, dummy2b
Labelf:

lw $t0, dummy2b
li $t1, 1
bne $t1, $t0, Labelg
li $v0, 4
la $a0 True
syscall
j Labelh
Labelg:
li $v0, 4
la $a0, False
syscall
Labelh:
