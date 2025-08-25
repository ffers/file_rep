from sqlalchemy import select

from infrastructure.models import Recipient
from infrastructure.context import current_project_id

from .base import ScopedRepo


class RecipientRep(ScopedRepo):
    def __init__(self, session):
        super().__init__(session, current_project_id.get())

    def create(self, item_new):
        item = Recipient(
            first_name=item_new.first_name,
            last_name=item_new.last_name,
            second_name=item_new.second_name,
            phone=item_new.phone,
            email=item_new.email,
            project_id=self.project_id,
        )
        self.session.add(item)
        self.session.commit()
        self.session.refresh(item)
        return item

    def read_item(self, item_id):
        item = self.session.get(Recipient, item_id)
        if item is None:
            raise ValueError("Recipient not found")
        return item

    def update(self, item_id, item_new):
        item = self.read_item(item_id)
        item.first_name = item_new.first_name
        item.last_name = item_new.last_name
        item.second_name = item_new.second_name
        item.phone = item_new.phone
        item.email = item_new.email
        self.session.commit()
        self.session.refresh(item)
        return item

    def delete(self, item_id):
        item = self.read_item(item_id)
        self.session.delete(item)
        self.session.commit()
        return True

    def read_all(self):
        stmt = select(Recipient)
        return self.session.scalars(stmt).all()

