import email

from domain import events


def send_out_of_stock_notification(event: events.OutOfStock):
    email.send_mail(
        "stock@made.com", f"Out of stock for {event.sku}",
    )


HANDLERS = {
    events.OutOfStock: [send_out_of_stock_notification],
}


def handle(event: events.Event):
    for handler in HANDLERS[type(event)]:
        handler(event)
