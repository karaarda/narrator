class EventHandler:
    def __init__(self):
        self.listeners = {}
        self.events = {}
        #TODO add scheduler

    def fireEvent(self, tag, data = {}):
        if tag in self.listeners:
            for listener in self.listeners[tag]:
                listener(data)
                return True
        
        return False

    def subscribe(self, tag, listener):
        if not tag in self.listeners:
            self.listeners[tag] = []
        
        if not listener in self.listeners[tag]:
            self.listeners[tag].append(listener)

    def unsubscribe(self, tag, listener):
        if tag in self.listeners and listener in self.listeners[tag]:
            self.listeners[tag].remove(listener)