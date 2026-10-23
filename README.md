# Buongiorno Lulù

Quotidiano personale A4: https://antucpa.github.io/buongiorno-lulu/

## Generazione quotidiana

L'automazione ChatGPT «Prepara Buongiorno Lulù» ricerca e sintetizza le notizie ogni mattina nella fascia delle 06:00 italiane e aggiorna contenuti.json tramite il collegamento GitHub autorizzato. Questo avvia il workflow quotidiano.yml, che genera e pubblica PDF, JPEG e pagina web. Non servono chiavi API. Gli orari di esecuzione e pubblicazione possono variare.

Il workflow può essere avviato manualmente ed esegue controlli aggiuntivi alle 04:17, 05:17 e 06:17 UTC. Se i contenuti odierni non sono ancora pronti, salta la generazione e conserva l'edizione precedente. Le cinque rubriche devono avere testi completi, fonti e date recenti. Nessun titolo RSS viene pubblicato come articolo. La verifica del PDF impedisce tagli dei testi.

La grafica originale è mantenuta in genera.py; ESEMPIO_GRAFICA_APPROVATA.pdf resta il riferimento. Le istruzioni editoriali sono in REDAZIONE.md. Le sintesi sono preparate con assistenza AI: le fonti dirette consentono verifica e approfondimenti. La stampa ESP32 richiede dispositivo e relativo sketch.
