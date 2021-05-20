mystack		SEGMENT PARA STACK 'y'
			DW 20 DUP(?)
mystack		ENDS
myds		SEGMENT PARA 'v'
n			DW 280
kalan		DW 0
but			DW 0
basarili	DW 0
topNot 		DW 0		;100*80 = 28000
esik		DB 40
notlar		DB 280 DUP(?)
myds		ENDS
mycs		SEGMENT PARA 'k'
			ASSUME CS:mycs, SS:mystack, DS:myds
CAN			PROC FAR
			PUSH DS
			XOR AX, AX
			PUSH AX
			MOV AX,  myds
			MOV DS, AX
			
			XOR SI, SI
			MOV CX, n
L1:			MOV AL, notlar[SI]
			CMP AL, esik
			JAE esikustu
			INC kalan
			JMP d1
esikustu:	CBW					; AL -> AX
			ADD topNot, AX
d1:			INC SI
			LOOP L1
			
			MOV CX, n
			SUB CX, kalan
			
			XOR DX, DX
			MOV AX, topNot		
			DIV CX				;DX:AX / CX  -> Bolum: AX, Kalan: DX
			
			XOR SI, SI
			MOV CX, n
L2:			MOV AH, notlar[SI]
			CMP AL, AH
			JBE gecti
			CMP AH, esik
			JB kaldi
			INC but
			JMP kaldi
gecti:		INC basarili
kaldi:		INC SI
			LOOP L2
			RETF
CAN			ENDP
mycs		ENDS
			END CAN