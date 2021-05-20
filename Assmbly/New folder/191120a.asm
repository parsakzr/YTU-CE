datasg	SEGMENT BYTE 'veri'
a		DB 18
b		DB 18
c		DB 18
tip		DB ?
datasg	ENDS
stacksg	SEGMENT BYTE STACK 'yigin'
		DW 12 DUP(?)
stacksg	ENDS
codesg	SEGMENT PARA 'kod'
		ASSUME CS:codesg, DS:datasg, SS:stacksg
ANA		PROC FAR
		PUSH DS				; geri donus adreslerinin ayarlanmasi
		XOR AX, AX
		PUSH AX
		MOV AX, datasg		; data segment degerinin ayarlanmasi
		MOV DS, AX	
		MOV AL, a
		MOV BL, b
		MOV CL, c
		CMP AL, BL
		JE J1
		CMP AL, CL
		JE J2
		CMP BL, CL
		JE J2
		MOV tip, 3
		JMP SON
J1:		CMP AL, CL
		JNE J2
		MOV tip, 1
		JMP SON
J2:		MOV tip, 2
SON:	RETF
ANA		ENDP
codesg	ENDS
		END ANA