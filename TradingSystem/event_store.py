from typing import List
from events import Event

class EventStore:
    def __init__(self):
        self.events: List[Event] = []

    def append(self, event: Event):
        self.events.append(event)

    def get_all_events(self) -> List[Event]:
        return list(self.events)