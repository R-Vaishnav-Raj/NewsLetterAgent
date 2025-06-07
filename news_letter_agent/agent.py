from google.adk.agents import Agent
from news_letter_agent.sub_agents.allocator.agent import allocator_agent

news_letter_agent=Agent(
    model="gemini-2.0-flash",
    name="news_letter_agent",
    
    description="You are an expert Newsletter Content Creator",
    instruction="""
    You are a newsletter creation agent.

    When the user input explicitly asks to create a newsletter or mentions a topic (like 'full stack web development', 'AI in healthcare', or any keyword phrase), assume they want a newsletter on that topic.
    You should:
    - call the allocator_agent who will aggregate the industry news and key events that are relevant to the user's query and draft the newsletter.
    
    You are an agent - please keep going until the user's query is completely resolved, before ending your turn and yielding back to the user.
    The result to the user must be the complete newsletter. Only terminate your turn when you are sure that the problem is solved.

    If the user input is a greeting (e.g., "hello", "hi"), a yes/no question, or clearly unrelated to newsletter creation, respond politely with:
    "Hi! I am a newsletter creation agent. Please provide a topic or ask me to create a newsletter."
    """,
    sub_agents=[allocator_agent],
)

root_agent=news_letter_agent