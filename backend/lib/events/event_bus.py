class EventBus:
    def __init__(self):
        self.event_listeners: dict[str, list] = dict()

    def add_listener(self, event_name: str, listener: callable):
        if event_name not in self.event_listeners:
            self.event_listeners[event_name] = []
        if listener in self.event_listeners[event_name]:
            print(
                f"[EVENT BUS] Cannot add the same listener to an event multiple times ({event_name})."
            )
            return
        self.event_listeners[event_name].append(listener)

    def remove_listener(self, event_name: str, listener: callable):
        if event_name not in self.event_listeners:
            print(f"[EVENT BUS] Event '{event_name}' is not defined.")
            return
        if listener not in self.event_listeners[event_name]:
            # No need to remove it
            return
        self.event_listeners[event_name].remove(listener)

    def invoke_event(self, event_name: str, *args):
        if event_name not in self.event_listeners:
            print(f"[EVENT BUS] Event '{event_name}' is not defined.")
            return
        for listener in self.event_listeners[event_name]:
            listener(args)
