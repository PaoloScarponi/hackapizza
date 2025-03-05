# Project Description

This project contains the code for the Kaggle Challenge [Hackapizza 2025 - Community Edition](https://www.kaggle.com/competitions/hackapizza-2025-community).

## Manual Preprocessing Steps

We applied some simple manual pre-processing step to simplify the data ingestion step:

* Compressed Datapizza Menu from ~50MB to 2~MB.
* Updated some names in the dish_mapping file to compensate for inconsistencies.
  * "Sinfonia Astrale" -> "Sinfonia Astrale - Risotto Multiversale con Risacca Celeste"

## Instructions 

The sequence of operations required to produce the uploaded results are the following:

1. Create a .env file containing the following environment variables
   * OLLAMA_SERVER_URI=<put the URI to an Ollama Server Here, if you are hosting it on your machine use 
     http://localhost:11434>
   * LBP_MODEL_NAME=<Put the name of the Ollama Model to use for LLM-Based parsing here, we used gemma2:latest>
2. Execute the process_menu.py script to load every menu as a DoclingDocument and serialize the object as is. We 
   did this to speed up the experimentation phase by avoiding extracting the content of each pdf multiple times.
3. Execute the build_knowledge_base.py script to create the knowledge base, which consists of a set of json 
   descriptors, each containing the information of a single dish.
4. Execute the query_knowledge_base.py script to submit all the test questions to the system and save the results.

## Potential Post-Submission Improvements

* Double-check license extraction and filtering.
* Try to handle planets distances manually using function calling.
* Add order check, no matter if it is extracted from the question (low impact, low complexity).
* There are some questions that ask for subcategories of techniques, which we do not take care of (medium impact, medium complexity).
* The assumption that different attributes connect with each other with a _conjunction_ is not always valid (low impact, medium complexity).
* There are some questions about licenses required for a dish, which we do not take care of (medium impact, high complexity).
* There are some questions that ask for a certain number of ingredients or techniques among a larger set, which we do not take care of (medium impact, high complexity).
