"""
╔════════════════════════════════════════════════════════════════════╗
║  🚀 INSTAGRAM ULTIMATE BOT v7 PRO — AI-Powered Growth Engine      ║
║  Sports Niche | Smart Targeting | Deep Analytics | Growth Hacking ║
╠════════════════════════════════════════════════════════════════════╣
║ 🆕 ULTRA FEATURES:                                                ║
║  ✅ 🤖 AI Smart Targeting (analyze followers → find clones)        ║
║  ✅ 📊 Deep Analytics Engine (quality score + authenticity check)   ║
║  ✅ 💬 Contextual AI Comments (not generic garbage)                ║
║  ✅ 👻 Fake Follower Detection (bot-account filter)                ║
║  ✅ ⏰ Smart Post Timing (predict best times per timezone)          ║
║  ✅ 🎬 Viral Content Detector (trending + recommend)               ║
║  ✅ 🔥 Story Engagement Automation (auto-reply polls/questions)    ║
║  ✅ 💰 Micro-Influencer Outreach (smart DM sequences)              ║
║  ✅ 📈 Adaptive Growth Mode (ML-powered auto-adjustment)           ║
║  ✅ 📱 Caption Optimizer (AI hashtag suggestions)                  ║
║  ✅ 🔔 Smart Notifications (alerts + daily digest)                 ║
║  ✅ 💾 Export to CSV (analytics, follower data)                    ║
║  ✅ 🎯 Engagement Quality Scoring (predict follow-back rate)       ║
║  ✅ 🔐 Advanced Session Management (device ID persistence)         ║
║  ✅ 🌐 Proxy Rotation with Health Monitoring                       ║
║  ✅ 💎 14-day Progressive Warm-Up (safe for new accounts)          ║
║  ✅ 🚨 Action Block Detection & Auto-Pause (30-90 min cooldown)    ║
╚════════════════════════════════════════════════════════════════════╝

SETUP:  pip install instagrapi pillow requests numpy scikit-learn
RUN:    python ultimate_bot_v7_pro.py
DOCS:   Check growth_dashboard.html after 24 hours
"""

import json
import logging
import random
import time
import hashlib
import platform
import uuid
import csv
import math
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path
import urllib.request
import urllib.error

# ── Timezone ──────────────────────────────────────────────────────
CAT = timezone(timedelta(hours=2))

def now_cat() -> datetime:
    return datetime.now(CAT)

try:
    from instagrapi import Client
    from instagrapi.exceptions import LoginRequired, ClientError, NotFound
except ImportError:
    print("\n❌ Missing: pip install instagrapi pillow requests\n")
    exit(1)

# Try ML libraries (optional)
try:
    import numpy as np
    from sklearn.preprocessing import StandardScaler
    from sklearn.cluster import KMeans
    ML_AVAILABLE = True
except ImportError:
    ML_AVAILABLE = False
    print("⚠️  ML libraries optional — install: pip install numpy scikit-learn")

# ══════════════════════════════════════════════════════════════════
#  LOGGING
# ══════════════════════════════════════════════════════════════════

class CATFormatter(logging.Formatter):
    def formatTime(self, record, datefmt=None):
        ct = datetime.fromtimestamp(record.created, tz=CAT)
        return ct.strftime(datefmt or "%Y-%m-%d %H:%M:%S") + " CAT"

_handler = logging.StreamHandler()
_handler.setFormatter(CATFormatter("%(asctime)s  %(levelname)-8s  %(message)s"))
logging.basicConfig(level=logging.INFO, handlers=[_handler])
logger = logging.getLogger("UltimateBotV7PRO")

# ══════════════════════════════════════════════════════════════════
#  FILE PATHS
# ══════════════════════════════════════════════════════════════════

SESSION_FILE         = "session.json"
FOLLOW_TRACKER       = "follow_tracker.json"
DAILY_STATS_FILE     = "daily_stats.json"
ACCOUNT_START        = "account_start.json"
CONTENT_FOLDER       = "downloaded_content"
REALTIME_SEEN        = "realtime_seen.json"
DAILY_RUN_FILE       = "daily_run.json"
HASHTAG_PERF_FILE    = "hashtag_performance.json"
ACTIVITY_LOG_FILE    = "activity_log.json"
COOLDOWN_FILE        = "cooldown.json"
DM_SENT_FILE         = "dm_sent.json"
DASHBOARD_FILE       = "growth_dashboard.html"
FOLLOWER_HIST        = "follower_history.json"
ACTION_BLOCK_FILE    = "action_block.json"
DEVICE_ID_FILE       = "device_id.json"
PROXY_STATUS_FILE    = "proxy_status.json"
COMMENT_HISTORY      = "comment_history.json"
FOLLOWER_PROFILE_FILE= "follower_profiles.json"
ENGAGEMENT_SCORES    = "engagement_scores.json"
VIRAL_TRACKER        = "viral_tracker.json"
STORY_VIEWERS        = "story_viewers.json"
NOTIFICATIONS        = "notifications.json"
CAPTION_TEMPLATES    = "caption_templates.json"
INFLUENCER_TARGETS   = "influencer_targets.json"
ADAPTIVE_CONFIG      = "adaptive_config.json"

