			PUBLIC func2 ; to be used elsewhere
			; EXTRN var1:BYTE, var2:WORD ( )
mycode		SEGMENT PARA 'cseg'
			ASSUME CS:mycode

func2		PROC FAR
;
;			push AX ; registers to use
;			;
;			;
;			pop AX
;
;
			RETF ; back to cs, offset (and popped from stack)
;			OR RETF 6 ; pops the parameters given in stack (Size in Bytes e.g. 6)
func2		ENDP
mycode		ENDS
			END