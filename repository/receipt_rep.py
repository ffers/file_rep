from sqlalchemy import select
from sqlalchemy.orm import Session

from infrastructure.models import Receipt, Shift
from DTO import ReceiptDTO, ShiftDTO
from infrastructure import current_project_id

from .base import ScopedRepo


class ReceiptRep(ScopedRepo):
    def __init__(self, session: Session):
        super().__init__(session, current_project_id.get())

    def add(self, d: ReceiptDTO):
        try:
            item = Receipt(d)
            item.project_id = self.project_id
            self.session.add(item)
            self.session.commit()
            return True
        except Exception as e:
            return False, str(e)

    def update(self):
        pass

    def delete(self):
        pass


class ShiftRep(ScopedRepo):
    def __init__(self, session: Session):
        super().__init__(session, current_project_id.get())

    def add(self, d: ShiftDTO):
        try:
            item = Shift(d)
            item.project_id = self.project_id
            self.session.add(item)
            self.session.commit()
            return True
        except Exception as e:
            return False, str(e)

    def update(self, d: ShiftDTO):
        stmt = select(Shift).where(
            Shift.shift_id == d.shift_id, Shift.project_id == self.project_id
        )
        load = self.session.scalars(stmt).first()
        if not load:
            return False
        item = Shift(d)
        item.id = load.id
        item.project_id = self.project_id
        self.session.merge(item)
        self.session.commit()
        return True

    def delete(self):
        pass

    def load_shift_date_token(self, date):
        stmt = select(Shift).where(
            Shift.timestamp == date, Shift.project_id == self.project_id
        )
        token = self.session.scalars(stmt).first()
        return token.checkbox_access_token if token else None

    def load_shift_open(self, date):
        stmt = select(Shift).where(
            Shift.closed == None, Shift.project_id == self.project_id
        )
        return self.session.scalars(stmt).all()

