FIRST      START     1000              . program starts at address 1000
           LDX       ZERO              . initialize index register X to 0
RLOOP      TD        INDEV             . test if input device ready
           JEQ       RLOOP             . if not ready, keep waiting
           RD        INDEV             . read a byte from input device into A
           COMP      ZERO              . check if byte read is 0 (end of record)
           JEQ       EXIT              . if it is 0, exit read loop
           STCH      BUFFER,X          . store the character from A into buffer
           TIX       MAXLEN            . increment X and compare with max length
           JLT       RLOOP             . if X < MAXLEN, continue reading
EXIT       STX       LENGTH            . store number of chars read in LENGTH
           LDX       ZERO              . reset index register for writing
WLOOP      TD        OUTDEV            . test if output device ready
           JEQ       WLOOP             . if not, wait
           LDCH      BUFFER,X          . load character from buffer into A
           WD        OUTDEV            . write character from A to output device
           TIX       LENGTH            . increment X and compare with LENGTH
           JLT       WLOOP             . if X < LENGTH, keep writing
           RSUB                        . return (end of program)
INDEV      BYTE      X'F1'             . device code for input
OUTDEV     BYTE      X'06'             . device code for output
ZERO       WORD      0                 . constant zero
MAXLEN     WORD      4096              . maximum record length
LENGTH     RESW      1                 . space to store record length
BUFFER     RESB      4096              . buffer to hold input record
           END       FIRST             . end of program, entry at FIRST
