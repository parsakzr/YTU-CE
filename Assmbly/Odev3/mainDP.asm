			EXTRN CONWAY: FAR
			PUBLIC dplist
myss		SEGMENT PARA STACK 'stacksg'
			DW 20 DUP(?)
myss		ENDS

myds		SEGMENT PARA 'datasg'
dplist		DW 500 DUP (?)
n			DW 500
myds		ENDS

mycs		SEGMENT PARA PUBLIC 'codesg'
			ASSUME CS:mycs, DS:myds, SS:myss

main		PROC FAR
			PUSH DS
			XOR AX, AX
			PUSH AX
			MOV AX, myds
			MOV DS, AX
			
			MOV dplist[0h], 0 ; initialize
			MOV dplist[1h], 1
			MOV dplist[2h], 1

			MOV AX, n
			PUSH AX
			CALL CONWAY
			
			; PUSH AX
			; PRINTINT
		
			RETF
main		ENDP

mycs		ENDS
			END main