import praw
import os
import json
from dotenv import load_dotenv

load_dotenv()

def get_reddit_instance():
    return praw.Reddit(
        client_id=os.getenv("REDDIT_CLIENT_ID"),
        client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
        user_agent=os.getenv("REDDIT_USER_AGENT")
    )

def fetch_user_data(username="demo_user", limit=50):
    # 1. Check if API keys exist
    cid = os.getenv("REDDIT_CLIENT_ID")
    csec = os.getenv("REDDIT_CLIENT_SECRET")
    
    # 2. If keys are missing or empty, use Sample Data
    if not cid or not csec or cid == "paste_your_client_id_here":
        print("No API keys found. Loading sample_data.json instead...")
        return load_sample_data()

    # 3. Try using the real API
    try:
        reddit = get_reddit_instance()
        user = reddit.redditor(username)
        comments_data = []
        
        print(f"Fetching live comments for {username}...")
        for comment in user.comments.new(limit=limit):
            comments_data.append({
                "text": comment.body,
                "subreddit": comment.subreddit.display_name,
                "created_utc": comment.created_utc
            })
        return comments_data
    except Exception as e:
        print(f"API Error: {e}. Falling back to sample_data.json...")
        return load_sample_data()

def load_sample_data():
    # Helper to load the JSON file
    try:
        # This handles the path correctly whether you are in the root folder or src folder
        current_dir = os.path.dirname(__file__)
        file_path = os.path.join(current_dir, '..', 'sample_data.json')
        
        with open(file_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print("ERROR: Could not find sample_data.json. Make sure it is in your main project folder.")
        return []