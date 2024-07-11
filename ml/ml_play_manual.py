import pygame

class MLPlay:
    def __init__(self, *args, **kwargs):
        print("Initial ML script")

    def update(self, scene_info: dict, keyboard=[], *args, **kwargs):
        command = []

        if pygame.K_LEFT in keyboard or pygame.K_a in keyboard:
            command.append("move_left")
        if pygame.K_RIGHT in keyboard or pygame.K_d in keyboard:
            command.append("move_right")
        if pygame.K_UP in keyboard or pygame.K_w in keyboard:
            command.append("move_left")
        if pygame.K_DOWN in keyboard or pygame.K_s in keyboard:
            command.append("move_down")
        if pygame.K_SPACE in keyboard:
            command.append("place_bomb")

        return command

    def reset(self):
        pass
