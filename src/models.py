from datetime import datetime
from sqlalchemy import Column, String, Numeric, DateTime

from database import Base


class Purchase(Base):
    __tablename__ = "purchases"

    id = Column(String, primary_key=True, index=True)
    price = Column(Numeric(10, 2), nullable=False)
    campaign = Column(String)
    source = Column(String)
    medium = Column(String)

    timestamp = Column(DateTime, insert_default=datetime.now)
