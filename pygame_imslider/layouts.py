# -*- coding: utf-8 -*-

import pygame
import pygame_imslider.animations as anim


class SlidesLayout(pygame.sprite.LayeredDirty):

    def __init__(self, per_page, focus, padding=10):
        super(SlidesLayout, self).__init__()
        self.rect = pygame.Rect((0, 0), (10, 10))
        self.per_page = per_page
        self.focus = focus
        self.padding = padding
        self.selection = 0
        self.set_clip(pygame.Rect((0, 0), (10, 10)))

    @property
    def last_idx(self):
        """Return last index.
        """
        return len(self.sprites()) - 1

    def update_slide_sizes(self):
        """Update slides size and position.
        """
        width, height = self.rect.size
        slide_width = (width - ((1 + self.per_page) * self.padding)) // self.per_page
        slide_height = height - 2 * self.padding
        pos = self.padding
        for slide in self.sprites():
            slide.set_position(self.rect.x + pos, self.rect.y + self.padding)
            slide.set_size(slide_width, slide_height)
            pos += slide_width + self.padding

    def set_position(self, x, y):
        """Set the background position.

        :param x: position x
        :type x: int
        :param y: position y
        :type y: int
        """
        self.rect.topleft = (x, y)
        self.get_clip().topleft = (x + self.padding, y + self.padding)

    def set_size(self, width, height):
        """Set the background size.

        :param width: background width
        :type width: int
        :param height: background height
        :type height: int
        """
        self.rect.size = (width, height)
        self.get_clip().size = (width - 2 * self.padding, height - 2 * self.padding)
        self.update_slide_sizes()

    def set_selection(self, pos=None, step=None):
        """Change selected slide to next one.

        :param pos: got to the
        :type pos: int
        :param step: how many slides to move the selection
        :type step: int
        """
        if pos is not None and step is not None:
            raise ValueError("Both position and step can not be specified.")

        if self.sprites():
            self.get_sprite(self.selection).set_selected(0)
            if pos is not None:
                assert pos >= 0 and pos < len(self.sprites())
                self.selection = pos
            if step is not None:
                self.selection += step
                self.selection %= len(self.sprites())

            if self.focus:
                self.get_sprite(self.selection).set_selected(1)

    def is_animated(self):
        """Return True if only one slide is currently annimated.
        """
        for slide in self.sprites():
            if slide.is_animated():
                return True
        return False

    def get_visibles(self):
        """Return the list of visible slide indexes.
        """
        return [idx for idx, slide in enumerate(self.sprites())
                if self.get_clip().colliderect(slide.rect) and slide.visible]

    def got_to_selection_forward(self, duration, center=False):
        """Move forward all slides to ensure that selection is visible.

        :param duration: animation duration in second (0 = instantaneous)
        :type duration: int
        :param center: center on surface the selected slide (when possible)
        :type center: bool
        """
        visibles = self.get_visibles()
        if center:
            current = visibles[len(visibles) // 2]
        else:
            current = visibles[0]

        step = current - self.selection
        if step < 0:
            # Ensure to not go after last index
            step = max(step, visibles[-1] - self.last_idx)

        if step > 0:
            # Fast backward to begining
            step = min(step, len(self.sprites()) - len(visibles))

        for slide in self.sprites():
            pos = slide.rect.x + step * (slide.rect.width + self.padding)
            slide.add_animation(anim.Transpose(pos, slide.rect.y, duration))

    def got_to_selection_backward(self, duration, center=False):
        """Move backward all slides to ensure that selection is visible.

        :param duration: animation duration in second (0 = instantaneous)
        :type duration: int
        :param center: center on surface the selected slide (when possible)
        :type center: bool
        """
        visibles = self.get_visibles()
        if center:
            current = visibles[len(visibles) // 2]
        else:
            current = visibles[0]

        step = current - self.selection
        if step > 0:
            # Ensure to not go after first index
            step = min(step, visibles[0])

        if step < 0:
            # Fast forward to the end
            step = max(step, visibles[-1] - self.last_idx)

        for slide in self.sprites():
            pos = slide.rect.x + step * (slide.rect.width + self.padding)
            slide.add_animation(anim.Transpose(pos, slide.rect.y, duration))


class SlidesLayoutLoop(SlidesLayout):

    pass


class SlidesLayoutFade(SlidesLayout):

    def update_slide_sizes(self):
        for slide in self.sprites():
            width, height = self.rect.size
            slide.set_position(self.rect.x + self.padding, self.rect.y + self.padding)
            slide.set_size(width - 2 * self.padding, height - 2 * self.padding)
            if slide == self.sprites()[0]:
                slide.visible = 1
            else:
                slide.visible = 0

    def got_to_selection_forward(self, duration, center=False):
        current_idx = self.get_visibles()[0]
        current = self.sprites()[current_idx]
        if not current.visible:
            current.visible = 1
        selected = self.sprites()[self.selection]
        if not selected.visible:
            selected.visible = 1

        if current == self.sprites()[-1]:
            selected.set_alpha(255)
            current.add_animation(anim.Fade(0, duration))
        else:
            current.add_animation(anim.Exit(duration))
            selected.set_alpha(0)
            selected.add_animation(anim.Fade(255, duration, False))

    def got_to_selection_backward(self, duration, center=False):
        current_idx = self.get_visibles()[0]
        current = self.sprites()[current_idx]
        if not current.visible:
            current.visible = 1
        selected = self.sprites()[self.selection]
        if not selected.visible:
            selected.visible = 1

        if current == self.sprites()[0]:
            current.add_animation(anim.Exit(duration))
            selected.set_alpha(0)
            selected.add_animation(anim.Fade(255, duration, False))
        else:
            selected.set_alpha(255)
            current.add_animation(anim.Fade(0, duration))
