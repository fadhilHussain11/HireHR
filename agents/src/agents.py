import json, pdfplumber
from src.utils import ResultStore,create_agent,get_llm
from pydantic import BaseModel, Field, field_validator
from langchain.tools import StructuredTool
from langchain.prompts import SystemMessagePromptTemplate,HumanMessagePromptTemplate,ChatPromptTemplate


#llm model
llm = get_llm()

#initili...lize store for storing result
STORE = ResultStore()

#Making Tools 

#----------load pdf first tool and stores to STORE ----> texts--------

#definiing validation both input and output components to ensure the better ussage of tools
#input validation 
class LoadInput(BaseModel):
    resume_id: str = Field(...,description="A unique id to refer to this resume") # means Field are like a constraints which ensure it should not be not null (...) and give description 
    save_path: str = Field(...,description="FilePath of the pdf")

#output validation
class LoadOutput(BaseModel):
    texts: str = Field(...,description="Extracted text from pdf")

    @field_validator("texts")
    def check_not_null(txt):
        if not txt.strip():
            raise ValueError("No text extracted from pdf.")
        return txt
    
#function to load the pdf 
def load_pdf_and_store(resume_id,save_path):
    with pdfplumber.open(save_path) as pdf:
        text = "\n".join((p.extract_text() or "") for p in pdf.pages)
    
    #validating output
    validated_output = LoadOutput(texts=text)

    #store
    STORE.texts[resume_id] = validated_output.texts
    print(validated_output)
    return validated_output

#define load and store TOOl
LOADPDFTOSTORE = StructuredTool.from_function(
    func=load_pdf_and_store,
    name="LoadPdfStore",
    description="Extracts text from a PDF and saves it in STORE",
    args_schema=LoadInput,
    return_schema = LoadOutput
)


#------------- WholeResult saving Tools -----------

#input validation , for this we dont want need output validation 
class WholeresultInput(BaseModel):
    resume_id: str = Field(...,description="A unique id to refer to this resume")

#defining tools function 
def whole_result(resume_id):
    text = STORE.texts.get(resume_id,"")
    result_out = {
        "text" : text
    }
    return json.dumps(result_out)


#defining WholeResult TOOL
WHOLERESULT = StructuredTool.from_function(
    func=whole_result,
    name="WholeResult",
    description="returns final JSON with text for the given resume_id",
    args_schema=WholeresultInput
)

#defining list of tools
tools = [LOADPDFTOSTORE,WHOLERESULT]

#agent initi...lization
agent = create_agent(
    tools=tools,
    llm=llm,
)


def call_agent(resume_id:str,save_path:str) -> dict:
    system_template = """You must process resume in EXACTLY this order:
    1) LOADPDFTOSTORE(resume_id,save_path)
    2) WHOLERESULT(resume_id)  <-- return THIS as the final output


    Rules:
    - DO NOT print or Return the full resume text anywhere
    - The ONLY final answer should be the JSON returned by WholeResult.
    """
    system_prompt = SystemMessagePromptTemplate.from_template(system_template)


    human_template = "resume_id={resume_id}, save_path={save_path}"
    human_prompt = HumanMessagePromptTemplate.from_template(human_template)

    chat_prompt = ChatPromptTemplate.from_messages([system_prompt,human_prompt])

    out = agent.invoke(chat_prompt.format_prompt(resume_id=resume_id,save_path=save_path))
    result = out.get("output") if isinstance(out,dict) else str(out)
    try:
        return json.loads(result) # bt this loads by model if not , do by whole_result()
    except Exception:
        return json.loads(whole_result(resume_id))

    