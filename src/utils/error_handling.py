# utils/error_handling.py

from src.utils.logger import setup_logger

logger = setup_logger()


def handle_error(func):
    """Decorator to handle exceptions gracefully and log them."""

    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.error(f"Error in {func.__name__}: {e}")
            raise  # Optionally re-raise the exception if you want it to propagate

    return wrapper
