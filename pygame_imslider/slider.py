# -*- coding: utf-8 -*-

import pygame
from .sprites import Arrow, Slide
from .renderers import SliderRenderer

# Regular slider.
STYPE_SLIDE = 'slide'
# Carousel slider
STYPE_LOOP = 'loop'
#  Change slides with fade transition. per_page option is ignored.
STYPE_FADE = 'fade'


class ImageSlider(object):

    """
    Flexible images slider for Pygame engine.

    :param stype: determine a slider type
    :type stype: str

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
                 focus=False, rewind=True, speed=0.4):
        self.position = (0, 0)
        self.size = size
        self.stype = stype
        self.per_page = per_page
        self.per_move = per_move
        self.focus = focus
        self.rewind = rewind
        self.speed = speed
