mys		SEGMENT PARA 'kod'
		ORG 100h
		ASSUME CS:mys, DS:mys, SS:mys
kaynak	PROC NEAR
		XOR BX, BX
		MOV AL, k_esik
		MOV AH, b_esik
don:	CMP dizi[BX], AL
		JB sonraki				;saglandigi icin zipladik
		CMP dizi[BX], AH
		JBE bulduk				;saglanamadigi icin zipladik
sonraki: INC BX
		JMP don
bulduk:	MOV sonuc, BL
		RET
kaynak	ENDP
dizi	DB 14, 11, 54, 45, 11, 3, 8, 63, 81, 5, 12
k_esik	DB 15
b_esik	DB 50
sonuc	DB ?
mys		ENDS
		END kaynak