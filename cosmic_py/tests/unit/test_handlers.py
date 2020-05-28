import pytest

from adapters.repository import AbstractRepository
from service_layer import handlers, unit_of_work
from domain import events


class FakeRepository(AbstractRepository):
    def __init__(self, products):
        super().__init__()
        self._products = set(products)

    def _add(self, batch):
        self._products.add(batch)

    def _get(self, sku):
        return next((p for p in self._products if p.sku == sku), None)


class FakeUnitOfWork(unit_of_work.AbstractUnitOfWork):
    def __init__(self):
        self.products = FakeRepository([])
        self.committed = False

    def _commit(self):
        self.committed = True

    def rollback(self):
        pass


class FakeSession:
    committed = False

    def commit(self):
        self.committed = True


def test_add_batch():
    uow = FakeUnitOfWork()
    handlers.add_batch(events.BatchCreated("b1", "CRUNCHY-ARMCHAIR", 100, None), uow)
    assert uow.products.get("CRUNCHY-ARMCHAIR") is not None
    assert uow.committed


def test_allocate_returns_allocation():
    uow = FakeUnitOfWork()
    handlers.add_batch(
        events.BatchCreated("batch1", "COMPLICATED-LAMP", 100, None), uow
    )
    result = handlers.allocate(
        events.AllocationRequired("o1", "COMPLICATED-LAMP", 10), uow
    )
    assert result == "batch1"


def test_error_for_invalid_sku():
    uow = FakeUnitOfWork()
    handlers.add_batch(events.BatchCreated("b1", "AREALSKU", 100, None), uow)
    with pytest.raises(handlers.InvalidSku, match="Invalid sku NONEXISTENTSKU"):
        handlers.allocate(events.AllocationRequired("o1", "NONEXISTENTSKU", 10), uow)


def test_commits():
    uow = FakeUnitOfWork()
    handlers.add_batch(events.BatchCreated("b1", "OMINOUS-MIRROR", 100, None), uow)
    handlers.allocate(events.AllocationRequired("o1", "OMINOUS-MIRROR", 10), uow)
    assert uow.committed is True
