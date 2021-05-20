myds		SEGMENT PARA 'veri'
dizi		DB 1, 2, 3, 6, 5
n			DW 5
S			DB 0
myds		ENDS
myss		SEGMENT PARA STACK 'yigin'
			DW 20 DUP(?)
myss		ENDS
mycs		SEGMENT PARA 'kod'
			ASSUME CS:mycs, SS:myss, DS:myds
MAIN		PROC FAR
			PUSH DS
			XOR AX, AX
			PUSH AX
			MOV AX, myds
			MOV DS, AX

			XOR SI, SI
			MOV BX, 0
			
			MOV CX, n
			DEC CX
don:		CMP BX, 0
			JNE son_if
			CMP SI, CX
			JGE son_if
			MOV AL, dizi[SI]
			CMP AL, dizi[SI+1]
			JLE artir
			MOV BX, 1
artir:		INC SI
			JMP don
son_if:		CMP BX, 0
			JNE SON
			MOV S, 1
SON:		RETF
MAIN		ENDP
mycs		ENDS
			END MAIN