import pygame
import datetime

from config import get_pixeloid_font_res
from config import SCREEN_SIZE

class _PomodoroTimeText(pygame.sprite.Sprite):
    def __init__(self, group):
        pygame.sprite.Sprite.__init__(self, group)
        self.font = pygame.font.Font(get_pixeloid_font_res(), size=50)
        self.setTime('00:00')
    def setTime(self, time):
        self.image = self.font.render(time, False, (255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_SIZE[0]//2, SCREEN_SIZE[1]//2)

class Pomodoro():
    '''
    Attributes:
        timeout  : timer is set in 'timeout' minutes (> 0),
        ival     : interval timer is 'ival' minutes (> 0),
        li_after : long interval after 'li_after' intervals 
                    (if < 1 long interval disabled),
        li_ival  : long interval timer is 'li_ival' minutes 
                    (if < 1 long interval disabled)
        gfx_group: sprite group that will contain pomodoro sprites
    '''
    def __init__(self, timeout:int=25, ival:int=5, 
                li_after:int=0, li_ival:int=0, 
                gfx_group:pygame.sprite.Group=None):
        if timeout < 1 or ival < 1:
            raise ValueError
        self.inittime = datetime.datetime.now() # when pomodoro started
        self.timeout = timeout
        self.ival = ival
        self.longIval = li_ival
        self.__sprites = []
        self.__states = [
            self.__stateWorking,
            self.__statePause
        ]
        self.__state = None
        self.__stateName = ''
        if li_after > 0 and li_ival > 0:
            for i in range(1, li_after):
                self.__states.append(self.__stateWorking)
                self.__states.append(self.__statePause)
            self.__states.append(self.__stateLongPause)
        if gfx_group != None:
            self.__buildGfx(gfx_group)
        self.__setup()
    def __setup(self):
        self.__cycleinittime = datetime.datetime.now()
        self.__lapsetime = self.__cycleinittime
        self.__state = self.__nextState()
    def __stateWorking(self) -> bool:
        self.__stateName = 'Working'
        self.__delta = self.__cycleinittime + \
                datetime.timedelta(minutes=self.timeout)        
        return self.__delta > self.__lapsetime
    def __statePause(self) -> bool:
        self.__stateName = 'Pause'
        self.__delta = self.__cycleinittime + \
                datetime.timedelta(minutes=self.ival)        
        return self.__delta > self.__lapsetime
    def __stateLongPause(self) -> bool:
        self.__stateName = 'Long Pause'
        self.__delta = self.__cycleinittime + \
                datetime.timedelta(minutes=self.longIval)        
        return self.__delta > self.__lapsetime
    def __nextState(self) -> 'state':
        state = self.__states.pop(0)
        self.__states.append(state)
        return state
    def __buildGfx(self, group):
        self.__ptt = _PomodoroTimeText(group)
    def displayInfo(self):
        t = self.__delta - self.__lapsetime
        print(f'{self.__stateName}: ', t, end='                  \r')
        m, s = divmod(t.seconds, 60)
        self.__ptt.setTime(f'{"{:0>2}".format(m)}:{"{:0>2}".format(s)}')
    def update(self):
        self.__lapsetime = datetime.datetime.now()
        if not self.__state():
            self.__cycleinittime = datetime.datetime.now()
            self.__state = self.__nextState()
        self.displayInfo()
