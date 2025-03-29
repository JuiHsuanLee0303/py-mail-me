"""
Example of using retry mechanism and logging with py-mail-me.
"""

import os
import logging
import random
from dotenv import load_dotenv
from py_mail_me import py_mail_me
from py_mail_me.exceptions import EmailSendError

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class SimulatedError(Exception):
    """Simulated error for demonstration purposes."""
    pass

@py_mail_me(
    email=os.getenv("TEST_EMAIL"),
    subject="Retry and Logging Test",
    attach_logs=True,  # Enable log attachment
    max_retries=3  # Set maximum retry attempts
)
def process_with_potential_errors():
    """Example function that might fail and trigger retries."""
    logger.info("Starting data processing with potential errors...")
    
    # Simulate random failures
    if random.random() < 0.7:  # 70% chance of failure
        logger.error("Encountered an error during processing")
        raise SimulatedError("Simulated failure to demonstrate retry mechanism")
    
    logger.info("Processing completed successfully")
    return "Success"

def main():
    """Main function to demonstrate retry and logging."""
    try:
        logger.info("Starting the example...")
        result = process_with_potential_errors()
        logger.info(f"Process completed with result: {result}")
    except Exception as e:
        logger.error(f"Final error after retries: {e}")
        raise

if __name__ == "__main__":
    main() 