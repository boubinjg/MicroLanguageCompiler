.data
dummybk: .space 64
dummybe: .space 64
dummyay: .space 64
dummyav: .word 0
dummyas: .space 64
dummyaq: .word 0
dummyaj: .space 64
dummyad: .space 64
dummyx: .space 64
dummyv: .word 0
dummym: .space 64
dummyk: .word 0
dummyd: .space 64
True: .asciiz "True"
False: .asciiz "False"
newline: .asciiz "\n"
xfoo3: .word 0
yfoo3: .word 0
xfoo2: .word 0
zfoo2: .word 0
xfoo1: .word 0
tfoo1: .word 0
xmain: .word 0
.text
j main

foo3:
addi $sp, $sp, -4
sw $ra, 0($sp)
la $s0, dummyd

li $t0, 'f'
sb $t0, ($s0)
addi $s0, $s0, 1

li $t0, 'o'
sb $t0, ($s0)
addi $s0, $s0, 1

li $t0, 'o'
sb $t0, ($s0)
addi $s0, $s0, 1

li $t0, '3'
sb $t0, ($s0)
addi $s0, $s0, 1

li $t0, ':'
sb $t0, ($s0)
addi $s0, $s0, 1

la $t0 dummyd
move $a0, $t0
li $v0,4
syscall

li $v0,1
lw $t0, xfoo3
 lw $a0, 0($t0)
syscall
li $v0,4 
la $a0, newline
syscall

li $v0, 5
syscall
la $t0, yfoo3
sw $v0, 0($t0)

lw $s0, xfoo3
lw $t1, 0($s0)
la $s0, yfoo3
lw $t2, 0($s0)
add $t0, $t1, $t2
la $s0,dummyk
sw $t0, 0($s0)

#In AssignPointerVal()
lw $t0, dummyk
lw $t1, xfoo3
sw $t0, 0($t1)

la $s0, dummym

li $t0, 'f'
sb $t0, ($s0)
addi $s0, $s0, 1

li $t0, 'o'
sb $t0, ($s0)
addi $s0, $s0, 1

li $t0, 'o'
sb $t0, ($s0)
addi $s0, $s0, 1

li $t0, '3'
sb $t0, ($s0)
addi $s0, $s0, 1

li $t0, ':'
sb $t0, ($s0)
addi $s0, $s0, 1

la $t0 dummym
move $a0, $t0
li $v0,4
syscall

li $v0,1
lw $t0, xfoo3
 lw $a0, 0($t0)
syscall
li $v0,4 
la $a0, newline
syscall

lw $s0, 0($sp)
addi $sp, $sp, 4
jr $s0

foo2:
addi $sp, $sp, -4
sw $ra, 0($sp)
li $v0, 5
syscall
la $t0, zfoo2
sw $v0, 0($t0)

lw $s0, xfoo2
lw $t1, 0($s0)
la $s0, zfoo2
lw $t2, 0($s0)
add $t0, $t1, $t2
la $s0,dummyv
sw $t0, 0($s0)

#In AssignPointerVal()
lw $t0, dummyv
lw $t1, xfoo2
sw $t0, 0($t1)

la $s0, dummyx

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

la $t0 dummyx
move $a0, $t0
li $v0,4
syscall

li $v0,1
lw $t0, xfoo2
 lw $a0, 0($t0)
syscall
li $v0,4 
la $a0, newline
syscall

la $t0,xfoo2
la $t1,xfoo3
lw $t2, 0($t0)
sw $t2, 0($t1)

jal foo3

la $s0, dummyad

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

la $t0 dummyad
move $a0, $t0
li $v0,4
syscall

li $v0,1
lw $t0, xfoo2
 lw $a0, 0($t0)
syscall
li $v0,4 
la $a0, newline
syscall

lw $s0, 0($sp)
addi $sp, $sp, 4
jr $s0

foo1:
addi $sp, $sp, -4
sw $ra, 0($sp)
li $v0, 5
syscall
la $t0, tfoo1
sw $v0, 0($t0)

la $s0, dummyaj

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

la $t0 dummyaj
move $a0, $t0
li $v0,4
syscall

li $v0,1
lw $t0, xfoo1
 lw $a0, 0($t0)
syscall
li $v0,4 
la $a0, newline
syscall

lw $s0, xfoo1
lw $t1, 0($s0)
la $s0, tfoo1
lw $t2, 0($s0)
mul $t0, $t1, $t2
la $s0,dummyaq
sw $t0, 0($s0)

#In AssignPointerVal()
lw $t0, dummyaq
lw $t1, xfoo1
sw $t0, 0($t1)

la $s0, dummyas

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

la $t0 dummyas
move $a0, $t0
li $v0,4
syscall

li $v0,1
lw $t0, xfoo1
 lw $a0, 0($t0)
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
la $t0, xmain
sw $v0, 0($t0)

la $s0, dummyay

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

la $t0 dummyay
move $a0, $t0
li $v0,4
syscall

li $v0,1
lw $a0,xmain
syscall
li $v0,4 
la $a0, newline
syscall

la $t0,xmain
la $t1,xfoo1
la $t2, 0($t0)
sw $t2, 0($t1)

jal foo1

la $s0, dummybe

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

la $t0 dummybe
move $a0, $t0
li $v0,4
syscall

li $v0,1
lw $a0,xmain
syscall
li $v0,4 
la $a0, newline
syscall

la $t0,xmain
la $t1,xfoo2
la $t2, 0($t0)
sw $t2, 0($t1)

jal foo2

la $s0, dummybk

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

la $t0 dummybk
move $a0, $t0
li $v0,4
syscall

li $v0,1
lw $a0,xmain
syscall
li $v0,4 
la $a0, newline
syscall

li $t0,0
la $t1,dummyav
sw $t0, 0($t1)

li $v0, 10
syscall
