			PUBLIC SIRALIMI
			EXTRN dizi:BYTE, n:WORD
mycode		SEGMENT PARA 'test2'
			ASSUME CS:mycode
SIRALIMI	PROC FAR
			PUSH SI
			PUSH CX
			XOR AX, AX
			XOR SI, SI
			MOV CX, n
			DEC CX
don:		CMP SI, CX
			JAE sirali
			MOV AH, dizi[SI]
			CMP AH, dizi[SI+1]
			JG sirasiz
			INC SI
			JMP don
sirasiz:	MOV AL, 1	
sirali:		POP CX
			POP SI
			RET
SIRALIMI	ENDP
mycode		ENDS
			END