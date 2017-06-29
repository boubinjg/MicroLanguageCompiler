.data
dummye: .word 0
dummya: .word 0
True: .asciiz "True"
False: .asciiz "False"
.text

li $t1, 1
li $t2, 0
or $t0, $t1, $t2
sw $t0, dummya

lw $t1, dummya
li $t2, 0
and $t0, $t1, $t2
sw $t0, dummya

lw $t0, dummya
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
sw $t0, dummye

lw $t1, dummye
li $t2, 1
or $t0, $t1, $t2
sw $t0, dummye

lw $t0, dummye
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
