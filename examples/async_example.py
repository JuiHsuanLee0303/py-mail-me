"""
Example of using async mode with py-mail-me.
"""

import os
import asyncio
import logging
from dotenv import load_dotenv
from py_mail_me import py_mail_me

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

@py_mail_me(
    email=os.getenv("TEST_EMAIL"),
    subject="Async Task Notification",
    attach_logs=True,
    async_mode=True  # Enable async mode
)
async def process_data_async(task_id: int):
    """Example async function that processes data."""
    logger.info(f"Starting async task {task_id}...")
    
    # Simulate some async work
    await asyncio.sleep(2)
    
    logger.info(f"Task {task_id} completed!")
    return f"Result from task {task_id}"

async def run_multiple_tasks():
    """Run multiple async tasks concurrently."""
    logger.info("Starting multiple async tasks...")
    
    tasks = []
    for i in range(3):
        task = process_data_async(i)
        tasks.append(task)
    
    # Wait for all tasks to complete
    results = await asyncio.gather(*tasks)
    logger.info(f"All tasks completed with results: {results}")

if __name__ == "__main__":
    # Run the async tasks
    asyncio.run(run_multiple_tasks()) 