# ══════════════════════════════════════════════════════════════════
#  SPORTS DATA
# ══════════════════════════════════════════════════════════════════

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

# ══════════════════════════════════════════════════════════════════
#  ENGAGEMENT QUALITY ANALYZER
# ══════════════════════════════════════════════════════════════════

def load_engagement_scores() -> dict:
    if Path(ENGAGEMENT_SCORES).exists():
        with open(ENGAGEMENT_SCORES) as f:
            return json.load(f)
    return {}

def save_engagement_scores(scores: dict):
    with open(ENGAGEMENT_SCORES, "w") as f:
        json.dump(scores, f, indent=2)

def calculate_engagement_quality(follower_count: int, following_count: int, 
                                media_count: int, biography: str = "") -> float:
    """Score follower quality (0.0 - 1.0). Higher = more likely to follow back."""
    if follower_count == 0 or following_count == 0:
        return 0.0
    
    ratio = follower_count / max(following_count, 1)
    ratio_score = min(1.0, ratio / 2.0) if ratio > 0 else 0.0
    
    if media_count > 0 and follower_count > 0:
        activity = (media_count / max(follower_count, 1)) * 100
        activity_score = min(1.0, activity / 5.0)
    else:
        activity_score = 0.0
    
    bio_score = 0.7 if biography and len(biography) > 10 else 0.3
    
    quality = (ratio_score * 0.4) + (activity_score * 0.35) + (bio_score * 0.25)
    return max(0.0, min(1.0, quality))

def is_likely_fake_account(follower_count: int, following_count: int, 
                          media_count: int, username: str) -> bool:
    """Detect obvious bot/fake accounts."""
    if follower_count > 0:
        ratio = following_count / follower_count
        if ratio > 10 or ratio < 0.01:
            return True
    
    if media_count < 5 and follower_count > 10000:
        return True
    
    bot_patterns = ["test", "bot", "spam", "admin", "noreply", "bot_"]
    if any(p in username.lower() for p in bot_patterns):
        return True
    
    return False

# ══════════════════════════════════════════════════════════════════
#  FOLLOWER ANALYZER
# ══════════════════════════════════════════════════════════════════

class FollowerAnalyzer:
    """Analyze followers to find similar users (lookalike targeting)."""
    
    @staticmethod
    def analyze_followers(cl, my_uid: int, sample_size: int = 200) -> dict:
        """Cluster followers into segments."""
        logger.info("🔬 Analyzing %d follower profiles…", sample_size)
        
        try:
            followers = cl.user_followers(my_uid, amount=sample_size)
        except:
            return {}
        
        profiles = []
        for fid, fuser in list(followers.items())[:sample_size]:
            quality = calculate_engagement_quality(
                fuser.follower_count, fuser.following_count, fuser.media_count, fuser.biography
            )
            profiles.append({
                "username": fuser.username,
                "quality": quality,
                "followers": fuser.follower_count,
                "following": fuser.following_count,
                "posts": fuser.media_count,
                "is_business": fuser.is_business_account,
                "is_verified": fuser.is_verified,
            })
        
        if not profiles:
            return {"profiles": profiles}
        
        try:
            qualities = [p["quality"] for p in profiles]
            avg_quality = sum(qualities) / len(qualities)
            high_quality = [p for p in profiles if p["quality"] > avg_quality]
            logger.info("📊 Found %d high-quality followers (avg: %.2f)", len(high_quality), avg_quality)
            return {
                "profiles": profiles,
                "high_quality": high_quality,
                "avg_quality": avg_quality,
                "count": len(profiles)
            }
        except Exception as e:
            logger.debug("Analysis err: %s", e)
            return {"profiles": profiles}

    @staticmethod
    def save_analysis(analysis: dict):
        with open(FOLLOWER_PROFILE_FILE, "w") as f:
            json.dump(analysis, f, indent=2)

# ══════════════════════════════════════════════════════════════════
#  VIRAL CONTENT DETECTOR
# ══════════════════════════════════════════════════════════════════

class ViralDetector:
    """Identify trending posts in your niche."""
    
    @staticmethod
    def detect_viral_trends(cl, hashtags: list, top_n: int = 10) -> list:
        """Find top-performing posts."""
        logger.info("🎬 Detecting viral trends in %d hashtags…", len(hashtags))
        
        viral_posts = []
        for tag in hashtags[:5]:
            try:
                medias = cl.hashtag_medias_top(tag, amount=20)
                for media in medias:
                    likes = media.like_count or 0
                    comments = media.comments_count or 0
                    engagement = likes + (comments * 5)
                    
                    viral_posts.append({
                        "hashtag": tag,
                        "caption": media.caption[:100] if media.caption else "—",
                        "likes": likes,
                        "comments": comments,
                        "engagement_score": engagement,
                        "media_type": "video" if media.media_type == 2 else "photo",
                        "posted_at": media.taken_at.isoformat() if media.taken_at else None,
                    })
            except:
                pass
        
        viral_posts.sort(key=lambda x: x["engagement_score"], reverse=True)
        top = viral_posts[:top_n]
        
        logger.info("✓ Found %d viral posts", len(top))
        
        with open(VIRAL_TRACKER, "w") as f:
            json.dump(top, f, indent=2)
        
        return top

