			EXTRN TOPLAMA:FAR
myss		SEGMENT PARA STACK 'yi'
			DW 20 DUP(?)
myss		ENDS
myds		SEGMENT PARA 've'
sayi1		DB 250
sayi2		DB 150
sonuc		DW ?
myds		ENDS
mycs		SEGMENT PARA 'ko'
			ASSUME CS:mycs, DS:myds, SS:myss
ANA			PROC FAR
			PUSH DS
			XOR AX, AX
			PUSH AX
			MOV AX, myds
			MOV DS, AX
			
			MOV BL, sayi1
			MOV BH, sayi2
			CALL TOPLAMA
			MOV sonuc, AX
			RETF
ANA			ENDP
mycs		ENDS
			END ANA