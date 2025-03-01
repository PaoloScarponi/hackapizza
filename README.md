# Project Description

This project contains the code for the Kaggle Challenge [Hackapizza 2025 - Community Edition](https://www.kaggle.com/competitions/hackapizza-2025-community).

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
4. ...

## Improvements

### Online Creation

* Understand how to handle distances between planets.

### Offline Phase

* Understand the effect of not using ingredients categories and techniques subcategories on the performance.
* Understand the effect of not updating the chef licenses based on dishes techniques.
* Understand the effect of not handling substances law limits.
