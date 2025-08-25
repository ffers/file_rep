from server_flask.db import db
from server_flask.models import (Products,
                                 ProductAnalitic,
                                 ProductRelate,
                                 ProductSource)
from utils import OC_logger
from dataclasses import dataclass
from infrastructure import current_project_id

@dataclass
class ProductRelateDTO:
    id: int
    product_id: int 
    quantity: int
    product_source_id: int

class ProductRep():
    def __init__(self):
        self.log = OC_logger.oc_log('prod_rep')
        self.pid = current_project_id.get()

    def add_product(self, description, article, product_name, price, quantity):
        try:
            product = Products(description=description,
                            article=article,
                            product_name=product_name,
                            price=price,
                            quantity=quantity,
                            project_id=self.pid)
            db.session.add(product)
            db.session.commit()
            add_analitic = ProductAnalitic(product_id=product.id)
            db.session.add(add_analitic)
            db.session.commit()
            return True
        except:
            return False
    
    def create_v2(self, article, product_name):
        try:
            product = Products(
                        article=article,
                        product_name=product_name
                    )
            db.session.add(product)
            db.session.commit()
            return product
        except Exception as e:
            self.log.exception(f'create_v2: {e}')
            raise
        
    def add_product_relate(self, data_list):
        try:
            item = ProductRelate(
                article=data_list[0], # надо поменять - ето id исходника
                product_source_id=data_list[0],
                name="",
                quantity=int(data_list[1]),
                product_id=data_list[2],
            )
            db.session.add(item)
            db.session.commit()
            db.session.close()
            return True
        except:
            return False
        
    def update_v2(self, id, *args):
        try:
            product = Products.query.get_or_404(id)
            print(id, args)
            product.article = args[0]
            product.product_name = args[1]
            db.session.commit()
            return product
        except:
            return False
 

    def update_product_item(self, data, id):
        try:
            product = Products.query.get_or_404(id)
            print(id, product.id, product.product_name, product.article)
            product.article = data[0]
            product.product_name = data[1]
            db.session.commit()
            return True
        except:
            return False
                  
                                  
    def update_after_arrival(self, combined_list):
        for item in combined_list:
            datetime_new, product_id, quantity, price, total = item
            product = Products.query.get_or_404(product_id)
            product.quantity = quantity + product.quantity
            product.body_product_price = price
            db.session.commit()
        return True
         
    def delete_product(self, id):
        task_to_delete = Products.query.get_or_404(id)
        print(">>> Start delete in datebase")
        db.session.delete(task_to_delete)
        db.session.commit()
        print(">>> Delete in datebase")
        return True

    def changeBodyPrice(self):
        products = self.load_product_all()
        for item in products:
            if not item.body_product_price:
                item.body_product_price = 0

    def update_product_relate(self, data, id):
        try:
            product = ProductRelate.query.get_or_404(id)

            print(f"артикил {data}")
            product.article = data[0]
            product.quantity = data[1],
            product.product_id = data[2]
            product.product_source_id = data[0]
            db.session.commit()
            return True
        except:
            return False

    def load_product_all(self):
        products = Products.query.order_by(Products.timestamp).all()
        return products

    def load_product_item(self, product_id):
        product = Products.query.get_or_404(product_id)
        return product
    
    def load_product_by_id(self, product_id):
        product = Products.query.get_or_404(product_id)
        return product
    
    def load_by_article(self, art):
        try:
            product = Products.query.filter_by(article=art).first()
            return product
        except:
            return False

    def load_product_relate(self):
        products = ProductRelate.query.order_by(ProductRelate.timestamp).all()
        return products

    def load_product_relate_item(self, product_id):
        item = ProductRelate.query.get_or_404(product_id) 
        return item

    def load_prod_relate_product_id(self, id):
        item = ProductRelate.query.filter_by(product_id=id).first()
        return item

    def load_prod_relate_product_id_all(self, id):
        items = ProductRelate.query.filter_by(product_id=id).all()
        select = []
        for i in items:
            select.append(
                ProductRelateDTO(
                i.id, i.product_id, i.quantity, i.product_source_id
            ))
        return select


    def delete_product_relate(self, id):
        task_to_delete = ProductRelate.query.get_or_404(id)
        print(">>> Start delete in datebase")
        db.session.delete(task_to_delete)
        db.session.commit()
        print(">>> Delete in datebase")
        return True






prod_rep = ProductRep()



