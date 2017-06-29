.data
y: .word 0
x: .word 0
.text

li $t0,5
la $t1,x
sw $t0, 0($t1)

la $s0, x
lw $t1, 0($s0)
la $s0, x
lw $t2, 0($s0)
sub $t0, $t1, $t2
la $s0,y
sw $t0, 0($s0)

li $v0,1
lw $a0,y
syscall
