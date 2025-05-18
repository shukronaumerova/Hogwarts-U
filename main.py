from typing import Final
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

    # import langchain dependencies
from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA
from transformers import pipeline

# === Telegram token and bot username ===
TOKEN: Final = '8117749042:AAFUyKUq-xc2JA5WVMf4gTXP47y9UkIXpTI'
BOT_USERNAME: Final = '@Hogwarts_ubot'

# === Prepare langchain ===
def setup_qa_chain():
    # Load the text file
    loader = TextLoader('data.txt')
    documents = loader.load()

    # Split the documents into smaller chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    texts = text_splitter.split_documents(documents)

    # Create embeddings
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    # Create a vector store
    vector_store = FAISS.from_documents(texts, embeddings)

    # Create a retrieval QA chain
    qa_chain = RetrievalQA.from_chain_type(
        llm=pipeline("text2text-generation", model="facebook/bart-large-cnn"),
        chain_type="stuff",
        retriever=vector_store.as_retriever(search_kwargs={"k": 1}),
        return_source_documents=True,
    )

    return qa_chain

# Initialize qa_chain globally
qa_chain = setup_qa_chain()

# === Telegram commands ===
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text("Assalamu alaikum, I'm Hogwarts Ubot. Ask me anything about Hogwarts Summer School!")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("I can help you with information about Hogwarts Summer School. Just ask me anything!")

async def connect_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("You can connect with the creator of this bot here: @shuna_u")

# === reply to any text message from the user ===
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    response = qa_chain({"query": user_message})
    answer = response['result']
    source_documents = response['source_documents']

    # Format the answer and sources
    formatted_answer = f"Answer: {answer}\n\nSources:\n"
    for doc in source_documents:
        formatted_answer += f"- {doc.metadata['source']}\n"

    await update.message.reply_text(formatted_answer)

# === Main function to run the bot ===
async def main():
    # Create the application
    application = ApplicationBuilder().token(TOKEN).build()

    # Register handlers
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("connect", connect_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Run the bot
    print("Bot is running...")
    application.run_polling()

if __name__ == "__main__":
    main()
    