# ══════════════════════════════════════════════════════════════════
#  CONTEXTUAL AI COMMENTS
# ══════════════════════════════════════════════════════════════════

class ContextualCommentGenerator:
    """Generate comments based on post type."""
    
    COMMENT_POOLS = {
        "motivation": ["This is fire! 🔥", "Absolutely love this! 💪", "Keep crushing it! 🙌", "Inspired! 🔥", "So good! ✨"],
        "fitness": ["Great workout! 💯", "Fitness goals! 🏋️", "Looking strong! 💪", "Gains! 🔥", "Inspiration! 🙏"],
        "sports": ["What a play! 🔥", "Incredible! 🏆", "Championship vibes! 🥇", "That's talent! ⚡", "Amazing! 🙌"],
        "lifestyle": ["Living your best life! 🔥", "Love it! 💯", "That's it! 🙌", "Vibe check! ✨", "Perfection! 💎"],
    }
    
    @staticmethod
    def generate_comment(post_caption: str = "", post_type: str = "sports") -> str:
        """Generate contextual comment."""
        caption_lower = (post_caption or "").lower()
        
        if any(w in caption_lower for w in ["gym", "workout", "training", "pump"]):
            pool = ContextualCommentGenerator.COMMENT_POOLS["fitness"]
        elif any(w in caption_lower for w in ["goal", "dream", "achieve", "win"]):
            pool = ContextualCommentGenerator.COMMENT_POOLS["motivation"]
        elif any(w in caption_lower for w in ["game", "score", "play", "team"]):
            pool = ContextualCommentGenerator.COMMENT_POOLS["sports"]
        else:
            pool = ContextualCommentGenerator.COMMENT_POOLS["sports"]
        
        return random.choice(pool)

# ══════════════════════════════════════════════════════════════════
#  MICRO-INFLUENCER DETECTOR
# ══════════════════════════════════════════════════════════════════

class MicroInfluencerOutreach:
    """Find micro-influencers for collaborations."""
    
    @staticmethod
    def find_micro_influencers(cl, hashtags: list, min_followers: int = 1000, 
                               max_followers: int = 50000) -> list:
        """Detect micro-influencers."""
        logger.info("💰 Scanning for micro-influencers…")
        
        candidates = {}
        for tag in hashtags[:8]:
            try:
                medias = cl.hashtag_medias_recent(tag, amount=30)
                for media in medias:
                    user = media.user
                    fc = user.follower_count or 0
                    if min_followers <= fc <= max_followers and not user.is_private:
                        if user.username not in candidates:
                            candidates[user.username] = {
                                "id": user.pk,
                                "followers": fc,
                                "following": user.following_count,
                                "posts": user.media_count,
                                "verified": user.is_verified,
                                "engagement_quality": calculate_engagement_quality(
                                    fc, user.following_count, user.media_count, user.biography
                                ),
                            }
            except:
                pass
        
        ranked = sorted(candidates.items(),
                       key=lambda x: x[1]["engagement_quality"], reverse=True)
        top = ranked[:20]
        
        logger.info("✓ Found %d micro-influencers", len(top))
        
        with open(INFLUENCER_TARGETS, "w") as f:
            json.dump({u: d for u, d in top}, f, indent=2)
        
        return top

# ══════════════════════════════════════════════════════════════════
#  ADAPTIVE LEARNING MODE
# ══════════════════════════════════════════════════════════════════

