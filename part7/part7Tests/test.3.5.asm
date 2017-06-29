.data
dummya: .space 64
True: .asciiz "True"
False: .asciiz "False"
.text

la $s0, dummya

li $t0, '"'
sb $t0, ($s0)
addi $s0, $s0, 1

li $t0, 'D'
sb $t0, ($s0)
addi $s0, $s0, 1

li $t0, 'o'
sb $t0, ($s0)
addi $s0, $s0, 1

li $t0, 'n'
sb $t0, ($s0)
addi $s0, $s0, 1

li $t0, '\''
sb $t0, ($s0)
addi $s0, $s0, 1

li $t0, 't'
sb $t0, ($s0)
addi $s0, $s0, 1

li $t0, ' '
sb $t0, ($s0)
addi $s0, $s0, 1

li $t0, 'p'
sb $t0, ($s0)
addi $s0, $s0, 1

li $t0, 'a'
sb $t0, ($s0)
addi $s0, $s0, 1

li $t0, 'n'
sb $t0, ($s0)
addi $s0, $s0, 1

li $t0, 'i'
sb $t0, ($s0)
addi $s0, $s0, 1

li $t0, 'c'
sb $t0, ($s0)
addi $s0, $s0, 1

li $t0, '.'
sb $t0, ($s0)
addi $s0, $s0, 1

li $t0, '"'
sb $t0, ($s0)
addi $s0, $s0, 1

la $t0 dummya
move $a0, $t0
li $v0,4
syscall
