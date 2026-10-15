; Project-owned guard, 80186 / real mode. Source ROM code is NOT fully decompiled.
; Hook at ROM 154392 (CPU 5000:4392), before: BF 90 01 C1 E1 02.
; New jump: 4392 -> FD40, followed by three NOPs.
; Native entry already pushed the old C2 bank at 438C.
bits 16
org 0xfd40
    cmp cx, byte -1
    jne valid_model
    jmp near 0x44cc          ; POP AX; OUT C2,AL; native cleanup; RETF
valid_model:
    mov di, 0x0190          ; displaced native instructions
    shl cx, byte 2
    jmp near 0x4398
; No stack/register adjustment beyond the displaced native operations.
