my_ss       SEGMENT PARA STACK 'yigin'
            DW 20 DUP(?)
my_ss       ENDS

my_ds       SEGMENT PARA 'veri'
dizi        DW 7FFFh, 7AB2h, 70ABh, 7111h, 71FAh, 7232h, 7AF8h, 78c5h, 753Dh, 70E0h
n           DW 10
tek_top     DD 0
tek_say     DW 0
cift_top    DD 0
cift_say    DW 0
tek_ort     DW ?
cift_ort    DW ?
my_ds   ENDS

my_cs       SEGMENT PARA 'kod'
            ASSUME CS:my_cs, DS:my_ds, SS:my_ss
YORDAM      PROC FAR
            PUSH DS
            XOR AX, AX
            PUSH AX
            MOV AX, my_ds
            MOV DS, AX

            MOV CX, n
            LEA SI, dizi
don:        MOV AX, [SI]
            TEST AX, 0001h
            JZ c_label
            INC tek_say
            ADD WORD PTR [tek_top], AX
            ADC WORD PTR [tek_top+2], 0
            JMP artir
c_label:    ADD WORD PTR [cift_top], AX
            ADC WORD PTR [cift_top+2], 0
            INC cift_say
artir:      ADD SI, 2
            LOOP don

            ;DX:AX / op -> AX
            MOV DX, WORD PTR [cift_top+2]
            MOV AX, WORD PTR [cift_top]
            DIV cift_say                    ; DIV DADDR
            MOV cift_ort, AX

            MOV DX, WORD PTR [tek_top+2]
            MOV AX, WORD PTR [tek_top]
            DIV tek_say                    ; DIV DADDR
            MOV tek_ort, AX

            RETF
YORDAM      ENDP
my_cs       ENDS
            END YORDAM