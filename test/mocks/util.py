import os
from pygame import Surface

class mock_surface:
    def __init__(*args):
      pass

    def convert(self):
      pass

def load_image(dir, name, alpha=False, colorkey=None):
    return mock_surface((5,5))
