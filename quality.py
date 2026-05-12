"""Account quality scoring and fake account detection."""
from typing import Tuple
from config import (
    QUALITY_RATIO_WEIGHT,
    QUALITY_ACTIVITY_WEIGHT,
    QUALITY_BIO_WEIGHT,
)
from utils import logger

# ═══════════════════════════════════════════════════════════════════════
#  ENGAGEMENT QUALITY SCORING
# ═══════════════════════════════════════════════════════════════════════

def calculate_engagement_quality(
    follower_count: int,
    following_count: int,
    media_count: int,
    biography: str = ""
) -> float:
    """
    Score follower quality (0.0 - 1.0).
    Higher score = more likely to follow back.
    
    Factors:
    - Follower/Following Ratio (40%): Healthy accounts follow fewer than their followers
    - Activity Level (35%): Posts relative to follower count
    - Bio (25%): Accounts with detailed bios are more real
    
    Args:
        follower_count: Number of followers
        following_count: Number of accounts followed
        media_count: Number of posts
        biography: User biography text
    
    Returns:
        Quality score between 0.0 and 1.0
    """
    # Ratio score: ideal ratio is 1:1 or higher
    if follower_count == 0 or following_count == 0:
        return 0.0
    
    ratio = follower_count / max(following_count, 1)
    # Normalize: score peaks at ratio of 2.0, decreases for higher ratios
    ratio_score = min(1.0, ratio / 2.0) if ratio > 0 else 0.0
    
    # Activity score: posts per 100 followers
    if media_count > 0 and follower_count > 0:
        posts_per_100 = (media_count / max(follower_count, 1)) * 100
        # Normalize: ~5 posts per 100 followers is healthy
        activity_score = min(1.0, posts_per_100 / 5.0)
    else:
        activity_score = 0.0
    
    # Bio score: longer bios indicate real accounts
    bio_score = 0.7 if biography and len(biography) > 10 else 0.3
    
    # Weighted average
    quality = (
        (ratio_score * QUALITY_RATIO_WEIGHT) +
        (activity_score * QUALITY_ACTIVITY_WEIGHT) +
        (bio_score * QUALITY_BIO_WEIGHT)
    )
    
    return max(0.0, min(1.0, quality))

# ═══════════════════════════════════════════════════════════════════════
#  FAKE ACCOUNT DETECTION
# ═══════════════════════════════════════════════════════════════════════

BOT_PATTERNS = [
    "test", "bot", "spam", "admin", "noreply", "bot_",
    "auto", "script", "fake", "scam", "follow4follow",
    "likeforlike", "tagforlike", "f4f", "l4l",
]

SUSPICIOUS_RATIOS = {
    "max_following_ratio": 10.0,  # Following 10x more than followers is suspicious
    "min_following_ratio": 0.01,  # Following 1% of followers is suspicious
}

FAKE_THRESHOLDS = {
    "min_media_for_huge_followers": 5,  # If 10k+ followers but <5 posts = fake
    "min_followers_for_threshold": 10000,
}

def is_likely_fake_account(
    follower_count: int,
    following_count: int,
    media_count: int,
    username: str
) -> bool:
    """
    Detect obvious bot and fake accounts.
    
    Checks:
    1. Following/Follower ratio is suspiciously high or low
    2. Has many followers but very few posts
    3. Username matches common bot patterns
    
    Args:
        follower_count: Number of followers
        following_count: Number of accounts followed
        media_count: Number of posts
        username: Account username
    
    Returns:
        True if likely a fake/bot account
    """
    # Check 1: Following/Follower ratio
    if follower_count > 0:
        ratio = following_count / follower_count
        if ratio > SUSPICIOUS_RATIOS["max_following_ratio"]:
            logger.debug(f"🤖 {username}: Following ratio {ratio:.2f} (too high)")
            return True
        if ratio < SUSPICIOUS_RATIOS["min_following_ratio"]:
            logger.debug(f"🤖 {username}: Following ratio {ratio:.4f} (too low)")
            return True
    
    # Check 2: Many followers but few posts (likely purchased followers)
    if (media_count < FAKE_THRESHOLDS["min_media_for_huge_followers"] and
        follower_count > FAKE_THRESHOLDS["min_followers_for_threshold"]):
        logger.debug(f"🤖 {username}: {follower_count} followers but only {media_count} posts")
        return True
    
    # Check 3: Bot name patterns
    username_lower = username.lower()
    if any(pattern in username_lower for pattern in BOT_PATTERNS):
        logger.debug(f"🤖 {username}: Matches bot pattern")
        return True
    
    return False

