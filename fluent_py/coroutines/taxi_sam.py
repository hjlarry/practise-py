import collections
import queue
import random
import time

Event = collections.namedtuple("Event", "time proc action")
NUM_TAXI = 3
DEPARTURE_INTERVAL = 5
SEARCH_DURATION = 5
TRIP_DURATION = 20
DEFAULT_END_TIME = 180


def taxi_process(ident, trips, start_time=0):
    time = yield Event(start_time, ident, "leave garage")
    for i in range(trips):
        time = yield Event(time, ident, "pick up passenger")
        time = yield Event(time, ident, "drop off passenger")
    yield Event(time, ident, "going home")


def test_taxi_process():
    taxi = taxi_process(13, 2)
    e1 = next(taxi)
    print(e1)
    e2 = taxi.send(e1.time + 7)
    print(e2)
    e3 = taxi.send(e2.time + 23)
    print(e3)
    print(next(taxi))
    print(next(taxi))
    print(next(taxi))
    print(next(taxi))
    print(next(taxi))


class Simulator:
    def __init__(self, procs_map):
        self.events = queue.PriorityQueue()
        self.procs = dict(procs_map)

    def run(self, end_time):
        for _, proc in sorted(self.procs.items()):
            first_event = next(proc)
            self.events.put(first_event)
        sim_time = 0
        while sim_time < end_time:
            if self.events.empty():
                print("*** end of events")
                break
            current_event = self.events.get()
            sim_time, proc_id, previous_action = current_event
            print(f"taxi:{proc_id} ", current_event)
            active_proc = self.procs[proc_id]
            next_time = sim_time + compute_duration(previous_action)
            try:
                next_event = active_proc.send(next_time)
            except StopIteration:
                del self.procs[proc_id]
            else:
                self.events.put(next_event)
        else:
            print(f"*** end of simulation time:{self.events.qsize()} events pending")


def compute_duration(previous_action):
    if previous_action in ["leave garage", "drop off passenger"]:
        interval = SEARCH_DURATION
    elif previous_action == "pick up passenger":
        interval = TRIP_DURATION
    elif previous_action == "going home":
        interval = 1
    else:
        raise ValueError("unknown previous action:", previous_action)
    return int(random.expovariate(1 / interval)) + 1


def main(end_time=DEFAULT_END_TIME, num_taxi=NUM_TAXI):
    random.seed(1)
    taxis = {
        i: taxi_process(i, (i + 1) * 2, i * DEPARTURE_INTERVAL) for i in range(num_taxi)
    }
    sim = Simulator(taxis)
    sim.run(end_time)


main(num_taxi=5)