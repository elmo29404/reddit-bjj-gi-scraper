import praw
import pandas as pd
import os
from dotenv import load_dotenv

# 🔐 Load credentials from .env file
load_dotenv()

reddit = praw.Reddit(
    client_id=os.getenv("CLIENT_ID"),
    client_secret=os.getenv("CLIENT_SECRET"),
    user_agent=os.getenv("USER_AGENT")
)

# ✅ Subreddits to scan
subreddits = ["bjj", "jiujitsu", "mma"]

# ✅ Keywords to match (can expand this list)
keywords = [
    "bjj gi", "gi brand", "recommend a gi", "best gi", "favorite gi",
    "gi review", "lightweight gi", "starter gi", "training gi", "shoyoroll",
    "tatami", "fuji", "hyperfly", "origin", "gold bjj", "kingz", "aesthetic gi"
]

# 📦 Store results
results = []

for sub in subreddits:
    subreddit = reddit.subreddit(sub)
    print(f"🔍 Searching r/{sub}...")

    for submission in subreddit.search(" OR ".join(keywords), limit=50, sort="new"):
        submission.comments.replace_more(limit=0)

        # Check if post title itself matches
        if any(kw in submission.title.lower() for kw in keywords):
            results.append({
                "subreddit": sub,
                "type": "post",
                "post_title": submission.title,
                "comment": "",
                "score": submission.score,
                "url": submission.url
            })

        # Check each comment
        for comment in submission.comments.list():
            body = comment.body.lower()
            if any(kw in body for kw in keywords):
                results.append({
                    "subreddit": sub,
                    "type": "comment",
                    "post_title": submission.title,
                    "comment": comment.body,
                    "score": comment.score,
                    "url": submission.url
                })

# 📄 Save to CSV
df = pd.DataFrame(results)
df = df.sort_values(by="score", ascending=False)
df.to_csv("bjj_gi_recommendations_all_subreddits.csv", index=False)

print(f"\n✅ Done! Saved {len(df)} results to bjj_gi_recommendations_all_subreddits.csv")
