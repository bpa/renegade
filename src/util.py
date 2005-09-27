import os
from core import image, RLEACCEL, error

cached_images = {}

def load_image(dir, name, alpha=False, colorkey=None):
    global cached_images
    fullname = os.path.join(dir, "%s.png" % name)
    if cached_images.has_key(fullname):
        return cached_images[fullname]
    else:
        try:
            img = image.load(fullname)
        except error, message:
            print 'Cannot load image:', name
            raise SystemExit, message
        if colorkey is not None:
            if colorkey is -1:
                colorkey = img.get_at((0,0))
            img.set_colorkey(colorkey, RLEACCEL)
        if alpha: img = img.convert_alpha()
        else: img = img.convert()
        cached_images[fullname] = img
    return img
