
cseg		SEGMENT PARA 'ortak'
			ORG 100h
			ASSUME CS:cseg, SS:cseg, DS:cseg
ENKCK		MACRO dizi, n
			LOCAL L1
			XOR SI, SI
			MOV AL, dizi[SI]
			INC SI
			MOV CX, n
			DEC CX
L1:			CMP AL, dizi[SI]
			JL don
			MOV AL, dizi[SI]
don:		INC SI
			LOOP L1
			ENDM
ANA			PROC NEAR
			XOR SI, SI
			MOV CX, n
L1:			SAR dizi[SI], 1
			INC SI
			LOOP L1
			ENKCK dizi, n
			MOV kck, AL
			RET
ANA			ENDP
dizi 		DB 10, -2, 4, 6, 10, 3, 5, 17
n			DW 8
kck			DB ?
cseg		ENDS
			END ANA
			