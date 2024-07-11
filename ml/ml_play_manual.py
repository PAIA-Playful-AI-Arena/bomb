import pygame

class MLPlay:
    def __init__(self, *args, **kwargs):
        print("Initial ML script")

    def update(self, scene_info: dict, keyboard = [], *args, **kwargs):
        commands = []

        if pygame.K_LEFT in keyboard or pygame.K_a in keyboard:
            commands.append("move_left")
        elif pygame.K_RIGHT in keyboard or pygame.K_d in keyboard:
            commands.append("move_right")

        if pygame.K_UP in keyboard or pygame.K_w in keyboard:
            commands.append("move_up")
        elif pygame.K_DOWN in keyboard or pygame.K_s in keyboard:
            commands.append("move_down")
        
        if pygame.K_SPACE in keyboard:
            commands.append("place_bomb")

        return commands

    def reset(self):
        pass
