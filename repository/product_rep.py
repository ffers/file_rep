from dataclasses import dataclass

from sqlalchemy import select
from sqlalchemy.orm import Session

from infrastructure.models import ProductAnalitic, ProductRelate, Products
from utils import OC_logger
from infrastructure import current_project_id

from .base import ScopedRepo


@dataclass
class ProductRelateDTO:
    id: int
    product_id: int
    quantity: int
    product_source_id: int


class ProductRep(ScopedRepo):
    def __init__(self, session: Session):
        super().__init__(session, current_project_id.get())
        self.log = OC_logger.oc_log("prod_rep")

    def add_product(self, description, article, product_name, price, quantity):
        try:
            product = Products(
                description=description,
                article=article,
                product_name=product_name,
                price=price,
                quantity=quantity,
                project_id=self.project_id,
            )
            self.session.add(product)
            self.session.commit()
            add_analitic = ProductAnalitic(product_id=product.id)
            self.session.add(add_analitic)
            self.session.commit()
            return True
        except Exception:
            return False

    def create_v2(self, article, product_name):
        product = Products(article=article, product_name=product_name, project_id=self.project_id)
        self.session.add(product)
        self.session.commit()
        return product

    def add_product_relate(self, data_list):
        try:
            item = ProductRelate(
                article=data_list[0],
                product_source_id=data_list[0],
                name="",
                quantity=int(data_list[1]),
                product_id=data_list[2],
            )
            self.session.add(item)
            self.session.commit()
            return True
        except Exception:
            return False

    def update_v2(self, item_id, article, product_name):
        product = self.get_by_id(Products, item_id)
        if not product:
            return False
        product.article = article
        product.product_name = product_name
        self.session.commit()
        return product

    def update_product_item(self, data, item_id):
        product = self.get_by_id(Products, item_id)
        if not product:
            return False
        product.article = data[0]
        product.product_name = data[1]
        self.session.commit()
        return True

    def update_after_arrival(self, combined_list):
        for datetime_new, product_id, quantity, price, total in combined_list:
            product = self.get_by_id(Products, product_id)
            if product:
                product.quantity = quantity + product.quantity
                product.body_product_price = price
        self.session.commit()
        return True

    def delete_product(self, item_id):
        product = self.get_by_id(Products, item_id)
        if not product:
            return False
        self.session.delete(product)
        self.session.commit()
        return True

    def changeBodyPrice(self):
        for item in self.load_product_all():
            if not item.body_product_price:
                item.body_product_price = 0
        self.session.commit()

    def update_product_relate(self, data, item_id):
        product = self.get_by_id(ProductRelate, item_id)
        if not product:
            return False
        product.article = data[0]
        product.quantity = data[1]
        product.product_id = data[2]
        product.product_source_id = data[0]
        self.session.commit()
        return True

    def load_product_all(self):
        stmt = select(Products).where(Products.project_id == self.project_id).order_by(Products.timestamp)
        return self.session.scalars(stmt).all()

    def load_product_item(self, product_id):
        return self.get_by_id(Products, product_id)

    def load_product_by_id(self, product_id):
        return self.get_by_id(Products, product_id)

    def load_by_article(self, art):
        stmt = select(Products).where(
            Products.article == art, Products.project_id == self.project_id
        )
        return self.session.scalars(stmt).first()

    def load_product_relate(self):
        stmt = select(ProductRelate).order_by(ProductRelate.timestamp)
        return self.session.scalars(stmt).all()

    def load_product_relate_item(self, product_id):
        return self.get_by_id(ProductRelate, product_id)

    def load_prod_relate_product_id(self, item_id):
        stmt = select(ProductRelate).where(ProductRelate.product_id == item_id)
        return self.session.scalars(stmt).first()

    def load_prod_relate_product_id_all(self, item_id):
        stmt = select(ProductRelate).where(ProductRelate.product_id == item_id)
        items = self.session.scalars(stmt).all()
        return [
            ProductRelateDTO(i.id, i.product_id, i.quantity, i.product_source_id)
            for i in items
        ]

    def delete_product_relate(self, item_id):
        item = self.get_by_id(ProductRelate, item_id)
        if not item:
            return False
        self.session.delete(item)
        self.session.commit()
        return True

