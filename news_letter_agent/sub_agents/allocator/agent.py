from google.adk.agents import Agent
from news_letter_agent.sub_agents.research.agent import research_coordinator
from news_letter_agent.sub_agents.content.agent import content_agent
from google.adk.tools.agent_tool import AgentTool

allocator_agent=Agent(
    
    name="allocator_agent",
    model="gemini-2.0-flash",
    description="This agent allocates works to all other sub agents to create a good newsletter",
    instruction="""
    You are a coordinator agent responsible for creating a high-quality newsletter by assigning tasks to sub-agents.

    Your role is to call the research_coordinator tool to gather all necessary information about industry news and what the audience cares about.

    Then, call the content_agent to write the newsletter content based on that information.

    It is critical that you first gather the research and then write the content. After receiving the newsletter content from the content_agent, consolidate it and return only the final newsletter content.

    **Do NOT output any intermediate or status messages such as 'Now that I have...', 'Here's the complete newsletter content:', or any other commentary.**

    Return only the final consolidated newsletter content without any extra text.
    """,
    tools=[AgentTool(agent=research_coordinator),AgentTool(agent=content_agent)]
)