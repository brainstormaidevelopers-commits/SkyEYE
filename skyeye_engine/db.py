from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, JSON, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from skyeye_engine.config import Config

Base = declarative_base()

class DBManager:
    def __init__(self):
        # We replace postgresql:// with postgresql+psycopg2:// for SQLAlchemy if needed
        db_url = Config.DATABASE_URL
        if db_url.startswith("postgresql://"):
            db_url = db_url.replace("postgresql://", "postgresql+psycopg2://", 1)
        
        self.engine = create_engine(db_url)
        self.Session = sessionmaker(bind=self.engine)

    def init_db(self):
        Base.metadata.create_all(self.engine)

class EventModel(Base):
    __tablename__ = 'events'
    id = Column(Integer, primary_key=True)
    external_id = Column(String(255), unique=True)
    title = Column(String(255))
    description = Column(Text)
    lat = Column(Float)
    lon = Column(Float)
    score = Column(Float)
    category = Column(String(50))
    timestamp = Column(DateTime, default=datetime.utcnow)
    data = Column(JSON) # Store raw signals

class ReconstructionModel(Base):
    __tablename__ = 'reconstructions'
    id = Column(Integer, primary_key=True)
    lat = Column(Float)
    lon = Column(Float)
    base_timestamp = Column(DateTime)
    last_sync = Column(DateTime)
    sensors = Column(JSON)
    physics_score = Column(Float)
    ontology = Column(String(100))
    path_to_tiles = Column(String(512)) # S3 or local path

class LogModel(Base):
    __tablename__ = 'system_logs'
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    category = Column(String(50))
    message = Column(Text)
    data = Column(JSON)

# Singleton instance
db_manager = DBManager()
