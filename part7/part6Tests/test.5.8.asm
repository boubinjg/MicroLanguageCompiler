.data
dummyn: .word 0
dummym: .word 0
dummyg: .word 0
dummye: .word 0
True: .asciiz "True"
False: .asciiz "False"
.text

li $s0, 2
la $t1, 0($s0)
li $s0, 3
la $t2, 0($s0)
add $t0, $t1, $t2
la $s0,dummye
sw $t0, 0($s0)

la $s0, dummye
lw $t1, 0($s0)
li $s0, 4
la $t0, 0($s0)
mul $t0, $t1, $t0
la $s0,dummyg
sw $t0, 0($s0)

li $v0,1
lw $a0,dummyg
syscall

li $s0, 2
la $t1, 0($s0)
li $s0, 3
la $t0, 0($s0)
mul $t0, $t1, $t0
la $s0,dummym
sw $t0, 0($s0)

li $s0, 6
la $t1, 0($s0)
la $s0, dummym
lw $t0, 0($s0)
div $t0, $t1, $t0
la $s0,dummyn
sw $t0, 0($s0)

li $v0,1
lw $a0,dummyn
syscall
