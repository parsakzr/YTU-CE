			EXTRN ALAN_BUL:FAR
myss		SEGMENT PARA STACK 's'
			DW 20 DUP(?)
myss		ENDS

myds		SEGMENT PARA 'd'
kenarlar	DW 6, 8, 5, 9, 4, 8, 2, 2, 3
n			DW 3
enbykalan	DW 0
myds		ENDS

mycs		SEGMENT PARA 'k'
			ASSUME CS:mycs, DS:myds, SS:myss
ANA 		PROC FAR
			PUSH DS
			XOR AX, AX
			PUSH AX
			MOV AX, myds
			MOV DS, AX
			MOV CX, n
			XOR SI, SI
L1:			PUSH kenarlar[SI]
			PUSH kenarlar[SI+2]
			PUSH kenarlar[SI+4]
			CALL ALAN_BUL
			CMP AX, enbykalan
			JB kucuk
			MOV enbykalan, AX
kucuk:		ADD SI, 6
			LOOP L1
			RETF
ANA			ENDP
mycs		ENDS
			END ANA