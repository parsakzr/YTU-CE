			EXTRN SIRALIMI:FAR
			PUBLIC dizi, n
myss		SEGMENT PARA STACK 'sss'
			DW 20 DUP(?)
myss		ENDS
myds		SEGMENT PARA 'd'
n			DW 7
s			DB 0
dizi		DB 12, 17, 16, 18, 20, 22, 24
myds		ENDS
mycs		SEGMENT PARA 'k'
			ASSUME CS:mycs, DS:myds, SS:myss
ANA			PROC FAR
			PUSH DS
			XOR AX, AX
			PUSH AX
			MOV AX, myds
			MOV DS, AX
			CALL SIRALIMI
			CMP AL, 0
			JZ sirali
			MOV s, 1
sirali:		RET
ANA			ENDP
mycs		ENDS
			END ANA