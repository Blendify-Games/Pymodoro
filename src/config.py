import json
import os

APP_NAME        = 'Pymodoro'
APP_VERSION     = 'not released yet'
SCREEN_SIZE     = (1024, 768)

# res
WD              = os.path.dirname(os.path.realpath(__file__))
RESDIR          = os.path.join(WD, '..', 'res')
FONTDIR         = os.path.join(RESDIR, 'font')
SPRDIR          = os.path.join(RESDIR, 'sprites')

def get_caption():
    return f'{APP_NAME} ({APP_VERSION})'

def get_font_path():
    return os.path.join(FONTDIR, '04b_30', '04B_30__.TTF')

def get_sprite_res(name:str) -> dict:
    '''get a dict containing sprite information like animation
    and source image path'''
    jsonpath = os.path.join(SPRDIR, f'{name}.json')
    with open(jsonpath, encoding='utf-8') as fjson:
        sprite_info = json.load(fjson)
        sprite_info['imgpath'] = os.path.join(SPRDIR, f'{name}.png')
        return sprite_info
