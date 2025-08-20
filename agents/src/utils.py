import os
from dotenv import load_dotenv
load_dotenv()
from typing import Dict
from langchain_groq import ChatGroq
from langchain.agents import initialize_agent,AgentType

#shared meomery which initi..lize globally
class ResultStore():
    def __init__(self):
        self.texts: Dict[str,str] = {}
        self.info: Dict[str,dict] = {}
        self.summaries: Dict[str,str] = {}
        self.scores: Dict[str,float] = {}


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