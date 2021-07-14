# -*- coding: utf-8 -*-

import os.path as osp
import pygame
from .sprites import Background, Arrow, Slide
from .renderers import SliderRenderer

# Joystick controls
JOYHAT_UP = (0, 1)
JOYHAT_LEFT = (-1, 0)
JOYHAT_RIGHT = (1, 0)
JOYHAT_DOWN = (0, -1)

# Regular slider.
STYPE_SLIDE = 'slide'
# Carousel slider. rewind is ignored
STYPE_LOOP = 'loop'
#  Change slides with fade transition. per_page option is ignored.
STYPE_FADE = 'fade'


class SlidesLayout(object):

    def __init__(self, slides, per_page, focus, padding=10):
        self.rect = pygame.Rect((0, 0), (10, 10))
        self.slides = slides
        self.per_page = per_page
        self.focus = focus
        self.padding = padding
        self.selection = 0
        self.set_selection(pos=0)

    def set_position(self, x, y):
        """Set the background position.

        :param x: position x
        :type x: int
        :param y: position y
        :type y: int
        """
        self.rect.topleft = (x, y)

    def set_size(self, width, height):
        """Set the background size.

        :param width: background width
        :type width: int
        :param height: background height
        :type height: int
        """
        self.rect.size = (width, height)
        slide_width = (width - ((1 + self.per_page) * self.padding)) // self.per_page
        slide_height = height - 2 * self.padding
        pos = self.padding
        for slide in self.slides:
            slide.set_position(self.rect.x + pos, self.rect.y + self.padding)
            slide.set_size(slide_width, slide_height)
            if pos < self.rect.width - self.padding:
                slide.visible = 1
            else:
                slide.visible = 0
            pos += slide_width + self.padding

    def set_selection(self, pos=None, step=None):
        """Change selected slide to next one.

        :param pos: got to the
        :type pos: int
        :param step: how many slides to move the selection
        :type step: int
        """
        if pos is not None and step is not None:
            raise ValueError("Both position and step can not be specified.")
        self.slides[self.selection].set_selected(0)
        if pos is not None:
            assert pos >= 0 and pos < len(self.slides)
            self.selection = pos
        if step is not None:
            self.selection += step
            if self.selection < 0:
                self.selection = len(self.slides) - 1 + self.selection
            elif self.selection > len(self.slides) - 1:
                self.selection = self.selection - (len(self.slides) - 1)

        if self.focus:
            self.slides[self.selection].set_selected(1)


