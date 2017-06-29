.data
dummy2a: .asciiz "Hello, world"
True: .asciiz "True"
False: .asciiz "False"
.text

la $t0 dummy2a
move $a0, $t0
li $v0,4
syscall
