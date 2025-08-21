import os
from dotenv import load_dotenv
load_dotenv()
from typing import Dict
from langchain_groq import ChatGroq
from langchain.agents import initialize_agent,AgentType
from langchain.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings


#embedded 
def get_embeddings():
    JD_embeded_file = r"D:\llmora\agents\embeddings\job_description"
    embeddings = HuggingFaceEmbeddings(model_name ="BAAI/bge-small-en",show_progress=True)
    db = FAISS.load_local(
    folder_path=JD_embeded_file,
    embeddings=embeddings,
    allow_dangerous_deserialization=True
    )
    return db




#shared meomery which initi..lize globally
class ResultStore():
    def __init__(self):
        self.texts: Dict[str,str] = {}
        self.name: Dict[str,str] = {}
        self.email: Dict[str,str] = {}
        self.phone: Dict[str,str] = {}
        self.summary: Dict[str,str] = {}
        self.scores: Dict[str,float] = {}

#shared meomery for scheduling info 
class ScheduleStore():
    def __init__(self):
        self.name: Dict[str,str] = {}
        self.email: Dict[str,str] = {}
        self.start_time: Dict[str,str] = {}
        self.end_time: Dict[str,str] = {}
        self.link: Dict[str,str] = {}

#Agent initialization
def create_agent(tools,llm):
    agent = initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
        handle_parsing_errors=True,
        return_intermediate_steps=True
    )
    return agent

#definig llm
def get_llm():
    groq_api_key = os.getenv("GROQ_API_KEY")
    llm = ChatGroq(model="gemma2-9b-it",groq_api_key=groq_api_key)
    return llm


