.data
dummy2b: .word 0
dummy2a: .word 0
True: .asciiz "True"
False: .asciiz "False"
.text

li $t1, 0
li $t2, 1
xor $t0, $t1, $t2
sw $t0, dummy2a

lw $t1, dummy2a
li $t2, 1
and $t0, $t1, $t2
sw $t0, dummy2b

lw $t0, dummy2b
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
