.data
dummyd: .word 0
dummyb: .word 0
True: .asciiz "True"
False: .asciiz "False"
.text

li $t1, 1
li $t2, 1
xor $t0, $t1, $t2
sw $t0, dummyb

lw $t0, dummyb
li $t1, 1
bne $t1, $t0, Labelc
li $v0, 4
la $a0 True
syscall
j Labeld
Labelc:
li $v0, 4
la $a0, False
syscall
Labeld:

li $t1, 0
li $t2, 1
xor $t0, $t1, $t2
sw $t0, dummyd

lw $t0, dummyd
li $t1, 1
bne $t1, $t0, Labelg
li $v0, 4
la $a0 True
syscall
j Labelh
Labelg:
li $v0, 4
la $a0, False
syscall
Labelh:
