			EXTRN func2:FAR ; Tell the assmbler that func2 is not here, chill!
			;PUBLIC $var (if pass via data segment instead of stack or register)
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
			; CALL func2
			;
			RETF
main		ENDP

mycs		ENDS
			END main


;;; to link: link file1.obj + file2.obj
