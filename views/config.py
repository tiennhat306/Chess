import os, pygame

from utils.sound import Sound
from utils.theme import Theme

class Config:
    def __init__(self):
        self._add_themes()
        self.idx = 0
        self.theme = self.themes[self.idx]
        self.font = pygame.font.SysFont('monospace', 18, bold=True)
        self.move_sound = Sound(os.path.join('../static/sounds/move.wav'))
        self.capture_sound = Sound(os.path.join('../static/sounds/capture.wav'))
    
    def _add_themes(self):
        green = Theme((234, 235, 200), (119, 154, 88), (244, 247, 116), (172, 195, 51), '#C86464', '#C84646')
        blue = Theme((229, 228, 200), (60, 95, 135), (123, 187, 227), (43, 119, 191), '#C86464', '#C84646')

        self.themes = [
            green,
            blue,
        ]