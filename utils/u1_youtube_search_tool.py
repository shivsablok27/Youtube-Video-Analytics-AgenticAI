import os # Lets you read environment variables (like API keys) and work with file paths.
from crewai.tools import tool # Decorator used to turn a normal Python function into a CrewAI tool (so agents can call it).
from googleapiclient.discovery import build # Lets you build a YouTube API client to make requests.
from dotenv import load_dotenv # Gives you load_dotenv(), which reads your .env file and loads keys into environment variables.

load_dotenv() # Reads the .env file and loads the variables into the environment. Loads keys from .env into os.environ.
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY") # your YouTube API key


# Tool: YouTube Search
@tool # This decorator turns the function into a CrewAI tool that agents can call.
def youtube_search_tool(query: str, max_results: int = 5):
    """Search YouTube videos sorted by view count, excluding Shorts and ensuring title contains query."""
    youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY) # Creates a YouTube API client using the API key.
    
    # Step 1: Search videos
    search_request = youtube.search().list(
        q=query, # The exact query provided by the user, e.g., "Machine Learning"
        part="snippet", # What parts of the video data to return. "snippet" includes title, description, etc.
        type="video", # Only search for videos (not channels or playlists)
        maxResults=50,  # Get more initially to allow filtering
        order="viewCount" # Sort by view count to get the most popular videos first
    )
    search_response = search_request.execute() # Actually calls the API and gets a JSON response.

    video_ids = [item["id"]["videoId"] for item in search_response.get("items", [])] # Pulls out just the video IDs from the search results (we need them to fetch duration, etc.).

    if not video_ids:
        return []

    # Step 2: Get video details to filter out Shorts
    details_request = youtube.videos().list(  # Now we need to get more details about each video, like duration.
        part="snippet,contentDetails", # "snippet" gives title, channel, etc. "contentDetails" gives duration.
        id=",".join(video_ids) # Joins the video IDs into a comma-separated string for the API request
    )
    details_response = details_request.execute() 

    from isodate import parse_duration # Imports a helper that converts ISO 8601 duration (e.g., PT59S) into seconds.

    results = []
    for item in details_response.get("items", []):
        title = item["snippet"]["title"] # The title of the video
        duration = parse_duration(item["contentDetails"]["duration"]).total_seconds()

        # Filter: Must contain query (case-insensitive) AND duration >= 60 seconds
        if query.lower() in title.lower() and duration >= 180: # Ensures the video is not a Short (which are usually under 60 seconds) and the title contains the exact query.
            results.append({
                "video_id": item["id"], # The unique ID for the video, used to construct the link
                "title": title, # The title of the video
                "channel": item["snippet"]["channelTitle"], # The name of the channel that uploaded the video
                "publish_time": item["snippet"]["publishedAt"], # When the video was published
                "duration (in minutes)": round(duration/60,2),  # Convert seconds to minutes  
                "link": f"https://www.youtube.com/watch?v={item['id']}"
            })

        if len(results) >= max_results: # Stop if we have enough results
            break

    return results