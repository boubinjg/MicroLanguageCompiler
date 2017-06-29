.data
dummya: .space 64
dummyf: .word 0
dummyd: .word 0
dummyb: .word 0
True: .asciiz "True"
False: .asciiz "False"
.text
li $t0, 1
li $t1, 1
bne $t0, $t1, ifa

li $t1, 0
li $t2, 1
xor $t0, $t1, $t2
sw $t0, dummyb
lw $t0, dummyb
li $t1, 1
bne $t0, $t1, ifb

li $t1, 1
li $t2, 0
or $t0, $t1, $t2
sw $t0, dummyd
lw $t0, dummyd
li $t1, 1
bne $t0, $t1, ifc

li $t1, 1
li $t2, 0
or $t0, $t1, $t2
sw $t0, dummyf

lw $t1, dummyf
li $t2, 1
xor $t0, $t1, $t2
sw $t0, dummyb
lw $t0, dummyb
li $t1, 1
bne $t0, $t1, ifd

li $t1, 1
li $t2, 0
or $t0, $t1, $t2
sw $t0, dummyd

lw $t1, dummyd
li $t2, 0
and $t0, $t1, $t2
sw $t0, dummyf
lw $t0, dummyf
li $t1, 1
bne $t0, $t1, ife

la $s0, dummya

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

li $t0, '"'
sb $t0, ($s0)
addi $s0, $s0, 1

la $t0 dummya
move $a0, $t0
li $v0,4
syscall
ife:
ifd:
ifc:
ifb:
ifa:
