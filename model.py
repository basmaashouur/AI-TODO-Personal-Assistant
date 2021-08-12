import os
import sys
import datetime
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class Todo(Base):
    __tablename__ = 'todo'

    id = Column(Integer, primary_key=True)
    text = Column(String(200), nullable=False)
    complete = Column(Boolean, nullable=True)
    created_at = Column(DateTime, nullable=True)
  

engine = create_engine('sqlite:///rctrl.db')


Base.metadata.create_all(engine)