import logging
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.engine import Engine
from tenacity import after_log, before_log, retry, stop_after_attempt, wait_fixed

from app.database.session import engine

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

max_tries = 60 * 5  # 5 minutes
wait_seconds = 1


@retry(
    stop=stop_after_attempt(max_tries),
    wait=wait_fixed(wait_seconds),
    before=before_log(logger, logging.INFO),
    after=after_log(logger, logging.WARN),
)
def init(db_engine: Engine) -> None:
    try:
        with Session(db_engine) as session:
            session.execute(select(1))
    except Exception as e:
        logger.error("Database connection failed: %s", e)
        raise e


def main() -> None:
    logger.info("🔧 Initializing service (DB connection test)")
    init(engine)
    logger.info("✅ Service finished initializing")


if __name__ == "__main__":
    main()
