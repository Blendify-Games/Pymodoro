import pygame
from config import (
    get_pixeloid_font_res, get_string,
    get_countdown_sound_res
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
        #print(f'{self.__stateName}: {self.__rText}', end=' '*10 + '\r')
        return self.__timeLap < (minutes * 60000)
    def __render(self):
        if self.__nextrText != self.__rText:
            self.__rText = self.__nextrText
            self.image = self.__font.render(self.__rText, True, (0, 0, 0))
    def getTimeStamp(self) -> str:
        return self.__rText
    def update(self):
        if self.__state and not self.__state():
            self.__nextState()
            if self.__onChangeState:
                self.__onChangeState(self.__stateName)
        self.__render()

_COUNTDOWN_SOUND = None
def _get_countdown_sound() -> pygame.mixer.Sound:
    global _COUNTDOWN_SOUND
    if not _COUNTDOWN_SOUND:
        _COUNTDOWN_SOUND = pygame.mixer.Sound(get_countdown_sound_res())
    return _COUNTDOWN_SOUND

class PomodoroSocket(SpriteFSM):
    def __init__(self, *groups):
        super().__init__('timer', 2, 'idle', *groups)
        self.sound = _get_countdown_sound()
        self.pomodoro = Pomodoro(*groups)
        self.label = Label('---------', (255, 215, 0), 14, *groups)
        self.pomodoro.setOnChangeState(self.__onChangeState)
        self.setPos(0, 0)
        self.__status = {
            get_string('working'): 0,
            get_string('break'): 0,
            get_string('longbreak'): 0
        }
        self.__lastState = None
        self.__statusUpdateListener = None
        self.__canPlayCountdownSound = True
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
    def setStatusUpdateListener(self, callback:'function'):
        '''callback must be calback(status:str)'''
        self.__statusUpdateListener = callback
    def statusToStr(self):
        u = get_string('untilnow')
        w = get_string('working')
        b = get_string('break')
        lb = get_string('longbreak')
        mt = get_string('m_times')
        ot = get_string('1_time')
        wv = self.__status[w]
        bv = self.__status[b]
        lbv = self.__status[lb]
        return f'{u}\n\n{w}: {wv} {ot if wv == 1 else mt}.\n' + \
               f'{b}: {bv} {ot if bv == 1 else mt}.\n' + \
               f'{lb}: {lbv} {ot if lbv == 1 else mt}.'
    def __onChangeState(self, state:str):
        self.label.setText(f'{state}...')
        if self.__lastState:
            self.__status[self.__lastState] += 1
        self.__lastState = state
        if self.__statusUpdateListener:
            self.__statusUpdateListener(self.statusToStr())
        self.__canPlayCountdownSound = True
    def setPos(self, x:int, y:int):
        self.rect.topleft = x, y
        self.pomodoro.rect.topleft = x + 45, y + 108
        self.label.setPos(x + 20, y + 218)
    def update(self):
        super().update()
        if self.__canPlayCountdownSound and \
            self.pomodoro.getTimeStamp() == '00:03':
            self.sound.play()
            self.__canPlayCountdownSound = False