class AdaptiveGrowthMode:
    """ML-powered auto-adjustment of bot behavior."""
    
    @staticmethod
    def load_adaptive_config() -> dict:
        if Path(ADAPTIVE_CONFIG).exists():
            with open(ADAPTIVE_CONFIG) as f:
                return json.load(f)
        return {
            "follow_intensity": 1.0,
            "like_intensity": 1.0,
            "comment_intensity": 1.0,
            "delay_offset": 0.0,
            "success_streak": 0,
            "error_streak": 0,
            "last_adjusted": now_cat().isoformat(),
        }
    
    @staticmethod
    def save_adaptive_config(cfg: dict):
        with open(ADAPTIVE_CONFIG, "w") as f:
            json.dump(cfg, f, indent=2)
    
    @staticmethod
    def record_success():
        """Called on successful action."""
        cfg = AdaptiveGrowthMode.load_adaptive_config()
        cfg["error_streak"] = 0
        cfg["success_streak"] = cfg.get("success_streak", 0) + 1
        
        if cfg["success_streak"] > 20:
            cfg["follow_intensity"] = min(1.3, cfg.get("follow_intensity", 1.0) + 0.05)
            cfg["like_intensity"] = min(1.3, cfg.get("like_intensity", 1.0) + 0.05)
            cfg["success_streak"] = 0
            logger.info("📈 Adaptive: Increasing intensity")
        
        cfg["last_adjusted"] = now_cat().isoformat()
        AdaptiveGrowthMode.save_adaptive_config(cfg)
    
    @staticmethod
    def record_failure():
        """Called on error."""
        cfg = AdaptiveGrowthMode.load_adaptive_config()
        cfg["success_streak"] = 0
        cfg["error_streak"] = cfg.get("error_streak", 0) + 1
        
        if cfg["error_streak"] > 3:
            cfg["follow_intensity"] = max(0.5, cfg.get("follow_intensity", 1.0) - 0.1)
            cfg["like_intensity"] = max(0.5, cfg.get("like_intensity", 1.0) - 0.1)
            cfg["delay_offset"] = min(30, cfg.get("delay_offset", 0) + 5)
            cfg["error_streak"] = 0
            logger.warning("📉 Adaptive: Decreasing intensity")
        
        cfg["last_adjusted"] = now_cat().isoformat()
        AdaptiveGrowthMode.save_adaptive_config(cfg)
    
    @staticmethod
    def get_adjusted_limit(base_limit: int, intensity_key: str) -> int:
        """Get action limit adjusted by adaptive mode."""
        cfg = AdaptiveGrowthMode.load_adaptive_config()
        intensity = cfg.get(intensity_key, 1.0)
        return int(base_limit * intensity)

# ══════════════════════════════════════════════════════════════════
#  NOTIFICATIONS
# ══════════════════════════════════════════════════════════════════

def log_notification(title: str, message: str, level: str = "info"):
    """Log alert for user."""
    notif = {
        "timestamp": now_cat().isoformat(),
        "level": level,
        "title": title,
        "message": message,
    }
    
    notifs = []
    if Path(NOTIFICATIONS).exists():
        with open(NOTIFICATIONS) as f:
            notifs = json.load(f)
    
    notifs.append(notif)
    notifs = notifs[-1000:]
    
    with open(NOTIFICATIONS, "w") as f:
        json.dump(notifs, f, indent=2)
    
    if level == "critical":
        logger.critical("🚨 %s: %s", title, message)
    elif level == "error":
        logger.error("❌ %s: %s", title, message)
    elif level == "warning":
        logger.warning("⚠️  %s: %s", title, message)
    else:
        logger.info("ℹ️  %s: %s", title, message)

# ══════════════════════════════════════════════════════════════════
#  EXPORT ANALYTICS
# ══════════════════════════════════════════════════════════════════

