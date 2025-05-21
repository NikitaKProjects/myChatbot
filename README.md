# 🤖 myChatbot

A conversational AI chatbot powered by **Large Language Models (LLMs)** using **Retrieval-Augmented Generation (RAG)** with a **FAISS vector store** and **document parsing via Unstructured**.

---

## 🚀 Features

* **Contextual Responses**: Get answers based on your own documents.
* **Fast Similarity Search**: Leverages **FAISS** for efficient document retrieval.
* **Markdown Support**: Processes `.md` documents using the **Unstructured** library.
* **FastAPI Backend**: Includes a development server with **hot reload** for quick iterations.

---

## 🛠️ Complete Setup & Run Instructions

Follow these exact steps to get myChatbot up and running smoothly on your machine.

### 1. Clone the Repository

Start by cloning the project to your local machine:

```bash
git clone https://github.com/NikitaKProjects/myChatbot.git
cd myChatbot
```

### 2. Install Python Dependencies

Install all necessary Python libraries:

```bash
pip install -r requirements.txt
pip install unstructured
pip install "unstructured[md]"
pip install python-magic
```

### 3. Fix NLTK Errors (If Any)

If you encounter errors about missing NLTK data, run the following commands to download them:

```bash
python -c "import nltk; nltk.download('punkt')"
python -c "import nltk; nltk.download('averaged_perceptron_tagger')"
```

**Note**: If you encounter SSL certificate errors during these downloads, you might need to configure your system to properly verify SSL certificates. One common solution is to set the `REQUESTS_CA_BUNDLE` environment variable to the path of your `cacert.pem` file. This helps Python's `requests` library (used by NLTK in some cases) verify SSL certificates properly. The location of `cacert.pem` varies by operating system and Python installation. You may need to search for it on your system or consult your Python documentation.

### 4. Create the FAISS Vector Store

Generate the FAISS vector store from your documents:

```bash
python create_database.py
```

### 5. Configure Your OpenAI API Key

Create a file named `.env` in the root directory of the project and paste your OpenAI API key into it like this:

```
OPENAI_API_KEY="your_openai_api_key_here"
```

**Remember to replace `"your_openai_api_key_here"` with your actual API key.**

### 6. Run the FastAPI Server

Start the FastAPI backend server:

```bash
uvicorn app.main:app --reload
```

### 7. Open the Chatbot in Your Browser

Once the server is running, access the chatbot at:

[http://127.0.0.1:8000](http://127.0.0.1:8000)

Now you're ready to chat!
