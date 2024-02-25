import config
import event_handler as evth
import pygame

from pomodoro import Pomodoro
from sprites import Tomato
from gui import (
    ChatBalloon, NaturalNumberSelector, 
    StartButton, Label
)

class Scene():
    def __init__(self, screen: pygame.Surface, name: str):
        print(f'Running scene: {name}.')
        self.name = name
        self.screen = screen
        self.build()
    def build(self):
        raise NotImplemented
    def update(self):
        raise NotImplemented

class SetupPomodoroScene(Scene):
    def __init__(self, screen: pygame.Surface):
        super().__init__(screen, 'Setup Pomodoro')
        pygame.mixer.music.load(config.get_clair_de_lune_res())
        pygame.mixer.music.play(loops=-1)
        
        sw, sh = config.SCREEN_SIZE

        self.rendergp = pygame.sprite.Group()

        self.tomato = Tomato(self.rendergp)
        self.tomato.rect.center = sw//2, sh//2

        self.nnField1 = NaturalNumberSelector(self.rendergp)
        self.nnField1.setValue(25)
        self.nnField1.setMinValue(1)
        self.nnField1.setMaxValue(100)
        self.nnField1.setPos(96, 96)
        self.nnField2 = NaturalNumberSelector(self.rendergp)
        self.nnField2.setValue(5)
        self.nnField2.setMinValue(1)
        self.nnField2.setPos(320, 96)
        self.nnField3 = NaturalNumberSelector(self.rendergp)
        self.nnField3.setPos(544, 96)
        self.nnField4 = NaturalNumberSelector(self.rendergp)
        self.nnField4.setPos(768, 96)
        
        self.cballoon = ChatBalloon(config.get_string('lt-balloon'), self.rendergp)
        self.cballoon.setPos(32, 576)

        self.label1 = Label(config.get_string('worktime'), 
                            (255, 215, 0), self.rendergp)
        self.label1.setPos(100, 70)

        self.label2 = Label(config.get_string('breaktime'), 
                            (255, 215, 0), self.rendergp)
        self.label2.setPos(324, 70)

        self.label3 = Label(config.get_string('cblbreak'), 
                            (255, 215, 0), self.rendergp)
        self.label3.setPos(548, 70)

        self.label4 = Label(config.get_string('lbtime'), 
                            (255, 215, 0), self.rendergp)
        self.label4.setPos(772, 70)

        self.startButton = StartButton(self.rendergp)
        self.startButton.rect.bottomright = (sw - 32, sh - 48)
        self.startButton.setButtonUpListener(self.gotoNextScene)
    def gotoNextScene(self):
        pygame.mixer.music.fadeout(1000)
        self.rendergp.empty()
        boot_scene(
            ShowPomodoroScene, 
            (self.nnField1.getValue(), self.nnField2.getValue(), 
             self.nnField3.getValue(), self.nnField4.getValue())
        )
    def build(self):
        self.screen.fill((100, 0, 0))
    def update(self):
        self.screen.fill((100, 0, 0))
        self.rendergp.update()
        self.rendergp.draw(self.screen)
        pygame.display.flip()
   
class ShowPomodoroScene(Scene):
    def __init__(self, screen: pygame.Surface, pomodoro_params:tuple):
        super().__init__(screen, 'Show Pomodoro')
        self.rendergp = pygame.sprite.Group()
        self.pomodoro = Pomodoro(*pomodoro_params, self.rendergp)
    def build(self):
        self.screen.fill((100, 0, 0))
    def update(self):
        self.pomodoro.update()
        self.screen.fill((100, 0, 0))
        self.rendergp.draw(self.screen)
        pygame.display.flip()

class __SceneLoop():
    def __init__(self):
        self.screen = pygame.display.set_mode(config.SCREEN_SIZE)
        pygame.display.set_caption(config.get_caption())
        self.__runningScene = None
        evth.setup_listener({
            'type': evth.EVT_QUIT,
            'name': 'quit',
            'callback': self.__stop
        })
        self.clock = pygame.time.Clock()
    def __stop(self):
        self.__runningScene = None
    def setScene(self, SceneClass: 'Scene.__class__', *args):
        self.__runningScene = SceneClass(self.screen, *args)
        self.__run()
    def __run(self):
        while self.__runningScene:
            self.clock.tick(60)
            self.__runningScene.update()
            evth.event_listening()
            pygame.display.flip()

_SCENE_LOOP = __SceneLoop()

def boot_scene(SceneClass: 'Scene.__class__', *args):
    _SCENE_LOOP.setScene(SceneClass, *args)
