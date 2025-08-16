# streamlit
import streamlit as st
# local
from agents.orchestration import youtube_analysis_crew
# A simple Streamlit app to test the crew
st.title("▶️ YouTube Insight Agent")
st.write("This app uses the YouTube Insight Agent to analyze YouTube videos.")

# Taking user input
query = st.text_input("Enter your search query:", "Python programming")
max_results = st.number_input("Max results to fetch:", min_value=1, max_value=5, value=2)
inputs = {"query": query, "max_results": max_results}

# Run the crew with the provided input
import ast
import pandas as pd

if st.button("Analyze"):
    with st.spinner("Analyzing..."):
        try:
            # Kickoff the YouTube analysis crew
            result = youtube_analysis_crew.kickoff(inputs=inputs)
            st.success("Analysis complete!")

            final_raw = result.tasks_output[2].raw  
            videos_list = ast.literal_eval(final_raw)
            df = pd.DataFrame(videos_list)

            # Loop through each video and create a card
            for _, row in df.iterrows():
                st.markdown(
                    f"""
                    <div style="
                        background-color:#1E1E1E;
                        padding:20px;
                        border-radius:15px;
                        margin-bottom:20px;
                        box-shadow: 0px 4px 10px rgba(0,0,0,0.3);
                    ">
                        <h3 style="color:#00C6FF; margin-bottom:10px;">{row['title']}</h3>
                        <p><b>📺 Channel:</b> {row['channel']}</p>
                        <p><b>🗓 Published:</b> {row['publish_time']}</p>
                        <p><b>⏱ Duration:</b> {row['duration (in minutes)']} mins</p>
                        <p><b>👀 Views:</b> {row['views']:,} | <b>👍 Likes:</b> {row['likes']:,} | <b>💬 Comments:</b> {row['comments']:,}</p>
                        <p><b>👤 Subscribers:</b> {row['subscribers']:,}</p>
                        <p><b>🏆 Rank:</b> {row['rank']} | <b>⚖️ Final Score:</b> {row['final_score']}</p>
                        <a href="{row['link']}" target="_blank" style="
                            display:inline-block;
                            margin-top:10px;
                            padding:10px 20px;
                            background-color:#00C6FF;
                            color:white;
                            border-radius:8px;
                            text-decoration:none;
                            font-weight:bold;
                        ">▶️ Watch Video</a>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
        except Exception as e:
            st.error(f"An error occurred, Most Probably the API hit the limit. Please try again after 24 hours.")
