from sqlalchemy import Column, Integer, String, DateTime, Index
from db.engine import Base


class User(Base):
    __tablename__ = "users"
    __table_args__ = (
        Index(
            'ix_users_name', 'name',
            postgresql_ops={'name': 'varchar_pattern_ops'},
            ),
        Index(
            'ix_users_surname', 'surname',
            postgresql_ops={'surname': 'varchar_pattern_ops'},
            ),
        Index(
            'ix_users_patronymic', 'patronymic',
            postgresql_ops={'patronymic': 'varchar_pattern_ops'},
            ),
        )

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(511))
    surname = Column(String(511))
    patronymic = Column(String(511))
    email = Column(String(511), unique=True, index=True)
    password = Column(String(511))
    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True), nullable=False)
