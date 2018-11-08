from .database import Base
from sqlalchemy import Column, Integer, String, Date, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declared_attr


class BaseMixin(object):
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    __table_args__ = {'mysql_engine': 'InnoDB'}
    __mapper_args__ = {'always_refresh': True}

    id = Column(Integer, primary_key=True)


class NamedMixin(BaseMixin):
    name = Column(String(64), unique=True)

    def __init__(self, name=None):
        self.name = name

    def __repr__(self):
        return '<{0} {1}>'.format(self.__class__.name, self.name)


class ProductArea(NamedMixin, Base):
    feature_requests = relationship("FeatureRequest", back_populates="product_area")


class Client(NamedMixin, Base):
    feature_requests = relationship("FeatureRequest", back_populates="client")


class FeatureRequest(BaseMixin):
    title = Column(String(128), unique=True)
    description = Column(Text)

    client_id = Column(Integer, ForeignKey('client.id'))
    client = relationship("Client", back_populates("feature_requests"))

    client_priority = Column(Integer)
    target_date = Column(Date)

    product_area_id = Column(Integer, ForeignKey('productarea.id'))
    product_area = relationship("ProductArea", back_populates("feature_requests"))

    def __init__(self, user_id, timestamp, lat, lon, readings):
        self.user_id = user_id
        self.timestamp = timestamp
        self.lat = lat
        self.lon = lon
        self.readings = readings

    def __repr__(self):
        return '<FeatureRequest {0}>'.format(self.title)
