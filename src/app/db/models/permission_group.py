from sqlalchemy import Column, BigInteger, String
from app.db.base import Base


class PermissionGroup(Base):
    __tablename__ = "permission_group"

    permission_grp_id = Column(
        BigInteger,
        primary_key=True,
        autoincrement=True
    )

    name = Column(String(100), nullable=False)

    def __repr__(self) -> str:
        return f"<PermissionGroup id={self.permission_grp_id} name={self.name}>"
