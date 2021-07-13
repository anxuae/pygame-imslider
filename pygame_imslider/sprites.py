# -*- coding: utf-8 -*-

import pygame


class Background(pygame.sprite.DirtySprite):

    """Background of the image slider box.
    """

    def __init__(self, size, renderer):
        """
        :param size: size tuple (width, height) of the background
        :type size: tuple
        :param renderer: render used to render the background
        :type renderer: :py:class:`SliderRenderer`
        """
        super(Background, self).__init__()
        self.renderer = renderer
        self.image = pygame.Surface(size, pygame.SRCALPHA, 32)
        self.rect = pygame.Rect((0, 0), size)

        self.renderer.draw_background(self.image)

    def set_position(self, x, y):
        """Set the background position.

        :param x: position x
        :type x: int
        :param y: position y
        :type y: int
        """
        if self.rect.topleft != (x, y):
            self.rect.topleft = (x, y)
            self.dirty = 1

    def set_size(self, width, height):
        """Set the background size.

        :param width: background width
        :type width: int
        :param height: background height
        :type height: int
        """
        if self.rect.size != (width, height):
            self.rect.size = (width, height)
            self.image = pygame.Surface((width, height), pygame.SRCALPHA, 32)
            self.renderer.draw_background(self.image)
            self.dirty = 1

class Arrow(pygame.sprite.DirtySprite):
    """
    Arrow sprite.

    Holds arrow information and its state, size / position.

    pressed = 0
        If set to 0, the arrow is released.
        If set to 1, the arrow is pressed.
    """

    def __init__(self, arrow_path, renderer):
        """
        :param arrow_path: path to the arrow image shape
        :type arrow_path: str
        :param renderer: render used to render the arrow
        :type renderer: :py:class:`SliderRenderer`
        """
        super(Arrow, self).__init__()
        self.renderer = renderer
        self.pressed = 0
        self.arrow = pygame.image.load(arrow_path)
        self.rect = pygame.Rect((0, 0), (10, 10))
        self.image = pygame.Surface(self.rect.size, pygame.SRCALPHA, 32)

    def set_position(self, x, y):
        """Set the arrow position.

        :param x: position x
        :type x: int
        :param y: position y
        :type y: int
        """
        if self.rect.topleft != (x, y):
            self.rect.topleft = (x, y)
            self.dirty = 1

    def set_size(self, width, height):
        """Set the arrow size.

        :param width: arrow width
        :type width: int
        :param height: arrow height
        :type height: int
        """
        if self.rect.size != (width, height):
            self.rect.size = (width, height)
            self.image = pygame.Surface(self.rect.size, pygame.SRCALPHA, 32)
            self.renderer.draw_arrow(self.image, self.arrow)
            self.dirty = 1

    def set_pressed(self, state):
        """Set the arrow pressed state (1 for pressed 0 for released)
        and redraws it.

        :param state: new arrow state.
        """
        if self.pressed != int(state):
            self.pressed = int(state)
            self.renderer.draw_arrow(self.image, self.arrow)
            self.dirty = 1


class Slide(pygame.sprite.DirtySprite):
    """
    Slide sprite.

    Holds arrow information and its state, size / position.

    selected = 0
        If set to 0, the key is selectable but not selected.
        If set to 1, the key is selected.
    """

    def __init__(self, image_path, renderer, load=True):
        """
        :param image_path: path to the image displayed in the slide
        :type image_path: str
        :param renderer: render used to render the arrow
        :type renderer: :py:class:`SliderRenderer`
        :param load: load image when initialize class
        :type load: bool
        """
        super(Slide, self).__init__()
        self.renderer = renderer
        self.selected = 0
        if load:
            self.source = pygame.image.load(image_path)
        else:
            self.source = None
        self.rect = pygame.Rect((0, 0), (10, 10))
        self.image = pygame.Surface(self.rect.size, pygame.SRCALPHA, 32)

    def set_position(self, x, y):
        """Set the slide position.

        :param x: position x
        :type x: int
        :param y: position y
        :type y: int
        """
        if self.rect.topleft != (x, y):
            self.rect.topleft = (x, y)
            self.dirty = 1

    def set_size(self, width, height):
        """Set the slide size.

        :param width: slide width
        :type width: int
        :param height: slide height
        :type height: int
        """
        if self.rect.size != (width, height):
            self.rect.size = (width, height)
            self.image = pygame.Surface(self.rect.size, pygame.SRCALPHA, 32)
            self.renderer.draw_slide(self.image, self.selected)
            self.dirty = 1
