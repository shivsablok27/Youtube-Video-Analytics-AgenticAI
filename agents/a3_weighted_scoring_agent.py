import os
from dotenv import load_dotenv
from crewai import Agent, Task
from crewai.tools import tool
import litellm 
from utils.u3_weighted_scoring_tool import weighted_scoring_tool

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env file")


weighted_scoring_agent = Agent(
    role="YouTube Video Weighted Scoring Specialist",
    goal="Rank videos using a weighted scoring formula based on views, likes, subscribers, comments, and current position.",
    backstory="You specialize in applying scoring formulas to fairly rank YouTube videos for data analysis.",
    tools=[weighted_scoring_tool],
    llm="gemini/gemini-1.5-flash",
    verbose=True,
    input_schema={
        "videos": "List of video dictionaries with views, likes, subscribers, comments, and position."
    }
)

weighted_scoring_task = Task(
    agent=weighted_scoring_agent,
    description="Apply weighted scoring to the given videos and return them with a new 'final_score' field.",
    expected_output="List of video dictionaries with all details from previous agents and 'final_score' added as well as 'rank' based on the score, ordered by rank in increasing order. (no duplicates)",
    human_input=False
)