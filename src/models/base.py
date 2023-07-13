from db.db import Base
from sqlalchemy import Column, DateTime, Integer, String, func


class Url(Base):
    __tablename__ = "url"
    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, server_default=func.now())
    original_url = Column(String(1024), unique=True)
    use_count = Column(Integer, default=0)

    def __repr__(self):
        return f"Url {self.original_url}"
