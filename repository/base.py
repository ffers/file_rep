# repos/base.py
from sqlalchemy import select
from sqlalchemy.orm import Session

class ScopedRepo:
    def __init__(self, session: Session, project_id: int):
        self.session = session
        self.project_id = project_id

    # універсальний фільтр
    def _scope(self, stmt, Model):
        return stmt.where(Model.project_id == self.project_id)

    # поширені методи
    def get_by_id(self, Model, item_id: int):
        stmt = select(Model).where(Model.id == item_id, Model.project_id == self.project_id)
        return self.session.execute(stmt).scalar_one_or_none()

    def list_all(self, Model):
        stmt = self._scope(select(Model), Model)
        return self.session.execute(stmt).scalars().all()
