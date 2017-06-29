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
#LESS THAN
li $t0, 3
li $t1, 4
bgt $t0, $t1, Labelc
li $t2, 0
sw $t2, dummy2c
j Labeld
Labelc:
li $t2, 1
sw $t2, dummy2c
Labeld:

lw $t1, dummy2c
lw $t2, dummy2a
or $t0, $t1, $t2
sw $t0, dummy2c

li $v0,1
lw $a0,dummy2c
syscall
#GREATER THAN
li $t0, 1
li $t1, 2
bgt $t0, $t1, Labele
li $t2, 0
sw $t2, dummy2d
j Labelf
Labele:
li $t2, 1
sw $t2, dummy2d
Labelf:
#LESS THAN
li $t0, 3
li $t1, 4
bgt $t0, $t1, Labelg
li $t2, 0
sw $t2, dummy2f
j Labelh
Labelg:
li $t2, 1
sw $t2, dummy2f
Labelh:

lw $t1, dummy2f
lw $t2, dummy2d
or $t0, $t1, $t2
sw $t0, dummy2f

li $v0,1
lw $a0,dummy2f
syscall
#LESS THAN
li $t0, 1
li $t1, 2
bgt $t0, $t1, Labeli
li $t2, 0
sw $t2, dummy2g
j Labelj
Labeli:
li $t2, 1
sw $t2, dummy2g
Labelj:
#GREATER THAN
li $t0, 3
li $t1, 4
bgt $t0, $t1, Labelk
li $t2, 0
sw $t2, dummy2i
j Labell
Labelk:
li $t2, 1
sw $t2, dummy2i
Labell:

lw $t1, dummy2i
lw $t2, dummy2g
or $t0, $t1, $t2
sw $t0, dummy2i

li $v0,1
lw $a0,dummy2i
syscall
#GREATER THAN
li $t0, 1
li $t1, 2
bgt $t0, $t1, Labelm
li $t2, 0
sw $t2, dummy2j
j Labeln
Labelm:
li $t2, 1
sw $t2, dummy2j
Labeln:
#GREATER THAN
li $t0, 3
li $t1, 4
bgt $t0, $t1, Labelo
li $t2, 0
sw $t2, dummy2l
j Labelp
Labelo:
li $t2, 1
sw $t2, dummy2l
Labelp:

lw $t1, dummy2l
lw $t2, dummy2j
or $t0, $t1, $t2
sw $t0, dummy2l

li $v0,1
lw $a0,dummy2l
syscall
