codesg		SEGMENT PARA 'kod'
			ORG 100h
			ASSUME CS:codesg, DS:codesg, SS:codesg
basla:		JMP SICAKLIK
n			DW 5
dizi		DB -20, 25, 10, -40, 17
esik		DB -20
sonuc		DB 0
SICAKLIK 	PROC NEAR
			XOR SI, SI
			MOV CX, n
			MOV AL, esik
don:		CMP SI, CX
			JAE SON
			CMP AL, dizi[SI]			; CMP AL, DADDR
			JG L2
			INC SI
			JMP don
L2:			MOV sonuc, 1
SON:		RET
SICAKLIK	ENDP
codesg		ENDS
			END basla

; DOSBOX->
;	masm test.asm
;	link test.obj ( Warning: No Stack Segment. Acceptable! )
;	exe2com test.exe
;	debug test.com

; Degug:
;	-u
;	-u cs:$ADDR
;	-d cd:$ADDR // 