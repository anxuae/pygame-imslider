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


def get_roundrect_shape(rect, radius=0.1, width=0):
    """Return a rounded rectangle shape.

    Parameters
    ----------
    rect:
        Rectangle to draw, position and dimensions.
    radius:
        Used for drawing rectangle with rounded corners. The supported range is
        [0, 1] with 0 representing a rectangle without rounded corners.
    width:
        Line thickness (0 to fill the rectangle).
    """
    rect = pygame.Rect(rect)
    shape = pygame.Surface(rect.size, pygame.SRCALPHA)

    circle = pygame.Surface([min(rect.size) * 3] * 2, pygame.SRCALPHA)
    if width > 0:
        pygame.draw.arc(circle, (0, 0, 0), circle.get_rect(), 1.571, 3.1415, width * 8)
    else:
        pygame.draw.ellipse(circle, (0, 0, 0), circle.get_rect(), 0)
    circle = pygame.transform.smoothscale(circle, [int(min(rect.size) * radius)] * 2)

    i = 1
    shape_rect = shape.get_rect()
    for pos in ('topleft', 'topright', 'bottomleft', 'bottomright'):
        r = circle.get_rect(**{pos: getattr(shape_rect, pos)})
        shape.blit(circle, r)
        if width > 0:
            circle = pygame.transform.rotate(circle, -i * 90)
        i += 1

    hrect = shape_rect.inflate(0, -circle.get_height() + 1)
    vrect = shape_rect.inflate(-circle.get_width() + 1, 0)
    if width > 0:
        hrect.width = width
        vrect.height = width
        shape.fill((0, 0, 0), hrect)
        shape.fill((0, 0, 0), vrect)
        hrect.right = shape_rect.right
        vrect.bottom = shape_rect.bottom
        shape.fill((0, 0, 0), hrect)
        shape.fill((0, 0, 0), vrect)
    else:
        shape.fill((0, 0, 0), hrect)
        shape.fill((0, 0, 0), vrect)
    return shape


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

    def draw_selection(self, surface, image_cache, selected):
        """Draw selection around the slide.

        :param surface: surface background should be drawn in
        :type surface: :py:class:`pygame.Surface`
        :param image_cache: cached (scaled image, shape) built when drawing slide
        :type image_cache: (:py:class:`pygame.Surface`, :py:class:`pygame.Surface`)
        :param selected: the slide is selected/focused
        :type selected: bool
        """
        scaled, shape = image_cache
        surface.fill((255, 255, 255, 0))  # Clear the current slide
        if selected:
            surface.blit(colorize(shape, self.selection_color), (0, 0))
        else:
            surface.blit(colorize(shape, self.slide_color), (0, 0))
        surface.blit(scaled, scaled.get_rect(center=surface.get_rect().center))

    def draw_slide(self, surface, image_source):
        """Draw a slide.

        :param surface: surface background should be drawn in
        :type surface: :py:class:`pygame.Surface`
        :param image_source: source image to draw on slide
        :type image_source: :py:class:`pygame.Surface`
        """
        shape = get_roundrect_shape(surface.get_rect(), 0.2)
        scaled = pygame.transform.smoothscale(image_source, image_source.get_rect().fit(surface.get_rect()).size)
        surface.blit(colorize(shape, self.slide_color), (0, 0))
        surface.blit(scaled, scaled.get_rect(center=surface.get_rect().center))
        return (scaled, shape)

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
