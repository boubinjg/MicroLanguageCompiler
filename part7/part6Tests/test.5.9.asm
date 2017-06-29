.data
dummyh: .word 0
dummye: .word 0
dummyb: .word 0
True: .asciiz "True"
False: .asciiz "False"
.text

li $s0, 0
la $t1, 0($s0)
li $s0, 2
la $t0, 0($s0)
sub $t0, $t1, $t0
la $s0,dummyb
sw $t0, 0($s0)

li $v0,1
lw $a0,dummyb
syscall

li $s0, 0
la $t1, 0($s0)
li $s0, 2
la $t0, 0($s0)
sub $t0, $t1, $t0
la $s0,dummye
sw $t0, 0($s0)

la $s0, dummye
lw $t1, 0($s0)
li $s0, 3
la $t2, 0($s0)
add $t0, $t1, $t2
la $s0,dummyh
sw $t0, 0($s0)

li $v0,1
lw $a0,dummyh
syscall
