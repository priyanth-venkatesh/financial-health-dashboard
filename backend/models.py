from sqlalchemy import Column, Integer, String, Float, ForeignKey, Text
from sqlalchemy.orm import relationship
from database import Base




class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)

class FinancialRecord(Base):
    __tablename__ = "financial_records"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    revenue = Column(Float)
    expenses = Column(Float)
    debt = Column(Float)
    cash = Column(Float)
    user = relationship("User")

class Insight(Base):
    __tablename__ = "insights"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    summary = Column(Text)