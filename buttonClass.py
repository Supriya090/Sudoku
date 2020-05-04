import pygame

class Button:
    def __init__(self, x, y, width, height, text = None, colour = (73, 73, 73), highlightedColour = (189, 189, 189), function = None, params = None):
        self.image = pygame.Surface((width, height))
        self.pos = (x, y)
        self.rect = self.image.get_rect()
        self.rect.topleft = self.pos
        self.text = text
        self.colour = colour
        self.highlightedColour = highlightedColour
        self.function = function
        self.params = params
        self.highlighted = False

    def update(self, mouse):
        if self.rect.collidepoint(mouse):
            self.highlighted = True
        else:
            self.highlighted = False

    def draw(self, window):
        if self.highlighted:
            self.image.fill(self.highlightedColour)
        else:
            self.image.fill(self.colour)
        window.blit(self.image, self.pos)