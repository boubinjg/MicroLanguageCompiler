.data
dummyf: .word 0
dummyd: .word 0
dummyb: .word 0
True: .asciiz "True"
False: .asciiz "False"
.text

li $s0, 0
la $t1, 0($s0)
li $s0, 5
la $t0, 0($s0)
sub $t0, $t1, $t0
la $s0,dummyb
sw $t0, 0($s0)

li $s0, 0
la $t1, 0($s0)
li $s0, 3
la $t0, 0($s0)
sub $t0, $t1, $t0
la $s0,dummyd
sw $t0, 0($s0)

la $s0, dummyb
lw $t1, 0($s0)
la $s0, dummyd
lw $t0, 0($s0)
sub $t0, $t1, $t0
la $s0,dummyf
sw $t0, 0($s0)

li $v0,1
lw $a0,dummyf
syscall
