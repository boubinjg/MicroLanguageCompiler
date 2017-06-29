.data
True: .asciiz "True"
False: .asciiz "False"
.text

li $t0, 1
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
