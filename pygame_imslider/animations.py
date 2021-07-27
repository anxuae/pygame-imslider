# -*- coding: utf-8 -*-

import pygame


class Animation(object):

    def __init__(self, duration):
        self.time = 0
        self.duration = duration
        self.finished = False

    def __call__(self, slide, dt):
        """Update slide according to the current time increased by dt.

        :param slide: slide to animate
        :type slide: :py:class:`pygame.DirtySprite`
        :param dt: elapsed time since last call
        :type dt: int
        """
        if self.finished:
            return
        self.time += dt
        self._apply(slide)

    def _apply(self, slide):
        raise NotImplementedError


class TransposeAnimation(Animation):

    """Transpose to the position.

    :param x: X coordinate to move to
    :type x: int
    :param y: Y coordinate to move to
    :type y: int
    :param duration: animation duration in second (0 = instantaneous)
    :type duration: int
    """

    def __init__(self, x, y, duration):
        super(TransposeAnimation, self).__init__(duration)
        self.destination = pygame.math.Vector2(x, y)
        self.velocity = None

    def _apply(self, slide):
        if self.duration <= 0:
            slide.set_position(*self.destination)
            self.finished = True

        # Initialize velocity according to distance between current position and
        # destination
        if not self.velocity:
            self.velocity = (self.destination - slide.rect.topleft) / self.duration

        new_pos = slide.rect.topleft + self.velocity * self.time

        # Ensure that destination is not overrun
        if (self.velocity.x > 0 and new_pos.x > self.destination.x)\
                or (self.velocity.x < 0 and new_pos.x < self.destination.x):
            new_pos.x = self.destination.x
        if (self.velocity.y > 0 and new_pos.y > self.destination.y)\
                or (self.velocity.y < 0 and new_pos.y < self.destination.y):
            new_pos.y = self.destination.y

        slide.set_position(*new_pos)
        if slide.rect.topleft == self.destination:
            self.finished = True


class FadeAnimation(Animation):

    """Change image alpha.

    :param to_alpha: alpha value between 0 (tranparent) -> 255 (opaque)
    :type to_alpha: int
    :param duration: animation duration in second (0 = instantaneous)
    :type duration: int
    """

    def __init__(self, to_alpha, duration):
        super(FadeAnimation, self).__init__(duration)
        assert to_alpha >= 0 and to_alpha <= 255
        self.to_alpha = to_alpha
        self.velocity = None

    def _apply(self, slide):
        if self.duration <= 0:
            slide.image.set_alpha(self.to_alpha)
            slide.dirty = True
            self.finished = True

        if not self.velocity:
            self.velocity = (self.to_alpha - slide.image.get_alpha()) / self.duration

        new_alpha = slide.image.get_alpha() + self.velocity * self.time

        # Ensure that max alpha is not overrun
        if new_alpha < 0:
            new_alpha = 0
        elif new_alpha > 255:
            new_alpha = 255

        slide.image.set_alpha(new_alpha)
        slide.dirty = True
        if slide.new_alpha == self.to_alpha:
            self.finished = True
