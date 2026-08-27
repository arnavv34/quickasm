.global _start
.intel_syntax noprefix
.section .text

_start:
    mov rax, 1
    mov rdi, 1
    lea rsi, [rip + msg]
    mov rdx, offset msg_len
    syscall

    mov rax, 60
    xor rdi, rdi
    syscall

.section .rodata
msg: .ascii "Hello, world!\n"
msg_len = . - msg
