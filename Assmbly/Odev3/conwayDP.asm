			PUBLIC CONWAY
			EXTRN dplist:WORD
mycs		SEGMENT PARA PUBLIC 'cseg'
			ASSUME CS:mycs
CONWAY		PROC FAR
			
			PUSH CX
			PUSH BX
			PUSH DI
			PUSH BP
			
			MOV BP, SP
			MOV CX, [BP+12] ; CX <-- n
			

			XOR DI, DI
			ADD DI, 3 
			ADD AX, CX
			SUB CX , 3 ; DI: 3->n, CX-3 kere
			
L_for: 		ADD BX, dplist[DI-1]  ; a(n-1)
			SUB AX, BX       	  ; n-a(n-1)
			ADD AX,dplist[AX]     ; + a(n-a(n-1))
			ADD AX, dplist[BX]    ; + a(a(n-1))
			ADD dplist[DI], AX

			INC DI
			LOOP L_for
			
			
			POP BP
			POP DI
			POP BX
			POP CX

			RETF 2
CONWAY		ENDP
mycs		ENDS
			END		