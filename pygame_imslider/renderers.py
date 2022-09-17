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
                 background_color,
                 slide_padding=10):
        """VKeyboardStyle default constructor.

        Some parameters take a list of color tuples, one per state.
        The states are: (released, pressed)

        :param arrow_color: RGB tuple for arrow color (one tuple per state)
        :param dot_color: RGB tuple for dot color (one tuple per state)
        :param slide_color: RGB tuple for sldie color
        :param selection_color: RGB tuple for selected image color
        :param selection_page_color: RGB tuple for selected page color
        :param background_color: RGB tuple for background color
        :param slide_padding: border between slide and image
        """
        self.arrow_color = arrow_color
        self.dot_color = dot_color
        self.slide_color = slide_color
        self.selection_color = selection_color
        self.selection_page_color = selection_page_color
        self.background_color = background_color
        self.slide_padding = slide_padding

    def draw_arrow(self, surface, arrow):
        """Draw an arrow.

        :param surface: surface background should be drawn in
        :type surface: :py:class:`pygame.Surface`
        :param arrow: arrow to draw
        :type arrow: :py:class:`Arrow`
        """
        fit_to_rect = arrow.image_source.get_rect().fit(surface.get_rect())
        fit_to_rect.center = surface.get_rect().center
        scaled = pygame.transform.smoothscale(arrow.image_source, fit_to_rect.size)
        arrow.shape = colorize(scaled, self.arrow_color[0])
        arrow.shape_pressed = colorize(scaled, self.arrow_color[1])

        if self.background_color is None:
            surface.fill((255, 255, 255, 0))
        else:
            surface.fill(self.background_color)
        surface.blit(arrow.shape, arrow.shape.get_rect(center=surface.get_rect().center))

    def draw_arrow_state(self, surface, arrow):
        """Draw arrow state.

        :param surface: surface background should be drawn in
        :type surface: :py:class:`pygame.Surface`
        :param arrow: arrow to draw
        :type arrow: :py:class:`Arrow`
        """
        if self.background_color is None:
            surface.fill((255, 255, 255, 0))
        else:
            surface.fill(self.background_color)
        if arrow.pressed:
            image = arrow.shape_pressed
        else:
            image = arrow.shape
        surface.blit(image, image.get_rect(center=surface.get_rect().center))

    def draw_dot(self, surface, dot):
        """Draw a dot.

        :param surface: surface background should be drawn in
        :type surface: :py:class:`pygame.Surface`
        :param dot: dot to draw
        :type dot: :py:class:`Dot`
        """
        fit_to_rect = dot.image_source.get_rect().fit(surface.get_rect())
        fit_to_rect.center = surface.get_rect().center
        scaled = pygame.transform.smoothscale(dot.image_source, fit_to_rect.size)
        dot.shape = colorize(scaled, self.dot_color[0])
        dot.shape_pressed = colorize(scaled, self.dot_color[1])
        dot.shape_selected = colorize(scaled, self.selection_page_color)

        if self.background_color is None:
            surface.fill((255, 255, 255, 0))
        else:
            surface.fill(self.background_color)
        surface.blit(dot.shape, dot.shape.get_rect(center=surface.get_rect().center))

    def draw_dot_state(self, surface, dot):
        """Draw dot state.

        :param surface: surface background should be drawn in
        :type surface: :py:class:`pygame.Surface`
        :param dot: dot to draw
        :type dot: :py:class:`Dot`
        """
        if self.background_color is None:
            surface.fill((255, 255, 255, 0))
        else:
            surface.fill(self.background_color)
        if dot.pressed:
            image = dot.shape_pressed
        elif dot.selected:
            image = dot.shape_selected
        else:
            image = dot.shape
        surface.blit(image, image.get_rect(center=surface.get_rect().center))

    def draw_slide(self, surface, slide):
        """Draw a slide.

        :param surface: surface background should be drawn in
        :type surface: :py:class:`pygame.Surface`
        :param slide: slide to draw
        :type slide: :py:class:`Slide`

        :return: scaled image for next blit without resize
        """
        fit_to_rect = slide.image_source.get_rect().fit(surface.get_rect())
        fit_to_rect = fit_to_rect.inflate(-self.slide_padding, -self.slide_padding)
        fit_to_rect.center = surface.get_rect().center
        slide.scaled = pygame.transform.smoothscale(slide.image_source, fit_to_rect.size)
        shape = get_roundrect_shape(surface.get_rect(), 0.2)
        slide.shape_selected = colorize(shape, self.selection_color)
        if self.slide_color is not None:
            slide.shape = colorize(shape, self.slide_color)
        else:
            # Slide is transparent
            slide.shape = surface.copy()
            slide.shape.fill((0, 0, 0, 0))

        self.draw_slide_state(surface, slide)

    def draw_slide_state(self, surface, slide):
        """Draw selection around the slide.
        :param surface: surface background should be drawn in
        :type surface: :py:class:`pygame.Surface`
        :param slide: slide to draw
        :type slide: :py:class:`Slide`
        """
        surface.fill((0, 0, 0, 0))  # Clear the current slide
        if slide.selected:
            surface.blit(slide.shape_selected, (0, 0))
        else:
            surface.blit(slide.shape, (0, 0))
        surface.blit(slide.scaled, slide.scaled.get_rect(center=surface.get_rect().center))
        surface.set_alpha(slide.alpha)

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
