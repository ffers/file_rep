from sqlalchemy import select
from sqlalchemy.orm import Session

from server_flask.models import UserToken
from DTO import UserTokenDTO
from infrastructure import current_project_id

from .base import ScopedRepo


class UserTokenRep(ScopedRepo):
    def __init__(self, session: Session, token):
        super().__init__(session, current_project_id.get())
        self.token = token

    def add_token(self, d: UserTokenDTO):
        try:
            item = UserToken(d)
            item.project_id = self.project_id
            self.session.add(item)
            self.session.commit()
            return True
        except Exception as e:
            return False, str(e)

    def update_token(self, d: UserTokenDTO):
        try:
            stmt = select(UserToken).where(
                UserToken.user_id == d.user_id,
                UserToken.project_id == self.project_id,
            )
            item = self.session.scalars(stmt).first()
            if not item:
                return False, "not found"
            item.update_from_dto(d)
            self.session.commit()
            return True
        except Exception as e:
            self.session.rollback()
            return False, str(e)

    def load_token_checkbox(self, user_id):
        stmt = select(UserToken).where(
            UserToken.user_id == user_id,
            UserToken.project_id == self.project_id,
        )
        token = self.session.scalars(stmt).first()
        return token.checkbox_access_token if token else None

