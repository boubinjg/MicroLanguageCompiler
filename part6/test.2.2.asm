.data
True: .asciiz "True"
False: .asciiz "False"
.text

li $t0, 1
li $t1, 1
bne $t1, $t0, Labela
li $v0, 4
la $a0 True
syscall
j Labelb
Labela:
li $v0, 4
la $a0, False
syscall
Labelb:
