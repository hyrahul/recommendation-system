from sqlalchemy import Column, BigInteger, String, DateTime, CheckConstraint
from sqlalchemy.sql import func
from app.db.base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True)
    username = Column(String(100), nullable=False, unique=True)
    full_name = Column(String(200), nullable=False)
    affiliation = Column(String(50), nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=func.now())

    __table_args__ = (
        CheckConstraint(
            "affiliation IN ('Korea', 'USA', 'China')",
            name="chk_user_affiliation"
        ),
    )

    def __repr__(self) -> str:
        return f"<User id={self.id} username={self.username} affiliation={self.affiliation}>"
