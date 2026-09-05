from agno.db.sqlite import SqliteDb

from config.settings import SQLITE_DIR

SQLITE_DIR.mkdir(
    parents=True,
    exist_ok=True
)

def get_sqlite():

    return SqliteDb(
        session_table="agent_session",
        db_file=str(SQLITE_DIR / "agent.db")
    )