# ═══════════════════════════════════════════════════════════════════════
#  BATCH QUALITY ANALYSIS
# ═══════════════════════════════════════════════════════════════════════

def analyze_account_batch(
    accounts: list,
    quality_threshold: float = 0.5
) -> Tuple[list, list, float]:
    """
    Analyze a batch of accounts and categorize them.
    
    Args:
        accounts: List of account data dicts with follower_count, following_count, etc.
        quality_threshold: Minimum quality score to consider "high quality"
    
    Returns:
        Tuple of (high_quality_accounts, low_quality_accounts, average_quality)
    """
    high_quality = []
    low_quality = []
    qualities = []
    
    for account in accounts:
        quality = calculate_engagement_quality(
            account.get("follower_count", 0),
            account.get("following_count", 0),
            account.get("media_count", 0),
            account.get("biography", "")
        )
        
        is_fake = is_likely_fake_account(
            account.get("follower_count", 0),
            account.get("following_count", 0),
            account.get("media_count", 0),
            account.get("username", "")
        )
        
        account["quality_score"] = quality
        account["is_fake"] = is_fake
        qualities.append(quality)
        
        if not is_fake and quality >= quality_threshold:
            high_quality.append(account)
        else:
            low_quality.append(account)
    
    avg_quality = sum(qualities) / len(qualities) if qualities else 0.0
    
    return high_quality, low_quality, avg_quality

# ═══════════════════════════════════════════════════════════════════════
#  ENGAGEMENT PREDICTION
# ═══════════════════════════════════════════════════════════════════════

def predict_follow_back_rate(quality_score: float) -> float:
    """
    Predict follow-back rate based on quality score.
    
    Uses empirical model:
    - 0.0-0.2: ~5% follow back
    - 0.2-0.4: ~15% follow back
    - 0.4-0.6: ~35% follow back
    - 0.6-0.8: ~65% follow back
    - 0.8-1.0: ~85% follow back
    
    Args:
        quality_score: Account quality score (0.0-1.0)
    
    Returns:
        Estimated follow-back rate (0.0-1.0)
    """
    if quality_score < 0.2:
        return 0.05
    elif quality_score < 0.4:
        return 0.15
    elif quality_score < 0.6:
        return 0.35
    elif quality_score < 0.8:
        return 0.65
    else:
        return 0.85

# ═══════════════════════════════════════════════════════════════════════
#  DEBUG UTILITIES
# ═══════════════════════════════════════════════════════════════════════

def debug_quality_calculation(
    follower_count: int,
    following_count: int,
    media_count: int,
    biography: str = "",
    username: str = "unknown"
) -> dict:
    """
    Debug quality calculation by showing component scores.
    
    Args:
        follower_count: Number of followers
        following_count: Number of accounts followed
        media_count: Number of posts
        biography: User biography
        username: Username for logging
    
    Returns:
        Dict with all component scores and final score
    """
    # Calculate components
    ratio = follower_count / max(following_count, 1) if following_count > 0 else 0
    ratio_score = min(1.0, ratio / 2.0) if ratio > 0 else 0.0
    
    posts_per_100 = (media_count / max(follower_count, 1)) * 100 if follower_count > 0 else 0
    activity_score = min(1.0, posts_per_100 / 5.0) if follower_count > 0 else 0.0
    
    bio_score = 0.7 if biography and len(biography) > 10 else 0.3
    
    quality = (
        (ratio_score * QUALITY_RATIO_WEIGHT) +
        (activity_score * QUALITY_ACTIVITY_WEIGHT) +
        (bio_score * QUALITY_BIO_WEIGHT)
    )
    quality = max(0.0, min(1.0, quality))
    
    is_fake = is_likely_fake_account(follower_count, following_count, media_count, username)
    follow_back_rate = predict_follow_back_rate(quality)
    
    return {
        "username": username,
        "follower_count": follower_count,
        "following_count": following_count,
        "media_count": media_count,
        "f_f_ratio": ratio,
        "ratio_score": ratio_score,
        "posts_per_100_followers": posts_per_100,
        "activity_score": activity_score,
        "bio_length": len(biography),
        "bio_score": bio_score,
        "overall_quality": quality,
        "is_likely_fake": is_fake,
        "estimated_follow_back_rate": follow_back_rate,
    }
