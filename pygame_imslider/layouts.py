# -*- coding: utf-8 -*-

import itertools
import pygame
import pygame_imslider.animations as anim


class SlidesLayout(pygame.sprite.LayeredDirty):

    def __init__(self, per_page, focus, padding=24):
        super(SlidesLayout, self).__init__()
        self.slides = []
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
        return len(self.slides) - 1

    def add_slide(self, slide):
        self.slides.append(slide)
        slide.set_index(self.slides.index(slide))
        self.add(slide)

    def empty(self):
        super(SlidesLayout, self).empty()
        self.slides = []

    def update_slide_sizes(self):
        """Update slides size and position.
        """
        width, height = self.rect.size
        slide_width = (width - ((1 + self.per_page) * self.padding)) // self.per_page
        slide_height = height - 2 * self.padding
        pos = self.padding - self.selection * (slide_width + self.padding)
        for slide in self.slides:
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
        if self.rect.topleft != (int(x), int(y)):
            self.rect.topleft = (int(x), int(y))
            self.get_clip().topleft = (int(x) + self.padding, int(y) + self.padding)

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

        :param pos: go to the given position
        :type pos: int
        :param step: how many slides to move the selection
        :type step: int
        """
        if pos is not None and step is not None:
            raise ValueError("Both position and step can not be specified.")

        if self.slides:
            self.slides[self.selection].set_selected(0)
            if pos is not None:
                assert pos >= 0 and pos < len(self.slides)
                self.selection = pos
            if step is not None:
                self.selection += step
                self.selection %= len(self.slides)

            if self.focus:
                self.slides[self.selection].set_selected(1)

    def is_animated(self):
        """Return True if only one slide is currently annimated.
        """
        for slide in self.slides:
            if slide.is_animated():
                return True
        return False

    def get_visible_slides(self):
        """Return the list of visible slides.
        """
        return [slide for slide in self.slides
                if self.get_clip().colliderect(slide.rect) and slide.visible]

    def go_to_selection_forward(self, duration, center=False):
        """Move forward all slides to ensure that selection is visible.

        :param duration: animation duration in second (0 = instantaneous)
        :type duration: int
        :param center: center on surface the selected slide (when possible)
        :type center: bool
        """
        visibles = self.get_visible_slides()
        if center:
            current = visibles[len(visibles) // 2]
        else:
            current = visibles[0]

        step = self.slides.index(current) - self.selection
        if step < 0:
            # Ensure to not go after last index
            step = max(step, self.slides.index(visibles[-1]) - self.last_idx)

        if step > 0:
            # Fast backward to begining
            step = min(step, len(self.slides) - len(visibles))

        for slide in self.slides:
            pos = slide.rect.x + step * (slide.rect.width + self.padding)
            slide.add_animation(anim.Transpose(self.get_clip(), pos, slide.rect.y, duration))

    def go_to_selection_backward(self, duration, center=False):
        """Move backward all slides to ensure that selection is visible.

        :param duration: animation duration in second (0 = instantaneous)
        :type duration: int
        :param center: center on surface the selected slide (when possible)
        :type center: bool
        """
        visibles = self.get_visible_slides()
        if center:
            current = visibles[len(visibles) // 2]
        else:
            current = visibles[0]

        step = self.slides.index(current) - self.selection
        if step > 0:
            # Ensure to not go after first index
            step = min(step, self.slides.index(visibles[0]))

        if step < 0:
            # Fast forward to the end
            step = max(step, self.slides.index(visibles[-1]) - self.last_idx)

        for slide in self.slides:
            pos = slide.rect.x + step * (slide.rect.width + self.padding)
            slide.add_animation(anim.Transpose(self.get_clip(), pos, slide.rect.y, duration))


class SlidesLayoutLoop(SlidesLayout):

    def get_visible_slides(self):
        """Return the list of visible slides and possible clones.
        """
        return [slide for slide in self.get_x_ordered_slides()
                if self.get_clip().colliderect(slide.rect) and slide.visible]

    def get_x_ordered_slides(self, reverse=False):
        """Return the list of slides and possible clones ordered by their X position.
        """
        return sorted(self.sprites(), key=lambda sprite: sprite.rect.x, reverse=reverse)

    def go_to_selection_forward(self, duration, center=False):
        # Remove clones and replace it with hidden parent
        for sprite in self.sprites():
            if sprite.parent:
                self.remove(sprite)
                sprite.parent.set_position(*sprite.rect.topleft)

        visibles = self.get_visible_slides()
        if center:
            current = visibles[len(visibles) // 2]
        else:
            current = visibles[0]

        # Move all left hidden slides to the end
        sprites = self.get_x_ordered_slides()
        last_pos_x = sprites[-1].rect.right + self.padding
        for slide in sprites[:sprites.index(visibles[0])]:
            slide.set_position(last_pos_x, slide.rect.y)
            last_pos_x = slide.rect.right + self.padding

        sprites = self.get_x_ordered_slides()
        current_idx = sprites.index(current)
        selected_idx = sprites.index(self.slides[self.selection])
        if current_idx <= selected_idx:
            step = current_idx - selected_idx
        else:
            step = current_idx - len(sprites) + selected_idx

        # Clone slides to complete the sprites list
        # Clones are not added to slides list, use self.add() method instead of self.add_slide()
        right_hidden = len(sprites[sprites.index(visibles[-1]) + 1:])
        missing = self.per_page - len(visibles) + abs(step) - right_hidden
        count = 0
        last_pos_x = sprites[-1].rect.right + self.padding
        for slide in itertools.cycle(self.get_x_ordered_slides()):
            if count >= missing:
                break
            clone = slide.clone()
            clone.set_position(last_pos_x, slide.rect.y)
            self.add(clone)
            count += 1
            last_pos_x = clone.rect.right + self.padding

        # Add slide animations
        for slide in self.get_x_ordered_slides():
            pos = slide.rect.x + step * (slide.rect.width + self.padding)
            slide.add_animation(anim.Transpose(self.get_clip(), pos, slide.rect.y, duration))

    def go_to_selection_backward(self, duration, center=False):
        # Remove clones and replace it with hidden parent
        for sprite in self.sprites():
            if sprite.parent:
                self.remove(sprite)
                sprite.parent.set_position(*sprite.rect.topleft)

        visibles = self.get_visible_slides()
        if center:
            current = visibles[len(visibles) // 2]
        else:
            current = visibles[0]

        # Move all right hidden slides to the begining
        sprites = self.get_x_ordered_slides()
        first_pos_x = sprites[0].rect.left - self.padding
        for slide in reversed(sprites[sprites.index(visibles[-1]) + 1:]):
            slide.set_position(first_pos_x - slide.rect.width, slide.rect.y)
            first_pos_x = slide.rect.left - self.padding

        sprites = self.get_x_ordered_slides()
        current_idx = sprites.index(current)
        selected_idx = sprites.index(self.slides[self.selection])
        if current_idx < selected_idx:
            step = current_idx + len(sprites) - selected_idx
        else:
            step = current_idx - selected_idx

        # Clone slides to complete the sprites list
        # Clones are not added to slides list, use self.add() method instead of self.add_slide()
        left_hidden = len(sprites[:sprites.index(visibles[0])])
        missing = abs(step) - left_hidden
        count = 0
        first_pos_x = sprites[0].rect.left - self.padding
        for slide in itertools.cycle(self.get_x_ordered_slides(reverse=True)):
            if count >= missing:
                break
            clone = slide.clone()
            clone.set_position(first_pos_x - slide.rect.width, slide.rect.y)
            self.add(clone)
            count += 1
            first_pos_x = clone.rect.left - self.padding

        # Add slide animations
        for slide in self.get_x_ordered_slides():
            pos = slide.rect.x + step * (slide.rect.width + self.padding)
            slide.add_animation(anim.Transpose(self.get_clip(), pos, slide.rect.y, duration))


class SlidesLayoutFade(SlidesLayout):

    def add_slide(self, slide):
        super(SlidesLayoutFade, self).add_slide(slide)
        if slide == self.slides[self.selection]:
            if not slide.visible:
                slide.visible = 1
        elif slide.visible:
            slide.visible = 0

    def update_slide_sizes(self):
        for slide in self.slides:
            width, height = self.rect.size
            slide.set_position(self.rect.x + self.padding, self.rect.y + self.padding)
            slide.set_size(width - 2 * self.padding, height - 2 * self.padding)

    def go_to_selection_forward(self, duration, center=False):
        current = self.get_visible_slides()[0]
        if not current.visible:
            current.visible = 1
        selected = self.slides[self.selection]
        if not selected.visible:
            selected.visible = 1

        if current == self.slides[-1]:
            selected.set_alpha(255)
            current.add_animation(anim.Fade(self.get_clip(), 0, duration))
        else:
            current.add_animation(anim.Exit(self.get_clip(), duration))
            selected.set_alpha(0)
            selected.add_animation(anim.Fade(self.get_clip(), 255, duration, False))

    def go_to_selection_backward(self, duration, center=False):
        current = self.get_visible_slides()[0]
        if not current.visible:
            current.visible = 1
        selected = self.slides[self.selection]
        if not selected.visible:
            selected.visible = 1

        if current == self.slides[0]:
            current.add_animation(anim.Exit(self.get_clip(), duration))
            selected.set_alpha(0)
            selected.add_animation(anim.Fade(self.get_clip(), 255, duration, False))
        else:
            selected.set_alpha(255)
            current.add_animation(anim.Fade(self.get_clip(), 0, duration))
