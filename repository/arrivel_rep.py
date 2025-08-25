from sqlalchemy import select

from infrastructure.models import Arrival
from infrastructure.context import current_project_id

from .base import ScopedRepo


class ArrivalRep(ScopedRepo):
    def __init__(self, session):
        super().__init__(session, current_project_id.get())

    def add_arrival(self, combined_list):
        for datetime_new, product_id, quantity, price, total in combined_list:
            arrival = Arrival(
                product_id=product_id,
                body_price=price,
                quantity=quantity,
                total_price=total,
                datetime_new=datetime_new,
                project_id=self.project_id,
            )
            self.session.add(arrival)
        self.session.commit()
        return True

    def load_arrival(self):
        stmt = select(Arrival).order_by(Arrival.timestamp)
        return self.session.scalars(stmt).all()

