# Project Description

This project contains the code for the Kaggle Challenge [Hackapizza 2025 - Community Edition](https://www.kaggle.com/competitions/hackapizza-2025-community).

## Manual Preprocessing Steps

We applied some simple manual pre-processing step to simplify the data ingestion step:

* Compressed Datapizza Menu from 50MB to 2MB.
* Updated some names in the dish_mapping file to compensate for inconsistencies.
  * "Sinfonia Astrale" -> "Sinfonia Astrale - Risotto Multiversale con Risacca Celeste"

## Instructions 

The sequence of operations required to produce the uploaded results are the following:

1. Create a .env file containing the following environment variables
   * OLLAMA_SERVER_URI=...
     * put the URI to an Ollama Server Here, if you are hosting it on your machine use http://localhost:11434
   * LBP_MODEL_NAME=...
     * Put the name of the Ollama Model to use for LLM-Based parsing here, we used gemma2:latest for generating the Knowledge Base and gemma2:27b for answering questions.
2. Execute the process_menu.py script to load every menu as a DoclingDocument and serialize the object as is. We 
   did this to speed up the experimentation phase by avoiding extracting the content of each pdf multiple times.
3. Execute the build_knowledge_base.py script to create the knowledge base, which consists of a set of json 
   descriptors, each containing the information of a single dish.
4. Execute the query_knowledge_base.py script to submit all the test questions to the system and save the results 
   inside the 'data' folder, in a versioned and submission-ready file named 'test_answers.csv'.

## Potential Post-Submission Improvements

* There are some questions that ask for subcategories of techniques, which we do not take care of (high impact, medium complexity).
  * Quali piatti includono gli Spaghi del Sole e sono preparati utilizzando almeno una tecnica di Surgelamento del di Sirius Cosmo?
  * Quali piatti, realizzati utilizzando almeno una tecnica di taglio descritta nel di Sirius Cosmo, includono i Fusilli del Vento nella preparazione?
  * Quali piatti sono preparati utilizzando almeno una tecnica di taglio e una di surgelamento secondo il di Sirius Cosmo, ma senza l'uso di Polvere di Crononite?
  * Quali piatti sono preparati utilizzando sia tecniche di impasto che di taglio, ma senza l'uso di Shard di Prisma Stellare?
  * Quali piatti creati con almeno una tecnica di taglio dal Manuale di Cucina di Sirius Cosmo e che necessitano della licenza t non base per la preparazione, escludendo quelli con Fusilli del Vento, sono serviti?
* There are some questions about licenses required for a dish, which we do not take care of (high impact, high complexity).
  * Quali piatti preparati su Asgard richiedono la licenza temporale superiore a 0 e includono Farina di Nettuno?
  * Quali piatti, preparati in un ristorante su Asgard, richiedono la licenza LTK non base e utilizzano Carne di Xenodonte?
  * Quali piatti, che necessitano almeno della licenza P di grado 2 per essere preparati, serviti in un ristorante su Pandora, utilizzano Spore Quantiche?
  * Quali piatti che necessitano della licenza e+ con un grado minimo di 1 sono serviti su Arrakis e utilizzano l'ingrediente Riso di Cassandra?
* There are some questions that ask for a certain number of ingredients or techniques among a larger set, which we do not take care of (high impact, high complexity).
  * Quali piatti contengono almeno 2 ingredienti tra Spore Quantiche, Latte+ e Radici di Singolarità?
  * Quali piatti contengono almeno 2 ingredienti tra Ravioli al Vaporeon, Spaghi del Sole e Nettare di Sirena?
  * Quali piatti contengono almeno 2 ingredienti tra Polvere di Crononite, Nduja Fritta Tanto, Spezie di Melange e Polvere di Stelle?
  * Quali piatti contengono almeno 2 ingredienti tra Carne di Drago, Chocobo Wings, Foglie di Mandragora e Burrobirra?
* The assumption that different attributes connect with each other with a _conjunction_ is not always valid (low impact, medium complexity).
  * Quali sono i piatti serviti al ristorante L'Universo in Cucina che utilizzano Frammenti di Supernova o la tecnica di Fermentazione Psionica Energetica?
  * Quali piatti del ristorante Cosmica Essenza sono preparati utilizzando i Funghi dell’Etere o la tecnica di Marinatura Temporale Sincronizzata?
  * Quali piatti sono creati da uno chef con almeno la licenza LTK di grado 6 che utilizza Polvere di Pulsar o la tecnica di Cottura al Forno con Paradosso Temporale Cronospeculare?
