# -*- coding: utf-8 -*-

import pygame


def colorize(image, color):
    """
    Create a "colorized" copy of a surface (replaces RGB values with the given
    color, preserving the per-pixel alphas of original).

    :param image: surface to create a colorized copy of
    :param color: RGB color to use (original alpha values are preserved)

    :return: new colorized Surface instance
    """
    image = image.copy()

    # Zero out RGB values
    image.fill((0, 0, 0, 255), None, pygame.BLEND_RGBA_MULT)
    # Add in new RGB values
    image.fill(color[0:3] + (0,), None, pygame.BLEND_RGBA_ADD)
    return image


def draw_round_rect(surface, color, rect, radius=0.1):
    """
    Draw a filled rounded rectangle.

    :param surface: surface to draw on
    :type surface: :py:class:`pygame.Surface`
    :param color: RGBA tuple color to draw with, the alpha value is optional
    :type color: tuple
    :param rect: rectangle to draw, position and dimensions
    :type rect: :py:class:`pygame.Rect`
    :param radius: used for drawing rectangle with rounded corners. The supported
                   range is [0, 1] with 0 representing a rectangle without rounded
                   corners
    :type radius: int
    """
    rect = pygame.Rect(rect)
    color = pygame.Color(*color)
    alpha = color.a
    color.a = 0
    pos = rect.topleft
    rect.topleft = 0, 0
    rectangle = pygame.Surface(rect.size, pygame.SRCALPHA)

    circle = pygame.Surface([min(rect.size)*3]*2, pygame.SRCALPHA)
    pygame.draw.ellipse(circle, (0, 0, 0), circle.get_rect(), 0)
    circle = pygame.transform.smoothscale(circle, [int(min(rect.size)*radius)]*2)

    radius = rectangle.blit(circle, (0, 0))
    radius.bottomright = rect.bottomright
    rectangle.blit(circle, radius)
    radius.topright = rect.topright
    rectangle.blit(circle, radius)
    radius.bottomleft = rect.bottomleft
    rectangle.blit(circle, radius)

    rectangle.fill((0, 0, 0), rect.inflate(-radius.w, 0))
    rectangle.fill((0, 0, 0), rect.inflate(0, -radius.h))

    rectangle.fill(color, special_flags=pygame.BLEND_RGBA_MAX)
    rectangle.fill((255, 255, 255, alpha), special_flags=pygame.BLEND_RGBA_MIN)

    return surface.blit(rectangle, pos)


class ImSliderRenderer(object):

    """ImSliderRenderer is in charge of image slider rendering.

    It handles keyboard rendering properties such as color or padding,
    and provides several rendering methods.

    .. note::
        A DEFAULT and DARK styles are available as class attribute.
    """

    DEFAULT = None
    DARK = None

    def __init__(self,
                 arrow_color,
                 dot_color,
                 slide_color,
                 selection_color,
                 selection_page_color,
                 background_color):
        """VKeyboardStyle default constructor.

        Some parameters take a list of color tuples, one per state.
        The states are: (released, pressed)

        :param arrow_color: RGB tuple for arrow color (one tuple per state)
        :param dot_color: RGB tuple for dot color (one tuple per state)
        :param slide_color: RGB tuple for sldie color
        :param selection_color: RGB tuple for selected image color
        :param selection_page_color: RGB tuple for selected page color
        :param background_color: RGB tuple for background color
        """
        self.arrow_color = arrow_color
        self.dot_color = dot_color
        self.slide_color = slide_color
        self.selection_color = selection_color
        self.selection_page_color = selection_page_color
        self.background_color = background_color

    def draw_arrow(self, surface, image, pressed):
        """Draw an arrow.

        :param surface: surface background should be drawn in
        :type surface: :py:class:`pygame.Surface`
        :param image: image of the arrow to draw
        :type image: :py:class:`pygame.Surface`
        :param pressed: the slide is pressed
        :type pressed: bool
        """
        if pressed:
            arrow = colorize(image, self.arrow_color[1])
        else:
            arrow = colorize(image, self.arrow_color[0])
        fit_to_rect = arrow.get_rect().fit(surface.get_rect())
        fit_to_rect.center = surface.get_rect().center
        scaled = pygame.transform.smoothscale(arrow, fit_to_rect.size)
        if self.background_color is None:
            surface.fill((255, 255, 255, 0))
        else:
            surface.fill(self.background_color)
        surface.blit(scaled, scaled.get_rect(center=surface.get_rect().center))

    def draw_dot(self, surface, image, pressed, selected):
        """Draw a dot.

        :param surface: surface background should be drawn in
        :type surface: :py:class:`pygame.Surface`
        :param pressed: the dote is pressed
        :type pressed: bool
        :param selected: the dot is selected/focused
        :type selected: bool
        """
        if pressed:
            dot = colorize(image, self.dot_color[1])
        elif selected:
            dot = colorize(image, self.selection_page_color)
        else:
            dot = colorize(image, self.dot_color[0])
        fit_to_rect = dot.get_rect().fit(surface.get_rect())
        fit_to_rect.center = surface.get_rect().center
        scaled = pygame.transform.smoothscale(dot, fit_to_rect.size)
        if self.background_color is None:
            surface.fill((255, 255, 255, 0))
        else:
            surface.fill(self.background_color)
        surface.blit(scaled, scaled.get_rect(center=surface.get_rect().center))

    def draw_slide(self, surface, image, selected):
        """Draw a slide.

        :param surface: surface background should be drawn in
        :type surface: :py:class:`pygame.Surface`
        :param image: image to draw on slide
        :type image: :py:class:`pygame.Surface`
        :param selected: the slide is selected/focused
        :type selected: bool
        """
        surface.fill((255, 255, 255, 0))  # Clear the current slide
        if selected:
            draw_round_rect(surface, self.selection_color, surface.get_rect(), 0.2)
        else:
            draw_round_rect(surface, self.slide_color, surface.get_rect(), 0.2)
        scaled = pygame.transform.smoothscale(image, image.get_rect().fit(surface.get_rect()).size)
        surface.blit(scaled, scaled.get_rect(center=surface.get_rect().center))

    def draw_background(self, surface):
        """Draw background.

        Background is drawn as a simple rectangle filled using this
        style background color attribute.

        :param surface: surface background should be drawn in
        :type surface: :py:class:`pygame.Surface`
        """
        if self.background_color is not None:
            surface.fill(self.background_color)


ImSliderRenderer.DEFAULT = ImSliderRenderer(
    arrow_color=((255, 255, 255), (54, 54, 54)),
    dot_color=((120, 120, 120), (54, 54, 54)),
    slide_color=(242, 195, 195),
    selection_color=(245, 95, 76),
    selection_page_color=(255, 255, 255),
    background_color=(32, 135, 156),
)

ImSliderRenderer.DARK = ImSliderRenderer(
    arrow_color=((182, 183, 184), (124, 183, 62)),
    dot_color=((182, 183, 184), (124, 183, 62)),
    slide_color=(255, 255, 255),
    selection_color=(124, 183, 62),
    selection_page_color=(180, 220, 130),
    background_color=(0, 0, 0),
)
