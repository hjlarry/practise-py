from typing import Optional
from datetime import date
import email

from domain import models, commands, events
from adapters import redis_eventpublisher
from .unit_of_work import AbstractUnitOfWork


class InvalidSku(Exception):
    pass


def add_batch(cmd: commands.CreateBatch, uow: AbstractUnitOfWork):
    with uow:
        product = uow.products.get(sku=cmd.sku)
        if product is None:
            product = models.Product(cmd.sku, batches=[])
            uow.products.add(product)
        product.batches.append(models.Batch(cmd.ref, cmd.sku, cmd.qty, cmd.eta))
        uow.commit()


def allocate(cmd: commands.Allocate, uow: AbstractUnitOfWork) -> str:
    line = models.OrderLine(cmd.orderid, cmd.sku, cmd.qty)
    with uow:
        product = uow.products.get(sku=line.sku)
        if product is None:
            raise InvalidSku(f"Invalid sku {line.sku}")
        batchref = product.allocate(line)
        uow.commit()
    return batchref


def send_out_of_stock_notification(event: events.OutOfStock, uow: AbstractUnitOfWork):
    email.send(
        "stock@made.com", f"Out of stock for {event.sku}",
    )


def change_batch_quantity(cmd: commands.ChangeBatchQuantity, uow: AbstractUnitOfWork):
    with uow:
        product = uow.products.get_by_batchref(batchref=cmd.ref)
        product.change_batch_quantity(ref=cmd.ref, qty=cmd.qty)
        uow.commit()


def publish_allocated_event(event: events.Allocated, uow: AbstractUnitOfWork):
    redis_eventpublisher.publish("line_allocated", event)


def add_allocation_to_read_model(event: events.Allocated, uow: AbstractUnitOfWork):
    with uow:
        uow.session.execute(
            "INSERT INTO allocations_view (orderid, sku, batchref) VALUES (:orderid, :sku, :batchref)",
            dict(orderid=event.orderid, sku=event.sku, batchref=event.batchref),
        )
        uow.commit()
