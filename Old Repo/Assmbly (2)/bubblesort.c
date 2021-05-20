#include <stdio.h>

int main(){

    short n=6, x=5, T;

    __asm {
        MOV CX, n
        MOV SI, 5
        MOV BX, 1
        MOV AX, SI
        MOV DI, 1
        MOV DX, 0
    L1: PUSH AX
        DIV DI
        ADD BX, AX
        POP AX
        MUL SI
        INC DI
        LOOP L1
        MOV T, BX
    }
    printf("Toplam: %d:\n", T);

    return 0;
}