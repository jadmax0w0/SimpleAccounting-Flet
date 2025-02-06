from typing import Callable


class UIMessage:
    def __init__(self):
        self.subs: list[Callable[[object], None]] = []

    def add(self, *subscribers: Callable[[object], None]):
        for s in subscribers:
            if s not in self.subs:
                self.subs.append(s)

    def remove(self, subscriber: Callable[[object], None]):
        if subscriber in self.subs:
            self.subs.remove(subscriber)
    
    def invoke(self, sender: object):
        for s in self.subs:
            s(sender)