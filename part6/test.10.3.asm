.data
y: .space 64
True: .asciiz "True"
False: .asciiz "False"
x: .word 0
.text

la $s0, y

li $t0, '"'
sb $t0, ($s0)
addi $s0, $s0, 1

li $t0, 'H'
sb $t0, ($s0)
addi $s0, $s0, 1

li $t0, 'e'
sb $t0, ($s0)
addi $s0, $s0, 1

li $t0, 'r'
sb $t0, ($s0)
addi $s0, $s0, 1

li $t0, 'e'
sb $t0, ($s0)
addi $s0, $s0, 1

li $t0, ' '
sb $t0, ($s0)
addi $s0, $s0, 1

li $t0, 'i'
sb $t0, ($s0)
addi $s0, $s0, 1

li $t0, 's'
sb $t0, ($s0)
addi $s0, $s0, 1

li $t0, ' '
sb $t0, ($s0)
addi $s0, $s0, 1

li $t0, 't'
sb $t0, ($s0)
addi $s0, $s0, 1

li $t0, 'h'
sb $t0, ($s0)
addi $s0, $s0, 1

li $t0, 'e'
sb $t0, ($s0)
addi $s0, $s0, 1

li $t0, ' '
sb $t0, ($s0)
addi $s0, $s0, 1

li $t0, 's'
sb $t0, ($s0)
addi $s0, $s0, 1

li $t0, 't'
sb $t0, ($s0)
addi $s0, $s0, 1

li $t0, 'r'
sb $t0, ($s0)
addi $s0, $s0, 1

li $t0, 'i'
sb $t0, ($s0)
addi $s0, $s0, 1

li $t0, 'n'
sb $t0, ($s0)
addi $s0, $s0, 1

li $t0, 'g'
sb $t0, ($s0)
addi $s0, $s0, 1

li $t0, '.'
sb $t0, ($s0)
addi $s0, $s0, 1

li $t0, '"'
sb $t0, ($s0)
addi $s0, $s0, 1

la $t0,string
la $t1,x
lw $t2, 0($t0)
sw $t2, 0($t1)
