.data
True: .asciiz "True"
False: .asciiz "False"
x: .word 0
y: .word 0
z: .word 0
.text

li $t0,1
la $t1,x
sw $t0, 0($t1)

li $t0,5
la $t1,y
sw $t0, 0($t1)

lw $t1, bool
lw $t2, int
or $t0, $t1, $t2
sw $t0, y

la $t0,y
la $t1,z
lw $t2, 0($t0)
sw $t2, 0($t1)
