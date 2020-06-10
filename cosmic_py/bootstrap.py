import inspect
from typing import Callable
import email

from adapters import orm, redis_eventpublisher
from service_layer import unit_of_work, messagebus, handlers


def bootstrap(
    start_orm: bool = True,
    uow: unit_of_work.AbstractUnitOfWork = unit_of_work.SqlAlchemyUnitOfWork(),
    send_mail: Callable = email.send_mail,
    publish: Callable = redis_eventpublisher.publish,
):
    if start_orm:
        orm.start_mappers()
    dependencies = {"uow": uow, "send_mail": send_mail, "publish": publish}
    injected_event_handlers = {
        event_type: [
            inject_dependices(handler, dependencies) for handler in event_handlers
        ]
        for event_type, event_handlers in messagebus.EVENT_HANDLERS.items()
    }
    injected_event_commands = {
        command_type: inject_dependices(handler, dependencies)
        for command_type, handler in messagebus.COMMAND_HANDLERS.items()
    }


def inject_dependices(handler, dependencies):
    params = inspect.signature(handler).parameters
    deps = {
        name: dependency for name, dependency in dependencies.items() if name in params
    }
    return lambda message: handler(message, **deps)
