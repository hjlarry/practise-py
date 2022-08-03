import json


class Worker:
    def __init__(self, task):
        self.task = task

    def start(self):
        while True:
            try:
                _dequeued_item = self.task.broker.dequeue(
                    queue_name=self.task.task_name
                )
                dequeued_item = json.loads(_dequeued_item)
                task_id = dequeued_item["task_id"]
                task_args = dequeued_item["args"]
                task_kwargs = dequeued_item["kwargs"]
                task_kwargs["task_id"] = task_id
                self.task.run(*task_args, **task_kwargs)
                print(f"succesful run of task: {task_id}")
            except Exception:
                print("Unable to execute task.")
                continue
