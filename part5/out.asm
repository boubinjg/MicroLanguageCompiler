.data
x: .word 0
y: .word 0
.text

li $t0,2
la $t1,x
sw $t0, 0($t1)

li $t0,3
la $t1,y
sw $t0, 0($t1)

li $v0, 5
syscall
la $t0, x
sw $v0, 0($t0)

li $v0, 5
syscall
la $t0, y
sw $v0, 0($t0)

li $v0,1
lw $a0,x
syscall

li $v0,1
lw $a0,y
syscall
