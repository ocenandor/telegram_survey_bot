import os
from datetime import datetime, timezone

from sqlalchemy import (Boolean, Column, DateTime, ForeignKey, Integer, String,
                        create_engine)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    telegram_id = Column(String, unique=True)
    username = Column(String)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    answers = relationship("Answer", back_populates="user")
    promo_code = relationship("PromoCode", back_populates="user", uselist=False)

class Answer(Base):
    __tablename__ = 'answers'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    question = Column(String)
    answer = Column(String)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    version = Column(Integer, nullable=False)
    
    user = relationship("User", back_populates="answers")

class PromoCode(Base):
    __tablename__ = 'promo_codes'
    id = Column(Integer, primary_key=True)
    code = Column(String, unique=True)
    # is_used = Column(Boolean, default=False)
    used_by_user = Column(Integer, ForeignKey('users.id'), nullable=True)
    issued_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    user = relationship("User", back_populates="promo_code")
