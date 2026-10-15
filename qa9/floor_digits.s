.intel_syntax noprefix
.code16
.section .text
.org 0xfda8
.global floor_digits_guard
floor_digits_guard:
    call 0xe1bc
    pushf
    cmp byte ptr [0x649b], 0xe1
    jne done
    cmp word ptr [0x64a1], 0x639c
    jb done
    cmp word ptr [0x64a1], 0x6a00
    jae done
    cmp di, 0x753a
    jb done
    cmp di, 0x753e
    ja done
    pusha
    .byte 0x9a
    .word 0x6e1c, 0x9000
    popa
done:
    popf
    jmp 0xd39b
