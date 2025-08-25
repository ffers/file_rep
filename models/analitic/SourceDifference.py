from sqlalchemy import Column, Integer, String, Text, Float, Boolean, DateTime, Date, Numeric, BigInteger, SmallInteger, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from infrastructure.db_core.base import Base as db
 
class SourceDifference(db):
    __tablename__ = 'source_difference'
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    event_date = Column(DateTime)
    source_id = Column(Integer, ForeignKey(
        'product_source.id', name='fk_source_difference_product_source_id'))
    quantity_crm = Column(Integer)
    quantity_stock = Column(Integer)
    difference = Column(Integer)   
    sold = Column(Integer)
    comment = Column(Text)
    project_id = Column(Integer, ForeignKey(
        'project.id', name='fk_source_difference_project_id'))
    product_source = relationship('ProductSource', back_populates='source_difference')  


 
