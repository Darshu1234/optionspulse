from sqlalchemy import Column, Integer, Float, String, DateTime
from backend.database import Base

class PricingHistory(Base):
    __tablename__ = "pricing_history"
    id = Column(Integer, primary_key = True)
    ticker = Column(String)
    s = Column(Float)
    k = Column(Float)
    r = Column(Float)
    sigma = Column(Float)
    t = Column(Float)
    option_type = Column(String)
    option_style = Column(String)
    price = Column(Float)
    created_at = Column(DateTime)


class SavedPosition(Base):
    __tablename__ = "saved_positions"
    id = Column(Integer, primary_key = True)
    ticker = Column(String)
    s = Column(Float)
    k = Column(Float)
    r = Column(Float)
    sigma = Column(Float)
    t = Column(Float)
    option_type = Column(String)
    option_style = Column(String)
    price = Column(Float)
    delta = Column(Float)
    gamma = Column(Float)
    vega = Column(Float)
    theta = Column(Float)
    rho = Column(Float)
    created_at = Column(DateTime)


