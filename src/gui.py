import pygame
import uuid

from event_handler import (
    setup_listener, unset_listener,
    EVT_MOUSE_D
)
from config import (
    get_buttons_res, get_button_sound_res, 
    get_field_res, get_number_imgfont_res,
    get_startbutton_res
)
from util import tiledsurf_slice_from_path

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
        self.callbackButtonDown = None
        self.callbackButtonUp = None
    def kill(self):
        unset_listener(self.buttonId)
    def setButtonDownListener(self, callback:'func'):
        self.callbackButtonDown = callback
    def setButtonUpListener(self, callback:'func'):
        self.callbackButtonUp = callback
    def onButtonDown(self):
        self.image = self.img2
        self.time = pygame.time.get_ticks()
        if self.callbackButtonDown:
            self.callbackButtonDown()
    def onButtonUp(self):
        self.image = self.img1
        self.time = None
        if self.callbackButtonUp:
            self.callbackButtonUp()
    def update(self):
        if self.time:
            timelapsed = pygame.time.get_ticks()
            if timelapsed - self.time > 100:
                self.onButtonUp()

_BUTTON_FRAMES = None
def _get_button_frames() -> 'SurfList':
    global _BUTTON_FRAMES
    if not _BUTTON_FRAMES:
        _BUTTON_FRAMES = tiledsurf_slice_from_path(
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

_NUMBERS_FONT = None
def _get_numbers_font() -> 'SurfList':
    global _NUMBERS_FONT
    if not _NUMBERS_FONT:
        _NUMBERS_FONT = tiledsurf_slice_from_path(
            get_number_imgfont_res(), (32, 32), 2
        )
    return _NUMBERS_FONT

class NaturalNumberField(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)
        self.numbers = _get_numbers_font()
        self.imgbkg = pygame.image.load(get_field_res())
        self.image = self.imgbkg.copy()
        self.rect = self.image.get_rect()
        self.__value = 0
        self.__maxValue = 99
        self.__minValue = 0
        self.setValue(self.__minValue)
    def __render(self):
        vstr = f'{self.__value:02}'
        num1 = self.numbers[int(vstr[0])]
        num2 = self.numbers[int(vstr[1])]
        self.image = self.imgbkg.copy()
        self.image.blit(num1, (4, 4))
        self.image.blit(num2, (60, 4))
    def inc(self):
        self.setValue(self.__value + 1)
    def dec(self):
        self.setValue(self.__value - 1)
    def setValue(self, value:int):
        if self.__minValue <= value <= self.__maxValue:
            self.__value = value
            self.__render()
    def setMaxValue(self, maxValue: int):
        self.__maxValue = maxValue if 0 < maxValue <= 99 else 99
        if not self.__minValue <= self.__value < self.__maxValue:
            self.__value = self.__minValue
            self.__render()
    def setMinValue(self, minValue: int):
        self.__minValue = minValue if 0 <= minValue < 99 else 0
        if not self.__minValue <= self.__value < self.__maxValue:
            self.__value = self.__minValue
            self.__render()
    def getValue(self) -> int:
        return self.__value

class NaturalNumberSelector():
    def __init__(self, *groups):
        self.nnField = NaturalNumberField(*groups)
        self.arrowUp = ArrowUpButton(*groups)
        self.arrowDown = ArrowDownButton(*groups)
        self.arrowUp.setButtonUpListener(self.nnField.inc)
        self.arrowDown.setButtonDownListener(self.nnField.dec)
        self.setPos(*self.nnField.rect.topleft)
    def setPos(self, x:int, y:int):
        self.nnField.rect.topleft = (x, y)
        nnfw = self.nnField.rect.width
        self.arrowUp.rect.topleft = (x + nnfw, y + 2)
        auph = self.arrowUp.rect.height
        self.arrowDown.rect.topleft = (x + nnfw, y + auph + 6)
    def getValue(self) -> int:
        return self.nnField.getValue()
    def setValue(self, value:int):
        '''value must be 0 <= value < 100'''
        self.nnField.setValue(value)
    def setMaxValue(self, maxValue: int):
        '''maxValue must be 0 < maxValue < 100'''
        self.nnField.setMaxValue(maxValue)
    def setMinValue(self, minValue: int):
        '''minValue must be 0 <= minValue < 100'''
        self.nnField.setMinValue(minValue)

_STARTBUTTON_FRAMES = None
def _get_startbutton_frames() -> 'SurfList':
    global _STARTBUTTON_FRAMES
    if not _STARTBUTTON_FRAMES:
        _STARTBUTTON_FRAMES = tiledsurf_slice_from_path(
            get_startbutton_res(), (32, 32), 4
        )
    return _STARTBUTTON_FRAMES

_S_BUTTON_SOUND = None
def _get_start_button_sound() -> pygame.mixer.Sound:
    global _S_BUTTON_SOUND
    if not _S_BUTTON_SOUND:
        _S_BUTTON_SOUND = pygame.mixer.Sound(get_button_sound_res(2))
    return _S_BUTTON_SOUND

class StartButton(_Button):
    def __init__(self, *groups):
        self.sound = _get_start_button_sound()
        frames = _get_startbutton_frames()
        super().__init__(frames[0], frames[1], *groups)
    def onButtonDown(self):
        super().onButtonDown()
        self.sound.play()
