			EXTRN CONWAY:FAR ;, PRINTINT:FAR
myss		SEGMENT PARA 'stacksg'
			DW 200 DUP(?)
myss		ENDS

myds		SEGMENT PARA 'datasg'
n 			DW 10
result		DW ?
myds		ENDS

mycs		SEGMENT PARA 'codesg'
			ASSUME CS:mycs, DS:myds, SS:myss

main		PROC FAR
			PUSH DS
			XOR AX, AX
			PUSH AX
			MOV AX, myds
			MOV DS, AX
			
			MOV CX, n
			PUSH CX 
			CALL CONWAY ; a(n)
			POP AX ; <---/
			MOV result, AX

			;PUSH AX
			;CALL PRINTINT ; yazici
			
			RETF
main		ENDP

mycs		ENDS
			END main

