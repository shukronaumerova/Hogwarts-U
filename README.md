# Hogwarts Ubot (t.me/Hogwarts_ubot)

A Telegram bot that answers questions about Hogwarts Summer School. 

## Features
- Loads custom data from data.txt
- Uses LangChain and HuggingFace models
- Retrieves answers with sources
- Easy Telegram integration

## Technologies
- Python
- LangChain
- HuggingFace Transformers
- FAISS
- Telegram Bot API

## Setup
1. Add your Telegram token.
2. Install dependencies from requirements.txt
   **pip install -r requirements.txt**
#. Run main.py
   **python main.py**

## How it works
1. The user asks any question.
2. The bot searches for the most relevant part from 'data.txt'
3. The text split into smaller chunks using Langchain.
4. Each chunk converts into a vector using HuggingFace embeddings.
5. The chunk and a question are sent to a LLM to get an answer.
6. The answer is returned to the user through the Telegram bot.
   
## Limitations
- Only answers based on data.txt
- Doesn't learn new informations after deployment
- Runs a little slower
- Sometimes confuses words/answers to questions that user write

## Author
Created by Shukrona Umerova
