from dotenv import load_dotenv
from crewai import Crew
from agents.a1_search_agent import search_agent, search_task
from agents.a2_metadata_agent import metadata_agent, metadata_task
from agents.a3_weighted_scoring_agent import weighted_scoring_agent, weighted_scoring_task

# Load environment variables
load_dotenv()

# Create the Crew
youtube_analysis_crew = Crew(
    agents=[
        search_agent,
        metadata_agent,
        weighted_scoring_agent
    ],
    tasks=[
        search_task,
        metadata_task,
        weighted_scoring_task
    ],
    verbose=True
)
