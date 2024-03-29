;====================================================================
; Main.asm file generated by New Project wizard
;
; Created:   Pzt Eki 7 2019
; Processor: 8086
; Compiler:  MASM32
;
; Before starting simulation set Internal Memory Size 
; in the 8086 model properties to 0x10000
;====================================================================

CODE    SEGMENT PARA 'CODE'
        ASSUME CS:CODE, DS:DATA, SS:STAK
	
STAK    SEGMENT PARA STACK 'STACK'
        DW 20 DUP(?)
STAK    ENDS

DATA    SEGMENT PARA 'DATA'
TUSLAR	DB -1,-1
SAYILAR DB 2 DUP(?)
CIKTILAR DB 0C0H, 0F9H, 0A4H, 0B0H, 99H, 92H, 82H, 0F8H, 80H, 90H, 0A0H, 83H, 0A7H, 0A1H, 86H, 0EH
SONUC 	DB 1 DUP(?)
BASILDI DB 0 
DATA    ENDS


START PROC FAR

   MOV AX, DATA
   MOV DS, AX
   
   MOV AL, 81H
   OUT 0AFH, AL; control word
   
   MOV AL, 00H
   OUT 0ABH, AL   


YENI_SAYI: ; Yildizdan sonra
   XOR SI, SI
  
TUS_BAS:
   
   ;1. COLUMN
   MOV AL, 10H ; 0001 0000 - 16
   OUT 0ABH, AL ; B portuna yazma
   IN AL, 0ADH ; C portunu okuma
   
   CMP AL, 01H ; 1 basti mi
   JZ TUS1
   
   CMP AL, 02H ; 4 basti mi
   JZ TUS4
   
   CMP AL, 04H ; 7 basti mi
   JZ TUS7
   
   CMP AL, 08H ; * basti mi
   JZ TEMIZLE
   

   ;2. COLUMN
   MOV AL, 20H
   OUT 0ABH, AL ; B portuna yazma
   IN AL, 0ADH ; C portunu okuma
   
   CMP AL, 01H ; 2 basti mi
   JZ TUS2
   
   CMP AL, 02H ; 5 basti mi
   JZ TUS5
   
   CMP AL, 04H ; 8 basti mi
   JZ TUS8
 
   CMP AL, 08H ; 0 basti mi
   JZ TUS0

 
   ;3. COLOMN
   MOV AL, 40H
   OUT 0ABH, AL ; B portuna yazma
   IN AL, 0ADH ; C portunu okuma
   
   CMP AL, 01H ; 3 basti mi
   JZ TUS3
   
   CMP AL, 02H ; 6 basti mi
   JZ TUS6
   
   CMP AL, 04H ; 9 basti mi
   JZ TUS9
   
   CMP AL, 08H ; KARE basti mi
   JZ TUSKARE
   
   MOV DX, 0H ; flag: tusa basilmadi
   
   CMP BASILDI, 0
   JNE TUSKARE
   JMP TUS_BAS
      
TUS0:
   CMP DX, 1H ; tus basili oldugu surece okumaz
   JZ TUS_BAS
   MOV TUSLAR[SI], 0C0H
   MOV SAYILAR[SI], 0H
   INC BASILDI
   INC SI
   CMP SI, 2
   MOV DX, 1H ; tus kaydedildi, sadece ilk ani al
   JMP SON
   JMP TUS_BAS
   
TUS1:
   CMP DX, 1H ; tus basili oldugu surece okumaz
   JZ TUS_BAS
   MOV TUSLAR[SI], 0F9H
   MOV SAYILAR[SI], 1H
   INC BASILDI
   INC SI
   CMP SI, 2
   MOV DX, 1H ; tus kaydedildi, sadece ilk ani al
   JMP SON
   JMP TUS_BAS
   
TUS2:
   CMP DX, 1H ; tus kaydedildi, sadece ilk ani al
   JZ TUS_BAS
   MOV TUSLAR[SI], 0A4H
   MOV SAYILAR[SI], 2H
   INC BASILDI
   INC SI
   CMP SI, 2
   MOV DX, 1H ; tus kaydedildi, sadece ilk ani al
   JMP SON
   JMP TUS_BAS

TUS3:
   CMP DX, 1H
   JZ TUS_BAS
   MOV TUSLAR[SI], 0B0H
   MOV SAYILAR[SI], 3H
   INC BASILDI
   INC SI
   CMP SI, 2
   MOV DX, 1H
   JMP SON
   JMP TUS_BAS
   
