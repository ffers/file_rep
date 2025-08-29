

from infrastructure.models import Users as SQLItem
from domain.models.user_dto import UserDTO as DTO
from domain.repositories.user_repo import ItemRepository
from infrastructure.context import current_project_id, current_user_id

from utils.exception import EmailDoesNotExist
from sqlalchemy import select


class UserSqlAlchemy(ItemRepository):
    def __init__(self, session): 
        self.uid = current_user_id.get()
        self.pid = current_project_id.get()
        self.s = session

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
            stmt = select(SQLItem).where(SQLItem.id == item_id)
            i = self.s.execute(stmt).scalar_one_or_none()
            return i
        except Exception as e:

            print(f"get_item ПОМИлка репо прожект {e}")
            raise


    def get_by_user_id(self):
        try:
            stmt = select(SQLItem).where(SQLItem.id == self.uid)
            i = self.s.execute(stmt).scalar_one_or_none()
            return i
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
            username=item.username, 
            email=item.email,
            password=item.password
            )
        self.session.add(sql_item)
        self.session.commit()
        self.session.refresh(sql_item)
        return sql_item
    # DTO(
    #             id=i.id,
    #             email=i.email,
    #             username=i.username,
    #             password=i.password
    #         )

    def update(self, item: DTO):
        i = SQLItem.query.get_or_404(item.id)
        i.name = item.name
        i.email = item.email
        self.session.commit()

    def delete(self, item_id):
        i = SQLItem.query.get_or_404(item_id)
        self.session.delete(i)
        self.session.commit()
    
    def get_by_email(self, email):
        stmt = select(SQLItem).where(SQLItem.email == email)
        i = self.s.scalars(stmt).first()
        if i is None:
            raise EmailDoesNotExist
        return i
