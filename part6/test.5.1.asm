.data
dummy2a: .word 0
True: .asciiz "True"
False: .asciiz "False"
.text

li $s0, 6
la $t1, 0($s0)
li $s0, 7
la $t0, 0($s0)
mul $t0, $t1, $t0
la $s0,dummy2a
sw $t0, 0($s0)

li $v0,1
lw $a0,dummy2a
syscall
