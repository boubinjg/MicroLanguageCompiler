.data
True: .asciiz "True"
False: .asciiz "False"
s: .word 0
b: .word 0
.text

li $t0,0
la $t1,s
sw $t0, 0($t1)

la $t0,s
la $t1,b
lw $t2, 0($t0)
sw $t2, 0($t1)

lw $t0, b
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
