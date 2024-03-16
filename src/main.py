import asyncio
import pygame
import sys, platform

from config import change_lang
from scenes import boot_scene, SetupPomodoroScene

# pygbag uses async and was added for webapp
# no impact on desktop app execution
async def main():
    if sys.platform == 'emscripten':
        lang = platform.window.navigator.language
        change_lang(lang.replace('-', '_'))
    pygame.init()
    scene_loop = boot_scene(SetupPomodoroScene)
    while scene_loop.runningScene:
        scene_loop.iterate()
        await asyncio.sleep(0)
    pygame.quit()

asyncio.run(main())