class ImSlider(object):

    """Flexible images slider for Pygame engine.

    :param size: size of the image slider
    :type size: tuple
    :param stype: determine a slider type
    :type stype: str
    :param per_page: determine how many slides should be displayed per page. In
                     "fade" stype, this option is ignored.
    :type per_page: int
    :param per_move: determine how many slides should be moved when a slider goes
                     to next or perv. In "fade" stype, this option is ignored.
    :type per_move: int
    :param focus: determine which slide should be focused if there are multiple
                  slides in a page. A string "center" is acceptable for centering slides.
    :type focus: bool or str
    :param rewind: whether to rewind a slider before the first slide or after the
                   last one. In "loop" stype, this option is ignored.
    :type rewind: bool
    :param speed: transition speed in seconds.
    :type speed: int
    """

    def __init__(self, size, stype=STYPE_SLIDE, per_page=1, per_move=0, focus=True,
                 rewind=False, speed=0.4, renderer=SliderRenderer.DEFAULT):
        self.size = size
        self.stype = stype
        self.per_page = per_page
        self.per_move = per_move
        self.focus = focus
        self.rewind = rewind
        self.speed = speed
        self.eraser = None
        self.slides_layout = None

        self.renderer = renderer
        self.background = Background(self.renderer)

        here = osp.dirname(osp.abspath(__file__))
        self.arrows = (Arrow(osp.join(here, "left.png"), self.renderer),
                       Arrow(osp.join(here, "right.png"), self.renderer))

        self.sprites = pygame.sprite.LayeredDirty()
        self.sprites.add(self.background, layer=0)
        for arrow in self.arrows:
            self.sprites.add(arrow, layer=1)

        self.set_size(*self.size)

    @property
    def step(self):
        return self.per_move if self.per_move != 0 else self.per_page

    def load_images(self, images, lazy=False):
        """Load the images.

        :param images: sequence of images
        :type images: list
        :param lazy: load images only when needed
        :type lazy: bool
        """
        self.sprites.remove_sprites_of_layer(2)
        for path in images:
            self.sprites.add(Slide(path, self.renderer, not lazy), layer=2)
        self.slides_layout = SlidesLayout(self.sprites.get_sprites_from_layer(2), self.per_page, self.focus)
        self.slides_layout.set_position(self.background.rect.x + self.arrows[0].rect.width, self.background.rect.y)
        self.slides_layout.set_size(self.size[0] - 2 * self.arrows[0].rect.width, self.size[1])
        self.update_arrows()

    def set_eraser(self, surface):
        """Setup the surface used to hide/clear the keyboard.
        """
        self.eraser = surface.copy()
        self.sprites.clear(surface, self.eraser)

    def set_size(self, width, height):
        """Resize the images slider according to the given size.

        :param width: slider width
        :type width: int
        :param height: slider height
        :type height: int
        """
        self.size = (width, height)
        self.background.set_position(0, 0)
        self.background.set_size(*self.size)

        arrow_width = int(self.size[0] * 0.1 / 2)
        # Left Arrow
        self.arrows[0].set_size(arrow_width, 2 * arrow_width)
        self.arrows[0].set_position(0, self.background.rect.height // 2 - self.arrows[0].rect.height // 2)
        # Right Arrow
        self.arrows[1].set_size(arrow_width, 2 * arrow_width)
        self.arrows[1].set_position(self.background.rect.width - self.arrows[1].rect.width,
                                    self.background.rect.height // 2 - self.arrows[1].rect.height // 2)

        if self.slides_layout:
            self.slides_layout.set_position(self.background.rect.x + arrow_width, self.background.rect.y)
            self.slides_layout.set_size(self.size[0] - 2 * arrow_width, self.size[1])

        if self.sprites.get_clip() != self.background.rect:
            # Changing the clipping area will force update of all
            # sprites without using "dirty mechanism"
            self.sprites.set_clip(self.background.rect)

    def draw(self, surface=None, force=False):
        """Draw the image slider.

        This method is optimized to be called at each loop of the
        main application. It uses DirtySprite to update only parts
        of the screen that need to be refreshed.

        The first call to this method will setup the "eraser" surface that
        will be used to redraw dirty parts of the screen.

        The `force` parameter shall be used if the surface has been redrawn:
        it reset the eraser and redraw all sprites.

        :param surface: surface this keyboard will be displayed at
        :param force: force the drawing of the entire surface (time consuming)
        :type force: bool

        :return: list of updated area
        :rtype: list
        """
        # Check if surface has been resized
        if self.eraser and surface.get_rect() != self.eraser.get_rect():
            force = True  # To force creating new eraser
            self.set_size(*surface.get_size())

        # Setup eraser
        if not self.eraser or force:
            self.set_eraser(surface)

        rects = self.sprites.draw(surface)

        if force:
            self.sprites.repaint_rect(self.background.rect)
        return rects

    def update(self, events):
        """Pygame events processing method.

        :param events: list of events to process.
        :type events: list
        """
        self.sprites.update(events)

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN\
                    and event.button in (1, 2, 3):
                # Don't consider the mouse wheel (button 4 & 5)
                if self.arrows[0].rect.collidepoint(event.pos):
                    self.on_previous()

                elif self.arrows[1].rect.collidepoint(event.pos):
                    self.on_next()

            elif event.type == pygame.FINGERDOWN:
                display_size = pygame.display.get_surface().get_size()
                finger_pos = (event.x * display_size[0], event.y * display_size[1])

                # Check swipe
                pass

            elif event.type == pygame.JOYHATMOTION:
                if event.value == JOYHAT_LEFT:
                    pass
                elif event.value == JOYHAT_UP:
                    pass
                elif event.value == JOYHAT_RIGHT:
                    pass
                elif event.value == JOYHAT_DOWN:
                    pass

    def update_arrows(self):
        """Update arrows visibility.
        """
        if self.stype != STYPE_LOOP and not self.rewind:
            if self.slides_layout.selection == 0:
                if self.arrows[0].visible == 1:
                    self.arrows[0].visible = 0
                if self.slides_layout.selection != len(self.slides_layout.slides) - 1 and self.arrows[1].visible == 0:
                    self.arrows[1].visible = 1

            if self.slides_layout.selection == len(self.slides_layout.slides) - 1:
                if self.arrows[1].visible == 1:
                    self.arrows[1].visible = 0
                if self.slides_layout.selection != 0 and self.arrows[1].visible == 0:
                    self.arrows[0].visible = 1

    def on_previous(self):
        """Go to previous slide.
        """
        if self.stype == STYPE_LOOP:
            # Loop, don't check limites
            self.slides_layout.set_selection(step=-self.step)
        elif self.slides_layout.selection - self.step >= 0:
            # Move to given slide
            self.slides_layout.set_selection(step=-self.step)
        elif self.slides_layout.selection != 0:
            # Go to the first slide
            self.slides_layout.set_selection(pos=0)
        elif self.rewind:
            # Go to the last slide
            self.slides_layout.set_selection(pos=len(self.slides_layout.slides) - 1)

        self.update_arrows()

    def on_next(self):
        """Go to next slide.
        """
        if self.stype == STYPE_LOOP:
            # Loop, don't check limites
            self.slides_layout.set_selection(step=self.step)
        elif self.slides_layout.selection + self.step < len(self.slides_layout.slides):
            # Move to given slide
            self.slides_layout.set_selection(step=self.step)
        elif self.slides_layout.selection != len(self.slides_layout.slides) - 1:
            # Go to the last slide
            self.slides_layout.set_selection(pos=len(self.slides_layout.slides) - 1)
        elif self.rewind:
            # Go to the first slide
            self.slides_layout.set_selection(pos=0)

        self.update_arrows()
