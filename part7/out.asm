.data
dummyd: .space 64
dummyc: .space 64
dummyb: .space 64
dummya: .space 64
True: .asciiz "True"
False: .asciiz "False"
.text

la $s0, dummya

li $t0, 't'
sb $t0, ($s0)
addi $s0, $s0, 1

li $t0, 'e'
sb $t0, ($s0)
addi $s0, $s0, 1

li $t0, 's'
sb $t0, ($s0)
addi $s0, $s0, 1

li $t0, 't'
sb $t0, ($s0)
addi $s0, $s0, 1

la $t0 dummya
move $a0, $t0
li $v0,4
syscall

la $s0, dummyb

li $t0, 'T'
sb $t0, ($s0)
addi $s0, $s0, 1

li $t0, 'r'
sb $t0, ($s0)
addi $s0, $s0, 1

li $t0, 'u'
sb $t0, ($s0)
addi $s0, $s0, 1

li $t0, 'e'
sb $t0, ($s0)
addi $s0, $s0, 1

la $t0 dummyb
move $a0, $t0
li $v0,4
syscall

la $s0, dummyc

li $t0, 't'
sb $t0, ($s0)
addi $s0, $s0, 1

li $t0, 'e'
sb $t0, ($s0)
addi $s0, $s0, 1

li $t0, 's'
sb $t0, ($s0)
addi $s0, $s0, 1

li $t0, 't'
sb $t0, ($s0)
addi $s0, $s0, 1

la $t0 dummyc
move $a0, $t0
li $v0,4
syscall

la $s0, dummyd

li $t0, 'F'
sb $t0, ($s0)
addi $s0, $s0, 1

li $t0, 'a'
sb $t0, ($s0)
addi $s0, $s0, 1

li $t0, 'l'
sb $t0, ($s0)
addi $s0, $s0, 1

li $t0, 's'
sb $t0, ($s0)
addi $s0, $s0, 1

li $t0, 'e'
sb $t0, ($s0)
addi $s0, $s0, 1

la $t0 dummyd
move $a0, $t0
li $v0,4
syscall
