import email

from domain import events
from .unit_of_work import AbstractUnitOfWork


def send_out_of_stock_notification(event: events.OutOfStock):
    email.send_mail(
        "stock@made.com", f"Out of stock for {event.sku}",
    )


HANDLERS = {
    events.OutOfStock: [send_out_of_stock_notification],
}


def handle(event: events.Event, uow: AbstractUnitOfWork):
    queue = [event]
    while queue:
        event = queue.pop(0)
        for handler in HANDLERS[type(event)]:
            handler(event, uow=uow)
            queue.extend(uow.collect_new_events())
