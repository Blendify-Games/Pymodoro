import pygame
from config import (
    get_pixeloid_font_res, get_string,
    get_pixeloid_light_font_res
)
from sprites import SpriteFSM
from gui import Label

class Pomodoro(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)
        self.wt, self.bt, self.lbt = None, None, None
        self.__font = pygame.font.Font(get_pixeloid_font_res(), 50)
        self.__rText = ''
        self.__nextrText = '00:00'
        self.__state = None
        self.__stateName = None
        self.__states = []
        self.__onChangeState = None
        self.__time = None
        self.__timeLap = None
        self.__render() #image + rect produced here
        self.rect = self.image.get_rect()
    def start(self, wt:int=25, bt:int=5, 
              cblb:int=0, lbt:int=0):
        '''
        The time here is in minutes.
            wt      : work time (> 0, def: 25),
            bt      : break time (> 0, def: 5),
            cblb    : cycles before long break (if < 1 disabled),
            lbt     : long break time (if < 1 disabled)
        '''
        if wt < 1 or bt < 1:
            raise ValueError
        self.wt = wt
        self.bt = bt
        self.lbt = lbt
        if cblb > 0 and self.lbt > 0:
            self.__states.append(self.__work)
            for _ in range(0, cblb):
                self.__states.append(self.__break)
                self.__states.append(self.__work)
            self.__states.append(self.__longBreak)
        else:
            self.__states = [self.__work, self.__break]
        self.__nextState()
        if self.__onChangeState:
            self.__onChangeState(self.__stateName)
    def setOnChangeState(self, callback:'function'):
        '''callback must be: callback(state:str)'''
        self.__onChangeState = callback
    def __resetTime(self):
        self.__time = pygame.time.get_ticks()
        self.__timeLap = self.__time
    def __work(self) -> bool:
        self.__stateName = get_string('working')
        return self.__timeDone(self.wt)
    def __break(self) -> bool:
        self.__stateName = get_string('break')
        return self.__timeDone(self.bt)
    def __longBreak(self) -> bool:
        self.__stateName = get_string('longbreak')
        return self.__timeDone(self.lbt)
    def __nextState(self):
        self.__state = self.__states.pop(0)
        self.__states.append(self.__state)
        self.__resetTime()
        self.__state()
    def __timeDone(self, minutes:int) -> bool:
        self.__timeLap = pygame.time.get_ticks() - self.__time
        secondsLap = (minutes * 60) - (self.__timeLap // 1000)
        mins, secs = divmod(secondsLap, 60)
        self.__nextrText = '{:02d}:{:02d}'.format(mins, secs)
        print(f'{self.__stateName}: {self.__rText}', end=' '*10 + '\r')
        return self.__timeLap < (minutes * 60000)
    def __render(self):
        if self.__nextrText != self.__rText:
            self.__rText = self.__nextrText
            self.image = self.__font.render(self.__rText, True, (0, 0, 0))
    def update(self):
        if self.__state and not self.__state():
            self.__nextState()
            if self.__onChangeState:
                self.__onChangeState(self.__stateName)
        self.__render()

class PomodoroSocket(SpriteFSM):
    def __init__(self, *groups):
        super().__init__('timer', 2, 'idle', *groups)
        self.pomodoro = Pomodoro(*groups)
        self.label = Label('---------', (255, 215, 0), 14, *groups)
        self.pomodoro.setOnChangeState(self.__onChangeState)
        self.setPos(0, 0)
    def startPomodoro(self, *args):
        '''
        startPomodoro(wt, bt, cblb, lbt)
        The time here is in minutes.
            wt      : work time (> 0, def: 25),
            bt      : break time (> 0, def: 5),
            cblb    : cycles before long break (if < 1 disabled),
            lbt     : long break time (if < 1 disabled)
        '''
        self.pomodoro.start(*args)
        self.callState('run')
    def __onChangeState(self, state:str):
        self.label.setText(f'{state}...')
    def setPos(self, x:int, y:int):
        self.rect.topleft = x, y
        self.pomodoro.rect.topleft = x + 45, y + 108
        self.label.setPos(x + 20, y + 218)
