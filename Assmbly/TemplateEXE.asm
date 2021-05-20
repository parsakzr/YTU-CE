myss		SEGMENT PARA 'stacksg'
			DW 20 DUP(?)
myss		ENDS

myds		SEGMENT PARA 'datasg'
;
;
myds		ENDS

mycs		SEGMENT PARA 'codesg'
			ASSUME CS:mycs, DS:myds, SS:myss

main		PROC FAR
			PUSH DS
			XOR AX, AX
			PUSH AX
			MOV AX, myds
			MOV DS, AX
			;
			;
			;
			RETF
main		ENDP

mycs		ENDS
			END main