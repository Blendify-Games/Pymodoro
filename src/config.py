import locale
import json
import os

APP_NAME        = 'Pymodoro'
APP_VERSION     = 'v1.0.1'
APP_DEV         = 'Blendify Games'
SCREEN_SIZE     = (1024, 768)

# res
WD              = os.path.dirname(os.path.realpath(__file__))
RESDIR          = os.path.join(WD, 'res')
FONTDIR         = os.path.join(RESDIR, 'fonts')
SPRDIR          = os.path.join(RESDIR, 'sprites')
SOUNDDIR        = os.path.join(RESDIR, 'sounds')
MUSDIR          = os.path.join(RESDIR, 'musics')
STRDIR          = os.path.join(RESDIR, 'strings')
LTXDIR          = os.path.join(STRDIR, 'long-texts')


# get available system language to translate text
# if no string resource for that language, then
# en-us is default
def _get_language():
    l, e = locale.getdefaultlocale()
    if os.path.exists(os.path.join(STRDIR, f'{l}.json')):
        return (l, 'UTF-8')
    else:
        return ('en_US', 'UTF-8')
LANGUAGE, ENCODING = _get_language()

def _load_long_text(name: str) -> str:
    path = os.path.join(LTXDIR, name)
    with open(path, encoding=ENCODING) as ftxt:
        return ftxt.read()

STRINGS = None
def get_string(id:str) -> str:
    global STRINGS
    if not STRINGS:
        path = os.path.join(STRDIR, f'{LANGUAGE}.json')
        with open(path, encoding=ENCODING) as fjson:
            STRINGS = json.load(fjson)
            for k, v in STRINGS.items():
                if k.startswith('lt-'):
                    STRINGS[k] = _load_long_text(v)
    return STRINGS[id]

def get_caption() -> str:
    return f'{APP_NAME} ({APP_VERSION}) by {APP_DEV}'

def get_pixeloid_font_res() -> str:
    return os.path.join(FONTDIR, 'pixeloid-font', 'PixeloidSansBold-PKnYd.ttf')

def get_pixeloid_light_font_res() -> str:
    return os.path.join(FONTDIR, 'pixeloid-font', 'PixeloidSans-mLxMm.ttf')

def get_number_imgfont_res() -> str:
    return os.path.join(FONTDIR, 'numbers.png')

def get_clair_de_lune_res() -> str:
    return os.path.join(MUSDIR, f'clair_de_lune.ogg')

def get_countdown_sound_res() -> str:
    return os.path.join(SOUNDDIR, 'countdown.ogg')

def get_button_sound_res(nref:int) -> str:
    return os.path.join(SOUNDDIR, f'button{nref}.ogg')

def get_buttons_res() -> str:
    return os.path.join(SPRDIR, 'buttons.png')

def get_startbutton_res() -> str:
    return os.path.join(SPRDIR, 'startbutton.png')

def get_infobutton_res() -> str:
    return os.path.join(SPRDIR, 'infobutton.png')

def get_backbutton_res() -> str:
    return os.path.join(SPRDIR, 'backbutton.png')

def get_field_res() -> str:
    return os.path.join(SPRDIR, 'field.png')

def get_icon_res() -> str:
    return os.path.join(RESDIR, 'icon.png')

def get_sprite_res(name:str) -> dict:
    '''get a dict containing sprite information like animation
    and source image path'''
    jsonpath = os.path.join(SPRDIR, f'{name}.json')
    with open(jsonpath, encoding='utf-8') as fjson:
        sprite_info = json.load(fjson)
        sprite_info['imgpath'] = os.path.join(SPRDIR, f'{name}.png')
        return sprite_info
