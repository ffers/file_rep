from sqlalchemy import select
from sqlalchemy.orm import Session

from server_flask.models import BalanceJournal as SQLItem
from domain.models.balance_journal_dto import BalanceJournalDTO as DTO
from domain.repositories.balance_journal_repo import ItemRepository
from infrastructure.context import current_project_id


class BalanceJournalRepo(ItemRepository):
    def __init__(self, session: Session):
        self.s = session
        self.pid = current_project_id.get()

    def create(self, item: DTO):
        sql_item = SQLItem(
            event_date=item.event_date,
            desription=item.desription,
            income=item.income,
            total=item.total,
            balance_id=item.balance_id,
            project_id=self.pid,
        )
        self.s.add(sql_item)
        self.s.commit()

    def get_all(self):
        stmt = select(SQLItem).where(SQLItem.project_id == self.pid)
        items = self.s.scalars(stmt).all()
        return [DTO.model_validate(item) for item in items]

    def get_all_select(self):
        items = self.get_all()
        store_select = []
        for i in items:
            dto = {"id": i.id, "name": i.name}
            store_select.append(dto)
        return store_select

    def get(self, item_id):
        item = self.s.get(SQLItem, item_id)
        return DTO(item.id, item.name, item.api, item.token, item.token_market)

    def get_by_token(self, item_token):
        stmt = select(SQLItem).where(SQLItem.token == item_token)
        item = self.s.scalars(stmt).first()
        return DTO(item.id, item.name, item.api, item.token, item.token_market)

    def update(self, item: DTO):
        instance = self.s.get(SQLItem, item.id)
        instance.name = item.name
        instance.api = item.api
        instance.token = item.token
        instance.token_market = item.token_market
        self.s.commit()

    def delete(self, item_id):
        instance = self.s.get(SQLItem, item_id)
        self.s.delete(instance)
        self.s.commit()

