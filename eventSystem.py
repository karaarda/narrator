class EventHandler:
    def __init__(self):
        self.eventConfigs = {}
        self.listeners = {}
        self.eventQueue = {}
        #TODO add scheduler

    def fireEvent(self, tag, data = {}):
        if tag in self.listeners:
            for listener in self.listeners[tag]:
                listener(data)
                return True
        
        return False

    def subscribe(self, tag, listener):
        if not tag in self.listeners:
            self.listeners[tag] = [listener]
        
        elif not listener in self.listeners[tag]:
            if self.eventConfigs[tag].eventType | int('101',2) == int('111',2):
                self.listeners[tag] = [listener]
            else:
                self.listeners[tag].append(listener)

    def unsubscribe(self, tag, listener):
        if tag in self.listeners and listener in self.listeners[tag]:
            self.listeners[tag].remove(listener)

    def configureEvent(self, tag, eventType):
        for i in range(0, len(self.eventConfigs)):
            event = list(self.eventConfigs.values())[i]

            if event.tag == tag:
                event.eventType = eventType
                return

        self.listeners[tag] = []
        self.eventConfigs[tag] = EventConfig(tag,eventType)

class EventConfig:
    INSTANT = int('000', 2)
    DELAYED = int('001', 2)
    SINGLE   = int('010', 2)

    def __init__(self, tag, eventType):
        self.tag = tag
        self.eventType = eventType

class Event:
    def __init__(self, tag, data):
        self.tag = tag
        self.data = data