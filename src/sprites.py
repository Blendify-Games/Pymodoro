import pygame

from config import get_sprite_res
from random import randint

def _tiledsurf_slice(surf: pygame.Surface, 
                      tilewh: tuple) -> "SurfList":
    surfs = []
    w, h = surf.get_size()
    rect = pygame.Rect(0, 0, tilewh[0], tilewh[1])
    for i in range(0, h//tilewh[1]):
        for j in range(0, w//tilewh[0]):
            rect.topleft = j*tilewh[0], i*tilewh[1]
            surfs.append(surf.subsurface(rect))
    return surfs

class SpriteFSM(pygame.sprite.Sprite):
    def __init__(self, res_name:str, scale=1, first_anim:str='idle', *groups):
        super().__init__(*groups)
        self.sprinfo = get_sprite_res(res_name)
        sprsurf = pygame.image.load(self.sprinfo['imgpath'])
        sprsurf.convert_alpha()
        sprsurf = pygame.transform.scale_by(sprsurf, scale)
        frame_size = (
            self.sprinfo['frame_size'][0] * scale,
            self.sprinfo['frame_size'][1] * scale
        )
        self.frames = _tiledsurf_slice(sprsurf, frame_size)
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

class Tomato(SpriteFSM):
    def __init__(self, *groups):
        super().__init__('tomato', 6, 'blink', *groups)
    def update(self):
        super().update()
