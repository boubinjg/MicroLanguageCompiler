.data
dummy2d: .word 0
dummy2c: .word 0
dummy2b: .word 0
dummy2a: .word 0
True: .asciiz "True"
False: .asciiz "False"
.text

li $s0, 2
la $t1, 0($s0)
li $s0, 3
la $t0, 0($s0)
mul $t0, $t1, $t0
la $s0,dummy2a
sw $t0, 0($s0)

li $s0, 4
la $t1, 0($s0)
la $s0, dummy2a
lw $t2, 0($s0)
add $t0, $t1, $t2
la $s0,dummy2b
sw $t0, 0($s0)

li $v0,1
lw $a0,dummy2b
syscall

li $s0, 2
la $t1, 0($s0)
li $s0, 4
la $t2, 0($s0)
add $t0, $t1, $t2
la $s0,dummy2c
sw $t0, 0($s0)

la $s0, dummy2c
lw $t1, 0($s0)
li $s0, 3
la $t0, 0($s0)
mul $t0, $t1, $t0
la $s0,dummy2d
sw $t0, 0($s0)

li $v0,1
lw $a0,dummy2d
syscall
