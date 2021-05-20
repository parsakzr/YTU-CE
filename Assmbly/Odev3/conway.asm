			PUBLIC CONWAY
mycode		SEGMENT PARA 'cseg'
			ASSUME CS:mycode

CONWAY		PROC FAR

			PUSH CX
			PUSH BX
			PUSH BP
			
			
			MOV BP, SP
			MOV CX, [BP+10] ; CX <-- n
			

			CMP CX, 3
			JAE recurse ; n>=3 --> a(n) = a(a(n-1)) + a(n-a(n-1))
			CMP CX, 0
			JZ zero

			MOV AX, 1 ; n = 1, 2
			JMP son

zero:		MOV AX, 0 ; n = 0
			JMP son

recurse:	DEC CX ; CX --> n-1
			PUSH CX ;
			CALL CONWAY ; a(n-1)
			pop AX ; <---/
			
			INC CX ; recurse basinda n-1 icin DEC oldu.
			SUB CX, AX ; n-a(n-1). SUB AX, CX daha hizli oldugunu biliyorum
			PUSH CX
			CALL CONWAY ; a(n-a(n-1))
			pop BX ; <---/

			PUSH AX ; AX=a(n-1)
			CALL CONWAY ; a(a(n-1))
			pop AX ; <---/

			ADD AX, BX ; a(a(n-1)) + a(n-a(n-1))


son:		POP BP
			POP BX
			POP CX

			MOV [BP+10], AX ; update result
			RETF ; normalde RETF 2 olmaliydi, ama diger tarafta pop edip [BP+14] return edilir
CONWAY		ENDP

mycode		ENDS
			END