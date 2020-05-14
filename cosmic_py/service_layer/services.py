from domain import models
from adapters.repository import AbstractRepository


class InvalidSku(Exception):
    pass


def is_valid_sku(sku, batches):
    return sku in {b.sku for b in batches}


def allocate(
    orderid: str, sku: str, qty: int, repo: AbstractRepository, session
) -> str:
    batches = repo.list()
    line = models.OrderLine(orderid, sku, qty)
    if not is_valid_sku(line.sku, batches):
        raise InvalidSku(f"Invalid sku {line.sku}")
    batchref = models.allocate(line, batches)
    session.commit()
    return batchref
