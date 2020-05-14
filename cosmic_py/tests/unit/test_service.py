import pytest

from adapters.repository import AbstractRepository
from domain import models
from service_layer import services


class FakeRepository(AbstractRepository):
    def __init__(self, batches):
        self.batches = set(batches)

    def add(self, batch):
        self.batches.add(batch)

    def get(self, reference):
        return next(b for b in self.batches if b.reference == reference)

    def list(self):
        return list(self.batches)


class FakeSession:
    committed = False

    def commit(self):
        self.committed = True


def test_returns_allocation():
    batch = models.Batch("batch1", "COMPLICATED-LAMP", 100, eta=None)
    repo, session = FakeRepository([batch]), FakeSession()
    result = services.allocate("o1", "COMPLICATED-LAMP", 10, repo, session)
    assert result == "batch1"


def test_error_for_invalid_sku():
    batch = models.Batch("b1", "AREALSKU", 100, eta=None)
    repo = FakeRepository([batch])

    with pytest.raises(services.InvalidSku, match="Invalid sku NONEXISTENTSKU"):
        services.allocate("o1", "NONEXISTENTSKU", 10, repo, FakeSession())


def test_commits():
    batch = models.Batch("b1", "OMINOUS-MIRROR", 100, eta=None)
    repo = FakeRepository([batch])
    session = FakeSession()
    services.allocate("o1", "OMINOUS-MIRROR", 10, repo, session)
    assert session.committed is True
