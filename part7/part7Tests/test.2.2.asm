.data
dummyf: .word 0
dummya: .space 64
dummyh: .word 0
True: .asciiz "True"
False: .asciiz "False"
n: .word 0
i: .word 0
.text

li $v0, 5
syscall
la $t0, n
sw $v0, 0($t0)

la $t0,n
la $t1,i
lw $t2, 0($t0)
sw $t2, 0($t1)

Labelc:
#GREATER THAN EQUAL
lw $t0, i
li $t1, 0
bge $t0, $t1, Labelg
li $t2, 0
sw $t2, dummyh
j Labelh
Labelg:
li $t2, 1
sw $t2, dummyh
Labelh:
lw $t0, dummyh
li $t1, 1
bne $t0, $t1, Labeld
li $v0,1
lw $a0,i
syscall

la $s0, dummya

li $t0, '"'
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

la $s0, i
lw $t1, 0($s0)
li $s0, 2
la $t0, 0($s0)
sub $t0, $t1, $t0
la $s0,dummyf
sw $t0, 0($s0)

la $t0,dummyf
la $t1,i
lw $t2, 0($t0)
sw $t2, 0($t1)

j Labelc
Labeld:
