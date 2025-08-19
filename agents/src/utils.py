from langchain.agents import initialize_agent,AgentType


#Agent initialization
def create_agent(tools,llm,systemPrompt):
    agent = initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
        agent_kwargs={"system_message":systemPrompt}, 
        handle_parsing_errors=True,
        return_intermediate_steps=True
    )
    return agent