			EXTRN SAYveBOL: FAR
myss		SEGMENT PARA STACK 's'
			DW 20 DUP(?)
myss		ENDS
myds		SEGMENT PARA 'd'
dizi		DW 0FEh, 0A7h, 0B3h, 72h, 6Bh
n			DW 5
myds		ENDS
mycs		SEGMENT PARA PUBLIC 'birles'
			ASSUME CS:mycs, DS:myds, SS:myss
MAIN		PROC FAR
			PUSH DS
			XOR AX, AX
			PUSH AX
			MOV AX, myds
			MOV DS, AX
			
			MOV CX, n
			XOR SI, SI
L1:			PUSH dizi[SI]
			CALL SAYveBOL
			MOV dizi[SI], AX
			ADD SI, 2
			LOOP L1

			RETF
MAIN		ENDP
mycs		ENDS
			END MAIN