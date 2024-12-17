from app.bot import run_bot
import logging


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)
logger = logging.getLogger(__name__)


try:
    run_bot()
except Exception as e:
    logger.error(f'Error occurred: {e}', exc_info=True)