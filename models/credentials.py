
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base, Session
from datetime import datetime
from domain.models.credentials_dto import CredentialsDTO

Base = declarative_base()

class Credentials(Base):
    __tablename__ = "credentials"

    id = Column(Integer, primary_key=True, autoincrement=True)
    path = Column(Integer, nullable=False)
    project_id = Column(Integer, nullable=False)
    marketplace = Column(String, nullable=False)
    store_id = Column(String, nullable=True)
    secret = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dto(self):
        return CredentialsDTO(
            id=self.id,
            path=self.path,
            project_id=self.project_id,
            marketplace=self.marketplace,
            store_id=self.store_id,
            secret=self.secret,
            created_at=self.created_at.isoformat() if self.created_at else None,
            updated_at=self.updated_at.isoformat() if self.updated_at else None,
        )