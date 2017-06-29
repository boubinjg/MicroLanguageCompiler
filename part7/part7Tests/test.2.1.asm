.data
dummyo: .space 64
dummyl: .word 0
dummyh: .word 0
dummyd: .word 0
dummyn: .word 0
True: .asciiz "True"
False: .asciiz "False"
n: .word 0
s: .word 0
p: .word 0
i: .word 0
.text

li $t0,1
la $t1,i
sw $t0, 0($t1)

li $t0,0
la $t1,s
sw $t0, 0($t1)

li $t0,1
la $t1,p
sw $t0, 0($t1)

li $v0, 5
syscall
la $t0, n
sw $v0, 0($t0)

Labelg:
#LESS THAN
lw $t0, i
lw $t1, n
bge $t0, $t1, Labelm
li $t2, 1
sw $t2, dummyn
j Labeln
Labelm:
li $t2, 0
sw $t2, dummyn
Labeln:
lw $t0, dummyn
li $t1, 1
bne $t0, $t1, Labelh
la $s0, s
lw $t1, 0($s0)
la $s0, i
lw $t2, 0($s0)
add $t0, $t1, $t2
la $s0,dummyd
sw $t0, 0($s0)

la $t0,dummyd
la $t1,s
lw $t2, 0($t0)
sw $t2, 0($t1)

la $s0, p
lw $t1, 0($s0)
la $s0, i
lw $t0, 0($s0)
mul $t0, $t1, $t0
la $s0,dummyh
sw $t0, 0($s0)

la $t0,dummyh
la $t1,p
lw $t2, 0($t0)
sw $t2, 0($t1)

la $s0, i
lw $t1, 0($s0)
li $s0, 1
la $t2, 0($s0)
add $t0, $t1, $t2
la $s0,dummyl
sw $t0, 0($s0)

la $t0,dummyl
la $t1,i
lw $t2, 0($t0)
sw $t2, 0($t1)

j Labelg
Labelh:

li $v0,1
lw $a0,s
syscall

la $s0, dummyo

li $t0, '"'
sb $t0, ($s0)
addi $s0, $s0, 1

li $t0, ' '
sb $t0, ($s0)
addi $s0, $s0, 1

li $t0, '"'
sb $t0, ($s0)
addi $s0, $s0, 1

la $t0 dummyo
move $a0, $t0
li $v0,4
syscall

li $v0,1
lw $a0,p
syscall

la $s0, dummyo

li $t0, '"'
sb $t0, ($s0)
addi $s0, $s0, 1

li $t0, ' '
sb $t0, ($s0)
addi $s0, $s0, 1

li $t0, '"'
sb $t0, ($s0)
addi $s0, $s0, 1

la $t0 dummyo
move $a0, $t0
li $v0,4
syscall
