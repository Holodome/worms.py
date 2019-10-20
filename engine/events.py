class EventDispatcher:
    def __init__(self, event):
        self.event = event

    def dispatch(self, event_type, function) -> bool:
        if self.event.type == event_type and not self.event.Handled:
            function(self.event)
            return True
        return False
