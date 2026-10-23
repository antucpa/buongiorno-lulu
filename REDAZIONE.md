# Redazione di Buongiorno Lulù

La selezione non usa il primo titolo di un feed. La preparazione quotidiana è affidata all'automazione ChatGPT «Prepara Buongiorno Lulù», al mattino nella fascia delle 06:00 Europe/Rome. Il file contenuti.json avvia il workflow GitHub per generazione e pubblicazione; non serve una chiave API nel repository.

Scrivere cinque sintesi originali, comprensibili senza aprire i link. Leggere fonti reali, verificare date, luoghi e attribuzioni. Rubriche: italia e mondo (55–65 parole), buona e marche (35–42), cultura (40–50). Titoli entro 65 caratteri. Italia e mondo: ultime 24 ore. Macerata: ultimi 3 giorni. Cultura e buona notizia: preferibilmente ultimi 3 giorni, fino a 7 giorni se rilevanti, con data trasparente. Nessuna invenzione, testo generico o rinvio al sito al posto della notizia.

Schema: data odierna YYYY-MM-DD e notizie con le cinque chiavi; campi title, description, source, url diretto HTTPS, published_at (data della notizia verificata YYYY-MM-DD), ambito (macerata per marche; nazionale o internazionale per tutte le altre). Se impossibile completare una rubrica, non aggiornare il file e segnalare il problema.

Il generatore controlla tutte le rubriche e la capienza dei riquadri. Il workflow controlla che le sintesi siano presenti per intero nel PDF. L'edizione precedente resta online fino alla consegna di contenuti nuovi e completi. Impaginazione A4 originale, caratteri, colori, testata, poesia e sudoku conservati.

## Selezione geografica

Una sola notizia locale: esclusivamente la città di Macerata nella chiave tecnica marche. Tutte le altre rubriche hanno respiro nazionale o internazionale. Escludere cronaca locale/regionale e piccole iniziative di altre città. La cultura comprende teatro, cinema, musical, libri, musica e arte anche internazionali: privilegiare novità, grandi produzioni, festival e temi di rilievo. La sede di un fatto non basta a renderlo locale: conta il suo rilievo.

## Meteo quotidiano di Macerata

Consultare le previsioni odierne per Macerata città nelle Marche. Aggiungere meteo: data odierna YYYY-MM-DD, localita Macerata, condizioni (massimo 90 caratteri), min_c e max_c numerici in Celsius per l'intera giornata, source e url HTTPS realmente consultato. Non confondere Macerata con Macerata Campania o Feltria. Non usare la temperatura attuale come minima/massima. Se una fonte manca, cercarne un'altra. Il generatore verifica data, località, temperature e fonte prima di stampare il riquadro meteo.

## Da leggere

Aggiungere il blocco libro: titolo e autore entro 55 caratteri ciascuno; consiglio originale di 24–32 parole (limite 20–34), senza spoiler, che spieghi il valore della lettura; source e url HTTPS verificato presso l'editore o un catalogo autorevole. Non copiare la quarta di copertina. Alternare autori italiani e stranieri, gialli, romanzi e classici, senza limitarsi a nuove uscite o temi locali. Conservare libri_proposti (fino a 90 elementi con titolo, autore, data), evitare ripetizioni e aggiungere la scelta odierna. La rubrica occupa la colonna accanto al Sudoku, sotto la notizia di Macerata. Il workflow verifica che titolo, autore e consiglio siano leggibili integralmente nel PDF.

## Idea di viaggio

Aggiungere il blocco viaggio con meta (massimo 45 caratteri, Paese/area chiari), consiglio originale di 24–30 parole (limite 20–34), source e url HTTPS verificato di un ente turistico o di un'attrazione ufficiale. Indicare uno o due spunti concreti, senza prezzi, orari o affermazioni pratiche non verificati. Alternare destinazioni italiane e straniere, arte e natura. È una proposta di viaggio, distinta dalle cinque notizie. Conservare viaggi_proposti (ultime 90 mete con data), evitare ripetizioni e aggiungere la nuova scelta. La cultura occupa la colonna sinistra con titolo piccolo sopra il testo; la proposta di viaggio occupa la colonna destra. Per la cultura preferire titoli entro 55 caratteri. Il workflow verifica l'integrità dei testi nel PDF.
