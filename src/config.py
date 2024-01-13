import os

APP_NAME        = 'Pymodoro'
APP_VERSION     = 'not released yet'
SCREEN_SIZE     = (1024, 768)

# res
WD              = os.path.dirname(os.path.realpath(__file__))
RESDIR          = os.path.join(WD, '..', 'res')
FONTDIR         = os.path.join(RESDIR, 'font')

def get_font_path():
    return os.path.join(FONTDIR, '04b_30', '04B_30__.TTF')

def get_caption():
    return f'{APP_NAME} ({APP_VERSION})'
