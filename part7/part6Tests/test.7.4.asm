.data
dummyl: .word 0
dummyj: .word 0
dummyf: .word 0
dummyd: .word 0
True: .asciiz "True"
False: .asciiz "False"
.text

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
li $t2, 0
and $t0, $t1, $t2
sw $t0, dummyj

lw $t1, dummyj
li $t2, 1
or $t0, $t1, $t2
sw $t0, dummyl

lw $t0, dummyl
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
