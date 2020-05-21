import abc

from domain import models


class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    def add(self, product: models.Product):
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, sku) -> models.Product:
        raise NotImplementedError


class SqlAlchemyRepository(AbstractRepository):
    def __init__(self, session):
        self.session = session

    def add(self, product):
        self.session.add(product)

    def get(self, sku):
        return self.session.query(models.Product).filter_by(sku=sku).first()
