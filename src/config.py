import json
import os

APP_NAME        = 'Pymodoro'
APP_VERSION     = 'not released yet'
APP_DEV         = 'Blendify Games'
SCREEN_SIZE     = (1024, 768)

# res
WD              = os.path.dirname(os.path.realpath(__file__))
RESDIR          = os.path.join(WD, '..', 'res')
FONTDIR         = os.path.join(RESDIR, 'fonts')
SPRDIR          = os.path.join(RESDIR, 'sprites')
SOUNDDIR        = os.path.join(RESDIR, 'sounds')
MUSDIR          = os.path.join(RESDIR, 'musics')

def get_caption() -> str:
    return f'{APP_NAME} ({APP_VERSION}) by {APP_DEV}'

def get_font_path() -> str:
    return os.path.join(FONTDIR, '04b_30', '04B_30__.TTF')

def get_clair_de_lune_res() -> str:
    return os.path.join(MUSDIR, f'clair_de_lune.ogg')

def get_button_sound_res(nref:int) -> str:
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
