.data
dummy2d: .word 0
dummy2c: .word 0
dummy2b: .word 0
dummy2a: .word 0
True: .asciiz "True"
False: .asciiz "False"
.text

li $t1, 1
li $t2, 1
or $t0, $t1, $t2
sw $t0, dummy2a

lw $t0, dummy2a
li $t1, 1
bne $t1, $t0, Labela
li $v0, 4
la $a0 True
syscall
j Labelb
Labela:
li $v0, 4
la $a0, False
syscall
Labelb:

li $t1, 1
li $t2, 0
or $t0, $t1, $t2
sw $t0, dummy2b

lw $t0, dummy2b
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

li $t1, 0
li $t2, 1
or $t0, $t1, $t2
sw $t0, dummy2c

lw $t0, dummy2c
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

li $t1, 0
li $t2, 0
or $t0, $t1, $t2
sw $t0, dummy2d

lw $t0, dummy2d
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
