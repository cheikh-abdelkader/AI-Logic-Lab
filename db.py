# db.py
# db.py

from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, inspect, text
from sqlalchemy.orm import declarative_base, sessionmaker, scoped_session
from datetime import datetime

# =========================
# ENGINE (SQLite optimisé concurrence)
# =========================
engine = create_engine(
    "sqlite:///quiz.db",
    connect_args={"check_same_thread": False},  # autorise multi-threads
    pool_size=20,
    max_overflow=0,
    future=True
)

# =========================
# SESSION (thread-safe)
# =========================
SessionLocal = scoped_session(
    sessionmaker(
        bind=engine,
        autocommit=False,
        autoflush=False
    )
)

# =========================
# BASE
# =========================
Base = declarative_base()

# =========================
# MODELS
# =========================
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    matricule = Column(String, nullable=False)
    specialite = Column(String, nullable=False)


class Result(Base):
    __tablename__ = "results"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    score = Column(Float, nullable=False)
    total = Column(Integer, nullable=False)
    date = Column(DateTime, default=datetime.utcnow)


# =========================
# DATABASE INIT (WAL mode)
# =========================
def init_db():
    Base.metadata.create_all(bind=engine)

    # Activer WAL pour meilleure concurrence
    with engine.connect() as conn:
        conn.execute(text("PRAGMA journal_mode=WAL;"))
        conn.execute(text("PRAGMA synchronous=NORMAL;"))


# =========================
# MIGRATION SIMPLE
# =========================
def migrate_database():
    inspector = inspect(engine)

    # Vérifier table results
    if "results" in inspector.get_table_names():
        columns = [col["name"] for col in inspector.get_columns("results")]

        if "user_id" not in columns:
            with engine.connect() as conn:
                conn.execute(text("ALTER TABLE results ADD COLUMN user_id INTEGER"))
                conn.commit()
                print("✅ Added user_id column")


# =========================
# GET DB (SAFE USAGE)
# =========================
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# =========================
# INIT ON LOAD
# =========================
init_db()
migrate_database()
# from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, inspect
# from sqlalchemy.orm import declarative_base, sessionmaker
# from datetime import datetime

# engine = create_engine("sqlite:///quiz.db")
# SessionLocal = sessionmaker(bind=engine)
# Base = declarative_base()

# class User(Base):
#     __tablename__ = "users"
#     id = Column(Integer, primary_key=True)
#     name = Column(String)
#     matricule = Column(String)
#     specialite = Column(String)

# class Result(Base):
#     __tablename__ = "results"
#     id = Column(Integer, primary_key=True)
#     user_id = Column(Integer)
#     score = Column(Float)
#     total = Column(Integer)
#     date = Column(DateTime, default=datetime.utcnow)

# # Check if tables exist and add missing columns
# def migrate_database():
#     inspector = inspect(engine)
    
#     if 'results' in inspector.get_table_names():
#         columns = [col['name'] for col in inspector.get_columns('results')]
#         if 'user_id' not in columns:
#             from sqlalchemy import text
#             with engine.connect() as conn:
#                 conn.execute(text("ALTER TABLE results ADD COLUMN user_id INTEGER"))
#                 conn.commit()
#                 print("Added user_id column to results table")

# # Create tables if they don't exist
# Base.metadata.create_all(engine)

# # Run migration
# migrate_database()