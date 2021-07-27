# -*- coding: utf-8 -*-

import pygame


class Background(pygame.sprite.DirtySprite):

    """Background of the image slider box.
    """

    def __init__(self, renderer):
        """
        :param renderer: render used to render the background
        :type renderer: :py:class:`SliderRenderer`
        """
        super(Background, self).__init__()
        self.renderer = renderer
        self.rect = pygame.Rect((0, 0), (10, 10))
        self.image = pygame.Surface(self.rect.size, pygame.SRCALPHA, 32)
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
        self.source = pygame.image.load(arrow_path)
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
            self.renderer.draw_arrow(self.image, self.source, self.pressed)
            self.dirty = 1

    def set_pressed(self, state):
        """Set the arrow pressed state (1 for pressed 0 for released)
        and redraws it.

        :param state: new arrow state.
        """
        if self.pressed != int(state):
            self.pressed = int(state)
            self.renderer.draw_arrow(self.image, self.source, self.pressed)
            self.dirty = 1

    def update(self, events):
        """Pygame events processing method.

        :param events: list of events to process.
        :type events: list
        """
        if self.visible == 0:
            return

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN\
                    and event.button in (1, 2, 3):
                # Don't consider the mouse wheel (button 4 & 5):
                if self.rect.collidepoint(event.pos):
                    self.set_pressed(1)
            elif event.type == pygame.MOUSEBUTTONUP\
                    and event.button in (1, 2, 3):
                # Don't consider the mouse wheel (button 4 & 5):
                self.set_pressed(0)
            elif event.type == pygame.FINGERDOWN:
                display_size = pygame.display.get_surface().get_size()
                finger_pos = (event.x * display_size[0], event.y * display_size[1])
                if self.rect.collidepoint(finger_pos):
                    self.set_pressed(1)
            elif event.type == pygame.FINGERUP:
                self.set_pressed(0)


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
        self.image_path = image_path
        if load:
            self.source = pygame.image.load(image_path)
        else:
            self.source = None
        self.rect = pygame.Rect((0, 0), (10, 10))
        self.image = pygame.Surface(self.rect.size, pygame.SRCALPHA, 32)

        self.velocity = pygame.math.Vector2(0, 0)
        self.destination = pygame.math.Vector2(0, 0)
        self._time = 0

    def set_position(self, x, y):
        """Set the slide position.

        :param x: position x
        :type x: int
        :param y: position y
        :type y: int
        """
        if self.rect.topleft != (x, y):
            self.rect.topleft = (x, y)
            self.destination.xy = (x, y)
            self._time = 0
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
            self.renderer.draw_slide(self.image, self.source, self.selected)
            self.dirty = 1

    def set_selected(self, state):
        """Set the slide selection state (1 for selected else 0)
        and redraws it.

        :param state: new key state
        :type state: int
        """
        if self.selected != int(state):
            self.selected = int(state)
            self.renderer.draw_slide(self.image, self.source, self.selected)
            self.dirty = 1

    def set_destination(self, x, y, speed):
        """Set slide destination and speed of annimation.

        :param x: X coordinate to move to
        :type x: int
        :param y: Y coordinate to move to
        :type y: int
        :param speed: animation duration in second
        :type speed: int
        """
        self._time = 0
        self.destination.xy = (x, y)
        self.velocity.xy = (x - self.rect.x, y - self.rect.y)
        self.velocity = self.velocity / speed

    def is_moving(self):
        """Return True if the slide is moving.
        """
        return self.destination.xy != self.rect.topleft

    def update(self, events, dt):
        """Pygame events processing method.

        :param events: list of events to process.
        :type events: list
        :param dt: elapsed time since last call
        :type dt: int
        """
        if not self.is_moving():
            return

        self._time += dt
        self.rect.move_ip(*self.velocity * self._time)
        if (self.velocity.x > 0 and self.rect.x > self.destination.x)\
                or (self.velocity.x < 0 and self.rect.x < self.destination.x):
            self.rect.x = self.destination.x
        if (self.velocity.y > 0 and self.rect.y > self.destination.y)\
                or (self.velocity.y < 0 and self.rect.y < self.destination.y):
            self.rect.y = self.destination.y
        self.dirty = 1
