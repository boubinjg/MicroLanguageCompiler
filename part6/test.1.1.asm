.data
True: .asciiz "True"
False: .asciiz "False"
x: .word 0
.text

li $t0,1
la $t1,x
sw $t0, 0($t1)

li $v0,1
lw $a0,x
syscall
