.data
dummyl: .word 0
dummyh: .word 0
dummyd: .word 0
True: .asciiz "True"
False: .asciiz "False"
.text
#LESS THAN
li $t0, 5
li $t1, 10
bge $t0, $t1, Labele
li $t2, 1
sw $t2, dummyd
j Labelf
Labele:
li $t2, 0
sw $t2, dummyd
Labelf:

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
#LESS THAN
li $t0, 5
li $t1, 5
bge $t0, $t1, Labelm
li $t2, 1
sw $t2, dummyh
j Labeln
Labelm:
li $t2, 0
sw $t2, dummyh
Labeln:

lw $t0, dummyh
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
#LESS THAN
li $t0, 5
li $t1, 0
bge $t0, $t1, Labelu
li $t2, 1
sw $t2, dummyl
j Labelv
Labelu:
li $t2, 0
sw $t2, dummyl
Labelv:

lw $t0, dummyl
li $t1, 1
bne $t1, $t0, Labelw
li $v0, 4
la $a0 True
syscall
j Labelx
Labelw:
li $v0, 4
la $a0, False
syscall
Labelx:
