.data
dummy2b: .word 0
dummy2a: .word 0
True: .asciiz "True"
False: .asciiz "False"
.text

li $s0, 40
la $t1, 0($s0)
li $s0, 20
la $t0, 0($s0)
sub $t0, $t1, $t0
la $s0,dummy2a
sw $t0, 0($s0)

la $s0, dummy2a
lw $t1, 0($s0)
li $s0, 2
la $t0, 0($s0)
sub $t0, $t1, $t0
la $s0,dummy2b
sw $t0, 0($s0)

li $v0,1
lw $a0,dummy2b
syscall
