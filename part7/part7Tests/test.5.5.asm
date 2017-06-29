.data
dummyf: .word 0
dummyd: .word 0
True: .asciiz "True"
False: .asciiz "False"
.text

li $s0, 40
la $t1, 0($s0)
li $s0, 20
la $t0, 0($s0)
div $t0, $t1, $t0
la $s0,dummyd
sw $t0, 0($s0)

la $s0, dummyd
lw $t1, 0($s0)
li $s0, 2
la $t0, 0($s0)
div $t0, $t1, $t0
la $s0,dummyf
sw $t0, 0($s0)

li $v0,1
lw $a0,dummyf
syscall
