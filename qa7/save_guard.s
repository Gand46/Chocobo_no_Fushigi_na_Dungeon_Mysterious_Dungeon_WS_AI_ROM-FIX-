.intel_syntax noprefix
.code16
.section .text
.org 0xfa80
.global normal_save, alternate_save, validate_save, guard_end

# Six persistent bytes immediately after the native payload:
# 7f8a desired marker mask; 7f8b commit; 7f8c CRC; 7f8e CRC complement.
# CRC16-CCITT-FALSE covers payload75b6..7f89 plus desired mask7f8a.
normal_save:
    pushf
    pusha
    mov al, 1
    call begin_save
    popa
    popf
    .byte 0x9a
    .word 0xc47a, 0xe000
    .byte 0x9a
    .word 0x036c, 0x9000
    pushf
    pusha
    call commit_save
    popa
    popf
    retf

alternate_save:
    pushf
    pusha
    mov al, 2
    call begin_save
    popa
    popf
    mov di, 0x75b6
    .byte 0x9a
    .word 0x038f, 0x9000
    pushf
    pusha
    call commit_save
    popa
    popf
    retf

# AL=legacy mask, AH=protected mask. Prefix and suffix are checked separately.
recognize:
    xor ax, ax
    cmp word ptr [0x75b0], 0x5f6e
    jne alt_marker
    cmp byte ptr [0x75b2], 0x63
    jne alt_marker
    cmp byte ptr [0x75b3], 0x31
    jne normal_protected
    or al, 1
    jmp alt_marker
normal_protected:
    cmp byte ptr [0x75b3], 0x34
    jne alt_marker
    or ah, 1
alt_marker:
    cmp word ptr [0x75ac], 0x5f41
    jne recognized
    cmp byte ptr [0x75ae], 0x43
    jne recognized
    cmp byte ptr [0x75af], 0x31
    jne alt_protected
    or al, 2
    jmp recognized
alt_protected:
    cmp byte ptr [0x75af], 0x34
    jne recognized
    or ah, 2
recognized:
    ret

begin_save:
    mov bl, al
    call recognize
    or bl, al
    or bl, ah
    mov byte ptr [0x7f8b], 0
    mov byte ptr [0x7f8a], bl
    # Both headers address the same payload. Invalidate both before writing it.
    mov byte ptr [0x75b3], 0
    mov byte ptr [0x75af], 0
    ret

crc_payload:
    mov dx, 0xffff
    mov si, 0x75b6
    mov cx, 0x09d5
crc_byte:
    xor dh, byte ptr [si]
    inc si
    mov bl, 8
crc_bit:
    shl dx, 1
    jnc crc_no_xor
    xor dx, 0x1021
crc_no_xor:
    dec bl
    jne crc_bit
    loop crc_byte
    ret

commit_save:
    call crc_payload
    mov word ptr [0x7f8c], dx
    not dx
    mov word ptr [0x7f8e], dx
    test byte ptr [0x7f8a], 1
    jz commit_alt
    mov word ptr [0x75b0], 0x5f6e
    mov word ptr [0x75b2], 0x3463
commit_alt:
    test byte ptr [0x7f8a], 2
    jz commit_done
    mov word ptr [0x75ac], 0x5f41
    mov word ptr [0x75ae], 0x3443
commit_done:
    # Publish only after payload, CRC and both requested headers are complete.
    mov byte ptr [0x7f8b], 0xa5
    ret

validate_save:
    pushf
    pusha
    call recognize
    mov byte ptr [0x75b4], al
    test ah, ah
    jz validation_done
    cmp byte ptr [0x7f8b], 0xa5
    jne validation_done
    # Native code may clear one marker independently (e.g. normal Delete).
    # A remaining protected marker is valid when it belongs to the committed mask.
    mov bl, byte ptr [0x7f8a]
    and bl, ah
    cmp ah, bl
    jne validation_done
    push ax
    call crc_payload
    pop ax
    cmp dx, word ptr [0x7f8c]
    jne validation_done
    not dx
    cmp dx, word ptr [0x7f8e]
    jne validation_done
    or byte ptr [0x75b4], ah
validation_done:
    popa
    popf
    retf
guard_end:
