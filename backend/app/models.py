from sqlalchemy import create_engine, Column, String, DateTime, JSON, text, Integer
from sqlalchemy.dialects.postgresql import UUID, ARRAY, FLOAT
from sqlalchemy.orm import declarative_base, sessionmaker
from pgvector.sqlalchemy import Vector
import uuid
from datetime import datetime, timezone

Base = declarative_base()


class IssueModel(Base):
    """SQLAlchemy model for Issues with Vector support."""

    __tablename__ = "issues"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String, nullable=False, unique=True)
    content = Column(String, nullable=False)
    solution = Column(String, nullable=False)
    tags = Column(ARRAY(String), default=[])
    metadata_ = Column("metadata", JSON, default={})
    created_at = Column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    # Metrics
    view_count = Column(Integer, default=0)
    useful_count = Column(Integer, default=0)

    # 384 dimensions for all-MiniLM-L6-v2
    embedding = Column(Vector(384))
