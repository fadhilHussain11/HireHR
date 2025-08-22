import random,json
from agents.src.utils import create_agent,get_llm
from pydantic import BaseModel, Field, field_validator,model_validator
from langchain.tools import StructuredTool
from agents.src.google_auth import get_calender_service
from datetime import datetime, timedelta
from langchain.prompts import SystemMessagePromptTemplate,HumanMessagePromptTemplate,ChatPromptTemplate

llm = get_llm()



#--------Google Calender Tool-----------

class CalenderInput(BaseModel):
    name:str = Field(...,description="Name of the person")
    email:str = Field(...,description="Email address of the person")

def scheduler_calender(name,email):
    calender_service = get_calender_service()
    #randomly select a date from tommorow

    #start time
    base_date = datetime.now() + timedelta(days=13)
    start_hours = random.randint(10,16) #10am-4pm
    start_minute = random.choice([0,15,30,45]) #select time like 3:30,10:45,2:15
    start_time = base_date.replace(hour=start_hours, minute=start_minute,second=0,microsecond=0)

    #end time the interview only b/w 30-40 minutes
    duration_minutes = random.choice([30,40])
    end_time = start_time + timedelta(minutes=duration_minutes)

    #convert into ISO
    start_iso = start_time.isoformat()
    end_iso = end_time.isoformat()

    #event init..lizing
    event = {
        "summary": f"Interview: {name}",
        "start": {"dateTime": start_iso, "timeZone":"Asia/Kolkata"},
        "end": {"dateTime": end_iso, "timeZone":"Asia/Kolkata"},
        "attendees" : [
            {
                "email":email,
                "displayName":name
            }
        ],
        "sendUpdates":"all",
        "description":f"Interview invitation from AbcMachine.ltd\n\n",
        "extendedProperties":{
            "private":{
                "companyName":"AbcMachine.ltd",
                "organizerContact":"abcmachineOfficial@gmail.com"
            }
        }
    }
    created_event = calender_service.events().insert(
        calendarId="primary",body=event,
    ).execute()

    calender_link = created_event.get('htmlLink')

    response_message = {
        "name" : name,
        "calender_link":calender_link,
        "status":"success"
    }
    
    return response_message


CALENDER_TOOL = StructuredTool(
    name="GoogleCalenderTool",
    func=scheduler_calender,
    description="Schedules interview in Google Calender",
    args_schema=CalenderInput
)

tools = [CALENDER_TOOL]

#agent initi...lization
agent = create_agent(
    tools=tools,
    llm=llm,
)

def call_schedule_agent(name:str,email:str) -> dict:
    response_list = []
    system_template = """YOU are strict scheduler. your only job is to scedule an interview by calling 
    CALENDER_TOOL(name,email) Exactly, when all required parametrs are provided.

    Rules:
    1. If name, and email are provided -> call CALENDER_TOOL(name,email)
    2. do the scheduling by scheduler_calender function which is provided by tool
    3.The ONLY final answer should be the dictionary returned by CALENDER_TOOL.
    """

    system_prompt = SystemMessagePromptTemplate.from_template(system_template)

    human_template = "name={name}, email={email}"
    human_prompt = HumanMessagePromptTemplate.from_template(human_template)

    chat_prompt = ChatPromptTemplate.from_messages([system_prompt,human_prompt])
    out = agent.invoke(chat_prompt.format_prompt(name=name,email=email))
    result = out.get("output") if isinstance(out,dict) else str(out)
    return result # bt this loads by model if not , do by whole_result()