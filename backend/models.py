from sqlalchemy import Column, Integer, String
from database import Base

class Feedback(Base):
    __tablename__ = "feedback"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    event = Column(String)
    rating = Column(Integer)
    comment = Column(String)
    sentiment = Column(String)
    keywords = Column(String)