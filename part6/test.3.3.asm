.data
x: .space 64
True: .asciiz "True"
False: .asciiz "False"
.text

la $s0, x

li $t0, '"'
sb $t0, ($s0)
addi $s0, $s0, 1

li $t0, 'H'
sb $t0, ($s0)
addi $s0, $s0, 1

li $t0, 'e'
sb $t0, ($s0)
addi $s0, $s0, 1

li $t0, 'l'
sb $t0, ($s0)
addi $s0, $s0, 1

li $t0, 'l'
sb $t0, ($s0)
addi $s0, $s0, 1

li $t0, 'o'
sb $t0, ($s0)
addi $s0, $s0, 1

li $t0, ','
sb $t0, ($s0)
addi $s0, $s0, 1

li $t0, ' '
sb $t0, ($s0)
addi $s0, $s0, 1

li $t0, 'w'
sb $t0, ($s0)
addi $s0, $s0, 1

li $t0, 'o'
sb $t0, ($s0)
addi $s0, $s0, 1

li $t0, 'r'
sb $t0, ($s0)
addi $s0, $s0, 1

li $t0, 'l'
sb $t0, ($s0)
addi $s0, $s0, 1

li $t0, 'd'
sb $t0, ($s0)
addi $s0, $s0, 1

li $t0, '"'
sb $t0, ($s0)
addi $s0, $s0, 1

la $t0 x
move $a0, $t0
li $v0,4
syscall
