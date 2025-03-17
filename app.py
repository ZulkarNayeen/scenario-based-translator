import streamlit as st

from langchain_community.document_loaders import PDFPlumberLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_ollama import OllamaEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM

template = """
You are an assistant for question-answering tasks. Use the following pieces of retrieved context to answer the question. If you don't know the answer, just say that you don't know. Use three sentences maximum and keep the answer concise.
Question: {question} 
Context: {context} 
Answer:
"""

pdfs_directory = "./pdf/"
model_name = "deepseek-r1:latest"

print("[INFO] Loading embeddings...")
embeddings = OllamaEmbeddings(model=model_name)
print("[INFO] Embeddings loaded!\n[INFO] Loading vector store...")
vector_store = InMemoryVectorStore(embeddings)
print("[INFO] Vector store loaded!\n[INFO] Loading model...")
model = OllamaLLM(model=model_name)
print("[INFO] Model loaded!")

def upload_pdf(file):
    with open(pdfs_directory + file.name, "wb") as f:
        f.write(file.getbuffer())
        
def load_pdf(file_path):
    loader = PDFPlumberLoader(file_path)
    documents = loader.load()
    return documents

def split_text(documents):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        add_start_index=True
    )

    return text_splitter.split_documents(documents)

def index_docs(documents):
    vector_store.add_documents(documents)

def retrieve_docs(query):
    return vector_store.similarity_search(query)

def answer_question(question, documents):
    context = "\n\n".join([doc.page_content for doc in documents])
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | model
    
    return chain.invoke({"question": question, "context": context})

uploaded_file = st.file_uploader(
    "Upload PDF",
    type="pdf",
    accept_multiple_files=False
)

if uploaded_file:
    upload_pdf(uploaded_file)
    print("[INFO] PDF uploaded!")
    question = st.chat_input()

    if question:
        st.chat_message("user").write(question)
        documents = load_pdf(pdfs_directory + uploaded_file.name)
        print("[INFO] PDF loaded!")
        chunked_documents = split_text(documents)
        print("[INFO] documents chunked!")
        index_docs(chunked_documents)
        print("[INFO] documents indexed!")
        related_documents = retrieve_docs(question)
        print("[INFO] documents retrieved!")
        answer = answer_question(question, related_documents)
        print("[INFO] Answer generated!")
        st.chat_message("assistant").markdown(answer)