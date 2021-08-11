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

    By default pressed = 0
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
        self.pressed_time = 0
        self.rect = pygame.Rect((0, 0), (10, 10))
        self.image = pygame.Surface(self.rect.size, pygame.SRCALPHA, 32)
        self.image_source = pygame.image.load(arrow_path)

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
            self.renderer.draw_arrow(self.image, self.image_source, self.pressed)
            self.dirty = 1

    def set_pressed(self, state):
        """Set the arrow pressed state (1 for pressed 0 for released)
        and redraws it.

        :param state: new arrow state.
        """
        if self.pressed != int(state):
            self.pressed = int(state)
            self.renderer.draw_arrow(self.image, self.image_source, self.pressed)
            self.dirty = 1

    def update(self, events, dt):
        """Pygame events processing method.

        :param events: list of events to process.
        :type events: list
        :param dt: elapsed time since last call
        :type dt: int
        """
        if self.pressed:
            self.pressed_time += dt

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN\
                    and event.button in (1, 2, 3):
                # Don't consider the mouse wheel (button 4 & 5):
                if self.rect.collidepoint(event.pos) and self.visible:
                    self.set_pressed(1)
            elif event.type == pygame.MOUSEBUTTONUP\
                    and event.button in (1, 2, 3):
                # Don't consider the mouse wheel (button 4 & 5):
                self.set_pressed(0)
                self.pressed_time = 0
            elif event.type == pygame.FINGERDOWN:
                display_size = pygame.display.get_surface().get_size()
                finger_pos = (event.x * display_size[0], event.y * display_size[1])
                if self.rect.collidepoint(finger_pos) and self.visible:
                    self.set_pressed(1)
            elif event.type == pygame.FINGERUP:
                self.set_pressed(0)
                self.pressed_time = 0


class Dot(pygame.sprite.DirtySprite):

    image_source = None

    def __init__(self, dot_path, renderer):
        super(Dot, self).__init__()
        self.renderer = renderer
        self.pressed = 0
        self.selected = 0
        self.rect = pygame.Rect((0, 0), (10, 10))
        self.image = pygame.Surface(self.rect.size, pygame.SRCALPHA, 32)
        if not Dot.image_source:
            # Load image only one time to save memory
            Dot.image_source = pygame.image.load(dot_path)

    def set_position(self, x, y):
        """Set the dot position.

        :param x: position x
        :type x: int
        :param y: position y
        :type y: int
        """
        if self.rect.topleft != (x, y):
            self.rect.topleft = (x, y)
            self.dirty = 1

    def set_size(self, width, height):
        """Set the dot size.

        :param width: arrow width
        :type width: int
        :param height: arrow height
        :type height: int
        """
        if self.rect.size != (width, height):
            self.rect.size = (width, height)
            self.image = pygame.Surface(self.rect.size, pygame.SRCALPHA, 32)
            self.renderer.draw_dot(self.image, self.image_source, self.selected, self.pressed)
            self.dirty = 1

    def set_selected(self, state):
        """Set the dot selected state (1 for selected 0 for unselected)
        and redraws it.

        :param state: new dot state.
        """
        if self.selected != int(state):
            self.selected = int(state)
            self.renderer.draw_dot(self.image, self.image_source, self.selected, self.pressed)
            self.dirty = 1

    def set_pressed(self, state):
        """Set the dot pressed state (1 for pressed, 0 for released)
        and redraws it.

        :param state: new arrow state.
        """
        if self.pressed != int(state):
            self.pressed = int(state)
            self.renderer.draw_dot(self.image, self.image_source, self.selected, self.pressed)
            self.dirty = 1

    def update(self, events, dt):
        """Pygame events processing method.

        :param events: list of events to process.
        :type events: list
        :param dt: elapsed time since last call
        :type dt: int
        """
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN\
                    and event.button in (1, 2, 3):
                # Don't consider the mouse wheel (button 4 & 5):
                if self.rect.collidepoint(event.pos) and self.visible:
                    self.set_pressed(1)
            elif event.type == pygame.MOUSEBUTTONUP\
                    and event.button in (1, 2, 3):
                # Don't consider the mouse wheel (button 4 & 5):
                self.set_pressed(0)
            elif event.type == pygame.FINGERDOWN:
                display_size = pygame.display.get_surface().get_size()
                finger_pos = (event.x * display_size[0], event.y * display_size[1])
                if self.rect.collidepoint(finger_pos) and self.visible:
                    self.set_pressed(1)
            elif event.type == pygame.FINGERUP:
                self.set_pressed(0)


class Slide(pygame.sprite.DirtySprite):
    """
    Slide sprite.

    Holds slide information and its state, size / position.

    By default selected = 0
        If set to 0, the key is not selected.
        If set to 1, the key is selected.
    """

    def __init__(self, image_path, renderer, load=True, parent=None):
        """
        :param image_path: path to the image displayed in the slide
        :type image_path: str
        :param renderer: render used to render the arrow
        :type renderer: :py:class:`SliderRenderer`
        :param load: load image when initialize class
        :type load: bool
        :param parent: parent of the clone
        :type parent: :py:class:`Slide`
        """
        super(Slide, self).__init__()
        self.parent = parent
        if not parent:
            self._renderer = renderer
            self._selected = 0
            self._image_path = image_path
            if load:
                self._image_source = pygame.image.load(image_path).convert()
            else:
                self._image_source = None
            #     font = pygame.font.Font(pygame.font.match_font('arial'), 30)
            #     self._image_source = font.render(image_path, True, (0, 200, 0))

        # Attributes than can differe from parents
        self.rect = pygame.Rect((0, 0), (10, 10))
        self.image = pygame.Surface(self.rect.size, pygame.SRCALPHA, 32)
        self.animations = []

    def __repr__(self):
        return "Slide({}, clone={})".format(self.image_path, self.parent is not None)

    @property
    def renderer(self):
        if self.parent:
            return self.parent.renderer
        return self._renderer

    @property
    def selected(self):
        if self.parent:
            return self.parent.selected
        return self._selected

    @property
    def image_path(self):
        if self.parent:
            return self.parent.image_path
        return self._image_path

    @property
    def image_source(self):
        if self.parent:
            return self.parent.image_source
        return self._image_source

    def clone(self):
        """Return a clone of the slide. A clone has the same attributes than its parent
        but can have different:
         - size
         - position
         - animations
        """
        clone = Slide('', '', parent=self)
        clone.set_position(*self.rect.topleft)
        clone.set_size(*self.rect.size)
        return clone

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
            self.renderer.draw_slide(self.image, self.image_source, self.selected)
            self.dirty = 1

    def set_selected(self, state):
        """Set the slide selection state (1 for selected else 0)
        and redraws it.

        :param state: new key state
        :type state: int
        """
        if self._selected != int(state):
            self._selected = int(state)
            self.renderer.draw_slide(self.image, self.image_source, self.selected)
            self.dirty = 1

    def set_alpha(self, alpha):
        """Set slide transparency.
        """
        if alpha != self.image.get_alpha():
            self.image.set_alpha(alpha)
            self.dirty = 1

    def add_animation(self, animation):
        """Add a new animation. Animations are apply according to the add
        order. When finished, animation is discarded.
        """
        self.animations.append(animation)

    def is_animated(self):
        """Return True if the slide is currently animated.
        """
        return len(self.animations) > 0

    def update(self, events, dt):
        """Update slide according to current animations.

        :param events: list of events to process.
        :type events: list
        :param dt: elapsed time since last call
        :type dt: int
        """
        for animation in self.animations[:]:
            animation(self, dt)
            if animation.finished:
                self.animations.remove(animation)
