import abc
import json
import uuid

from broker import Broker
from backend import Backend


class BaseTask(abc.ABC):
    task_name = None

    def __init__(self):
        if not self.task_name:
            raise ValueError("task_name should set")
        self.broker = Broker()

    @abc.abstractmethod
    def run(self, *args, **kwargs):
        raise NotImplementedError("BaseTask run method must be implented.")

    def update_state(self, task_id, state, meta={}):
        _task = {"state": state, "meta": meta}
        serialized_task = json.dumps(_task)
        backend = Backend()
        backend.enqueue(queue_name=task_id, item=serialized_task)
        print(f"task {task_id} success queued")

    def delay(self, *args, **kwargs):
        try:
            self.task_id = str(uuid.uuid4())
            _task = {"task_id": self.task_id, "args": args, "kwargs": kwargs}
            serialized_task = json.dumps(_task)
            self.broker.enqueue(queue_name=self.task_name, item=serialized_task)
            print(f"task {task_id} success queued")
        except Exception:
            raise Exception("unable to publish task to broker")
        return self.task_id


def get_result(task_id):
    backend = Backend()
    dequeued_item = json.loads(backend.dequeue(queue_name=task_id))

    class Info:
        def __init__(self, state, meta):
            self.state = state
            self.meta = meta

    info = Info(dequeued_item["state"], dequeued_item["meta"])
    return info
