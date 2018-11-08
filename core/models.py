from . import db
from sqlalchemy import Column, Integer, String, Date, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declared_attr


class MysqlMixin(object):
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    __table_args__ = {"mysql_engine": "InnoDB"}
    __mapper_args__ = {"always_refresh": True}

    id = Column(Integer, primary_key=True)


class NamedMixin(MysqlMixin):
    name = Column(String(64), unique=True)

    def __init__(self, name=None):
        self.name = name

    def __repr__(self):
        return "<{0} {1}>".format(self.__class__.name, self.name)


class ProductArea(NamedMixin, db.Model):
    feature_requests = relationship("FeatureRequest", back_populates="product_area")


class Client(NamedMixin, db.Model):
    feature_requests = relationship("FeatureRequest", back_populates="client")


class FeatureRequest(MysqlMixin, db.Model):
    title = Column(String(128), unique=True)
    description = Column(Text)

    client_id = Column(Integer, ForeignKey("client.id"))
    client = relationship("Client", back_populates="feature_requests")

    client_priority = Column(Integer)
    target_date = Column(Date)

    product_area_id = Column(Integer, ForeignKey("productarea.id"))
    product_area = relationship("ProductArea", back_populates="feature_requests")

    def __init__(
        self, title, description, client, client_priority, target_date, product_area
    ):
        self.title = title
        self.description = description
        self.client = client
        self.client_priority = client_priority
        self.target_date = target_date
        self.product_area = product_area

    def __repr__(self):
        return "<FeatureRequest {0}>".format(self.title)
