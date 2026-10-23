# Buongiorno Lulù

Quotidiano personale A4 con grafica originale conservata in genera.py e riferimento ESEMPIO_GRAFICA_APPROVATA.pdf.

Il workflow .github/workflows/quotidiano.yml genera PDF, JPEG, pagina web e dati dell'edizione. Parte alle 04:17, 05:17 e 06:17 UTC ogni giorno (06:17, 07:17, 08:17 con ora legale italiana; 05:17, 06:17, 07:17 con ora solare), oltre che alle modifiche del generatore e su richiesta manuale. GitHub può ritardare i job programmati.

Sito: https://antucpa.github.io/buongiorno-lulu/

L'automazione usa i feed pubblici già previsti dal generatore e non richiede chiavi API. Se tutti i feed falliscono, il workflow si ferma prima di pubblicare per preservare l'ultima edizione. Le fonti originali sono consultabili sul sito. La stampa ESP32 richiede il dispositivo e relativo sketch, non inclusi qui.
