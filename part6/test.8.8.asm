.data
dummy2l: .word 0
dummy2k: .word 0
dummy2j: .word 0
dummy2i: .word 0
dummy2h: .word 0
dummy2g: .word 0
dummy2f: .word 0
dummy2e: .word 0
dummy2d: .word 0
dummy2c: .word 0
dummy2b: .word 0
dummy2a: .word 0
True: .asciiz "True"
False: .asciiz "False"
.text
#LESS THAN
li $t0, 1
li $t1, 2
bgt $t0, $t1, Labela
li $t2, 0
sw $t2, dummy2a
j Labelb
Labela:
li $t2, 1
sw $t2, dummy2a
Labelb:

lw $t1, 3
lw $t2, dummy2a
or $t0, $t1, $t2
sw $t0, dummy2b
#LESS THAN
lw $t0, dummy2b
li $t1, 4
bgt $t0, $t1, Labelc
li $t2, 0
sw $t2, dummy2c
j Labeld
Labelc:
li $t2, 1
sw $t2, dummy2c
Labeld:

lw $t0, dummy2c
li $t1, 1
bne $t1, $t0, Labele
li $v0, 4
la $a0 True
syscall
j Labelf
Labele:
li $v0, 4
la $a0, False
syscall
Labelf:
#GREATER THAN
li $t0, 1
li $t1, 2
bgt $t0, $t1, Labelg
li $t2, 0
sw $t2, dummy2d
j Labelh
Labelg:
li $t2, 1
sw $t2, dummy2d
Labelh:

lw $t1, 3
lw $t2, dummy2d
or $t0, $t1, $t2
sw $t0, dummy2e
#LESS THAN
lw $t0, dummy2e
li $t1, 4
bgt $t0, $t1, Labeli
li $t2, 0
sw $t2, dummy2f
j Labelj
Labeli:
li $t2, 1
sw $t2, dummy2f
Labelj:

lw $t0, dummy2f
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
#LESS THAN
li $t0, 1
li $t1, 2
bgt $t0, $t1, Labelm
li $t2, 0
sw $t2, dummy2g
j Labeln
Labelm:
li $t2, 1
sw $t2, dummy2g
Labeln:

lw $t1, 3
lw $t2, dummy2g
or $t0, $t1, $t2
sw $t0, dummy2h
#GREATER THAN
lw $t0, dummy2h
li $t1, 4
bgt $t0, $t1, Labelo
li $t2, 0
sw $t2, dummy2i
j Labelp
Labelo:
li $t2, 1
sw $t2, dummy2i
Labelp:

lw $t0, dummy2i
li $t1, 1
bne $t1, $t0, Labelq
li $v0, 4
la $a0 True
syscall
j Labelr
Labelq:
li $v0, 4
la $a0, False
syscall
Labelr:
#GREATER THAN
li $t0, 1
li $t1, 2
bgt $t0, $t1, Labels
li $t2, 0
sw $t2, dummy2j
j Labelt
Labels:
li $t2, 1
sw $t2, dummy2j
Labelt:

lw $t1, 3
lw $t2, dummy2j
or $t0, $t1, $t2
sw $t0, dummy2k
#GREATER THAN
lw $t0, dummy2k
li $t1, 4
bgt $t0, $t1, Labelu
li $t2, 0
sw $t2, dummy2l
j Labelv
Labelu:
li $t2, 1
sw $t2, dummy2l
Labelv:

lw $t0, dummy2l
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
