import os
from dotenv import load_dotenv
from crewai.tools import tool
from googleapiclient.discovery import build
from isodate import parse_duration  # import once at top

load_dotenv()
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

@tool
def fetch_video_metadata_tool(videos: list):
    """
    Takes a list of video dictionaries from the Search Agent and fetches:
    - View count
    - Like count
    - Comment count
    - Channel subscriber count
    - Duration (minutes)
    """
    youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)

    # Extract all video IDs from search agent's output
    video_ids = [video["video_id"] for video in videos]

    # Step 1: Get video statistics + snippet + contentDetails
    video_request = youtube.videos().list(
        part="snippet,statistics,contentDetails",
        id=",".join(video_ids)
    )
    video_response = video_request.execute()

    enriched_videos = []

    for item in video_response.get("items", []):
        video_id = item["id"]
        snippet = item["snippet"]
        stats = item["statistics"]
        content = item["contentDetails"]

        # Step 2: Get channel subscriber count
        channel_id = snippet["channelId"]
        channel_request = youtube.channels().list(
            part="statistics",
            id=channel_id
        )
        channel_response = channel_request.execute()
        channel_stats = channel_response["items"][0]["statistics"]
        subs = int(channel_stats.get("subscriberCount", 0))

        # Parse duration safely
        duration = parse_duration(content["duration"]).total_seconds()

        enriched_videos.append({
            "video_id": video_id,
            "title": snippet["title"],
            "channel": snippet["channelTitle"],
            "publish_time": snippet["publishedAt"],
            "duration (in minutes)": round(duration / 60, 2),
            "views": int(stats.get("viewCount", 0)),
            "likes": int(stats.get("likeCount", 0)),
            "comments": int(stats.get("commentCount", 0)),
            "subscribers": subs,
            "link": f"https://www.youtube.com/watch?v={video_id}"
        })

    return enriched_videos
