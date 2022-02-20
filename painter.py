class Painter:
    """Used to organize the drawing/ updating procedure.
    Objects added first, are always going to be drawn first.
    """
    def __init__(self):
        self.paintings = []
    def add(self, drawable):
        self.paintings.append(drawable)

    def paint(self):
        for drawing in self.paintings:
            drawing.draw()