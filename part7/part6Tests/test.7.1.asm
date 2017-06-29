.data
dummyp: .word 0
dummyl: .word 0
dummyh: .word 0
dummyd: .word 0
True: .asciiz "True"
False: .asciiz "False"
.text

li $t1, 1
li $t2, 1
or $t0, $t1, $t2
sw $t0, dummyd

lw $t0, dummyd
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

li $t1, 1
li $t2, 0
or $t0, $t1, $t2
sw $t0, dummyh

lw $t0, dummyh
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

li $t1, 0
li $t2, 1
or $t0, $t1, $t2
sw $t0, dummyl

lw $t0, dummyl
li $t1, 1
bne $t1, $t0, Labelk
li $v0, 4
la $a0 True
syscall
j Labell
Labelk:
li $v0, 4
la $a0, False
syscall
Labell:

li $t1, 0
li $t2, 0
or $t0, $t1, $t2
sw $t0, dummyp

lw $t0, dummyp
li $t1, 1
bne $t1, $t0, Labelo
li $v0, 4
la $a0 True
syscall
j Labelp
Labelo:
li $v0, 4
la $a0, False
syscall
Labelp:
