import pygame
from scenes import boot_scene, ShowPomodoroScene
from pomodoro import Pomodoro

if __name__ == '__main__':
    pygame.init()
    boot_scene(ShowPomodoroScene)
    pygame.quit()