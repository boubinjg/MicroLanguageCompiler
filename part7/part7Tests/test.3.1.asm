.data
dummyk: .word 0
dummyai: .word 0
dummya: .space 64
dummyae: .word 0
dummyad: .word 0
dummyx: .word 0
dummyv: .word 0
dummyr: .word 0
dummyp: .word 0
dummyl: .word 0
dummyj: .word 0
dummyh: .word 0
dummyg: .word 0
True: .asciiz "True"
False: .asciiz "False"
i: .word 0
j: .word 0
x: .word 0
y: .word 0
z: .word 0
.text

li $t0,0
la $t1,i
sw $t0, 0($t1)

Labelc:
#LESS THAN
lw $t0, i
li $t1, 5
bge $t0, $t1, Labeli
li $t2, 1
sw $t2, dummyg
j Labelj
Labeli:
li $t2, 0
sw $t2, dummyg
Labelj:
lw $t0, dummyg
li $t1, 1
bne $t0, $t1, Labeld
li $t0,0
la $t1,j
sw $t0, 0($t1)

Labelm:
#LESS THAN
lw $t0, j
li $t1, 5
bge $t0, $t1, Labels
li $t2, 1
sw $t2, dummyg
j Labelt
Labels:
li $t2, 0
sw $t2, dummyg
Labelt:
lw $t0, dummyg
li $t1, 1
bne $t0, $t1, Labeln
la $s0, i
lw $t1, 0($s0)
la $s0, j
lw $t2, 0($s0)
add $t0, $t1, $t2
la $s0,dummyh
sw $t0, 0($s0)

la $s0, dummyh
lw $t1, 0($s0)
li $s0, 3
la $t0, 0($s0)
rem $t0, $t1, $t0
la $s0,dummyj
sw $t0, 0($s0)

li $t0, 0
lw $t1, dummyj
bne $t0, $t1, Labelw
li $t2, 1
sw $t2, dummyl
j Labelx
Labelw:
li $t2, 0
sw $t2, dummyl
Labelx:

la $t0,dummyl
la $t1,x
lw $t2, 0($t0)
sw $t2, 0($t1)

la $s0, i
lw $t1, 0($s0)
li $s0, 2
la $t0, 0($s0)
rem $t0, $t1, $t0
la $s0,dummyp
sw $t0, 0($s0)

li $t0, 0
lw $t1, dummyp
bne $t0, $t1, Labelaa
li $t2, 1
sw $t2, dummyr
j Labelab
Labelaa:
li $t2, 0
sw $t2, dummyr
Labelab:

la $t0,dummyr
la $t1,y
lw $t2, 0($t0)
sw $t2, 0($t1)

la $s0, j
lw $t1, 0($s0)
li $s0, 2
la $t0, 0($s0)
rem $t0, $t1, $t0
la $s0,dummyv
sw $t0, 0($s0)

li $t0, 0
lw $t1, dummyv
bne $t0, $t1, Labelae
li $t2, 1
sw $t2, dummyx
j Labelaf
Labelae:
li $t2, 0
sw $t2, dummyx
Labelaf:

la $t0,dummyx
la $t1,z
lw $t2, 0($t0)
sw $t2, 0($t1)

lw $t1, z
lw $t2, y
or $t0, $t1, $t2
sw $t0, dummyad

lw $t1, dummyad
lw $t2, x
and $t0, $t1, $t2
sw $t0, dummyae
lw $t0, dummyae
li $t1, 1
bne $t0, $t1, ifa

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

li $v0,1
lw $a0,j
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
ifa:

la $s0, j
lw $t1, 0($s0)
li $s0, 1
la $t2, 0($s0)
add $t0, $t1, $t2
la $s0,dummyai
sw $t0, 0($s0)

la $t0,dummyai
la $t1,j
lw $t2, 0($t0)
sw $t2, 0($t1)

j Labelm
Labeln:

la $s0, i
lw $t1, 0($s0)
li $s0, 1
la $t2, 0($s0)
add $t0, $t1, $t2
la $s0,dummyk
sw $t0, 0($s0)

la $t0,dummyk
la $t1,i
lw $t2, 0($t0)
sw $t2, 0($t1)

j Labelc
Labeld:
