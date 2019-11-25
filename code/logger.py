def log_reddit_error(logger, praw_error, message=""):
    """Log a praw exception."""
    if message:
        logger.error("error while using the Reddit API: %s. Message = %s", praw_error, message)
    else:
        logger.error("error while using the Reddit API: %s", praw_error)
