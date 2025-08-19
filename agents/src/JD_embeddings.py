import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings

embedding_directory = os.path.join(os.path.dirname(os.path.dirname(__file__)),"embeddings","job_description")


#init...lize embedding by huggingface
embeddings = HuggingFaceEmbeddings(model_name ="BAAI/bge-small-en",show_progress=True)

def job_embedding(description):
    splitter = RecursiveCharacterTextSplitter(
    chunk_size=600,
    chunk_overlap=100
    )
    job_chunks = splitter.split_text(description)
    faiss_store = FAISS.from_texts(
        texts=job_chunks,
        embedding=embeddings
    )
    os.makedirs(embedding_directory,exist_ok=True)
    faiss_store.save_local(embedding_directory)
    print("done")
    return "embedding successfully"

