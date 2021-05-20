			PUBLIC SAYveBOL
mycs		SEGMENT PARA PUBLIC 'birles'
			ASSUME CS:mycs
SAYveBOL	PROC FAR
			PUSH BP
			PUSH CX
			PUSH BX
			PUSH DX
			
			MOV BP, SP
			MOV AX, [BP+12]
			MOV CX, 17
			XOR BX, BX
			
			CMP AX, 0
			JE next
			
			CLC
L1:			RCR AX, 1
			JNC artirma
			INC BX
artirma:	LOOP L1

			CWD				; AX ->DX:AX	AX: 00FEh
			IDIV BX			; DX:AX/BX -> Bolum: AX, Kalan: DX	
			
next:		POP DX
			POP BX
			POP CX
			POP BP
			RETF 2
SAYveBOL	ENDP
mycs		ENDS
			END