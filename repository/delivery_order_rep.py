from sqlalchemy import select
from sqlalchemy.orm import Session

from infrastructure.models import DeliveryOrder
from infrastructure.context import current_project_id

from .base import ScopedRepo


class DeliveryOrderRep(ScopedRepo):
    def __init__(self, session: Session):
        super().__init__(session, current_project_id.get())

    def add_item(self, order_id, status):
        item = DeliveryOrder(
            number_ttn="-",
            ref_ttn="-",
            number_registr="-",
            order_id=order_id,
            status_id=status,
            project_id=self.project_id,
        )
        self.session.add(item)
        self.session.commit()
        return True

    def load_item(self, order_id):
        stmt = select(DeliveryOrder).where(
            DeliveryOrder.order_id == order_id,
            DeliveryOrder.project_id == self.project_id,
        )
        return self.session.scalars(stmt).first()

    def update_ttn(self, order_id, data):
        order = self.load_item(order_id)
        if not order:
            self.add_item(order_id, 1)
            order = self.load_item(order_id)
        order.ref_ttn = data["ref_ttn"]
        order.number_ttn = data["number_ttn"]
        self.session.commit()
        return True

    def update_registr(self, items, data):
        for order_id in items:
            item = self.load_item(order_id)
            item.ref_registr = data["ref_registr"]
            item.number_registr = data["number_registr"]
        self.session.commit()
        return True

    def reg_delete_in_item(self, items):
        for order_id in items:
            v = self.load_item(order_id)
            v.ref_registr = ""
            v.number_registr = ""
        self.session.commit()
        return True

    def load_item_filter_order(self, data):
        order_list = []
        for order_id in data:
            stmt = select(DeliveryOrder).where(
                DeliveryOrder.order_id == int(order_id),
                DeliveryOrder.project_id == self.project_id,
            )
            order_list.append(self.session.scalars(stmt).first())
        return order_list

    def load_order_for_ref(self, number_ttn):
        stmt = select(DeliveryOrder).where(
            DeliveryOrder.number_ttn == number_ttn,
            DeliveryOrder.project_id == self.project_id,
        )
        return self.session.scalars(stmt).first()

    def load_registred(self):
        stmt = (
            select(DeliveryOrder)
            .join(DeliveryOrder.orders)
            .where(
                DeliveryOrder.orders.ordered_status_id == 11,
                DeliveryOrder.orders.delivery_method_id == 1,
                DeliveryOrder.project_id == self.project_id,
            )
        )
        return self.session.scalars(stmt).all()