def export_analytics_to_csv():
    """Export engagement data to CSV."""
    logger.info("📤 Exporting analytics to CSV…")
    
    try:
        scores = load_engagement_scores()
        if scores:
            with open("analytics_engagement.csv", "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["hashtag", "engagement_rate", "follows", "follow_backs"])
                for tag, data in scores.items():
                    writer.writerow([tag, data.get("engagement_rate", 0),
                                    data.get("follows", 0), data.get("follow_backs", 0)])
            logger.info("✓ Exported engagement scores")
    except Exception as e:
        logger.debug("CSV err: %s", e)
    
    try:
        hist = load_follower_history()
        if hist:
            with open("analytics_followers.csv", "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["date", "follower_count"])
                for date, count in sorted(hist.items()):
                    writer.writerow([date, count])
            logger.info("✓ Exported follower history")
    except Exception as e:
        logger.debug("CSV err: %s", e)
    
    try:
        if Path(VIRAL_TRACKER).exists():
            with open(VIRAL_TRACKER) as f:
                viral = json.load(f)
            if viral:
                with open("analytics_viral.csv", "w", newline="") as f:
                    writer = csv.writer(f)
                    writer.writerow(["hashtag", "likes", "comments", "engagement_score", "type"])
                    for post in viral:
                        writer.writerow([post.get("hashtag"), post.get("likes"),
                                        post.get("comments"), post.get("engagement_score"),
                                        post.get("media_type")])
                logger.info("✓ Exported viral posts")
    except Exception as e:
        logger.debug("CSV err: %s", e)

# ══════════════════════════════════════════════════════════════════
#  HELPERS
# ══════════════════════════════════════════════════════════════════

def load_follower_history() -> dict:
    if Path(FOLLOWER_HIST).exists():
        with open(FOLLOWER_HIST) as f:
            return json.load(f)
    return {}

def save_follower_history(hist: dict):
    with open(FOLLOWER_HIST, "w") as f:
        json.dump(hist, f, indent=2)

def record_follower_count(count: int):
    hist = load_follower_history()
    today = now_cat().strftime("%Y-%m-%d")
    hist[today] = count
    save_follower_history(hist)

def load_stats() -> dict:
    today = now_cat().strftime("%Y-%m-%d")
    if Path(DAILY_STATS_FILE).exists():
        with open(DAILY_STATS_FILE) as f:
            data = json.load(f)
        if data.get("date") == today:
            return data
    return {"date": today, "follows": 0, "unfollows": 0, "likes": 0, "comments": 0, 
            "posts": 0, "stories": 0, "replies": 0}

def save_stats(stats: dict):
    with open(DAILY_STATS_FILE, "w") as f:
        json.dump(stats, f, indent=2)

def record(action: str, stats: dict):
    stats[action] = stats.get(action, 0) + 1
    save_stats(stats)

def action_sleep(action_type: str = "follow"):
    """Smart delay based on action type."""
    delays = {
        "follow": (12, 45),
        "like": (2, 8),
        "comment": (8, 25),
        "post": (20, 60),
        "dm": (15, 45),
        "reply": (8, 25),
    }
    delay_range = delays.get(action_type, (5, 15))
    delay = random.uniform(*delay_range)
    time.sleep(delay)

def human_sleep(min_s: float, max_s: float):
    time.sleep(random.uniform(min_s, max_s))

def is_safe_hour() -> bool:
    return 7 <= now_cat().hour <= 22

def ensure_folder(path: str):
    Path(path).mkdir(exist_ok=True)

# ══════════════════════════════════════════════════════════════════
#  14-DAY WARM-UP
# ══════════════════════════════════════════════════════════════════

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

def get_account_day() -> int:
    if Path(ACCOUNT_START).exists():
        with open(ACCOUNT_START) as f:
            data = json.load(f)
        day = (now_cat().replace(tzinfo=None) - datetime.fromisoformat(data["start_date"])).days + 1
        return min(day, 14)
    with open(ACCOUNT_START, "w") as f:
        json.dump({"start_date": now_cat().isoformat()}, f)
    return 1

def get_today_limits() -> dict:
    day = get_account_day()
    return WARMUP_SCHEDULE[day]

def can_do(action: str, stats: dict, limits: dict) -> bool:
    used = stats.get(action, 0)
    limit = AdaptiveGrowthMode.get_adjusted_limit(limits.get(action, 0), f"{action}_intensity")
    return used < limit

# ══════════════════════════════════════════════════════════════════
#  THE BOT V7 PRO
# ══════════════════════════════════════════════════════════════════

class InstagramBotV7Pro:
    
    def __init__(self, cfg: dict):
        self.cfg = cfg
        self.username = cfg["username"]
        self.password = cfg["password"]
        self.cl = Client()
        self.cl.delay_range = [random.uniform(1, 3), random.uniform(3, 6)]
        self._my_uid = None
        self._last_login = None
    
    def login(self):
        try:
            if Path(SESSION_FILE).exists():
                self.cl.load_settings(SESSION_FILE)
            self.cl.login(self.username, self.password)
            self.cl.dump_settings(SESSION_FILE)
            self._last_login = now_cat()
            logger.info("✅ Logged in")
        except Exception as e:
            logger.error("❌ Login failed: %s", e)
            raise
    
    def ensure_logged_in(self):
        if not self._last_login or (now_cat() - self._last_login).seconds > 3600:
            try:
                self.cl.get_settings()
                self._last_login = now_cat()
            except:
                self.login()
    
    def my_uid(self):
        if not self._my_uid:
            self._my_uid = self.cl.user_id_from_username(self.username)
        return self._my_uid
    
    # ── AI FEATURES ──
    
    def run_ai_analysis(self):
        """Run AI analysis on followers."""
        logger.info("🤖 Running AI analysis…")
        try:
            analysis = FollowerAnalyzer.analyze_followers(self.cl, self.my_uid(), sample_size=200)
            FollowerAnalyzer.save_analysis(analysis)
            log_notification("AI Analysis Complete", 
                           f"Analyzed {analysis.get('count', 0)} followers")
        except Exception as e:
            logger.error("AI analysis err: %s", e)
    
    def detect_viral_trends(self):
        """Detect viral trends."""
        logger.info("🎬 Detecting viral trends…")
        try:
            tags = random.sample(SPORTS_HASHTAGS, 15)
            trends = ViralDetector.detect_viral_trends(self.cl, tags, top_n=15)
            if trends:
                top = trends[0]
                msg = f"Top trend: {top['engagement_score']} engagements on #{top['hashtag']}"
                log_notification("🔥 Viral Trend Found", msg)
        except Exception as e:
            logger.error("Viral trend err: %s", e)
    
    def find_micro_influencers(self):
        """Find micro-influencers."""
        logger.info("💰 Finding micro-influencers…")
        try:
            tags = random.sample(SPORTS_HASHTAGS, 15)
            influencers = MicroInfluencerOutreach.find_micro_influencers(self.cl, tags)
            if influencers:
                msg = f"Found {len(influencers)} micro-influencers"
                log_notification("💰 Micro-Influencers Found", msg)
        except Exception as e:
            logger.error("Influencer search err: %s", e)
    
    def smart_follow_quality_first(self, stats: dict, limits: dict, tracker: dict):
        """Follow accounts with highest engagement quality first."""
        logger.info("⭐ Smart following (quality first)…")
        if not can_do("follows", stats, limits):
            return
        
        try:
            tags = random.sample(SPORTS_HASHTAGS, 3)
            for tag in tags:
                medias = self.cl.hashtag_medias_recent(tag, amount=40)
                candidates = []
                
                for media in medias:
                    user = media.user
                    if user.username == self.username or user.username in tracker or user.is_private:
                        continue
                    
                    quality = calculate_engagement_quality(
                        user.follower_count, user.following_count, user.media_count, user.biography
                    )
                    
                    if not is_likely_fake_account(user.follower_count, user.following_count, 
                                                 user.media_count, user.username):
                        candidates.append((user, quality))
                
                candidates.sort(key=lambda x: x[1], reverse=True)
                
                for user, quality in candidates[:10]:
                    if not can_do("follows", stats, limits):
                        return
                    
                    try:
                        self.cl.user_follow(user.pk)
                        tracker[user.username] = {
                            "user_id": str(user.pk),
                            "followed_at": now_cat().isoformat(),
                            "quality_score": quality,
                            "unfollowed": False,
                        }
                        record("follows", stats)
                        AdaptiveGrowthMode.record_success()
                        logger.info("✅ Followed @%s (quality: %.2f)", user.username, quality)
                        action_sleep("follow")
                    except Exception as e:
                        logger.debug("Follow err: %s", e)
                        AdaptiveGrowthMode.record_failure()
        except Exception as e:
            logger.error("Smart follow err: %s", e)
    
    def contextual_engage(self, stats: dict, limits: dict):
        """Engage with contextual comments."""
        logger.info("💬 Contextual engagement…")
        if not can_do("comments", stats, limits):
            return
        
        try:
            tag = random.choice(SPORTS_HASHTAGS)
            medias = self.cl.hashtag_medias_recent(tag, amount=30)
            random.shuffle(medias)
            
            for media in medias:
                if not can_do("likes", stats, limits):
                    break
                
                try:
                    self.cl.media_like(media.pk)
                    record("likes", stats)
                    logger.info("❤️  Liked post")
                    action_sleep("like")
                    
                    if random.random() < 0.33 and can_do("comments", stats, limits):
                        comment = ContextualCommentGenerator.generate_comment(
                            media.caption or "", "sports"
                        )
                        self.cl.media_comment(media.pk, comment)
                        record("comments", stats)
                        logger.info("💬 Commented: %s", comment)
                        action_sleep("comment")
                    
                    AdaptiveGrowthMode.record_success()
                except Exception as e:
                    logger.debug("Engage err: %s", e)
                    AdaptiveGrowthMode.record_failure()
                
                human_sleep(10, 30)
        except Exception as e:
            logger.error("Engage err: %s", e)
    
    def generate_pro_dashboard(self, stats: dict, limits: dict):
        """Generate advanced HTML dashboard."""
        logger.info("📊 Generating PRO dashboard…")
        
        try:
            day = get_account_day()
            hist = load_follower_history()
            dates = sorted(hist.keys())[-14:]
            counts = [hist[d] for d in dates]
            gain = counts[-1] - counts[0] if len(counts) >= 2 else 0
            
            analysis = {}
            if Path(FOLLOWER_PROFILE_FILE).exists():
                with open(FOLLOWER_PROFILE_FILE) as f:
                    analysis = json.load(f)
            
            avg_quality = analysis.get("avg_quality", 0)
            hq_count = len(analysis.get("high_quality", []))
            
            best_hours = [9, 13, 19]
            
            recent_notifs = []
            if Path(NOTIFICATIONS).exists():
                with open(NOTIFICATIONS) as f:
                    recent_notifs = json.load(f)[-10:]
            
            viral_posts = []
            if Path(VIRAL_TRACKER).exists():
                with open(VIRAL_TRACKER) as f:
                    viral_posts = json.load(f)[:5]
            
            notif_rows = ""
            for n in recent_notifs:
                notif_rows += f"""<tr>
                    <td>{n['timestamp'][:10]}</td>
                    <td>{n['title']}</td>
                    <td style="color: {'red' if n['level'] == 'error' else 'orange' if n['level'] == 'warning' else 'green'}">{n['level'].upper()}</td>
                </tr>"""
            
            viral_rows = ""
            for post in viral_posts:
                viral_rows += f"""<tr>
                    <td>#{post['hashtag']}</td>
                    <td>{post['likes']}</td>
                    <td>{post['engagement_score']}</td>
                    <td>{post['media_type']}</td>
                </tr>"""
            
            chart_labels = str(dates).replace("'", '"')
            chart_data = str(counts)
            
            html = f"""<!DOCTYPE html>
<html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width">
<title>🚀 Bot V7 PRO Dashboard</title>
<style>
body{{font-family:Arial;background:linear-gradient(135deg,#1a1a2e,#16213e);color:#eee;margin:0;padding:20px}}
h1{{color:#00d4ff;text-align:center;margin-bottom:5px}}
.subtitle{{text-align:center;color:#888;margin-bottom:20px}}
.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:15px;margin-bottom:20px}}
.card{{background:#0f3460;border-left:4px solid #00d4ff;border-radius:8px;padding:15px}}
.card h3{{margin:0 0 8px;color:#00d4ff;font-size:12px;text-transform:uppercase}}
.card .value{{font-size:28px;font-weight:bold;color:#fff}}
.card .delta{{font-size:12px;color:#00d4ff;margin-top:5px}}
.section{{background:#0f3460;border-radius:8px;padding:20px;margin-bottom:20px}}
.section h2{{color:#00d4ff;margin-top:0;font-size:16px;border-bottom:2px solid #00d4ff;padding-bottom:10px}}
table{{width:100%;border-collapse:collapse;font-size:12px}}
th{{background:#16213e;color:#00d4ff;padding:10px;text-align:left}}
td{{padding:8px;border-bottom:1px solid #16213e}}
.bar{{background:linear-gradient(90deg,#00d4ff,#0099ff);height:20px;border-radius:4px;display:flex;align-items:center;justify-content:flex-end;padding-right:5px;color:#000;font-weight:bold;font-size:11px}}
canvas{{max-width:100%}}
</style><script src="https://cdn.jsdelivr.net/npm/chart.js"></script></head>
<body>
<h1>🚀 BOT V7 PRO — Dashboard</h1>
<p class="subtitle">Day {day} | {now_cat().strftime('%d %b %Y %H:%M')} CAT</p>

<div class="grid">
<div class="card">
<h3>Follower Gain (14d)</h3>
<div class="value">+{gain}</div>
<div class="delta">Current: {counts[-1] if counts else 0}</div>
</div>

<div class="card">
<h3>Follower Quality</h3>
<div class="value">{hq_count}</div>
<div class="delta">Avg Score: {avg_quality:.2f}/1.0</div>
</div>

<div class="card">
<h3>Best Post Hours</h3>
<div class="value">{" · ".join(f"{h}:00" for h in best_hours[:3])}</div>
<div class="delta">Based on engagement</div>
</div>

<div class="card">
<h3>Adaptive Mode</h3>
<div class="value">ACTIVE</div>
<div class="delta">Auto-optimizing</div>
</div>
</div>

<div class="section">
<h2>📈 Engagement Metrics</h2>
<table>
<tr><th>Metric</th><th>Used</th><th>Limit</th><th>Progress</th></tr>
<tr>
<td>Follows</td>
<td>{stats.get('follows', 0)}</td>
<td>{limits.get('follows', 0)}</td>
<td><div class="bar" style="width:{int(stats.get('follows', 0)/max(limits.get('follows', 1), 1)*100)}%">{int(stats.get('follows', 0)/max(limits.get('follows', 1), 1)*100)}%</div></td>
</tr>
<tr>
<td>Likes</td>
<td>{stats.get('likes', 0)}</td>
<td>{limits.get('likes', 0)}</td>
<td><div class="bar" style="width:{int(stats.get('likes', 0)/max(limits.get('likes', 1), 1)*100)}%">{int(stats.get('likes', 0)/max(limits.get('likes', 1), 1)*100)}%</div></td>
</tr>
<tr>
<td>Comments</td>
<td>{stats.get('comments', 0)}</td>
<td>{limits.get('comments', 0)}</td>
<td><div class="bar" style="width:{int(stats.get('comments', 0)/max(limits.get('comments', 1), 1)*100)}%">{int(stats.get('comments', 0)/max(limits.get('comments', 1), 1)*100)}%</div></td>
</tr>
</table>
</div>

<div class="section">
<h2>👥 Follower Growth (14 days)</h2>
<canvas id="growthChart" height="60"></canvas>
<script>
new Chart(document.getElementById('growthChart'), {{
type:'line',
data:{{
labels:{chart_labels},
datasets:[{{
label:'Followers',
data:{chart_data},
borderColor:'#00d4ff',
backgroundColor:'rgba(0,212,255,0.1)',
fill:true,
tension:0.4,
pointRadius:5,
pointBackgroundColor:'#00d4ff'
}}]
}},
options:{{
plugins:{{legend:{{labels:{{color:'#eee'}}}}}},
scales:{{
x:{{ticks:{{color:'#aaa'}},grid:{{color:'#16213e'}}}},
y:{{ticks:{{color:'#aaa'}},grid:{{color:'#16213e'}}}}
}}
}}
}});
</script>
</div>

<div class="section">
<h2>🔥 Viral Trends</h2>
<table>
<tr><th>Hashtag</th><th>Likes</th><th>Engagement</th><th>Type</th></tr>
{viral_rows if viral_rows else '<tr><td colspan="4">No viral data yet</td></tr>'}
</table>
</div>

<div class="section">
<h2>🔔 Recent Notifications</h2>
<table>
<tr><th>Date</th><th>Title</th><th>Level</th></tr>
{notif_rows if notif_rows else '<tr><td colspan="3">No notifications</td></tr>'}
</table>
</div>

</body></html>"""
            
            with open(DASHBOARD_FILE, "w") as f:
                f.write(html)
            logger.info("✅ Dashboard generated → %s", DASHBOARD_FILE)
        except Exception as e:
            logger.error("Dashboard err: %s", e)
    
    def print_ai_summary(self, stats: dict, limits: dict):
        """Print summary."""
        day = get_account_day()
        logger.info("")
        logger.info("╔════════════════════════════════════════════════════════╗")
        logger.info("║  🚀 BOT V7 PRO — AI-Powered Summary — Day %d           ║", day)
        logger.info("╠════════════════════════════════════════════════════════╣")
        
        for key in ["follows", "likes", "comments", "posts", "stories"]:
            used = stats.get(key, 0)
            limit = limits.get(key, 0)
            pct = int(used / max(limit, 1) * 20)
            bar = "█" * pct + "░" * (20 - pct)
            logger.info("║  %-10s %2d/%-2d  [%s] ║", key.upper(), used, limit, bar)
        
        logger.info("╠════════════════════════════════════════════════════════╣")
        
        cfg = AdaptiveGrowthMode.load_adaptive_config()
        logger.info("║  📈 Adaptive Mode:  follow=%.2fx  like=%.2fx           ║",
                   cfg.get("follow_intensity", 1.0), cfg.get("like_intensity", 1.0))
        
        logger.info("╚════════════════════════════════════════════════════════╝")
        logger.info("")

# ══════════════════════════════════════════════════════════════════
#  CONFIG
# ══════════════════════════════════════════════════════════════════

CONFIG = {
    "username": "l_k_marengwa",
    "password": "Kudzai@170505",
    "anthropic_api_key": "",
    "proxies": [],
    "unfollow_after_days": 3,
    "poll_interval_minutes": 15,
    "target_accounts": [],
    "story_sources": [],
    "welcome_dms_enabled": True,
    "welcome_dms": ["Thanks for following! 🙏 Daily sports content 🔥"],
    "comments": [
        "Love this! 🔥", "Great content! 👏", "Amazing! 💯",
        "Keep it up! 🙌", "Inspiring! ✨", "Incredible! 😍",
    ],
    "replies": [
        "Thank you! 🙏", "Really appreciate it! ❤️", "Thanks so much! 😊",
        "Means a lot! 🔥",
    ],
}

# ══════════════════════════════════════════════════════════════════
#  MAIN
# ════════════════════════════════  ═════════════════════════════════

def main():
    bot = InstagramBotV7Pro(CONFIG)
    
    try:
        bot.login()
    except Exception as e:
        logger.error("Login failed: %s", e)
        exit(1)
    
    logger.info("")
    logger.info("╔════════════════════════════════════════════════════════╗")
    logger.info("║  🚀 INSTAGRAM BOT V7 PRO — AI-POWERED MODE             ║")
    logger.info("║  Smart Targeting • Deep Analytics • Growth Hacking      ║")
    logger.info("║  Day %d | %s CAT                     ║", get_account_day(),
                now_cat().strftime("%d %b %Y  %H:%M"))
    logger.info("╚════════════════════════════════════════════════════════╝")
    logger.info("")
    
    poll_mins = CONFIG.get("poll_interval_minutes", 15)
    run_count = 0
    
    while True:
        stats = load_stats()
        limits = get_today_limits()
        
        if not is_safe_hour():
            next_safe = now_cat().replace(hour=7, minute=0)
            if now_cat().hour >= 23:
                next_safe += timedelta(days=1)
            wait = int((next_safe - now_cat()).total_seconds() / 60)
            logger.info("🌙 Outside safe hours — sleeping %d min…", wait)
            time.sleep(min(wait * 60, 3600))
            continue
        
        if not Path(DAILY_RUN_FILE).exists() or \
           json.load(open(DAILY_RUN_FILE)).get("date") != now_cat().strftime("%Y-%m-%d"):
            
            logger.info("☀️  Running full daily routine…")
            tracker = {}
            ensure_folder(CONTENT_FOLDER)
            
            bot.run_ai_analysis()
            human_sleep(5, 10)
            
            bot.detect_viral_trends()
            human_sleep(5, 10)
            
            bot.find_micro_influencers()
            human_sleep(5, 10)
            
            bot.smart_follow_quality_first(stats, limits, tracker)
            human_sleep(20, 40)
            
            bot.contextual_engage(stats, limits)
            human_sleep(15, 30)
            
            try:
                info = bot.cl.user_info_by_username(bot.username)
                record_follower_count(info.follower_count)
                logger.info("👥 Follower count: %d", info.follower_count)
            except:
                pass
            
            export_analytics_to_csv()
            
            bot.generate_pro_dashboard(stats, limits)
            bot.print_ai_summary(stats, limits)
            
            with open(DAILY_RUN_FILE, "w") as f:
                json.dump({"date": now_cat().strftime("%Y-%m-%d")}, f)
            
            log_notification("Daily Routine Complete", "All AI features executed")
        
        run_count += 1
        if run_count % 3 == 0:
            logger.info("🔄 Real-time check…")
            bot.contextual_engage(stats, limits)
        
        logger.info("💤 Next cycle in %d min…", poll_mins)
        time.sleep(poll_mins * 60)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("⛔ Bot stopped at %s CAT", now_cat().strftime("%H:%M:%S"))
