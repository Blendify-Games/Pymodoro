import json
import os

APP_NAME        = 'Pymodoro'
APP_VERSION     = 'not released yet'
SCREEN_SIZE     = (1024, 768)

# res
WD              = os.path.dirname(os.path.realpath(__file__))
RESDIR          = os.path.join(WD, '..', 'res')
FONTDIR         = os.path.join(RESDIR, 'fonts')
SPRDIR          = os.path.join(RESDIR, 'sprites')
SOUNDDIR        = os.path.join(RESDIR, 'sounds')

def get_caption():
    return f'{APP_NAME} ({APP_VERSION})'

def get_font_path():
    return os.path.join(FONTDIR, '04b_30', '04B_30__.TTF')

def get_button_sound_res(nref:int):
    return os.path.join(SOUNDDIR, f'button{nref}.ogg')

def get_buttons_res() -> str:
    return os.path.join(SPRDIR, 'buttons.png')

def get_sprite_res(name:str) -> dict:
    '''get a dict containing sprite information like animation
    and source image path'''
    jsonpath = os.path.join(SPRDIR, f'{name}.json')
    with open(jsonpath, encoding='utf-8') as fjson:
        sprite_info = json.load(fjson)
        sprite_info['imgpath'] = os.path.join(SPRDIR, f'{name}.png')
        return sprite_info
