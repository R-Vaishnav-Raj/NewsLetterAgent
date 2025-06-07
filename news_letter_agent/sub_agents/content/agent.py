from google.adk.agents import Agent,LoopAgent,SequentialAgent
from news_letter_agent.shared_libraries import types

intro_agent=Agent(
    name="intro_agent",
    model="gemini-2.0-flash",
    description="Writes intro for the newsletter",
    instruction="""
    You are responsible for writing the introduction of the newsletter.
    Use {{body}} as context to create the intro.
    Your goal is to hook the reader, set the tone, and briefly highlight what this edition covers. 
    Make it friendly, engaging, and give readers a reason to continue reading.

    Keep it concise, relevant to the audience, and aligned with the overall theme of the newsletter.
    """,
    output_schema=types.Intro,
    output_key="intro",
)

body_agent=Agent(
    name="body_agent",
    model="gemini-2.0-flash",
    description="Writes body for the newsletter",
    instruction = """
    You are responsible for writing the main body of the newsletter.
    Use the {{review}} as context to create the body.
    Use the provided topics or content sections to create informative, well-structured, and engaging paragraphs. 
    Maintain a consistent voice and ensure each section flows logically into the next.

    Ensure accuracy, clarity, and reader-friendliness. Include relevant facts, context, or examples when needed.
    """,
    output_schema=types.Body,
    output_key="body",
)

review_agent=Agent(
    name="review_agent",
    model="gemini-2.0-flash",
    description="Writes review for the newsletter",
    instruction ="""
    You are responsible for crafting a deep review for a given piece of news. Use the {{research_coordinator_output}} as context to create a deep review.

    #Instructions
    - The review should be a deep review of the given piece of news.
    - The review should be 1-2 sentences.

    #Sub-instructions
    - Introduce the news and mention why it matters
    - Tie back to Profile info

    #Example
    Market chaos is nothing new—it's our baseline. But today's volatility is driven by forces we haven't historically faced together. The U.S. trade-weighted tariff rate has ballooned from a steady 2.5% to a staggering 27% in mere months. This dramatic leap parallels economic uncertainty levels not seen since the 2008 crisis or the early COVID-19 days.

    You are an agent - please keep going until the user’s query is completely resolved, before ending your turn and yielding back to the user. Only terminate your turn when you are sure that the problem is solved.

    """,
    output_schema=types.Review,
    output_key="review",
)

conclusion_agent =Agent(
    name="conclusion_agent",
    model="gemini-2.0-flash",
    description="Writes conclusion for the newsletter",
    instruction = """
    You are responsible for writing the conclusion of the newsletter. 
    Use {{body}} as context to create the conclusion.
    Wrap up the content with a positive note, reflection, or call to action if relevant (e.g., upcoming events, contact info, next issue teaser).

    Keep it concise, warm, and aligned with the overall tone of the newsletter.
    Leave the reader with a sense of closure and anticipation.
    """,
    output_schema=types.Conclusion,
    output_key="conclusion",
)

writer_agent=Agent(
    name="writer_agent",
    model="gemini-2.0-flash",
    description="Combines the intro, body and conclusion to give the newspaper",
    instruction = """
    You are responsible for writing the final version of a newsletter that is ready to be published.

    You will receive three parts:
    - The introduction in {{intro}}
    - The body in {{body}}
    - The conclusion in {{conclusion}}

    Your job is to **combine** these into a polished, well-structured newsletter without adding any extra commentary or placeholder text.

    **Requirements**:
    - Do not mention "draft", "based on the research", or similar phrases.
    - Do not include any headings like "Newsletter:", "Here's a draft", etc.
    - Each section should be a clean paragraph — no labels like "Introduction:", "Conclusion:", etc.
    - The final output should be ready for direct publication.

    Return the final newsletter as plain text with well-formed transitions.
    """,
    output_schema=types.NewsLetter,
    output_key="combined_newsletter",
)

content_agent=SequentialAgent(
    name="content_agent",
    sub_agents=[review_agent,body_agent,intro_agent,conclusion_agent,writer_agent],
)


# content_agent=Agent(
#     model="gemini-2.0-flash",
#     name="content_agent",
#     sub_agents=[writer_agent],
    
#     description="This agent crafts the newsletter based on the info provided by the subagents.",
#     instruction="""
#     You are the final agent responsible for presenting the complete newsletter.

#     You will receive a fully composed newsletter object from the previous agents. This newsletter contains three main parts:

#     1. **Intro** - A friendly and engaging opening that sets the tone and highlights what's in this edition. (`{{combined_newsletter.intro}}`)
#     2. **Body** - The main content, well-structured and informative. (`{{combined_newsletter.body}}`)
#     3. **Conclusion** - A warm and thoughtful closing note that wraps everything up. (`{{combined_newsletter.conclusion}}`)

#     Your task:
#     - Present the newsletter in a clean, reader-friendly format.
#     - Ensure proper flow between the sections.
#     - Don't modify the content; just structure and finalize the delivery.

#     Make sure all three parts are clearly distinguishable as separate paragraphs.
#     """,
# )