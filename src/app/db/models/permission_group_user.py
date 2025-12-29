from sqlalchemy import Column, BigInteger, ForeignKey
from app.db.base import Base


class PermissionGroupUser(Base):
    __tablename__ = "permission_group_user"

    permission_grp_id = Column(
        BigInteger,
        ForeignKey("permission_group.permission_grp_id", ondelete="CASCADE"),
        primary_key=True
    )

    user_id = Column(
        BigInteger,
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True
    )

    def __repr__(self) -> str:
        return (
            f"<PermissionGroupUser "
            f"permission_grp_id={self.permission_grp_id} "
            f"user_id={self.user_id}>"
        )
