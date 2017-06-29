.data
dummy2b: .word 0
dummy2a: .word 0
True: .asciiz "True"
False: .asciiz "False"
.text

la $s0, dummy2b
lw $t1, 0($s0)
li $s0, 5
la $t2, 0($s0)
add $t0, $t1, $t2
la $s0,dummy2b
sw $t0, 0($s0)

li $v0,1
lw $a0,dummy2b
syscall
