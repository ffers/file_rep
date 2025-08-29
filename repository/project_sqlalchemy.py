

from infrastructure.models import Project as SQLItem
from domain.models.project_dto import ProjectDTO as DTO
from domain.repositories.project_repo import ItemRepository
from infrastructure.context import current_project_id, current_user_id
from sqlalchemy import select, insert, update, delete
from sqlalchemy.orm import Session


class ProjectSqlAlchemy(ItemRepository):
    def __init__(self, session): 
        self.uid = current_user_id.get()
        self.pid = current_project_id.get()
        self.s = session

    def get_all(self):
        items = SQLItem.query.filter_by(user_id=self.uid).all()
        dtos = []
        for item in items:
            dto = DTO.model_validate(item, from_attributes=True)
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
            stmt = select(SQLItem).where(SQLItem.id == item_id)
            i = self.s.execute(stmt).scalar_one_or_none()
            return DTO.model_validate(i, from_attributes=True)
        except Exception as e:
            print(f"get_item ПОМИлка репо прожект {e}")
            raise


    def get_by_user_id(self):
        try:
            stmt = select(SQLItem).where(SQLItem.user_id == self.uid)
            i = self.s.execute(stmt).scalar_one_or_none()
            return DTO(
                id=i.id, name=i.name
                )
        except Exception as e:
            print(f"ПОМИлка get_by_user_id {e}")
            return None
    
    def get_by_token(self, item_token):
        i = SQLItem.query.filter_by(token=item_token).first()
        return DTO(
            i.id, i.name, i.api, i.token, i.token_market
            )
            

    def add(self, item: DTO):
        sql_item = SQLItem(
            name=item.name, 
            user_id=self.uid,
            project_id=self.pid
            )
        self.session.add(sql_item)
        self.session.commit()

    def update(self, item: DTO):
        i = SQLItem.query.get_or_404(item.id)
        i.name = item.name
        i.user_id = self.uid
        self.session.commit()

    def delete(self, item_id):
        i = SQLItem.query.get_or_404(item_id)
        self.session.delete(i)
        self.session.commit()
