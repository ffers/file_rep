from sqlalchemy import desc, select
from sqlalchemy.orm import Session

from server_flask.models import JournalChange
from infrastructure.context import current_project_id

from .base import ScopedRepo


class JourChRep(ScopedRepo):
    def __init__(self, session: Session):
        super().__init__(session, current_project_id.get())

    def load_all(self):
        stmt = (
            select(JournalChange)
            .where(JournalChange.project_id == self.project_id)
            .order_by(desc(JournalChange.timestamp))
        )
        return self.session.scalars(stmt).all()

    def load_article(self, article):
        stmt = select(JournalChange).where(
            JournalChange.article == article,
            JournalChange.project_id == self.project_id,
        )
        return self.session.scalars(stmt).first()

    def add_(self, data):
        try:
            item = JournalChange(
                status=data[0],
                quantity=data[1],
                body=data[2],
                product_id=data[3],
                quantity_stock=data[4],
                event_date=data[5],
                project_id=self.project_id,
            )
            self.session.add(item)
            self.session.commit()
            return True
        except Exception as e:
            return False, e

    def update_(self, item_id, data):
        item = self.get_by_id(JournalChange, item_id)
        if not item:
            return False
        item.article = data[0]
        item.name = data[1]
        item.price = data[2]
        item.quantity = data[3]
        item.money = data[4]
        self.session.commit()
        return True

    def update_quan(self, item_id, quantity):
        item = self.get_by_id(JournalChange, item_id)
        if not item:
            return False
        item.quantity = quantity
        self.session.commit()
        return True

    def delete_(self, item_id):
        item = self.get_by_id(JournalChange, item_id)
        if not item:
            return False
        self.session.delete(item)
        self.session.commit()
        return True

