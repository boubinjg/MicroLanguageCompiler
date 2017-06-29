.data
dummyaf: .word 0
dummyae: .word 0
dummyab: .word 0
dummyx: .word 0
dummyw: .word 0
dummyt: .word 0
dummyp: .word 0
dummyo: .word 0
dummyl: .word 0
dummyh: .word 0
dummyg: .word 0
dummyd: .word 0
True: .asciiz "True"
False: .asciiz "False"
.text
#LESS THAN
li $t0, 1
li $t1, 2
bge $t0, $t1, Labele
li $t2, 1
sw $t2, dummyd
j Labelf
Labele:
li $t2, 0
sw $t2, dummyd
Labelf:
#LESS THAN
li $t0, 3
li $t1, 4
bge $t0, $t1, Labeli
li $t2, 1
sw $t2, dummyg
j Labelj
Labeli:
li $t2, 0
sw $t2, dummyg
Labelj:

lw $t1, dummyg
lw $t2, dummyd
or $t0, $t1, $t2
sw $t0, dummyh

lw $t0, dummyh
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
#GREATER THAN
li $t0, 1
li $t1, 2
bgt $t0, $t1, Labelo
li $t2, 0
sw $t2, dummyl
j Labelp
Labelo:
li $t2, 1
sw $t2, dummyl
Labelp:
#LESS THAN
li $t0, 3
li $t1, 4
bge $t0, $t1, Labels
li $t2, 1
sw $t2, dummyo
j Labelt
Labels:
li $t2, 0
sw $t2, dummyo
Labelt:

lw $t1, dummyo
lw $t2, dummyl
or $t0, $t1, $t2
sw $t0, dummyp

lw $t0, dummyp
li $t1, 1
bne $t1, $t0, Labelu
li $v0, 4
la $a0 True
syscall
j Labelv
Labelu:
li $v0, 4
la $a0, False
syscall
Labelv:
#LESS THAN
li $t0, 1
li $t1, 2
bge $t0, $t1, Labelaa
li $t2, 1
sw $t2, dummyt
j Labelab
Labelaa:
li $t2, 0
sw $t2, dummyt
Labelab:
#GREATER THAN
li $t0, 3
li $t1, 4
bgt $t0, $t1, Labelac
li $t2, 0
sw $t2, dummyw
j Labelad
Labelac:
li $t2, 1
sw $t2, dummyw
Labelad:

lw $t1, dummyw
lw $t2, dummyt
or $t0, $t1, $t2
sw $t0, dummyx

lw $t0, dummyx
li $t1, 1
bne $t1, $t0, Labelae
li $v0, 4
la $a0 True
syscall
j Labelaf
Labelae:
li $v0, 4
la $a0, False
syscall
Labelaf:
#GREATER THAN
li $t0, 1
li $t1, 2
bgt $t0, $t1, Labelai
li $t2, 0
sw $t2, dummyab
j Labelaj
Labelai:
li $t2, 1
sw $t2, dummyab
Labelaj:
#GREATER THAN
li $t0, 3
li $t1, 4
bgt $t0, $t1, Labelak
li $t2, 0
sw $t2, dummyae
j Labelal
Labelak:
li $t2, 1
sw $t2, dummyae
Labelal:

lw $t1, dummyae
lw $t2, dummyab
or $t0, $t1, $t2
sw $t0, dummyaf

lw $t0, dummyaf
li $t1, 1
bne $t1, $t0, Labelam
li $v0, 4
la $a0 True
syscall
j Labelan
Labelam:
li $v0, 4
la $a0, False
syscall
Labelan:
