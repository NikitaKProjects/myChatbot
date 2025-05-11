# prepares data for a Retrieval-Augmented Generation (RAG) chatbot by reading .md files, 
# splitting them into chunks, converting them to vector embeddings, 
# and saving them to a FAISS index for later use.
from langchain_community.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv
import os
import shutil

load_dotenv()

assert os.getenv("OPENAI_API_KEY"), "API Key not found in environment variables!"

DATA_PATH = "app/data/books"
FAISS_PATH = "faiss_index"

def load_documents():
    loader = DirectoryLoader(DATA_PATH, glob="*.md")
    return loader.load()

def split_text(documents: list[Document]):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=200,          # smaller chunks
        chunk_overlap=50,
        length_function=len,
        add_start_index=True,
    )
    chunks = text_splitter.split_documents(documents)
    print(f"Split {len(documents)} documents into {len(chunks)} chunks.")
    return chunks

def save_to_faiss(chunks: list[Document]):
    if os.path.exists(FAISS_PATH):
        shutil.rmtree(FAISS_PATH)

    embedding_function = OpenAIEmbeddings()
    db = FAISS.from_documents(chunks, embedding_function)
    db.save_local(FAISS_PATH)
    print(f"Saved {len(chunks)} chunks to {FAISS_PATH}.")

def main():
    documents = load_documents()
    chunks = split_text(documents)
    save_to_faiss(chunks)

if __name__ == "__main__":
    main()
