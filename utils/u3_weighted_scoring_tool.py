import os
from dotenv import load_dotenv
from crewai.tools import tool
from googleapiclient.discovery import build

load_dotenv() # Reads the .env file and loads the variables into the environment. Loads keys from .env into os.environ.
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY") # your YouTube API key


@tool
def weighted_scoring_tool(videos: list):
    """
    Takes enriched videos and computes a weighted score.
    Formula can be tuned by adjusting the weights below.
    """
    # Adjustable weights
    weights = {
        "views": 0.3,
        "likes": 0.2,
        "subscribers": 0.2,
        "comments": 0.2,
        "position": 0.1  # lower position (earlier) is better, so invert later
    }

    # Step 1: Add current position to each video (if not already present)
    for idx, v in enumerate(videos, start=1):
        v["position"] = idx

    # Step 2: Find max values for normalization (avoid division by zero)
    max_views = max(v["views"] for v in videos) or 1
    max_likes = max(v["likes"] for v in videos) or 1
    max_subs = max(v["subscribers"] for v in videos) or 1
    max_comments = max(v.get("comments", 0) for v in videos) or 1
    max_position = max(v["position"] for v in videos) or 1

    scored_videos = []

    # Step 3: Calculate normalized score & weighted sum
    for v in videos:
        normalized_views = v["views"] / max_views
        normalized_likes = v["likes"] / max_likes
        normalized_subs = v["subscribers"] / max_subs
        normalized_comments = v.get("comments", 0) / max_comments
        # For position, earlier videos should get higher score -> invert
        normalized_position = 1 - ((v["position"] - 1) / (max_position - 1)) if max_position > 1 else 1

        final_score = (
            weights["views"] * normalized_views +
            weights["likes"] * normalized_likes +
            weights["subscribers"] * normalized_subs +
            weights["comments"] * normalized_comments +
            weights["position"] * normalized_position
        )

        scored_videos.append({
            **v,  # keep all original fields
            "final_score": round(final_score, 4)
        })

    # Step 4: Sort videos by final score (descending)
    scored_videos = sorted(scored_videos, key=lambda x: x["final_score"], reverse=True)
    for i, v in enumerate(scored_videos, start=1):
        v["rank"] = i
    return scored_videos



