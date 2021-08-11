# -*- coding: utf-8 -*-

import math
import os.path as osp
import pygame
from .layouts import SlidesLayout, SlidesLayoutLoop, SlidesLayoutFade
from .sprites import Background, Arrow, Slide, Dot
from .renderers import ImSliderRenderer

HERE = osp.dirname(osp.abspath(__file__))

# Joystick controls
JOYHAT_UP = (0, 1)
JOYHAT_LEFT = (-1, 0)
JOYHAT_RIGHT = (1, 0)
JOYHAT_DOWN = (0, -1)

# Regular slider
STYPE_SLIDE = 'slide'
# Carousel slider
STYPE_LOOP = 'loop'
# Change slides with fade transition
STYPE_FADE = 'fade'


class ImSlider(object):

    """Flexible images slider for Pygame engine.

    :param size: size of the image slider
    :type size: tuple
    :param stype: determine a slider type
    :type stype: str
    :param per_page: determine how many slides should be displayed per page. If
                     stype=STYPE_FADE, this option is ignored.
    :type per_page: int
    :param per_move: determine how many slides should be moved when a slider goes
                     to next or perv. If stype=STYPE_FADE, this option is ignored.
    :type per_move: int
    :param focus: determine which slide should be focused if there are multiple
                  slides in a page. A string "center" is acceptable for centering slides.
    :type focus: bool or str
    :param rewind: whether to rewind a slider before the first slide or after the
                   last one. If stype=STYPE_LOOP, this option is ignored.
    :type rewind: bool
    :param speed: transition duration in seconds.
    :type speed: int
    :param renderer: renderer to customize colors of the slider.
    :type renderer: :py:class:`ImSliderRenderer`
    :param callback: callback called each time the selection is changed.
    :type callback: function
    """

    def __init__(self, size, stype=STYPE_SLIDE, per_page=1, per_move=0, focus=True,
                 rewind=False, speed=0.4, renderer=ImSliderRenderer.DEFAULT, callback=None):
        self._per_page = per_page
        self._per_move = per_move
        self.clock = pygame.time.Clock()
        self.size = size
        self.stype = stype
        self.focus = focus
        self.rewind = rewind
        self.speed = speed
        self.eraser = None
        if stype == STYPE_LOOP:
            self.layout = SlidesLayoutLoop(self.per_page, self.focus)
        elif stype == STYPE_FADE:
            self.layout = SlidesLayoutFade(self.per_page, self.focus)
        else:
            self.layout = SlidesLayout(self.per_page, self.focus)

        self.callback = callback
        self.renderer = renderer
        self.background = Background(self.renderer)

        self.arrows = (Arrow(osp.join(HERE, "left.png"), self.renderer, pygame.K_LEFT),
                       Arrow(osp.join(HERE, "right.png"), self.renderer, pygame.K_RIGHT))
        self.pressed_repeat_time = 0.4

        self.sprites = pygame.sprite.LayeredDirty()
        self.sprites.add(self.background, layer=0)
        for arrow in self.arrows:
            self.sprites.add(arrow, layer=1)

        self.set_size(*self.size)

    @property
    def per_page(self):
        return self._per_page if self.stype != STYPE_FADE else 1

    @property
    def per_move(self):
        return self._per_move if self._per_move != 0 else self._per_page

    def load_images(self, images, lazy=False):
        """Load the images.

        :param images: sequence of images
        :type images: list
        :param lazy: load images only when needed
        :type lazy: bool
        """
        self.layout.empty()
        for path in images:
            self.layout.add_slide(Slide(path, self.renderer, not lazy))
        self.layout.set_position(self.background.rect.x + self.arrows[0].rect.width, self.background.rect.y)
        self.layout.set_size(self.size[0] - 2 * self.arrows[0].rect.width, self.size[1])
        self.layout.set_selection(pos=0)

        self.sprites.remove_sprites_of_layer(2)
        self.setup_pagination()

        self.update_arrows()
        self.update_pages()

    def set_eraser(self, surface):
        """Setup the surface used to hide/clear the slider.
        """
        self.eraser = surface.copy()
        self.sprites.clear(surface, self.eraser)
        self.layout.clear(surface, self.background.image)

    def setup_pagination(self):
        """Setup pagination indication (one dot per page).
        """
        nbr_pages = int(math.ceil(len(self.layout.slides) / self.per_page))
        x_margin = 5
        x = self.background.rect.centerx - (nbr_pages * self.layout.padding + (nbr_pages - 1) * x_margin) // 2
        y_margin = 4
        y = self.background.rect.bottom - self.layout.padding + y_margin
        dot_radius = self.layout.padding - 2 * y_margin
        dots = self.sprites.get_sprites_from_layer(2)

        # Update size of existing dots
        for dot in dots:
            dot.set_size(dot_radius, dot_radius)
            dot.set_position(x, y)
            x += dot.rect.width + x_margin

        # Add missing dots
        for i in range(max(0, nbr_pages - len(dots))):
            dot = Dot(osp.join(HERE, "dot.png"), self.renderer)
            self.sprites.add(dot, layer=2)
            dot.set_size(dot_radius, dot_radius)
            dot.set_position(x, y)
            x += dot.rect.width + x_margin

    def get_page_at(self, position):
        """Retrieve if any page-dot is located at the given position.

        :param position: position to check key at.
        :return: page index if any at the given position, None otherwise.
        """
        for sprite in self.sprites.get_sprites_at(position):
            if isinstance(sprite, Dot):
                return self.sprites.get_sprites_from_layer(2).index(sprite)
        return None

    def get_rect(self):
        """Return slider rect."""
        return self.background.rect

    def get_index(self):
        """Return the index of the currently selected image."""
        return self.layout.selection

    def set_index(self, index):
        """Set the current index."""
        assert 0 <= index < len(self.layout.slides), "Invalid index '{}'".format(index)
        current = self.layout.selection
        self.layout.set_selection(pos=index)
        if current < index:
            self.layout.got_to_selection_forward(self.speed, self.focus == 'center')
        else:
            self.layout.got_to_selection_backward(self.speed, self.focus == 'center')
        self.update_arrows()
        self.update_pages()
        if self.callback:
            self.callback(self.layout.selection)

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

        self.layout.set_position(self.background.rect.x + arrow_width, self.background.rect.y)
        self.layout.set_size(self.size[0] - 2 * arrow_width, self.size[1])

        self.setup_pagination()

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

        :param surface: surface the slider will be displayed at
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
        rects += self.layout.draw(surface)

        if force:
            self.sprites.repaint_rect(self.background.rect)
            self.layout.repaint_rect(self.background.rect)
        return rects

    def update(self, events):
        """Pygame events processing method.

        :param events: list of events to process.
        :type events: list
        """
        dt = self.clock.tick() / 1000  # Amount of seconds between each loop.
        self.sprites.update(events, dt)
        self.layout.update(events, dt)

        if self.layout.is_animated():
            return  # Let's finish the current animations

        if self.arrows[0].pressed_time > self.pressed_repeat_time:
            self.arrows[0].pressed_time = 0
            self.on_previous()
            return  # Left arrow stay pressed
        elif self.arrows[1].pressed_time > self.pressed_repeat_time:
            self.arrows[1].pressed_time = 0
            self.on_next()
            return  # Right arrow stay pressed

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN\
                    and event.button in (1, 2, 3):
                # Don't consider the mouse wheel (button 4 & 5)
                if self.arrows[0].visible and self.arrows[0].rect.collidepoint(event.pos):
                    self.on_previous()
                elif self.arrows[1].visible and self.arrows[1].rect.collidepoint(event.pos):
                    self.on_next()

                page = self.get_page_at(event.pos)
                if page is not None:
                    self.set_index(self.per_page * page)

            elif event.type == pygame.FINGERDOWN:
                display_size = pygame.display.get_surface().get_size()
                finger_pos = (event.x * display_size[0], event.y * display_size[1])
                if self.arrows[0].visible and self.arrows[0].rect.collidepoint(finger_pos):
                    self.on_previous()
                elif self.arrows[1].visible and self.arrows[1].rect.collidepoint(finger_pos):
                    self.on_next()

                page = self.get_page_at(event.pos)
                if page is not None:
                    self.set_index(self.per_page * page)

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.on_previous()
                elif event.key == pygame.K_RIGHT:
                    self.on_next()

            elif event.type == pygame.JOYHATMOTION:
                if self.arrows[0].visible and event.value == JOYHAT_LEFT:
                    self.on_previous()
                elif self.arrows[1].visible and event.value == JOYHAT_RIGHT:
                    self.on_next()

    def update_arrows(self):
        """Update arrows visibility. The visibility is changed only if necessary
        to avoid unwelcome surface update.
        """
        if len(self.layout.slides) == 1\
                or (len(self.layout.slides) <= self.per_page and self.per_move >= self.per_page):
            # Only one page
            for i in range(2):
                if self.arrows[i].visible:
                    self.arrows[i].visible = 0
        elif self.stype != STYPE_LOOP and not self.rewind:
            if self.layout.selection == 0 and self.arrows[0].visible:
                self.arrows[0].visible = 0

            if self.layout.selection != 0 and not self.arrows[0].visible:
                self.arrows[0].visible = 1

            if self.layout.selection == self.layout.last_idx and self.arrows[1].visible:
                self.arrows[1].visible = 0

            if self.layout.selection != self.layout.last_idx and not self.arrows[1].visible:
                self.arrows[1].visible = 1

    def update_pages(self):
        """Update pages indication.
        """
        current_page = self.layout.selection // self.per_page
        count = 0
        for dot in self.sprites.get_sprites_from_layer(2):
            if count == current_page:
                dot.set_selected(1)
            else:
                dot.set_selected(0)
            count += 1

    def on_previous(self):
        """Go to previous slide.
        """
        if self.stype == STYPE_LOOP or self.rewind:
            # Loop, don't check limites
            self.layout.set_selection(step=-self.per_move)
            self.layout.got_to_selection_backward(self.speed, self.focus == 'center')
        elif self.layout.selection - self.per_move >= 0:
            # Move to given slide
            self.layout.set_selection(step=-self.per_move)
            self.layout.got_to_selection_backward(self.speed, self.focus == 'center')
        elif self.layout.selection != 0:
            # Go to the first slide
            self.layout.set_selection(pos=0)
            self.layout.got_to_selection_backward(self.speed, self.focus == 'center')

        self.update_arrows()
        self.update_pages()
        if self.callback:
            self.callback(self.layout.selection)

    def on_next(self):
        """Go to next slide.
        """
        if self.stype == STYPE_LOOP or self.rewind:
            # Loop, don't check limites
            self.layout.set_selection(step=self.per_move)
            self.layout.got_to_selection_forward(self.speed, self.focus == 'center')
        elif self.layout.selection + self.per_move < len(self.layout.slides):
            # Move to given slide
            self.layout.set_selection(step=self.per_move)
            self.layout.got_to_selection_forward(self.speed, self.focus == 'center')
        elif self.layout.selection != self.layout.last_idx:
            # Go to the last slide
            self.layout.set_selection(pos=self.layout.last_idx)
            self.layout.got_to_selection_forward(self.speed, self.focus == 'center')

        self.update_arrows()
        self.update_pages()
        if self.callback:
            self.callback(self.layout.selection)
