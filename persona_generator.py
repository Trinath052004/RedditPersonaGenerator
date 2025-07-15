
"""
Reddit User Persona Generator (PEP-8 Compliant)

Scrapes Reddit user data, analyzes patterns, and saves a text persona.

Requirements:
- praw
- python-dotenv
- requests
- beautifulsoup4
- textblob

Usage:
    python reddit_persona_generator.py
"""

# Standard Library Imports
import os
import re
import sys
from datetime import datetime, timedelta
from collections import Counter
from urllib.parse import urlparse

# Third-party Imports
import praw
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class RedditPersonaGenerator:
    def __init__(self):
        """Initialize the Reddit API client and data containers."""
        self.reddit = praw.Reddit(
            client_id=os.getenv("REDDIT_CLIENT_ID", "your_client_id"),
            client_secret=os.getenv("REDDIT_CLIENT_SECRET", "your_client_secret"),
            user_agent=os.getenv("REDDIT_USER_AGENT", "PersonaGenerator/1.0")
        )

        self.user_data = {
            "username": "",
            "posts": [],
            "comments": [],
            "subreddits": Counter(),
            "timestamps": [],
            "karma": {"post": 0, "comment": 0},
            "account_age": 0
        }

    def extract_username_from_url(self, url):
        """Extract username from Reddit profile URL."""
        patterns = [
            r"reddit\.com/user/([^/]+)",
            r"reddit\.com/u/([^/]+)"
        ]
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        raise ValueError("Invalid Reddit profile URL format")

    def scrape_user_data(self, username, limit=100):
        """Scrape user's posts and comments."""
        print(f"Scraping data for user: {username}")
        try:
            user = self.reddit.redditor(username)
            created = datetime.fromtimestamp(user.created_utc)
            self.user_data.update({
                "username": username,
                "account_age": (datetime.now() - created).days,
                "karma": {
                    "post": user.link_karma,
                    "comment": user.comment_karma
                }
            })

            for post in user.submissions.new(limit=limit):
                self.user_data["posts"].append({
                    "id": post.id,
                    "title": post.title,
                    "text": post.selftext,
                    "subreddit": post.subreddit.display_name,
                    "score": post.score,
                    "created_utc": post.created_utc,
                    "url": f"https://reddit.com{post.permalink}",
                    "type": "post"
                })
                self.user_data["subreddits"][post.subreddit.display_name] += 1
                self.user_data["timestamps"].append(post.created_utc)

            for comment in user.comments.new(limit=limit):
                self.user_data["comments"].append({
                    "id": comment.id,
                    "text": comment.body,
                    "subreddit": comment.subreddit.display_name,
                    "score": comment.score,
                    "created_utc": comment.created_utc,
                    "url": f"https://reddit.com{comment.permalink}",
                    "type": "comment"
                })
                self.user_data["subreddits"][comment.subreddit.display_name] += 1
                self.user_data["timestamps"].append(comment.created_utc)

            print(f"Scraped {len(self.user_data['posts'])} posts and "
                  f"{len(self.user_data['comments'])} comments")
            return True

        except Exception as e:
            print(f"Error scraping user data: {e}")
            return False

    def save_persona_to_txt(self, filename="persona.txt"):
        """Save full persona text like reference format."""
        data = self.user_data
        top_subreddits = data["subreddits"].most_common(5)
        weekday_map = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        times = [datetime.fromtimestamp(ts) for ts in data["timestamps"]]
        hour_count = Counter([dt.hour for dt in times])
        day_count = Counter([dt.weekday() for dt in times])
        peak_hour = max(hour_count.items(), key=lambda x: x[1])[0] if hour_count else 0
        peak_day = weekday_map[max(day_count.items(), key=lambda x: x[1])[0]] if day_count else "Unknown"
        recent_count = sum(1 for dt in times if dt > datetime.now() - timedelta(days=30))

        with open(filename, "w", encoding="utf-8") as f:
            f.write("=" * 60 + "\n")
            f.write(f"USER PERSONA: u/{data['username']}\n")
            f.write("=" * 60 + "\n\n")
            f.write("BASIC INFORMATION:\n")
            f.write(f"Account Age: {data['account_age']} days\n")
            f.write(f"Post Karma: {data['karma']['post']}\n")
            f.write(f"Comment Karma: {data['karma']['comment']}\n")
            f.write(f"Total Posts: {len(data['posts'])}\n")
            f.write(f"Total Comments: {len(data['comments'])}\n")
            f.write(f"Active Subreddits: {len(data['subreddits'])}\n\n")

            f.write("INTERESTS:\n")
            for sr, _ in top_subreddits:
                f.write(f"\u2022 Active in r/{sr}\n")
            f.write("\n")

            f.write("PERSONALITY TRAITS:\n")
            f.write("\u2022 Balanced emotional expression\n\n")

            f.write("ACTIVITY PATTERNS:\n")
            f.write(f"\u2022 Most active around {peak_hour}:00\n")
            f.write(f"\u2022 Most active on {peak_day}s\n")
            f.write(f"\u2022 Posted {recent_count} times in the last 30 days\n\n")

            f.write("EXPERTISE AREAS:\n\n")

            f.write("TOP SUBREDDITS:\n")
            for sr, count in top_subreddits:
                f.write(f"\u2022 r/{sr}: {count} posts/comments\n")
            f.write("\n")

            f.write("=" * 60 + "\n")
            f.write("CITATIONS AND EVIDENCE\n")
            f.write("=" * 60 + "\n\n")

            f.write("INTERESTS:\n")
            f.write("-" * 40 + "\n")
            for sr, _ in top_subreddits:
                f.write(f"Characteristic: Active in r/{sr}\n")
                f.write("Evidence:\n")
                found = 0
                for item in data['posts'] + data['comments']:
                    if item['subreddit'] == sr and found < 3:
                        prefix = "Post" if item['type'] == "post" else "Comment"
                        text = item.get("title") or item.get("text")
                        url = item["url"]
                        f.write(f"  \u2022 {prefix}: '{text[:50]}' ({url})\n")
                        found += 1
                f.write("\n")

            f.write("PERSONALITY TRAITS:\n")
            f.write("-" * 40 + "\n")
            f.write("Characteristic: Balanced emotional expression\n")
            f.write("Evidence:\n\n")

            f.write("ACTIVITY PATTERNS:\n")
            f.write("-" * 40 + "\n")
            f.write(f"Characteristic: Most active around {peak_hour}:00\n")
            f.write(f"Evidence:\n  \u2022 Based on analysis of {len(times)} posts and comments\n\n")
            f.write(f"Characteristic: Most active on {peak_day}s\n")
            f.write(f"Evidence:\n  \u2022 Based on analysis of {len(times)} posts and comments\n\n")
            f.write(f"Characteristic: Posted {recent_count} times in the last 30 days\n")
            f.write(f"Evidence:\n  \u2022 Based on analysis of {len(times)} posts and comments\n\n")

            f.write("EXPERTISE AREAS:\n")
            f.write("-" * 40 + "\n\n")

        print(f"Saved full persona to {filename}")


def main():
    print("Reddit User Persona Generator")
    print("=" * 40)
    profile_url = input("Enter Reddit profile URL: ").strip()

    generator = RedditPersonaGenerator()
    try:
        username = generator.extract_username_from_url(profile_url)
        if generator.scrape_user_data(username):
            generator.save_persona_to_txt(f"{username}_persona.txt")
    except Exception as err:
        print(f"Error: {err}")


if __name__ == "__main__":
    main()



