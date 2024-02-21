import pygame
import uuid

from event_handler import (
    setup_listener, unset_listener,
    EVT_MOUSE_D
)
from config import (
    get_sprite_res, get_buttons_res,
    get_button_sound_res
)
from random import randint

def _tiledsurf_slice(surf: pygame.Surface, 
                     tilewh: tuple) -> 'SurfList':
    surfs = []
    w, h = surf.get_size()
    rect = pygame.Rect(0, 0, tilewh[0], tilewh[1])
    for i in range(0, h//tilewh[1]):
        for j in range(0, w//tilewh[0]):
            rect.topleft = j*tilewh[0], i*tilewh[1]
            surfs.append(surf.subsurface(rect))
    return surfs

def _tiledsurf_slice_from_path(path: str,
                               tilewh: tuple,
                               scale: 'tuple or int' = (1, 1)) -> 'SurfList':
    surf = pygame.image.load(path)
    surf.convert_alpha()
    scale = (scale, scale) if type(scale) == int else scale
    if scale[0] > 1 or scale[1] > 1:
        tilewh = (
            tilewh[0] * scale[0],
            tilewh[1] * scale[1]
        )
        surf = pygame.transform.scale_by(surf, scale)
    return _tiledsurf_slice(surf, tilewh)

class _SpriteFSM(pygame.sprite.Sprite):
    def __init__(self, res_name:str, scale=1, first_anim:str='idle', *groups):
        super().__init__(*groups)
        self.sprinfo = get_sprite_res(res_name)
        frame_size = (
            self.sprinfo['frame_size'][0],
            self.sprinfo['frame_size'][1]
        )
        self.frames = _tiledsurf_slice_from_path(
                        self.sprinfo['imgpath'], frame_size, scale)
        # set first image as default to avoid problems
        self.image = self.frames[0]
        self.rect = self.image.get_rect()
        self.state = None
        self.stepIndex = None
        self.stateDelta = None
        self.stateRepeat = None
        self.__time = None
        self.callState(first_anim)
    def __nextFrame(self):
        fref = self.sprinfo[self.state]['frames']
        self.stepIndex += 1
        if self.stepIndex == len(fref):
            self.stepIndex = 0
            if self.stateRepeat:
                self.stateRepeat -= 1
            elif 'next_state' in self.sprinfo[self.state]:
                self.callState(self.sprinfo[self.state]['next_state'])
                return
            else:
                return
        self.image = self.frames[fref[self.stepIndex]]
        self.stateDelta = self.sprinfo[self.state]['delta'][self.stepIndex]
        self.__time = pygame.time.get_ticks()
    def callState(self, state_name:str):
        if state_name in self.sprinfo:
            self.state = state_name
            self.stepIndex = 0
            repeat = self.sprinfo[self.state]['repeat']
            if type(repeat) == list:
                self.stateRepeat = randint(repeat[0], repeat[1])
            else:
                self.stateRepeat = repeat
            self.__nextFrame()
    def update(self):
        if self.state:
            timelapsed = pygame.time.get_ticks() - self.__time
            if timelapsed > self.stateDelta:
                self.__nextFrame()

class Tomato(_SpriteFSM):
    def __init__(self, *groups):
        super().__init__('tomato', 6, 'blink', *groups)

class _Button(pygame.sprite.Sprite):
    def __init__(self,
                state_released_surf: pygame.Surface,
                state_pressed_surf: pygame.Surface,
                *groups):
        super().__init__(*groups)
        self.img1 = state_released_surf
        self.img2 = state_pressed_surf
        self.image = self.img1
        self.rect = self.image.get_rect()
        self.buttonId = uuid.uuid4().hex
        self.time = None
        setup_listener({
            'type'      : EVT_MOUSE_D,
            'name'      : self.buttonId,
            'callback'  : self.onButtonDown,
            'mouse_area': self.rect
        })
    def kill(self):
        unset_listener(self.buttonId)
    def onButtonDown(self):
        self.image = self.img2
        self.time = pygame.time.get_ticks()
    def onButtonUp(self):
        self.image = self.img1
        self.time = None
    def update(self):
        if self.time:
            timelapsed = pygame.time.get_ticks()
            if timelapsed - self.time > 100:
                self.onButtonUp()

_BUTTON_FRAMES = None
def _get_button_frames() -> 'SurfList':
    global _BUTTON_FRAMES
    if not _BUTTON_FRAMES:
        _BUTTON_FRAMES = _tiledsurf_slice_from_path(
            get_buttons_res(), (32, 32), 1
        )
    return _BUTTON_FRAMES

_A_BUTTON_SOUND = None
def _get_arrow_button_sound() -> pygame.mixer.Sound:
    global _A_BUTTON_SOUND
    if not _A_BUTTON_SOUND:
        _A_BUTTON_SOUND = pygame.mixer.Sound(get_button_sound_res(1))
    return _A_BUTTON_SOUND

class ArrowUpButton(_Button):
    def __init__(self, *groups):
        self.sound = _get_arrow_button_sound()
        frames = _get_button_frames()
        super().__init__(
            frames[0], frames[1], *groups
        )
    def onButtonDown(self):
        super().onButtonDown()
        self.sound.play()

class ArrowDownButton(_Button):
    def __init__(self, *groups):
        self.sound = _get_arrow_button_sound()
        frames = _get_button_frames()
        super().__init__(
            frames[2], frames[3], *groups
        )
    def onButtonDown(self):
        super().onButtonDown()
        self.sound.play()
