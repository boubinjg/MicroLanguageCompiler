.data
dummye: .word 0
dummyc: .word 0
True: .asciiz "True"
False: .asciiz "False"
.text

li $s0, 0
la $t1, 0($s0)
li $s0, 3
la $t0, 0($s0)
sub $t0, $t1, $t0
la $s0,dummyc
sw $t0, 0($s0)

li $s0, 5
la $t1, 0($s0)
la $s0, dummyc
lw $t0, 0($s0)
sub $t0, $t1, $t0
la $s0,dummye
sw $t0, 0($s0)

li $v0,1
lw $a0,dummye
syscall
