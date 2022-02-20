class Drawable:
    """Used as an abstract base-class for every drawable element.
    """
    def __init__(self, surface):
        self.surface = surface

    def draw(self):
        pass