"""Configuration management for Instagram Bot V7 PRO"""
import os
from pathlib import Path
from dataclasses import dataclass, asdict
from datetime import timezone, timedelta
import json

CAT = timezone(timedelta(hours=2))

# ═══════════════════════════════════════════════════════════════════════
#  DATA DIRECTORIES
# ═══════════════════════════════════════════════════════════════════════

DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

# File paths
SESSION_FILE = DATA_DIR / "session.json"
FOLLOW_TRACKER = DATA_DIR / "follow_tracker.json"
DAILY_STATS_FILE = DATA_DIR / "daily_stats.json"
ACCOUNT_START = DATA_DIR / "account_start.json"
CONTENT_FOLDER = DATA_DIR / "downloaded_content"
COOLDOWN_FILE = DATA_DIR / "cooldown.json"
ENGAGEMENT_SCORES = DATA_DIR / "engagement_scores.json"
VIRAL_TRACKER = DATA_DIR / "viral_tracker.json"
NOTIFICATIONS = DATA_DIR / "notifications.json"
ADAPTIVE_CONFIG = DATA_DIR / "adaptive_config.json"
INFLUENCER_TARGETS = DATA_DIR / "influencer_targets.json"
FOLLOWER_PROFILE_FILE = DATA_DIR / "follower_profiles.json"
DASHBOARD_FILE = DATA_DIR / "growth_dashboard.html"
FOLLOWER_HIST = DATA_DIR / "follower_history.json"

# ═══════════════════════════════════════════════════════════════════════
#  CONSTANTS
# ═══════════════════════════════════════════════════════════════════════

SPORTS_HASHTAGS = [
    "sports", "football", "basketball", "soccer", "fitness",
    "athlete", "sportsmotivation", "nba", "nfl", "cricket",
    "tennis", "rugby", "training", "gym", "workout",
    "champion", "sportslife", "sportsphotography", "motivation",
    "winning", "teamwork", "athletic", "sportsworld", "baseball",
    "swimming", "boxing", "mma", "cycling", "sportsnews",
    "strengthtraining", "cardio", "crossfit", "yoga", "running",
]

COMPETITOR_ACCOUNTS = [
    "espn", "bleacherreport", "sportscenter", "goal", "nba", "nfl", "bbcsport",
]

ACTION_DELAYS = {
    "follow": (12, 45),
    "like": (2, 8),
    "comment": (8, 25),
    "post": (20, 60),
    "dm": (15, 45),
    "reply": (8, 25),
}

WARMUP_SCHEDULE = {
    1:  {"follows": 15, "unfollows": 0,  "likes": 15, "comments": 3,  "posts": 0, "stories": 1, "replies": 2},
    2:  {"follows": 15, "unfollows": 0,  "likes": 20, "comments": 4,  "posts": 1, "stories": 1, "replies": 3},
    3:  {"follows": 15, "unfollows": 2,  "likes": 25, "comments": 5,  "posts": 1, "stories": 2, "replies": 4},
    4:  {"follows": 15, "unfollows": 5,  "likes": 30, "comments": 6,  "posts": 1, "stories": 2, "replies": 5},
    5:  {"follows": 20, "unfollows": 8,  "likes": 35, "comments": 8,  "posts": 2, "stories": 2, "replies": 6},
    6:  {"follows": 20, "unfollows": 10, "likes": 40, "comments": 10, "posts": 2, "stories": 3, "replies": 8},
    7:  {"follows": 20, "unfollows": 12, "likes": 45, "comments": 12, "posts": 2, "stories": 3, "replies": 10},
    8:  {"follows": 20, "unfollows": 15, "likes": 50, "comments": 13, "posts": 3, "stories": 3, "replies": 12},
    9:  {"follows": 25, "unfollows": 18, "likes": 55, "comments": 15, "posts": 3, "stories": 4, "replies": 15},
    10: {"follows": 25, "unfollows": 20, "likes": 60, "comments": 15, "posts": 3, "stories": 4, "replies": 18},
    11: {"follows": 30, "unfollows": 25, "likes": 65, "comments": 18, "posts": 3, "stories": 5, "replies": 20},
    12: {"follows": 30, "unfollows": 28, "likes": 70, "comments": 20, "posts": 3, "stories": 5, "replies": 22},
    13: {"follows": 30, "unfollows": 30, "likes": 75, "comments": 22, "posts": 3, "stories": 5, "replies": 25},
    14: {"follows": 30, "unfollows": 30, "likes": 75, "comments": 22, "posts": 3, "stories": 5, "replies": 25},
}

# Adaptive mode thresholds
SUCCESS_STREAK_THRESHOLD = 20
ERROR_STREAK_THRESHOLD = 3
MAX_INTENSITY = 1.3
MIN_INTENSITY = 0.5
INTENSITY_STEP = 0.05
MAX_DELAY_OFFSET = 30

# Quality scoring weights
QUALITY_RATIO_WEIGHT = 0.4
QUALITY_ACTIVITY_WEIGHT = 0.35
QUALITY_BIO_WEIGHT = 0.25

# ═══════════════════════════════════════════════════════════════════════
#  CONFIGURATION CLASS
# ═══════════════════════════════════════════════════════════════════════

@dataclass
class BotConfig:
    """Bot configuration with validation."""
    username: str
    password: str
    poll_interval_minutes: int = 15
    unfollow_after_days: int = 3
    sample_size: int = 200
    micro_influencer_min: int = 1000
    micro_influencer_max: int = 50000
    safe_hour_start: int = 7
    safe_hour_end: int = 22
    
    @classmethod
    def from_env(cls) -> "BotConfig":
        """Load config from environment variables."""
        username = os.getenv("INSTA_USERNAME")
        password = os.getenv("INSTA_PASSWORD")
        
        if not username or not password:
            raise ValueError(
                "Missing credentials. Set INSTA_USERNAME and INSTA_PASSWORD environment variables."
            )
        
        return cls(
            username=username,
            password=password,
            poll_interval_minutes=int(os.getenv("POLL_INTERVAL_MINUTES", "15")),
            unfollow_after_days=int(os.getenv("UNFOLLOW_AFTER_DAYS", "3")),
        )
    
    @classmethod
    def from_json(cls, path: str) -> "BotConfig":
        """Load config from JSON file."""
        with open(path) as f:
            data = json.load(f)
        return cls(**data)
    
    def validate(self) -> bool:
        """Validate configuration."""
        if not self.username or not self.password:
            raise ValueError("Username and password are required")
        if self.poll_interval_minutes < 5:
            raise ValueError("Poll interval must be at least 5 minutes")
        if self.safe_hour_start >= self.safe_hour_end:
            raise ValueError("Safe hours start must be before end")
        return True


def load_config() -> BotConfig:
    """Load config with priority: env vars > config.json > defaults."""
    try:
        return BotConfig.from_env()
    except ValueError:
        try:
            if Path("config.json").exists():
                return BotConfig.from_json("config.json")
        except Exception:
            pass
        raise ValueError("Could not load configuration")
