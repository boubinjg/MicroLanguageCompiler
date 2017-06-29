.data
y: .space 64
True: .asciiz "True"
False: .asciiz "False"
x: .word 0
.text

li $t0,1
la $t1,x
sw $t0, 0($t1)

la $s0, y

li $t0, '"'
sb $t0, ($s0)
addi $s0, $s0, 1

li $t0, '2'
sb $t0, ($s0)
addi $s0, $s0, 1

li $t0, '"'
sb $t0, ($s0)
addi $s0, $s0, 1
