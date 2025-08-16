import os # Lets you read environment variables (like API keys) and work with file paths.
from dotenv import load_dotenv # Gives you load_dotenv(), which reads your .env file and loads keys into environment variables.
from crewai import Agent, Task # CrewAI building blocks: Agent: an AI worker that can use tools. Task: what the agent should do. Crew: groups agents + tasks and runs them.
import litellm # A lightweight library for making API calls to language models like Gemini. LiteLLM is a model router CrewAI can use when you pass a model string like "gemini/gemini-1.5-flash".
from utils.u1_youtube_search_tool import youtube_search_tool # Import the YouTube search tool we defined earlier.

load_dotenv() # Reads the .env file and loads the variables into the environment. Loads keys from .env into os.environ.
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")  # your Gemini API key

# Early, clear errors if a key is missing, so you don’t get confusing failures later.
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env file")

# Agent
search_agent = Agent(
    role="YouTube Search Specialist",
    goal="Return the most viewed videos for the exact topic provided. Video language must be English.",
    backstory="You specialize in retrieving the top YouTube videos exactly as requested by the user.",
    tools=[youtube_search_tool],
    llm="gemini/gemini-1.5-flash", # The model to use for the agent. "gemini/gemini-1.5-flash" is a lightweight model from Google.
    verbose=True, # Set to True to see detailed logs of what the agent is doing
    input_schema={
        "query": "The exact topic to search for on YouTube",
        "max_results": "The maximum number of results to return"
    }
)

# Task
search_task = Task(
    agent=search_agent,
    description="Search YouTube for the topic: {query}. Do NOT change the topic. Always use exactly the query provided. Also only return {max_results} results.Video must be of English language. Title of video must be in English.",
    expected_output="A list of dictionaries containing all the details of the videos for the {query} topic. Video must be of English language. Title of video must be in English.",
    human_input=False,
)