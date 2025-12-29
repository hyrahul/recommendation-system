from sqlalchemy import Column, BigInteger, String, DateTime, CheckConstraint
from sqlalchemy.sql import func
from app.db.base import Base

class Category(Base):
    __tablename__ = "categories"

    id = Column(BigInteger, primary_key=True)
    name = Column(String(200), nullable=False, unique=True)
    visibility = Column(String(50), nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=func.now())

    __table_args__ = (
        CheckConstraint(
            "visibility IN ('Korea', 'USA', 'China', 'OverseasCommon')",
            name="chk_category_visibility"
        ),
    )

    def __repr__(self) -> str:
        return f"<Category id={self.id} name={self.name} visibility={self.visibility}>"
