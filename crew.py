# A simple script to test the crew
from agents.orchestration import youtube_analysis_crew

query = input("Enter the YouTube search query: ")
max_results = int(input("Enter the maximum number of results to return: "))
inputs = {"query": query, "max_results": max_results}


try:
    result = youtube_analysis_crew.kickoff(inputs=inputs)
    print("Final Result:", result)
except Exception as e:
    print(f"An error occurred during kickoff: {e}")