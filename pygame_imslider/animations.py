# -*- coding: utf-8 -*-

import pygame


class Animation(object):

    def __init__(self, clip, duration):
        self.time = 0
        self.clip = clip
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


class Transpose(Animation):

    """Transpose to the position.

    :param x: X coordinate to move to
    :type x: int
    :param y: Y coordinate to move to
    :type y: int
    :param duration: animation duration in second (0 = instantaneous)
    :type duration: int
    """

    def __init__(self, clip, x, y, duration):
        super(Transpose, self).__init__(clip, duration)
        self.destination = pygame.math.Vector2(x, y)
        self.velocity = None
        self.ini_position = None

    def _apply(self, slide):
        if self.duration <= 0:
            slide.set_position(*self.destination)
            self.finished = True
            return

        # Initialize velocity according to distance between current position and
        # destination
        if not self.velocity:
            self.ini_position = slide.rect.topleft
            self.velocity = (self.destination - slide.rect.topleft) / self.duration

        new_pos = self.ini_position + self.velocity * self.time

        # Ensure that destination is not overrun
        if (self.velocity.x > 0 and new_pos.x > self.destination.x)\
                or (self.velocity.x < 0 and new_pos.x < self.destination.x):
            new_pos.x = self.destination.x
        if (self.velocity.y > 0 and new_pos.y > self.destination.y)\
                or (self.velocity.y < 0 and new_pos.y < self.destination.y):
            new_pos.y = self.destination.y

        slide.set_position(*new_pos)
        if self.clip.colliderect(slide.rect):
            if not slide.visible:
                slide.visible = 1
        else:
            if slide.visible:
                slide.visible = 0

        if slide.rect.topleft == self.destination:
            self.finished = True


class Fade(Animation):

    """Change image alpha from current value to expected one.

    :param to_alpha: alpha value between 0 (tranparent) -> 255 (opaque)
    :type to_alpha: int
    :param duration: animation duration in second (0 = instantaneous)
    :type duration: int
    :param set_visibility: set visibility to False at the end of the animation
    :type set_visibility: bool
    """

    def __init__(self, clip, to_alpha, duration, set_visibility=True):
        super(Fade, self).__init__(clip, duration)
        assert to_alpha >= 0 and to_alpha <= 255
        self.to_alpha = to_alpha
        self.set_visibility = set_visibility
        self.velocity = None
        self.ini_alpha = None

    def _apply(self, slide):
        if self.duration <= 0:
            slide.set_alpha(self.to_alpha)
            if self.set_visibility and slide.visible:
                slide.visible = 0
            self.finished = True
            return

        if not self.velocity:
            self.ini_alpha = slide.alpha
            self.velocity = (self.to_alpha - slide.alpha) / self.duration

        new_alpha = int(self.ini_alpha + self.velocity * self.time)

        # Ensure that max alpha is not overrun
        if new_alpha < 0:
            new_alpha = 0
        elif new_alpha > 255:
            new_alpha = 255

        slide.set_alpha(new_alpha)
        if new_alpha == self.to_alpha:
            if self.set_visibility and slide.visible:
                slide.visible = 0
            self.finished = True


class Exit(Animation):

    """Change image visibility to 0.

    :param duration: animation duration in second (0 = instantaneous)
    :type duration: int
    """

    def _apply(self, slide):
        if self.time >= self.duration:
            if slide.visible:
                slide.visible = 0
            self.finished = True
