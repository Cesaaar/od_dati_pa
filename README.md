# Metadati Open Data Pubblica Amministrazione

Analisi del **catalogo dei dati aperti** della Pubblica Amministrazione Italiana 

## Fonti Dati
| Fonte | Descrizione | Link |
| ------ | ------ | ------ |
| AGID | Agenzia per l'Italia Digitale |https://www.dati.gov.it |

## Visualizzazioni
| File | Descrizione |
| ------ | ------ |
| input/XXX_DSMetadatiPA.csv | Dataset dei metadati degli open data |
| output/Cataloghi Dataset.png | Distribuzione dataset per catalogo padre |
| output/Gruppi Dataset.png | Distribuzione dataset per gruppo/tematica |
| output/XXX_Note_WordCloud.png | Word Cloud sul campo note |
| output/XXX_Titolo_WordCloud.png | Word Cloud sul campo titolo |

## Configurazioni
Queste istruzioni ti permetteranno di realizzare una copia del progetto in locale per eseguire il codice.

#### Prerequisiti
1. Installare l'ambiente Anaconda, comprende Jupyter. https://docs.anaconda.com/anaconda/install/
2. Copiare il repository sul proprio account GitHub.
3. Copiare il repository in locale

#### Librerie aggiuntive
Anaconda installa in automatico più di 150 package per analisi dati.
Libreria **luigi** per l'esecuzione batch di API_Dati_Pubblici_Luigi.py il cui compito è di realizzare il Dataset dei metadati.
Libreria **nltk** per la realizzazione del World Cloud
