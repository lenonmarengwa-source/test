"""Utility functions for file I/O, logging, and common operations."""
import json
import logging
import time
import random
from pathlib import Path
from datetime import datetime, timezone, timedelta
from typing import Any, Dict, Optional
from instagrapi.exceptions import LoginRequired, ClientError, NotFound

# ═══════════════════════════════════════════════════════════════════════
#  TIMEZONE
# ═══════════════════════════════════════════════════════════════════════

CAT = timezone(timedelta(hours=2))

def now_cat() -> datetime:
    """Get current time in CAT (Central Africa Time)."""
    return datetime.now(CAT)

# ═══════════════════════════════════════════════════════════════════════
#  LOGGING SETUP
# ═══════════════════════════════════════════════════════════════════════

class CATFormatter(logging.Formatter):
    """Custom formatter that displays time in CAT."""
    
    def formatTime(self, record, datefmt=None):
        ct = datetime.fromtimestamp(record.created, tz=CAT)
        return ct.strftime(datefmt or "%Y-%m-%d %H:%M:%S") + " CAT"

def setup_logger(name: str = "BotV7PRO", level: int = logging.INFO) -> logging.Logger:
    """Set up logger with CAT timezone formatter."""
    handler = logging.StreamHandler()
    handler.setFormatter(CATFormatter("%(asctime)s  %(levelname)-8s  %(message)s"))
    
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.handlers.clear()
    logger.addHandler(handler)
    
    return logger

logger = setup_logger()

# ═══════════════════════════════════════════════════════════════════════
#  SAFE JSON OPERATIONS
# ═══════════════════════════════════════════════════════════════════════

def load_json(path: Path, default: Optional[Any] = None) -> Any:
    """
    Safely load JSON file with error handling.
    
    Args:
        path: Path to JSON file
        default: Default value if file doesn't exist or is invalid
    
    Returns:
        Parsed JSON or default value
    """
    if default is None:
        default = {}
    
    try:
        if not isinstance(path, Path):
            path = Path(path)
        
        if not path.exists():
            logger.debug(f"File not found: {path}")
            return default
        
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        logger.error(f"JSON decode error in {path}: {e}")
        # Try to create backup
        if path.exists():
            backup_path = path.with_suffix(".json.bak")
            try:
                path.rename(backup_path)
                logger.info(f"Moved corrupted file to {backup_path}")
            except Exception as backup_err:
                logger.error(f"Failed to backup: {backup_err}")
        return default
    except IOError as e:
        logger.error(f"IO error reading {path}: {e}")
        return default
    except Exception as e:
        logger.error(f"Unexpected error loading {path}: {e}")
        return default

def save_json(path: Path, data: Any, indent: int = 2, backup: bool = True) -> bool:
    """
    Safely save JSON file with atomic write and optional backup.
    
    Args:
        path: Path to save JSON file
        data: Data to save
        indent: JSON indentation level
        backup: Create backup of existing file
    
    Returns:
        True if successful, False otherwise
    """
    try:
        if not isinstance(path, Path):
            path = Path(path)
        
        # Create parent directory if needed
        path.parent.mkdir(parents=True, exist_ok=True)
        
        # Create backup if file exists
        if backup and path.exists():
            backup_path = path.with_suffix(".json.bak")
            try:
                path.replace(backup_path)
            except Exception as e:
                logger.warning(f"Failed to create backup: {e}")
        
        # Write to temporary file first (atomic write)
        temp_path = path.with_suffix(".json.tmp")
        with open(temp_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=indent, ensure_ascii=False)
        
        # Atomic rename
        temp_path.replace(path)
        return True
    except Exception as e:
        logger.error(f"Failed to save {path}: {e}")
        return False

# ═══════════════════════════════════════════════════════════════════════
#  STATS MANAGEMENT
# ═══════════════════════════════════════════════════════════════════════

def load_stats(stats_file: Path) -> Dict[str, int]:
    """Load daily statistics."""
    today = now_cat().strftime("%Y-%m-%d")
    stats = load_json(stats_file, {})
    
    if stats.get("date") != today:
        return {
            "date": today,
            "follows": 0,
            "unfollows": 0,
            "likes": 0,
            "comments": 0,
            "posts": 0,
            "stories": 0,
            "replies": 0,
        }
    return stats

def save_stats(stats_file: Path, stats: Dict[str, int]) -> bool:
    """Save daily statistics."""
    return save_json(stats_file, stats)

def record_action(stats_file: Path, action: str) -> bool:
    """Increment action counter and save."""
    stats = load_stats(stats_file)
    stats[action] = stats.get(action, 0) + 1
    return save_stats(stats_file, stats)

