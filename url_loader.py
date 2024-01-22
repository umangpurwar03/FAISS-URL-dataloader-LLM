from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.document_loaders.recursive_url_loader import RecursiveUrlLoader
from bs4 import BeautifulSoup as Soup
import os
import threading

# Define paths
url = "https://mydukaan.io/"
faiss_db = 'vectorstore/db_faiss'

def process_url_content(content):
    # Initialize HuggingFaceEmbeddings using a specific model
    embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2', model_kwargs={'device': 'cpu'})
    
    # Create a vector store using FAISS from the text content and embeddings
    db = FAISS.from_documents([content], embeddings)
    
    # Save the vector store locally
    db.save_local(os.path.join(faiss_db, f"url_content_db"))
    print(f"Vector store saved for content from URL")

def process_urls_in_parallel():
    # Ensure the directory exists
    if not os.path.exists(faiss_db):
        os.makedirs(faiss_db)
        print(f"Created directory: {faiss_db}")

    # Load content from URL using RecursiveUrlLoader
    loader = RecursiveUrlLoader(
        url=url, max_depth=2, extractor=lambda x: Soup(x, "html.parser").text
    )
    contents = loader.load()
    print(contents)
    print(f"URL content loaded from {url}")

    # Create threads for each URL content processing
    threads = []
    for content in contents:
        thread = threading.Thread(target=process_url_content, args=(content,))
        threads.append(thread)
        thread.start()
        print(f"Processing content from URL in a thread")

    # Wait for all threads to complete
    for thread in threads:
        thread.join()
        print(f"Thread completed")

if __name__ == "__main__":
    process_urls_in_parallel()
