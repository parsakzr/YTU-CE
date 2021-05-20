			PUBLIC SAYAC
mycs		SEGMENT PARA PUBLIC 'code'
			ASSUME CS:mycs
SAYAC		PROC FAR
			PUSH CX
			PUSH BX
			PUSH DI
			PUSH BP

			MOV BP, SP
			MOV CX, [BP+12]
			MOV DI, [BP+14]
			MOV BX, [BP+16]
			
			XOR AX, AX
L1:			CMP BX, [DI]
			JNE atla
			INC AX
atla:		ADD DI, 2
			LOOP L1

			POP BP
			POP DI
			POP BX
			POP CX
			RETF 6
SAYAC		ENDP
mycs		ENDS
			END		