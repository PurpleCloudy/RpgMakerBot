from sqlalchemy import create_engine, Column, Integer, BigInteger, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os

DATABASE_URL = os.getenv('DB_URL')

engine = create_engine(DATABASE_URL, echo=False)
Base = declarative_base()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class KillsSaver(Base):
    __tablename__ = 'kills'

    id = Column(Integer, primary_key=True, index=True)
    player_id = Column(BigInteger, nullable=False, index=True)
    time = Column(DateTime(timezone=True), default=datetime.utcnow)
    mob_type = Column(String(10), nullable=False)

    def __str__(self):
        return f'Ты убил {self.mob_type} монстра в {self.time}'

    def __repr__(self):
        return f'id {self.id}; player_id {self.player_id}; time {self.time}; type {self.mob_type}'


Base.metadata.create_all(bind=engine)
