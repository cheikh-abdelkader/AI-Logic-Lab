# db.py
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, inspect
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime

engine = create_engine("sqlite:///quiz.db")
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    matricule = Column(String)
    specialite = Column(String)

class Result(Base):
    __tablename__ = "results"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    score = Column(Float)
    total = Column(Integer)
    date = Column(DateTime, default=datetime.utcnow)

# Check if tables exist and add missing columns
def migrate_database():
    inspector = inspect(engine)
    
    if 'results' in inspector.get_table_names():
        columns = [col['name'] for col in inspector.get_columns('results')]
        if 'user_id' not in columns:
            from sqlalchemy import text
            with engine.connect() as conn:
                conn.execute(text("ALTER TABLE results ADD COLUMN user_id INTEGER"))
                conn.commit()
                print("Added user_id column to results table")

# Create tables if they don't exist
Base.metadata.create_all(engine)

# Run migration
migrate_database()