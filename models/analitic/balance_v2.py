from server_flask.db import BaseModel
from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, DateTime, Numeric, \
    ForeignKey

class BalanceV2(BaseModel):
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime(timezone.utc()))
    name = Column(String(50))
    total = Column(Numeric(precision=10, scale=2))
    project_id = Column(Integer, ForeignKey(
        'project.id', name='fk_orders_crm_id'), unique=True)

