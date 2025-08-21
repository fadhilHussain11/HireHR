import random
from agents.src.utils import ScheduleStore,create_agent,get_llm
from pydantic import BaseModel, Field, field_validator,model_validator
from langchain.tools import StructuredTool
from agents.src.google_auth import calender_service
from datetime import datetime, timedelta
from langchain.prompts import SystemMessagePromptTemplate,HumanMessagePromptTemplate,ChatPromptTemplate

llm = get_llm()

STORE = ScheduleStore()

Schedules_info = []

#--------Google Calender Tool-----------

class CalenderInput(BaseModel):
    u_id:str = Field(...,description="Unique Id of the person")
    name:str = Field(...,description="Name of the person")
    email:str = Field(...,description="Email address of the person")

def scheduler_calender(u_id,name,email):
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
        "guestCanInviteOthers":False,
        "guestCanModify":False,
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

    #saving all varibles to ScheduleStore
    STORE.name[u_id] = name
    STORE.email[u_id] = email
    STORE.start_time[u_id] = start_iso
    STORE.end_time[u_id] = end_iso
    STORE.link[u_id] = calender_link

    Schedules_info.append({"name":name,"email":email,"start_time":start_iso,"end_time":end_iso,"link":calender_link}) #this dict will sent returned to HR 
    print("fadhil hi",Schedules_info)
    return f"Scheduled: {calender_link}"


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

def call_schedule_agent(u_id:str,name:str,email:str) -> dict:
    system_template = """YOU are strict scheduler. your only job is to scedule an interview by calling 
    CALENDER_TOOL(u_id,name,email) Exactly once.


    Rules:
    - if u_id, name, and email are present -> call CALENDER_TOOL(u_id,name,email)
    """

    system_prompt = SystemMessagePromptTemplate.from_template(system_template)

    human_template = "u_id={u_id}, name={name}, email={email}"
    human_prompt = HumanMessagePromptTemplate.from_template(human_template)

    chat_prompt = ChatPromptTemplate.from_messages([system_prompt,human_prompt])
    out = agent.invoke(chat_prompt.format_prompt(u_id=u_id,name=name,email=email))
    return "agent done"