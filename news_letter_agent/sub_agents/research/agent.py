from google.adk.agents import Agent,LoopAgent,SequentialAgent
from google.adk.tools.agent_tool import AgentTool
from google.adk.tools.google_search_tool import google_search
from news_letter_agent.shared_libraries import types

user_research_agent=Agent(
    name="user_research_agent",
    model="gemini-1.5-flash",
    description="Deeply analysis and understands the user and their interest. You populate the Profile object with the user's profile.",
    instruction="""
    You are responsible for building up a profile of the audience based on the info provided. This means you need to figure out the: motivations, desires, challenges, for a given role. You need to figure out the user's profile and populate the Profile object.
    """,
    output_schema=types.Profile,
    output_key="profile",
)

research_topic=Agent(
    name="research_topic",
    model="gemini-1.5-flash",
    description="Creates a topic for the news letter based on user input",
    instruction = """
    You are an idea generation agent. Your task is to analyze the user's input — which may include interests, events, goals, or themes — and generate exactly three distinct, engaging, and relevant topics for a newsletter.

    topic should:
    1. Be concise yet descriptive.
    2. Be suitable for a newsletter audience.
    3. Reflect the user's intent or interest.
    Avoid generic topics. Focus on creativity, relevance, and variety.
    """,
    tools=[google_search],
    output_key="research_topic",
)

initial_research_agent= Agent(
    name="initial_research_agent",
    model="gemini-1.5-flash",
    description="An Intelligent researcher that does an initial research on topics.",
    instruction = """
    Based on the topic, do an intial broad reserch on each topic and understand the keys events 
    and things happening around that topic
    You always try to understand why something matters to the user. 
    Figure out the historical context of the news and tie it back to the user's query.
    """,
    tools=[google_search]
)

refine_research_agent= Agent(
    name="refine_research_agent",
    model="gemini-1.5-flash",
    description = "An intelligent researcher that performs deep, refined analysis on specific industry news and key events.",
    instruction = """
    Based on the initial input, conduct a deep and refined investigation into each topic. 
    Your goal is to uncover key events, trends, and insights related to the topic, with a strong focus on context and relevance.

    Always aim to understand *why* something matters to the user. 
    Explore the historical background of the topic and connect it to current events and the user's query.
    Focus on clarity, depth, and actionable understanding.
    """,
    tools=[google_search]
)

loop_research_agent= LoopAgent(
    name="loop_research_agent",
    max_iterations=3,
    sub_agents=[initial_research_agent,refine_research_agent],
    description="This agent loops the research about specific industry news and key events. Perform deep dive into the research about specific industry news and key events. "
)

root_research_agent=SequentialAgent(
    name="root_research_agent",
    description="Performs Deep Research about 3 topics relevant to the user input",
    #sub_agents=[AgentTool(agent=topic_agent),AgentTool(agent=loop_research_agent)],
    sub_agents=[research_topic,loop_research_agent],
)

research_coordinator=Agent(
    name="research_coordinator",
    model="gemini-2.0-flash",
    description="A research coordinator that understand the needs of the user and performs a deep and refined research on the user topics",
    instruction="""
    You are a research coordinator agent responsible for producing high-quality, user-relevant insights.
    Your point is to tie back the news and events to the user profile and understand why it matters to the audience specifically today.
    You use the user_research_agent and root_research_agent tool to do the research
    Use user_research_agent to understand the user and generate 3 distinct interested topics
    User root_research_agent to perform a deep and refined research on those 3 generated topics
    The topics should be matching the user profile and input
    """,
    tools=[AgentTool(agent=user_research_agent),AgentTool(agent=root_research_agent)],
    output_key="research_coordinator_output",

) 