import logging
from datetime import datetime

# Configure logging to write to a file with timestamp
logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Create logger
logger = logging.getLogger(__name__)

# Example usage
def main():
    logger.info("Application started")
    
    # Different log levels
    logger.debug("This is a debug message")
    logger.info("Processing user request")
    logger.warning("Low memory warning")
    logger.error("Failed to connect to database")
    logger.critical("System critical error")
    
    # Log with variables
    user_id = 12345
    action = "login"
    logger.info(f"User {user_id} performed action: {action}")
    
    # Log exceptions
    try:
        result = 10 / 0
    except Exception as e:
        logger.exception("An error occurred during calculation")
    
    logger.info("Application finished")

if __name__ == "__main__":
    main()
    print("Check 'app.log' file for the logs")