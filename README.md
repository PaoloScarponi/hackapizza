# Project Description

This project contains the code for the Kaggle Challenge [Hackapizza 2025 - Community Edition](https://www.kaggle.com/competitions/hackapizza-2025-community).

## Instructions 

The sequence of operations required to produce the uploaded results are the following:

1. Create a .env file containing the following environment variables
   * LLM_URI=<put the URI to an Ollama Server Here, if you are hosting it on your machine use http://localhost:11434>
   * LLM_NAME=<Put the name of a LLM here, we used mistral:latest>
2. Execute the script process_menu.py to load every menu as a DoclingDocument and serialize the object as is. We did 
   this to speed up the experimentation phase by avoiding extracting the content of each pdf multiple times.
3. Execute the script build_knowledge_base.py to create the knowledge base, which consists of a set of json 
   descriptors, each containing the information of a single dish.
4. ...

## Improvements

* Handle noisy menus (Datapizza, L'Essenza delle Dune, Le Dimensioni del Gusto).
* Understand how to handle distances between planets.
* Understand how to handle orders.
* Understand how to handle substances law limits.
* Check unsure restaurants planets (L'Equilibrio Quantico - Tatooine, Le Stelle Danzanti - Undisclosed/Namecc)