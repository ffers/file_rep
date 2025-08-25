# repos/base.py
from sqlalchemy.orm import Session

class ScopedRepo:
    def __init__(self, session: Session, project_id: int):
        self.session = session
        self.project_id = project_id

    # універсальний фільтр
    def _scope(self, query, Model):
        return query.filter(Model.project_id == self.project_id)

    # поширені методи
    def get_by_id(self, Model, item_id: int):
        q = self.session.query(Model).filter(Model.id == item_id, Model.project_id == self.project_id)
        return q.first()

    def list_all(self, Model):
        return self._scope(self.session.query(Model), Model).all()
