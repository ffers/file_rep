


from domain.models.credentials_dto import CredentialsDTO
from infrastructure.models.credentials import Credentials
from sqlalchemy.orm import Session

class CredentialsSQLAlchemy:
    def __init__(self, session: Session):
        self.db = session

    def create(self, dto: CredentialsDTO) -> CredentialsDTO:
        cred = Credentials(
            path=dto.path,
            project_id=dto.project_id,
            marketplace=dto.marketplace,
            store_id=dto.store_id,
            secret=dto.secret,
        )
        self.db.add(cred)
        self.db.commit()
        self.db.refresh(cred)
        return cred.to_dto()
    
    def read(self, marketplace, store_id):
        pass
    
    def get_path(self, marketplace, store_id):
        cred = self.db.query(Credentials).filter(
                Credentials.marketplace == marketplace,
                Credentials.store_id == store_id
            ).first()
        return cred.path if cred else None
    
    def get_by_id(self, credentials_id: int) -> CredentialsDTO | None:
        cred = self.db.query(Credentials).filter(Credentials.id == credentials_id).first()
        return cred.to_dto() if cred else None

    def list(self) -> list[CredentialsDTO]:
        creds = self.db.query(Credentials).all()
        return [c.to_dto() for c in creds]

    def update(self, credentials_id: int, dto: CredentialsDTO) -> CredentialsDTO | None:
        cred = self.db.query(Credentials).filter(Credentials.id == credentials_id).first()
        if not cred:
            return None
        for field, value in dto.model_dump(exclude_unset=True).items():
            if hasattr(cred, field) and value is not None:
                setattr(cred, field, value)
        self.db.commit()
        self.db.refresh(cred)
        return cred.to_dto()

    def delete(self, credentials_id: int) -> bool:
        cred = self.db.query(Credentials).filter(Credentials.id == credentials_id).first()
        if not cred:
            return False
        self.db.delete(cred)
        self.db.commit()
        return True