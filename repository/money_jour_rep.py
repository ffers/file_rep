from sqlalchemy import desc, select
from sqlalchemy.orm import Session

from infrastructure.models import MoneyJournal
from domain.models.money_jour_dto import MoneyJournalDto
from infrastructure.context import current_project_id

from .base import ScopedRepo


class MoneyJourRep(ScopedRepo):
    def __init__(self, session: Session):
        super().__init__(session, current_project_id.get())

    def load_all(self):
        stmt = (
            select(MoneyJournal)
            .where(MoneyJournal.project_id == self.project_id)
            .order_by(desc(MoneyJournal.timestamp))
        )
        items = self.session.scalars(stmt).all()
        return [
            MoneyJournalDto(
                id=item.id,
                timestamp=item.timestamp,
                event_date=item.event_date,
                description=item.description,
                movement=item.movement,
                total=item.total,
            )
            for item in items
        ]

    def add_(self, dto: MoneyJournalDto):
        try:
            item = MoneyJournal(
                event_date=dto.event_date,
                description=dto.description,
                movement=dto.movement,
                total=dto.total,
                project_id=self.project_id,
            )
            self.session.add(item)
            self.session.commit()
            return True
        except Exception as e:
            raise ValueError(f"Помилка додавання в бд {e}")

    def update_(self, item_id, dto: MoneyJournalDto):
        try:
            instance = self.get_by_id(MoneyJournal, item_id)
            if not instance:
                return None
            instance.event_date = dto.event_date
            instance.description = dto.description
            instance.movement = dto.movement
            instance.total = dto.total
            self.session.commit()
            self.session.refresh(instance)
            return instance
        except Exception as e:
            raise ValueError(f"Помилка оновленя в бд {e}")

    def delete_(self, item_id):
        item = self.get_by_id(MoneyJournal, item_id)
        if not item:
            return False
        self.session.delete(item)
        self.session.commit()
        return True

