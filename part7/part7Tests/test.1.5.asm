.data
dummya: .space 64
dummye: .word 0
True: .asciiz "True"
False: .asciiz "False"
i: .word 0
.text

li $v0, 5
syscall
la $t0, i
sw $v0, 0($t0)
#LESS THAN
lw $t0, i
li $t1, 15
bge $t0, $t1, Labele
li $t2, 1
sw $t2, dummye
j Labelf
Labele:
li $t2, 0
sw $t2, dummye
Labelf:
lw $t0, dummye
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

li $t0, '"'
sb $t0, ($s0)
addi $s0, $s0, 1

la $t0 dummya
move $a0, $t0
li $v0,4
syscall
j elsea
ifa:

la $s0, dummya

li $t0, '"'
sb $t0, ($s0)
addi $s0, $s0, 1

li $t0, 'N'
sb $t0, ($s0)
addi $s0, $s0, 1

li $t0, 'o'
sb $t0, ($s0)
addi $s0, $s0, 1

li $t0, '"'
sb $t0, ($s0)
addi $s0, $s0, 1

la $t0 dummya
move $a0, $t0
li $v0,4
syscall
elsea:
