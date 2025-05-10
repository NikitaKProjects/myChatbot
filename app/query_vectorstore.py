import logging
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from dotenv import load_dotenv
import os
import tiktoken

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

if not openai_api_key:
    raise ValueError("No OpenAI API key found in environment variables.")

logging.basicConfig(level=logging.INFO)

llm = ChatOpenAI(openai_api_key=openai_api_key, model="gpt-3.5-turbo")

encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")

def count_tokens(text: str) -> int:
    return len(encoding.encode(text))

def truncate_context(context: str, max_tokens: int = 12000) -> str:
    tokens = encoding.encode(context)
    if len(tokens) <= max_tokens:
        return context
    return encoding.decode(tokens[:max_tokens])

def query_vectorstore(query: str, db_path: str):
    logging.info("Loading FAISS vectorstore...")

    try:
        vectorstore = FAISS.load_local(
            db_path, OpenAIEmbeddings(openai_api_key=openai_api_key),
            allow_dangerous_deserialization=True
        )
    except Exception as e:
        logging.error(f"Error loading vectorstore: {e}")
        return "Error loading the vectorstore."

    logging.info("Running similarity search...")

    try:
        results = vectorstore.similarity_search(query, k=3)
    except Exception as e:
        logging.error(f"Error during similarity search: {e}")
        return "Error during the similarity search."

    try:
        context = "\n\n".join([doc.page_content for doc in results])
        context = truncate_context(context)
    except Exception as e:
        logging.error(f"Error processing context: {e}")
        return "Error processing the content."

    prompt = f"Based on the following context, please answer the question:\n\nContext:\n{context}\n\nQuestion: {query}"

    try:
        response = llm.invoke(prompt)
        return response.content if hasattr(response, "content") else str(response)
    except Exception as e:
        logging.error(f"Error during LLM processing: {e}")
        return "Error generating the response."
