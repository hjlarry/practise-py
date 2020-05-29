import abc

from domain import models
from . import orm


class AbstractRepository(abc.ABC):
    def __init__(self):
        self.seen = set()

    def add(self, product: models.Product):
        self._add(product)
        self.seen.add(product)

    def get(self, sku) -> models.Product:
        product = self._get(sku)
        if product:
            self.seen.add(product)
        return product

    def get_by_batchref(self, batchref) -> models.Product:
        product = self._get_by_batchref(batchref)
        if product:
            self.seen.add(product)
        return product

    @abc.abstractmethod
    def _add(self, product: models.Product):
        raise NotImplementedError

    @abc.abstractmethod
    def _get(self, sku) -> models.Product:
        raise NotImplementedError

    @abc.abstractmethod
    def _get_by_batchref(self, batchref) -> models.Product:
        raise NotImplementedError


class SqlAlchemyRepository(AbstractRepository):
    def __init__(self, session):
        super().__init__()
        self.session = session

    def _add(self, product):
        self.session.add(product)

    def _get(self, sku):
        return self.session.query(models.Product).filter_by(sku=sku).first()

    def _get_by_batchref(self, batchref):
        return (
            self.session.query(models.Product)
            .join(models.Batch)
            .filter(orm.batches.c.reference == batchref)
            .first()
        )
