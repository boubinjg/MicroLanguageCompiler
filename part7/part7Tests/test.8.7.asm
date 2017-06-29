.data
dummyan: .word 0
dummyam: .word 0
dummyai: .word 0
dummyad: .word 0
dummyac: .word 0
dummyy: .word 0
dummyt: .word 0
dummys: .word 0
dummyo: .word 0
dummyj: .word 0
dummyi: .word 0
dummye: .word 0
True: .asciiz "True"
False: .asciiz "False"
.text
#LESS THAN
li $t0, 1
li $t1, 2
bge $t0, $t1, Labele
li $t2, 1
sw $t2, dummye
j Labelf
Labele:
li $t2, 0
sw $t2, dummye
Labelf:
#LESS THAN
li $t0, 3
li $t1, 4
bge $t0, $t1, Labeli
li $t2, 1
sw $t2, dummyi
j Labelj
Labeli:
li $t2, 0
sw $t2, dummyi
Labelj:

lw $t1, dummyi
lw $t2, dummye
or $t0, $t1, $t2
sw $t0, dummyj

lw $t0, dummyj
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
sw $t2, dummyo
j Labelp
Labelo:
li $t2, 1
sw $t2, dummyo
Labelp:
#LESS THAN
li $t0, 3
li $t1, 4
bge $t0, $t1, Labels
li $t2, 1
sw $t2, dummys
j Labelt
Labels:
li $t2, 0
sw $t2, dummys
Labelt:

lw $t1, dummys
lw $t2, dummyo
or $t0, $t1, $t2
sw $t0, dummyt

lw $t0, dummyt
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
sw $t2, dummyy
j Labelab
Labelaa:
li $t2, 0
sw $t2, dummyy
Labelab:
#GREATER THAN
li $t0, 3
li $t1, 4
bgt $t0, $t1, Labelac
li $t2, 0
sw $t2, dummyac
j Labelad
Labelac:
li $t2, 1
sw $t2, dummyac
Labelad:

lw $t1, dummyac
lw $t2, dummyy
or $t0, $t1, $t2
sw $t0, dummyad

lw $t0, dummyad
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
sw $t2, dummyai
j Labelaj
Labelai:
li $t2, 1
sw $t2, dummyai
Labelaj:
#GREATER THAN
li $t0, 3
li $t1, 4
bgt $t0, $t1, Labelak
li $t2, 0
sw $t2, dummyam
j Labelal
Labelak:
li $t2, 1
sw $t2, dummyam
Labelal:

lw $t1, dummyam
lw $t2, dummyai
or $t0, $t1, $t2
sw $t0, dummyan

lw $t0, dummyan
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
