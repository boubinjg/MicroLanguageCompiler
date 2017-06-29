.data
dummyf: .space 64
dummya: .space 64
True: .asciiz "True"
False: .asciiz "False"
x: .word 0
.text

li $t0,1
la $t1,x
sw $t0, 0($t1)
lw $t0, x
li $t1, 1
bne $t0, $t1, ifa

la $s0, dummya

li $t0, '"'
sb $t0, ($s0)
addi $s0, $s0, 1

li $t0, 'Y'
sb $t0, ($s0)
addi $s0, $s0, 1

li $t0, 'e'
sb $t0, ($s0)
addi $s0, $s0, 1

li $t0, 's'
sb $t0, ($s0)
addi $s0, $s0, 1

li $t0, ' '
sb $t0, ($s0)
addi $s0, $s0, 1

li $t0, '"'
sb $t0, ($s0)
addi $s0, $s0, 1

la $t0 dummya
move $a0, $t0
li $v0,4
syscall
ifa:

la $s0, dummyf

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

li $t0, 'e'
sb $t0, ($s0)
addi $s0, $s0, 1

li $t0, ' '
sb $t0, ($s0)
addi $s0, $s0, 1

li $t0, '"'
sb $t0, ($s0)
addi $s0, $s0, 1

la $t0 dummyf
move $a0, $t0
li $v0,4
syscall
