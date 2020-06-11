import inspect
from typing import Callable

from adapters import orm, redis_eventpublisher
from adapters.notifications import AbstractNotifications, EmailNotifications
from service_layer import unit_of_work, handlers, messagebus


def bootstrap(
    start_orm: bool = True,
    uow: unit_of_work.AbstractUnitOfWork = unit_of_work.SqlAlchemyUnitOfWork(),
    notifications: AbstractNotifications = None,
    publish: Callable = redis_eventpublisher.publish,
) -> messagebus.MessageBus:
    if notifications is None:
        notifications = EmailNotifications()
    if start_orm:
        orm.start_mappers()
    dependencies = {"uow": uow, "notifications": notifications, "publish": publish}
    injected_event_handlers = {
        event_type: [
            inject_dependices(handler, dependencies) for handler in event_handlers
        ]
        for event_type, event_handlers in handlers.EVENT_HANDLERS.items()
    }
    injected_event_commands = {
        command_type: inject_dependices(handler, dependencies)
        for command_type, handler in handlers.COMMAND_HANDLERS.items()
    }
    return messagebus.MessageBus(
        uow=uow,
        event_handlers=injected_event_handlers,
        command_handlers=injected_event_commands,
    )


def inject_dependices(handler, dependencies):
    params = inspect.signature(handler).parameters
    deps = {
        name: dependency for name, dependency in dependencies.items() if name in params
    }
    return lambda message: handler(message, **deps)
