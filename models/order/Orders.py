from sqlalchemy import Column, Integer, String, Text, Float, Boolean, DateTime, Date, Numeric, BigInteger, SmallInteger, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from infrastructure.db_core.base import Base as db

class Orders(db):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    phone = Column(String(50))
    email = Column(String(50))
    ttn = Column(String(50))
    ttn_ref = Column(String(50)) # edit
    client_firstname = Column(String(50))
    client_lastname = Column(String(50))
    client_surname = Column(String(50))
    recipient = relationship("Recipient", back_populates="orders")
    recipient_id = Column(Integer, ForeignKey(
        'recipient.id', name='fk_orders_recipient_id'))
    costumer = relationship("Costumer", back_populates="orders")
    costumer_id = Column(Integer, ForeignKey(
        'costumer.id', name='fk_orders_costumer_id'))
    
    ''' для фіксування кількості замовленнь по телефону '''
    quantity_orders_costumer = Column(Integer) # тимчасове поле 

    delivery_option = Column(String(50))
    city_name = Column(String(50))
    city_ref = Column(String(50))
    region = Column(String(50))
    area = Column(String(50))
    warehouse_option = Column(String(50))
    warehouse_text = Column(String(255))
    warehouse_ref = Column(String(50))
    sum_price = Column(Float)
    sum_before_goods = Column(Float)
    description = Column(String(500))
    history = Column(String(500))
    description_delivery = Column(String(50))
    cpa_commission = Column(String(50)) 
    client_id = Column(Integer)
    send_time = Column(DateTime)
    order_id_sources = Column(String(50))
    order_code = Column(String(50), unique=True)

    project_id = Column(Integer, ForeignKey(
        'project.id', name='fk_orders_project_id'))

    ordered_product = relationship('OrderedProduct', backref='orders', cascade='all, delete-orphan')
    delivery_order = relationship("DeliveryOrder", back_populates="orders", uselist=False, cascade="all, delete-orphan")
    payment_status = relationship("PaymentStatus", back_populates="orders")
    payment_status_id = Column(Integer, ForeignKey(
        'payment_status.id', name='fk_orders_payment_status_id'))
    ordered_status = relationship("OrderedStatus", back_populates="orders")
    ordered_status_id = Column(Integer, ForeignKey(
        'ordered_status.id', name='fk_orders_ordered_status_id'))
    warehouse_method = relationship("WarehouseMethod", back_populates="orders")
    warehouse_method_id = Column(Integer, ForeignKey(
        'warehouse_method.id', name='fk_orders_warehouse_method_id'))
    source_order = relationship("SourceOrder", back_populates="orders")
    source_order_id = Column(Integer, ForeignKey(
        'source_order.id', name='fk_orders_source_order_id'))
    store = relationship("Store", back_populates="orders")
    store_id = Column(Integer, ForeignKey(
        'store.id', name='fk_order_store_id'))
    payment_method = relationship("PaymentMethod", back_populates="orders")
    payment_method_id = Column(Integer, ForeignKey(
        'payment_method.id', name='fk_orders_payment_method_id'))
    delivery_method = relationship("DeliveryMethod", back_populates="orders")
    delivery_method_id = Column(Integer, ForeignKey(
        'delivery_method.id', name='fk_orders_delivery_method_id'))
    author_id = Column(Integer, ForeignKey(
        'users.id', name='fk_orders_users_id', ondelete="CASCADE"), nullable=True)
    comments = relationship('Comment', backref='orders', passive_deletes=True)
    likes = relationship('Likes', backref='orders', passive_deletes=True)
    telegram_ordered = relationship('TelegramOrdered', backref='orders', cascade='all, delete-orphan')
    products = relationship('Products', secondary='ordered_product', overlaps="ordered_product,orders")

