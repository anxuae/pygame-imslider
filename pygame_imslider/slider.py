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
# Carousel slider
STYPE_LOOP = 'loop'
#  Change slides with fade transition. per_page option is ignored.
STYPE_FADE = 'fade'


class ImageSlider(object):

    """Flexible images slider for Pygame engine.

    :param size: size of the image slider
    :type size: tuple
    :param stype: determine a slider type
    :type stype: str
    :param per_page: determine how many slides should be displayed per page.
    :type per_page: int
    :param per_move: determine how many slides should be moved when a slider goes
                     to next or perv.
    :type per_move: int
    :param focus: determine which slide should be focused if there are multiple
                  slides in a page. A string "center" is acceptable for centering slides.
    :type focus: bool or str
    :param rewind: Whether to rewind a slider before the first slide or after the
                   last one. In "loop" mode, this option is ignored.
    :type rewind: bool
    :param speed: transition speed in seconds.
    :type speed: int
    """

    def __init__(self, size, stype=STYPE_SLIDE, per_page=1, per_move=0,
                 focus=False, rewind=True, speed=0.4, renderer=SliderRenderer.DEFAULT):
        self.size = size
        self.stype = stype
        self.per_page = per_page
        self.per_move = per_move
        self.focus = focus
        self.rewind = rewind
        self.speed = speed
        self.eraser = None

        self.renderer = renderer
        self.background = Background(self.size, self.renderer)

        here = osp.dirname(osp.abspath(__file__))
        self.arrows = (Arrow(osp.join(here, "left.png"), self.renderer),
                       Arrow(osp.join(here, "right.png"), self.renderer))

        self.sprites = pygame.sprite.LayeredDirty()
        self.sprites.add(self.background, layer=0)
        for arrow in self.arrows:
            self.sprites.add(arrow, layer=1)

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

    def set_eraser(self, surface):
        """Setup the surface used to hide/clear the keyboard.
        """
        self.eraser = surface.copy()
        self.sprites.clear(surface, self.eraser)

    def resize(self, surface):
        """Resize the keyboard according to the surface size and the parameters
        of the layout(s).

        Parameters
        ----------
        surface:
            Surface this keyboard will be displayed at.
        """
        self.size = surface.get_size()
        self.background.set_position(0, 0)
        self.background.set_size(*self.size)

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
            self.resize(surface)

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

                # Check if arrow are clicked
                pass

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
