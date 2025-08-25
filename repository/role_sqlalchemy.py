

from server_flask.models import Role as SQLItem
from domain.repositories.role_repo import ItemRepository
from domain.models.role_dto import RoleDTO as DTO
from infrastructure.context import current_project_id, current_user_id
from utils.exception import RoleNotExist


class RoleSqlAlchemy(ItemRepository):
    def __init__(self, session): 
        self.uid = current_user_id.get()
        self.pid = current_project_id.get()
        self.session = session

    def get_all(self):
        items = SQLItem.query.filter_by(user_id=self.uid).all()
        dtos = []
        for i in items:
            dto = DTO(
                id=i.id,
                email=i.email,
                username=i.username
            )
            # DTO(
            #     id=item.id,   
            #     event_date=item.event_date,
            #     desription=item.desription,
            #     body=item.body,
            #     income=item.income,
            #     balance_id=item.balance_id
            # )
            dtos.append(dto)

        return dtos
    
    def get_all_select(self):
        items = self.get_all() 
        store_select = []
        for i in items:
            dto = {
                'id': i.id,
                'name': i.name
            }
            store_select.append(dto)

        return store_select
    
    def get_item(self, item_id):
        try:
            i = SQLItem.query.filter_by(id=item_id).first()
            return DTO(
                id=i.id,
                email=i.email,
                username=i.username
            )
        except Exception as e:

            print(f"get_item ПОМИлка репо прожект {e}")
            raise


            

    def add(self, item: DTO):
        sql_item = SQLItem(
            username=item.username, 
            email=item.email,
            password=item.password
            )
        self.session.add(sql_item)
        self.session.commit()
        self.session.refresh(sql_item)
        return sql_item

    def update(self, item: DTO):
        i = SQLItem.query.get_or_404(item.id)
        i.name = item.name
        i.email = item.email
        self.session.commit()

    def delete(self, item_id):
        i = SQLItem.query.get_or_404(item_id)
        self.session.delete(i)
        self.session.commit()

    def get_by_user_id(self):
        try:
            i = SQLItem.query.get_or_404(self.uid)
            return DTO(
                id=i.id,
                email=i.email,
                username=i.username
            )
        except Exception as e:
            print(f"ПОМИлка get_by_user_id {e}")
            return None
    
    def get_by_name(self, name):
        try:
            i = SQLItem.query.filter_by(name=name).first()
            if i is None:
                raise RoleNotExist
            return DTO(
                id=i.id,
                name=i.name
            )
        except Exception as e:

            print(f"get_item ПОМИлка репо прожект {e}")
            raise