# ═══════════════════════════════════════════════════════════════════════
#  FOLLOWER HISTORY
# ═══════════════════════════════════════════════════════════════════════

def load_follower_history(hist_file: Path) -> Dict[str, int]:
    """Load historical follower counts."""
    return load_json(hist_file, {})

def save_follower_history(hist_file: Path, history: Dict[str, int]) -> bool:
    """Save follower history."""
    return save_json(hist_file, history)

def record_follower_count(hist_file: Path, count: int) -> bool:
    """Record today's follower count."""
    today = now_cat().strftime("%Y-%m-%d")
    history = load_follower_history(hist_file)
    history[today] = count
    return save_follower_history(hist_file, history)

# ═══════════════════════════════════════════════════════════════════════
#  DELAY & TIMING
# ═══════════════════════════════════════════════════════════════════════

def action_sleep(action_type: str = "follow", delays: Dict[str, tuple] = None):
    """
    Smart delay based on action type to avoid detection.
    
    Args:
        action_type: Type of action (follow, like, comment, etc.)
        delays: Custom delay ranges, if None uses defaults
    """
    if delays is None:
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
    """Sleep for random duration between min and max seconds."""
    duration = random.uniform(min_s, max_s)
    time.sleep(duration)

def is_safe_hour(hour: int = None, safe_start: int = 7, safe_end: int = 22) -> bool:
    """
    Check if current hour is within safe operating hours.
    
    Args:
        hour: Hour to check (default: current hour)
        safe_start: Start hour (inclusive)
        safe_end: End hour (inclusive)
    
    Returns:
        True if within safe hours
    """
    if hour is None:
        hour = now_cat().hour
    return safe_start <= hour <= safe_end

# ═══════════════════════════════════════════════════════════════════════
#  NOTIFICATIONS
# ═══════════════════════════════════════════════════════════════════════

def log_notification(
    notif_file: Path,
    title: str,
    message: str,
    level: str = "info",
    max_notifications: int = 1000
) -> bool:
    """
    Log notification for user with optional email/alert.
    
    Args:
        notif_file: Path to notifications file
        title: Notification title
        message: Notification message
        level: Log level (info, warning, error, critical)
        max_notifications: Maximum notifications to keep
    
    Returns:
        True if saved successfully
    """
    notif = {
        "timestamp": now_cat().isoformat(),
        "level": level,
        "title": title,
        "message": message,
    }
    
    notifs = load_json(notif_file, [])
    if not isinstance(notifs, list):
        notifs = []
    
    notifs.append(notif)
    notifs = notifs[-max_notifications:]
    
    success = save_json(notif_file, notifs)
    
    # Also log to console
    if level == "critical":
        logger.critical(f"🚨 {title}: {message}")
    elif level == "error":
        logger.error(f"❌ {title}: {message}")
    elif level == "warning":
        logger.warning(f"⚠️  {title}: {message}")
    else:
        logger.info(f"ℹ️  {title}: {message}")
    
    return success

# ═══════════════════════════════════════════════════════════════════════
#  ERROR HANDLING DECORATORS
# ═══════════════════════════════════════════════════════════════════════

def handle_instagram_errors(func):
    """Decorator to handle common Instagram API errors."""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except LoginRequired:
            logger.error("Session expired, need to login again")
            raise
        except ClientError as e:
            logger.error(f"Instagram client error: {e}")
            return None
        except NotFound as e:
            logger.debug(f"Resource not found: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error in {func.__name__}: {e}")
            return None
    return wrapper

# ═══════════════════════════════════════════════════════════════════════
#  FILE MANAGEMENT
# ═══════════════════════════════════════════════════════════════════════

def ensure_folder(path: Path) -> Path:
    """Create folder if it doesn't exist."""
    if not isinstance(path, Path):
        path = Path(path)
    path.mkdir(parents=True, exist_ok=True)
    return path

def cleanup_old_files(folder: Path, days: int = 30, pattern: str = "*.json"):
    """Delete files older than specified days."""
    if not isinstance(folder, Path):
        folder = Path(folder)
    
    if not folder.exists():
        return 0
    
    cutoff_time = time.time() - (days * 86400)
    deleted_count = 0
    
    try:
        for file_path in folder.glob(pattern):
            if file_path.stat().st_mtime < cutoff_time:
                file_path.unlink()
                deleted_count += 1
                logger.info(f"Deleted old file: {file_path}")
    except Exception as e:
        logger.error(f"Error during cleanup: {e}")
    
    return deleted_count
