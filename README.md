# Calendario_Appuntamenti
Un piccolo e umile calendario scritto in Python per gestire i propri appuntamenti

Questo piccolo programma è generato per creare degli appuntamenti selezionando anno/mese/giorno/ora/minuti che verranno salvati in dei file .txt sul Desktop.
Il calendario può creare più appuntamenti alla volta, e all'apertura rimane "idle" in un'icona sul taskbar, implementata attraverso il modulo ctypes. Tuttavia, a causa di problemi d'implementazione, l'icona ha qualche difetto, e non è completamente interattiva (per farla sparire dalla chiusura del programma basta passarci sopra col cursore, purtroppo)

Il programma può essere eseguito in due modi:

1. Eseguire il file Python (.py) originale. Questo può essere fatto installando l'interprete di Python ufficiale (nello sviluppo io ho usato Python 3.12), e importare il modulo tk tkcalendar aprendo il terminal, e digitando
   "pip install tk tkcalendar", oppure attraverso il file "requirements.txt", digitando "pip install -r requirements.txt";

2. Eseguire l'.exe che al momento viene segnalato dai sistemi di protezione, a causa delle signature del compiler (Pyinstaller 6.1.0) che risultano "diffamate" da idioti che hanno abusato del compiler per buildare malware.
   In ogni caso, se si è paranoici, raccomando l'esecuzione dell'.exe su VMware, o VirtualBox.

Opinione di VirusTotal sull'artefatto .exe
https://www.virustotal.com/gui/file/1cb87958d1086306c5026a2fe698082c53beb044fd1f1f6af0ad1d1a406c4fdd/detection

SHA-256: 1cb87958d1086306c5026a2fe698082c53beb044fd1f1f6af0ad1d1a406c4fdd

OS Requirements per lanciare l'.exe: Windows 10 AMD64 (minimo)
Tutti gli OS inferiori al 10 e con processore i386 sono incompatibili.
