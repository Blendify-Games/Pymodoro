import pygame

from config import get_sprite_res
from random import randint
from util import tiledsurf_slice_from_path

class SpriteFSM(pygame.sprite.Sprite):
    def __init__(self, res_name:str, scale=1, first_anim:str='idle', *groups):
        super().__init__(*groups)
        self.sprinfo = get_sprite_res(res_name)
        frame_size = (
            self.sprinfo['frame_size'][0],
            self.sprinfo['frame_size'][1]
        )
        self.frames = tiledsurf_slice_from_path(
                        self.sprinfo['imgpath'], frame_size, scale)
        # set first image as default to avoid problems
        self.image = self.frames[0]
        self.rect = self.image.get_rect()
        self.state = None
        self.stepIndex = None
        self.stateDelta = None
        self.stateRepeat = None
        self.running = False
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
                self.running = False
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
            self.running = True
            self.__nextFrame()
    def update(self):
        if self.running and self.state:
            timelapsed = pygame.time.get_ticks() - self.__time
            if timelapsed > self.stateDelta:
                self.__nextFrame()

class Tomato(SpriteFSM):
    def __init__(self, *groups):
        super().__init__('tomato', 6, 'blink', *groups)
