.data
y: .space 64
True: .asciiz "True"
False: .asciiz "False"
x: .word 0
.text

li $t0,10
la $t1,x
sw $t0, 0($t1)