TUS4:
   CMP DX, 1H
   JZ TUS_BAS
   MOV TUSLAR[SI], 99H
   MOV SAYILAR[SI], 4H
   INC BASILDI
   INC SI
   CMP SI, 2
   MOV DX, 1H
   JMP SON
   JMP TUS_BAS
   
TUS5:
   CMP DX, 1H
   JZ TUS_BAS
   MOV TUSLAR[SI], 92H
   MOV SAYILAR[SI], 5H
   INC BASILDI
   INC SI
   CMP SI, 2
   MOV DX, 1H
   JMP SON
   JMP TUS_BAS

TUS6:
   CMP DX, 1H
   JZ TUS_BAS
   MOV TUSLAR[SI], 82H
   MOV SAYILAR[SI],6H
   INC BASILDI
   INC SI
   CMP SI, 2
   MOV DX, 1H
   JMP SON
   JMP TUS_BAS
  
TUS7:
   CMP DX, 1H
   JZ TUS_BAS
   MOV TUSLAR[SI], 0F8H
   MOV SAYILAR[SI], 7H
   INC BASILDI
   INC SI
   CMP SI, 2
   MOV DX, 1H
   JMP SON
   JMP TUS_BAS
   
TUS8:
   CMP DX, 1H
   JZ TUS_BAS
   MOV TUSLAR[SI], 80H
   MOV SAYILAR[SI], 8H
   INC BASILDI
   INC SI
   CMP SI, 2
   MOV DX, 1H
   JMP SON
   JMP TUS_BAS

TUS9:
   CMP DX, 1H
   JZ TUS_BAS
   MOV TUSLAR[SI], 90H
   MOV SAYILAR[SI], 9H
   INC BASILDI
   INC SI
   CMP SI, 2
   MOV DX, 1H
   JMP SON
   JMP TUS_BAS

TUSKARE:
   CMP BASILDI, 2 ; ikinci sayi da girmis oldugunda
   JE HESAPLA 
   CMP BASILDI, 1 ; ilk sayi girmis oldugunda
   JE CIZGI
   JMP TUS_BAS

; tuslarin kontrolu bitti


CIZGI: ; cizgiyi bastir
   MOV AL, 0FFH
   OUT 0ABH, AL ; temizle
   MOV AL, 0BFH ; cizgi kodu
   OUT 0A9H, AL ; bastir
   JMP TUS_BAS

HESAPLA: ; SAYI[0] OR SAYI[1] sonucunu ekrana bastir
    MOV AX, SAYILAR[0]
    OR AX,SAYILAR[1]
    MOV SI, AX
    MOV AL, 0FFH
    OUT 0A9H, AL ; A portuna yaz
    MOV AL, 01H
    OUT 0ABH, AL ; B portuna yazma: 1. 7-segment aktif
    MOV AL, CIKTILAR[SI]
    OUT 0A9H, AL ; A portuna yaz
    JMP TUS_BAS
  
SON:

; 7-SEGMENTS

;tus bastir ( loop icinde oldugu icin bastirmaya devam)
    MOV AL, 0FFH
    OUT 0A9H, AL ; A portuna yaz
    MOV AL, 01H
    OUT 0ABH, AL ; B portuna yazma: 1. 7-segment aktif
    MOV AL, TUSLAR[SI-1]
    OUT 0A9H, AL ; A portuna yaz

DEVAM:
    MOV AL, 10H ; * kontrolü için 1. sutun
    OUT 0ABH, AL ; B portuna yazma
    IN AL, 0ADH ; C portunu okuma
    CMP AL, 08H ; * mi?
    JE TEMIZLE

    MOV AL, 40H ; # kontrolü için 
    OUT 0ABH, AL ; B portuna yazma
    IN AL, 0ADH ; C portunu okuma
    CMP AL, 08H ; # mi?
    JE TUSKARE
    JMP SON

TEMIZLE:
    MOV AL, 0FFH ; hiçbirinin yanmamasi için (anot)
    MOV CX, 4H
    MOV BASILDI, 0 ; hic bir sayi girmemis gibi
    XOR SI, SI
L1:
    MOV TUSLAR[SI], AL 
    INC SI
    LOOP L1
    JMP YENI_SAYI

   
RETF
START ENDP
CODE    ENDS
        END START