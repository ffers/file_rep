import copy

from sqlalchemy import desc, select
from sqlalchemy.orm import Session

from server_flask.models import SourceDifference
from infrastructure import current_project_id

from .base import ScopedRepo


class SourDiffAnRep(ScopedRepo):
    def __init__(self, session: Session):
        super().__init__(session, current_project_id.get())

    def add_source_difference(self, body):
        try:
            add = SourceDifference(
                event_date=body[0],
                source_id=body[1],
                quantity_crm=body[2],
                quantity_stock=body[3],
                difference=body[4],
                project_id=self.project_id,
            )
            self.session.add(add)
            self.session.commit()
            return add
        except Exception:
            return False

    def add_quantity_crm(self, body):
        try:
            add = SourceDifference(
                event_date=body[0],
                source_id=body[1],
                quantity_crm=body[2],
                project_id=self.project_id,
            )
            self.session.add(add)
            self.session.commit()
            return add
        except Exception:
            return False

    def add_diff_comment(self, item_id, comment: str):
        try:
            line = self.load_source_diff_line(item_id)
            line.comment = f"{line.comment} \n {comment}" if line.comment else comment
            self.session.commit()
            return True
        except Exception as e:
            return ValueError(e)

    def load_source_difference(self):
        stmt = select(SourceDifference).where(
            SourceDifference.project_id == self.project_id
        )
        return self.session.scalars(stmt).all()

    def load_source_diff_line(self, item_id):
        return self.get_by_id(SourceDifference, item_id)

    def load_source_difference_period(self, start, stop):
        stmt = (
            select(SourceDifference)
            .where(
                SourceDifference.event_date >= start,
                SourceDifference.event_date <= stop,
                SourceDifference.project_id == self.project_id,
            )
            .order_by(desc(SourceDifference.timestamp))
        )
        return self.session.scalars(stmt).all()

    def load_source_difference_id_period(self, source_id, start, stop):
        stmt = (
            select(SourceDifference)
            .where(
                SourceDifference.event_date >= start,
                SourceDifference.event_date <= stop,
                SourceDifference.source_id == source_id,
                SourceDifference.project_id == self.project_id,
            )
            .order_by(desc(SourceDifference.timestamp))
        )
        return self.session.scalars(stmt).all()

    def load_last_line_id(self, source_id: int):
        stmt = (
            select(SourceDifference)
            .where(
                SourceDifference.source_id == source_id,
                SourceDifference.project_id == self.project_id,
            )
            .order_by(desc(SourceDifference.timestamp))
        )
        return self.session.scalars(stmt).first()

    def update_source_difference(self, source_id, quantity_crm, quantity_stock):
        try:
            stmt = select(SourceDifference).where(
                SourceDifference.source_id == source_id,
                SourceDifference.project_id == self.project_id,
            )
            item = self.session.scalars(stmt).first()
            if not item:
                return False
            item.quantity_crm = quantity_crm
            item.quantity_stock = quantity_stock
            self.session.commit()
            return True
        except Exception:
            return False

    def update_source_diff_line(self, args, item_id):
        try:
            item = self.load_source_diff_line(item_id)
            item.quantity_crm = args[0]
            item.quantity_stock = args[1]
            self.session.commit()
            return True
        except Exception:
            return False

    def update_source_diff_line_sold(self, quantity, item_id):
        try:
            item = self.load_source_diff_line(item_id)
            item.sold = quantity
            self.session.commit()
            return True
        except Exception:
            return False

    def update_diff_sum(self, item_id, quantity):
        try:
            item = self.load_source_diff_line(item_id)
            item.difference = quantity
            self.session.commit()
            return True
        except Exception:
            return False

    def update_diff_table(self, data):
        try:
            for row in data:
                item = self.load_source_diff_line(row[0])
                item.quantity_stock = row[1]
            self.session.commit()
            return True
        except Exception:
            return False

    def update_quantity_crm(self, data):
        try:
            for row in data:
                item = self.load_source_diff_line(row[0])
                item.quantity_crm = row[1]
            self.session.commit()
            return True
        except Exception:
            return False

    def delete_diff_line(self, item_id):
        try:
            item = self.load_source_diff_line(item_id)
            item_copy = copy.deepcopy(item)
            self.session.delete(item)
            self.session.commit()
            return True, item_copy.source_id
        except Exception:
            return False

