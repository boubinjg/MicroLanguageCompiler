.data
dummybh: .space 64
dummyat: .word 0
dummyap: .space 64
dummyan: .word 0
dummyad: .word 0
dummys: .space 64
dummyq: .word 0
dummyh: .space 64
dummyf: .word 0
dummya: .word 0
True: .asciiz "True"
False: .asciiz "False"
newline: .asciiz "\n"
xfoo1: .word 0
yfoo1: .word 0
xfoo2: .word 0
bfoo2: .word 0
afoo2: .word 0
amain: .word 0
bmain: .word 0
cmain: .word 0
.text
j main

foo1:
addi $sp, $sp, -4
sw $ra, 0($sp)
lw $s0, xfoo1
lw $t1, 0($s0)
li $s0, 1
la $t2, 0($s0)
add $t0, $t1, $t2
la $s0,dummyf
sw $t0, 0($s0)

#In AssignPointerVal()
lw $t0, dummyf
lw $t1, xfoo1
sw $t0, 0($t1)

la $s0, dummyh

li $t0, 'f'
sb $t0, ($s0)
addi $s0, $s0, 1

li $t0, 'o'
sb $t0, ($s0)
addi $s0, $s0, 1

li $t0, 'o'
sb $t0, ($s0)
addi $s0, $s0, 1

li $t0, '1'
sb $t0, ($s0)
addi $s0, $s0, 1

li $t0, ':'
sb $t0, ($s0)
addi $s0, $s0, 1

la $t0 dummyh
move $a0, $t0
li $v0,4
syscall

li $v0,1
lw $t0, xfoo1
 lw $a0, 0($t0)
syscall

li $v0,1
lw $t0, yfoo1
 lw $a0, 0($t0)
syscall
li $v0,4 
la $a0, newline
syscall

lw $s0, yfoo1
lw $t1, 0($s0)
li $s0, 1
la $t2, 0($s0)
add $t0, $t1, $t2
la $s0,dummyq
sw $t0, 0($s0)

#In AssignPointerVal()
lw $t0, dummyq
lw $t1, yfoo1
sw $t0, 0($t1)

la $s0, dummys

li $t0, 'f'
sb $t0, ($s0)
addi $s0, $s0, 1

li $t0, 'o'
sb $t0, ($s0)
addi $s0, $s0, 1

li $t0, 'o'
sb $t0, ($s0)
addi $s0, $s0, 1

li $t0, '1'
sb $t0, ($s0)
addi $s0, $s0, 1

li $t0, ':'
sb $t0, ($s0)
addi $s0, $s0, 1

la $t0 dummys
move $a0, $t0
li $v0,4
syscall

li $v0,1
lw $t0, xfoo1
 lw $a0, 0($t0)
syscall

li $v0,1
lw $t0, yfoo1
 lw $a0, 0($t0)
syscall
li $v0,4 
la $a0, newline
syscall

lw $s0, xfoo1
lw $t1, 0($s0)
lw $s0, yfoo1
lw $t2, 0($s0)
add $t0, $t1, $t2
la $s0,dummyad
sw $t0, 0($s0)

lw $t0,dummyad
la $t1,dummya
la $t2, 0($t0)
sw $t2, 0($t1)

lw $s0, 0($sp)
addi $sp, $sp, 4
jr $s0

foo2:
addi $sp, $sp, -4
sw $ra, 0($sp)
li $v0, 5
syscall
la $t0, bfoo2
sw $v0, 0($t0)

lw $t0,xfoo2
la $t1,afoo2
lw $t2, 0($t0)
sw $t2, 0($t1)

la $s0, afoo2
lw $t1, 0($s0)
la $s0, bfoo2
lw $t2, 0($s0)
add $t0, $t1, $t2
la $s0,dummyan
sw $t0, 0($s0)

la $t0,dummyan
la $t1,afoo2
lw $t2, 0($t0)
sw $t2, 0($t1)

la $s0, dummyap

li $t0, 'f'
sb $t0, ($s0)
addi $s0, $s0, 1

li $t0, 'o'
sb $t0, ($s0)
addi $s0, $s0, 1

li $t0, 'o'
sb $t0, ($s0)
addi $s0, $s0, 1

li $t0, '2'
sb $t0, ($s0)
addi $s0, $s0, 1

li $t0, ':'
sb $t0, ($s0)
addi $s0, $s0, 1

la $t0 dummyap
move $a0, $t0
li $v0,4
syscall

li $v0,1
lw $t0, xfoo2
 lw $a0, 0($t0)
syscall

li $v0,1
lw $a0,afoo2
syscall
li $v0,4 
la $a0, newline
syscall

lw $s0, 0($sp)
addi $sp, $sp, 4
jr $s0

main:
addi $sp, $sp, -4
sw $ra, 0($sp)
li $v0, 5
syscall
la $t0, amain
sw $v0, 0($t0)
#Parameter Assignment?
la $t0,amain
la $t1,xfoo1
la $t2, 0($t0)
sw $t2, 0($t1)

la $t0,amain
la $t1,yfoo1
la $t2, 0($t0)
sw $t2, 0($t1)

jal foo1

lw $t0,dummya
la $t1,bmain
la $t2, 0($t0)
sw $t2, 0($t1)

la $s0, dummybh

li $t0, 'm'
sb $t0, ($s0)
addi $s0, $s0, 1

li $t0, 'a'
sb $t0, ($s0)
addi $s0, $s0, 1

li $t0, 'i'
sb $t0, ($s0)
addi $s0, $s0, 1

li $t0, 'n'
sb $t0, ($s0)
addi $s0, $s0, 1

li $t0, ':'
sb $t0, ($s0)
addi $s0, $s0, 1

la $t0 dummybh
move $a0, $t0
li $v0,4
syscall

li $v0,1
lw $a0,amain
syscall

li $v0,1
lw $a0,bmain
syscall
li $v0,4 
la $a0, newline
syscall

li $v0, 5
syscall
la $t0, cmain
sw $v0, 0($t0)

la $t0,cmain
la $t1,xfoo2
la $t2, 0($t0)
sw $t2, 0($t1)

jal foo2

li $t0,0
la $t1,dummyat
sw $t0, 0($t1)

li $v0, 10
syscall
