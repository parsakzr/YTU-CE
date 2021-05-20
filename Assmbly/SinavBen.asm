codesg          SEGMENT PARA 'code'
                        ORG 100h
                        ASSUME cs:codesg, ds:codesg, ss:codesg

start:          JMP main
n               DW 294
arr             DB 294 DUP(?)
gnum            DW 0
gsum            DW 0

main            PROC NEAR
                
                xor SI, SI

forlp:          CMP SI, n
                JAE end
                CMP arr[SI], 0
                JLE artir
                ADD gsum, arr[SI]
                INC gnum
artir:          INC SI
                JMP forlp


end:            MOV AX, gsum
                DIV AX, gnum

                RET

main            ENDP

codesg          ENDS
                END start
