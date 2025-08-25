

from server_flask.models import BalanceJournal as SQLItem
from domain.models.balance_journal_dto import BalanceJournalDTO as DTO
from domain.repositories.balance_journal_repo import ItemRepository
from infrastructure.context import current_project_id

class BalanceJournalRepo(ItemRepository):
    def __init__(self, session): 
        self.s = session
        self.pid = current_project_id.get()

    def create(self, item: DTO):
        sql_item = SQLItem(
            event_date=item.event_date,
            desription=item.desription,
            income=item.income,
            total=item.total,
            balance_id=item.balance_id,
            project_id=self.pid
            )
        self.s.add(sql_item)
        self.s.commit()

    def get_all(self, ):
        items = self.s.query(SQLItem).filter_by(project_id=self.pid).all()

        dtos = []
        for item in items:
            dto = DTO.model_validate(item)
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


    def get(self, item_id):
        i = SQLItem.query.get_or_404(item_id)
        return DTO(
            i.id, i.name, i.api, i.token, i.token_market
            )
    
    def get_by_token(self, item_token):
        i = SQLItem.query.filter_by(token=item_token).first()
        return DTO(
            i.id, i.name, i.api, i.token, i.token_market
            )


    def update(self, item: DTO):
        i = SQLItem.query.get_or_404(item.id)
        i.name = item.name
        i.api = item.api
        i.token = item.token
        i.token_market=item.token_market
        self.s.commit()

    def delete(self, item_id):
        i = SQLItem.query.get_or_404(item_id)
        self.s.delete(i)
        self.s.commit()
