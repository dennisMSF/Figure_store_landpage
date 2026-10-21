from collections.abc import Iterator

from sqlalchemy import event
from sqlmodel import Session, create_engine

from figure_store.config import get_settings

settings = get_settings()
is_sqlite = settings.database_url.startswith("sqlite")
connect_args = {"check_same_thread": False} if is_sqlite else {}
engine = create_engine(url = settings.database_url, connect_args=connect_args)

# --- 2. Activar claves foráneas en SQLite ---------------------------------
@event.listens_for(engine, "connect")
def enable_sqlite_foreign_keys(dbapi_connection, connection_record) -> None:
    
    if not is_sqlite: return
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

# --- 3. Sesión por petición -------------------------------------------------
def get_session() -> Iterator[Session]:
    with Session(engine) as session:
        yield session
        
