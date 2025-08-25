from datetime import datetime, timedelta

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from server_flask.models import OrderedProduct, ProductAnalitic, Products
from infrastructure import current_project_id

from .base import ScopedRepo


class ProductAnaliticRep(ScopedRepo):
    def __init__(self, session: Session):
        super().__init__(session, current_project_id.get())

    def body_product_price(self, product_id: int):
        stmt = select(Products.body_product_price).where(
            Products.id == product_id,
            Products.project_id == self.project_id,
        )
        return self.session.scalar(stmt)

    def quantity_product(self, product_id: int):
        stmt = select(Products.quantity).where(
            Products.id == product_id,
            Products.project_id == self.project_id,
        )
        return self.session.scalar(stmt)

    def update_product_analitic(self, product_id: int, money_prod, qty_sale, money_sale):
        stmt = select(ProductAnalitic).where(
            ProductAnalitic.product_id == product_id,
            ProductAnalitic.project_id == self.project_id,
        )
        item = self.session.scalars(stmt).first()
        if not item:
            return False
        item.money_in_product = money_prod
        item.quantity_sale = qty_sale
        item.money_in_sale = money_sale
        self.session.commit()
        return True

    def item_product_analitic(self, product_id: int):
        stmt = select(ProductAnalitic).where(
            ProductAnalitic.product_id == product_id,
            ProductAnalitic.project_id == self.project_id,
        )
        return self.session.scalars(stmt).first()

    def all_product_analitic(self):
        stmt = (
            select(ProductAnalitic)
            .where(ProductAnalitic.project_id == self.project_id)
            .order_by(ProductAnalitic.timestamp.desc())
        )
        return self.session.scalars(stmt).all()

    def add_product_analitic(self, product_id: int):
        prod_analitic = ProductAnalitic(
            product_id=product_id, project_id=self.project_id
        )
        self.session.add(prod_analitic)
        self.session.commit()
        return True

    def search_an_product_id(self, product_id: int):
        return self.item_product_analitic(product_id)

    def get_sum_product_sale(self, product_id: int):
        stmt = select(func.sum(OrderedProduct.quantity)).where(
            OrderedProduct.product_id == product_id,
            OrderedProduct.project_id == self.project_id,
        )
        return self.session.scalar(stmt) or 0

    def get_money_sale_day(self):
        current_time = datetime.now()
        start_time = current_time - timedelta(days=1)
        start_time = start_time.replace(hour=17, minute=0, second=0, microsecond=0)
        stmt = select(func.count(ProductAnalitic.money_in_sale)).where(
            ProductAnalitic.timestamp >= start_time,
            ProductAnalitic.timestamp <= current_time,
            ProductAnalitic.project_id == self.project_id,
        )
        return self.session.scalar(stmt)

    def delete_item(self, item_id: int):
        item = self.get_by_id(ProductAnalitic, item_id)
        if not item:
            return False
        self.session.delete(item)
        self.session.commit()
        return True

    def load_prod_order(self):
        stmt = (
            select(OrderedProduct)
            .where(OrderedProduct.project_id == self.project_id)
            .order_by(OrderedProduct.timestamp.desc())
        )
        return self.session.scalars(stmt).all()

