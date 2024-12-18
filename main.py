import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    from app.bot.RunBot import run_bot
    run_bot()

if __name__ == "__main__":
    main()
