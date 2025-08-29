

from infrastructure.models import UserRoles as SQLItem
from domain.models.user_roles_dto import UserRoleReadDTO as DTO
from domain.repositories.user_roles_repo import ItemRepository
from infrastructure.context import current_project_id, current_user_id



class UserRolesSqlAlchemy(ItemRepository):
    def __init__(self, session): 
        self.uid = current_user_id.get()
        self.pid = current_project_id.get()
        self.session = session

    def get_all(self):
        items = SQLItem.query.filter_by().all()
        dtos = []
        for i in items:
            dto = DTO(
                id=i.id,
                user_id=i.user_id,
                role_id=i.role_id,
                user=i.user,
                role=i.role,
                project=i.project
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
    
    def update_project_id(self):
        items = SQLItem.query.filter_by().all()
        for item in items:
            item.project_id = self.pid
        self.session.commit()
        return True

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
                user_id=i.user_id,
                role_id=i.role_id,
                user=i.user,
                role=i.role,
                project=i.project
            )
        except Exception as e:

            print(f"get_item ПОМИлка репо прожект {e}")
            raise


    def get_by_user_id(self):
        try:
            i = SQLItem.query.get_or_404(self.uid)
            return DTO(
                id=i.id,
                user_id=i.user_is,
                project_id=i.project_id,
                role_id=i.role_id
            )
        except Exception as e:
            print(f"ПОМИлка get_by_user_id {e}")
            return None
    
    def get_by_token(self, item_token):
        i = SQLItem.query.filter_by(token=item_token).first()
        return DTO(
            i.id, i.name, i.api, i.token, i.token_market
            )
            

    def create(self, item: DTO):
        sql_item = SQLItem(
            user_id=item.user_id, 
            role_id=item.role_id,
            project_id=self.pid
            )
        self.session.add(sql_item)
        self.session.commit()
        self.session.refresh(sql_item)
        return sql_item

    def update(self, item: DTO):
        i = SQLItem.query.get_or_404(item.id)
        i.user_id=item.user_id, 
        i.role_id=item.role_id,
        i.project_id=self.pid
        self.session.commit()
        self.session.refresh(i)
        return i

    def delete(self, item_id):
        i = SQLItem.query.get_or_404(item_id)
        self.session.delete(i)
        self.session.commit()
