from server_flask.models import Costumer
from server_flask.db import db
from infrastructure.context import current_project_id



class CostumerRep:
    def __init__(self):
        self.pid = current_project_id.get()

    def create(self, item_new):
        item = Costumer(
            first_name=item_new.first_name,
            last_name=item_new.last_name,
            second_name=item_new.second_name,
            phone=item_new.phone,
            email=item_new.email,
            project_id=self.pid
        )
        db.session.add(item)
        db.session.commit()
        db.session.refresh(item)
        return item
    
    def read_item(self, item_id):
        return Costumer.query.get_or_404(item_id)
    
    def read_by_phone(self, phone):
        phone = phone.replace('+', '')
        return Costumer.query.filter_by(phone=phone).first()

    def update(self, item_id, item_new):
        item = self.read_item(item_id)
        item.first_name=item_new.first_name,
        item.last_name=item_new.last_name,
        item.second_name=item_new.second_name,
        item.phone=item_new.phone,
        item.email=item_new.email
        db.session.commit()
        db.session.refresh(item)
        return item

    def delete(self, item_id):
        item = self.read_item(item_id)
        db.session.delete(item)
        db.session.commit()
        return True

    def read_all(self):
        return Costumer.query.all()
        
    