

from server_flask.models import Store as SQLItem
from domain.models.store_dto import StoreDTO
from domain.repositories.store_repo import ItemRepository
from infrastructure import current_project_id

class StoreRepositorySQLAlchemy(ItemRepository):
    def __init__(self, session=None):
        self.session = session  
        self.pid = current_project_id.get()

    def get_all(self):
        stores = SQLItem.query.all()

        store_dtos = []
        for store in stores:
            dto = StoreDTO(
                id=store.id,
                name=store.name,
                api=store.api,
                token=store.token
            )
            store_dtos.append(dto)

        return store_dtos
    
    def get_all_select(self):
        stores = self.get_all() 
        store_select = []
        for store in stores:
            dto = {
                'id': store.id,
                'name': store.name,
            }
            store_select.append(dto)

        return store_select


    def get(self, item_id):
        i = SQLItem.query.get_or_404(item_id)
        return StoreDTO(
            i.id, i.name, i.api, i.token, i.token_market
            )
    
    def read(self, marketplace, store_id):
        i = SQLItem.query.filter_by(
            token_market=marketplace, 
            id=store_id, 
            prooject_id=self.pid
            ).first()
        return StoreDTO(
            i.id, i.name, i.api, i.token, i.token_market
            )
    
    def get_by_token(self, item_token):
        i = SQLItem.query.filter_by(token=item_token).first()
        return StoreDTO(
            i.id, i.name, i.api, i.token, i.token_market
            )

    def add(self, item: StoreDTO):
        sql_item = SQLItem(
            name=item.name, 
            api=item.api,
            token=item.token,
            token_market=item.token_market
            )
        self.session.add(sql_item)
        self.session.commit()

    def update(self, item: StoreDTO):
        i = SQLItem.query.get_or_404(item.id)
        i.name = item.name
        i.api = item.api
        i.token = item.token
        i.token_market=item.token_market
        self.session.commit()

    def delete(self, item_id):
        i = SQLItem.query.get_or_404(item_id)
        self.session.delete(i)
        self.session.commit()
