
from  langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import openai
from langchain.chat_models import ChatOpenAI
from langchain.callbacks import get_openai_callback
from pypdf import PdfReader

def process_text(text):
    text_splitter =CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')
    knowledgebase = FAISS.from_texts(chunks,embeddings)
    return knowledgebase

def summarizer(pdf):
    if pdf is not None:
        pdf_reader=PdfReader(pdf)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() or ""
        knowledgebase =process_text(text)
        query = "Summarize the content of the uploaded PDF file in approximately 3-5 sentences."
        
        if query:
            docs = knowledgebase.similarity_search(query)
            
            Model = "gpt-3.5-turbo-16k"
            llm= ChatOpenAI(model=Model,temprature=0.6)
            chain = load_qa_chain(llm,chain_type='stuff')
            
            response= chain.run(input_documents=docs , question=query)
            return response
        

