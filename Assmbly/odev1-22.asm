SSG     SEGMENT PARA STACK 'STK'
DW 30 DUP(?)
SSG ENDS

DSG     SEGMENT PARA 'DAT'
M     DW 8191
A     DW 884
C     DW 1
RND   DW 0
DSG ENDS

CSG     SEGMENT PARA 'CODE'
        ASSUME CS:CSG, DS:DSG, SS:SSG

BASLA   PROC FAR

        PUSH DS
        XOR AX,AX
        PUSH AX

        MOV AX, DSG
        MOV DS, AX

        MOV AX, CS:[23] 
sonraki:
        MUL A
        ADD AX, C
        ADC DX, 0
        DIV M
        MOV AX, DX
        CMP AX, 256
        JA sonraki
        MOV RND, AX

        RETF
BASLA   ENDP
CSG  ENDS
        END BASLA
