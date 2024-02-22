import pygame
from scenes import boot_scene, SetupPomodoroScene

if __name__ == '__main__':
    pygame.init()
    boot_scene(SetupPomodoroScene)
    pygame.quit()