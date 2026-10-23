# Buongiorno Lulù
Quotidiano personale in A4, una facciata, con testata classica, primi piani Italia e Mondo, buona notizia, Marche, cultura, poesia integrale, psicologia e Sudoku con soluzione unica.

## Installazione
Caricare **tutti i file e la cartella `.github`** nella radice del repository GitHub `buongiorno-lulu` (sostituire i file omonimi). Attivare GitHub Pages dal ramo `main` / `(root)`. In Settings → Actions → General impostare i permessi workflow in **Read and write permissions**, se il repository non consente già il push da Actions. Aprire Actions → `Buongiorno Lulu - giornale quotidiano` → `Run workflow` una prima volta.

L'azione programmata gira tre volte per compensare l'ora legale; il sito pubblica il numero con la data italiana. I job programmati di GitHub **non garantiscono un minuto esatto**: l'ESP32 dovrà stampare solo quando `edizione.json` contiene la data odierna.

## Limiti importanti
I titoli e gli eventuali estratti sono ottenuti automaticamente da Google News RSS. Non c'è revisione editoriale umana, quindi la rilevanza e l'accuratezza **non sono garantite**; le fonti sono linkate sul sito. Se un feed non risponde, compare una dicitura esplicita e non una notizia inventata. La poesia è integrale e di pubblico dominio. Il JPEG A4 è destinato alla Canon, ma **lo sketch ESP32 per scaricarlo e inviarlo alla stampante non è incluso**: va adattato allo sketch IPP che ha già stampato correttamente.
