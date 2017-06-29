.data
True: .asciiz "True"
False: .asciiz "False"
x: .word 0
.text

li $t0,0
la $t1,x
sw $t0, 0($t1)

lw $t0, x
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
