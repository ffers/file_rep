from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from psycopg2.errors import UniqueViolation

from infrastructure.models import ProductSource
from infrastructure.context import current_project_id
from utils import OC_logger

class SourceRep:
    def __init__(self, session: Session):
        self.session = session
        self.logger = OC_logger.oc_log("source")
        self.pid = current_project_id.get()

    def create_v2(self, data):
        try:
            item = ProductSource(
                article=data[0],
                name=data[1],
                price=data[2],
                quantity=data[3],
                money=data[4]
            )
            self.session.add(item)
            self.session.commit()
            return item
        except IntegrityError as e:
            assert isinstance(e.orig, UniqueViolation)
            raise ValueError('Артікул вже використовується')
        except Exception as e:
            self.logger.error("Помилка при створенні джерела", exc_info=True)
            raise ValueError('Джерело не створено!') 


    def load_all(self):
        try:
            stmt = select(ProductSource).order_by(ProductSource.timestamp)
            return self.session.execute(stmt).scalars().all()
        except Exception as e:
            self.logger.exception(f'load_all: {e}')
            raise


    def load_article(self, article):
        try:
            stmt = select(ProductSource).where(ProductSource.article == article)
            return self.session.execute(stmt).scalar_one_or_none()
        except Exception:
            self.session.rollback()
            return False

    def load_id(self, id):
        try:
            stmt = select(ProductSource).where(ProductSource.id == id)
            return self.session.execute(stmt).scalar_one_or_none()
        except Exception as e:
            return False, e

    def update_source(self, id, data):
        try:
            product = self.session.get(ProductSource, id)
            if not product:
                return False, ValueError("Item not found")
            product.article = data[0]
            product.name = data[1]
            product.price = data[2]
            product.quantity = data[3]
            product.money = data[4]
            self.session.commit()
            return True
        except Exception as e:
            self.session.rollback()
            return False, e


    def update_quantity(self, id, quantity):
        try:
            product = self.session.get(ProductSource, id)
            if not product:
                return False, ValueError("Item not found")
            product.quantity = quantity
            self.session.commit()
            return True
        except Exception as e:
            self.session.rollback()
            return False, e


    def delete_(self, id):
        try:
            task_to_delete = self.session.get(ProductSource, id)
            if not task_to_delete:
                return False, ValueError("Item not found")
            self.session.delete(task_to_delete)
            self.session.commit()
            return True
        except Exception as e:
            return False, e

    def load_item(self, product_id):
        return self.session.get(ProductSource, product_id)

 
    def add_product_source(self, data_list):
        try:
            item = ProductSource(
                article=data_list[0],
                name=data_list[1],
                price=data_list[2],
                quantity=data_list[3],
                money=data_list[4]
            )
            self.session.add(item)
            self.session.commit()
            return True
        except Exception as e:
            return False, e

    def delete_product_source(self, id):
        try:
            task_to_delete = self.session.get(ProductSource, id)
            if not task_to_delete:
                return False, ValueError("Item not found")
            self.session.delete(task_to_delete)
            self.session.commit()
            return True
        except Exception as e:
            return False, e
    