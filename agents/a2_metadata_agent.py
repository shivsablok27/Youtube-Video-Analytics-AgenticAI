import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew
from crewai.tools import tool
from googleapiclient.discovery import build
import litellm  
from utils.u2_fetch_video_metadata_tool import fetch_video_metadata_tool

# Load environment variables
load_dotenv() # Reads the .env file and loads the variables into the environment. Loads keys from .env into os.environ.
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")  # your Gemini API key


if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env file")


metadata_agent = Agent(
    role="YouTube Metadata Enrichment Specialist",
    goal="Fetch detailed statistics and thumbnails for given YouTube videos.",
    backstory="You specialize in enriching video data with detailed statistics for analysis.",
    tools=[fetch_video_metadata_tool],
    llm="gemini/gemini-1.5-flash",
    verbose=True,
    input_schema={
        "videos": "List of video dictionaries from Search Agent output."
    }
)

metadata_task = Task(
    agent=metadata_agent,
    description="Take the output of search_task as 'videos' input. Fetch detailed metadata for the given list of videos. Append the metadata to each video dictionary.",
    expected_output="A list of enriched video dictionaries with stats, subscribers and the previous details from the Search Agent. (not duplicated)",
    human_input=False
)

