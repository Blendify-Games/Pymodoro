import pygame

# event types are:
EVT_QUIT = 0
EVT_MOUSE = 1
EVT_KEYBOARD = 2

class _EventListener():
    def __init__(self, evtype: 'EVENT_TYPE', 
                    evname: str, callback: 'func'):
        FMAP = [
            self.__listenQuit, self.__listenMouse,
            self.__listenKeyboard
        ]
        self.name = evname
        self.callback = callback
        self.typeListener = FMAP[evtype]
    def __listenQuit(self):
        if pygame.event.get(pygame.QUIT):
            self.callback()
    def __listenMouse(self):
        pass
    def __listenKeyboard(self):
        pass
    def listenEvt(self):
        self.typeListener()

class _EventHandler():
    def __init__(self):
        self.listeners = []
    def addListener(self, listener: dict):
        evl = _EventListener(
            listener['type'],
            listener['name'],
            listener['callback']
        )
        self.listeners.append(evl)
    def rmListener(self, name: str):
        self.listeners = [
            lst for lst in self.listeners if lst != name
        ]
    def listen(self):
        for listener in self.listeners:
            listener.listenEvt()

_HANDLER = _EventHandler()

def setup_listener(listener: dict):
    ''' listener = {
            'type'      : EVT_TYPE,
            'name'      : str
            'callback'  : func
        }
    '''
    _HANDLER.addListener(listener)

def unset_listener(listener_name:str):
    _HANDLER.rmListener(listener_name)

def event_listening():
    _HANDLER.listen()