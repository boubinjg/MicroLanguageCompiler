.data
dummyf: .space 64
dummyd: .word 0
dummye: .word 0
True: .asciiz "True"
False: .asciiz "False"
i: .word 0
.text

li $v0, 5
syscall
la $t0, i
sw $v0, 0($t0)
#GREATER THAN EQUAL
lw $t0, i
li $t1, 5
bge $t0, $t1, Labelc
li $t2, 0
sw $t2, dummye
j Labeld
Labelc:
li $t2, 1
sw $t2, dummye
Labeld:
lw $t0, dummye
li $t1, 1
bne $t0, $t1, ifa

la $s0, i
lw $t1, 0($s0)
la $s0, i
lw $t0, 0($s0)
mul $t0, $t1, $t0
la $s0,dummyd
sw $t0, 0($s0)

la $t0,dummyd
la $t1,i
lw $t2, 0($t0)
sw $t2, 0($t1)

li $v0,1
lw $a0,i
syscall

la $s0, dummye

li $t0, '"'
sb $t0, ($s0)
addi $s0, $s0, 1

li $t0, ' '
sb $t0, ($s0)
addi $s0, $s0, 1

li $t0, '"'
sb $t0, ($s0)
addi $s0, $s0, 1

la $t0 dummye
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

li $t0, '"'
sb $t0, ($s0)
addi $s0, $s0, 1

la $t0 dummyf
move $a0, $t0
li $v0,4
syscall
