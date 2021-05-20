codesg		SEGMENT PARA 'csg'
			ORG 100h
			ASSUME cs:codesg, ds:codesg, ss:codesg

start:		JMP main
; Data

main		PROC NEAR
			; main()
			RET
main		ENDP

codesg		ENDS
			END start
