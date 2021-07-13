# -*- coding: utf-8 -*-


class SliderRenderer(object):
    """
    A SliderRenderer is in charge of image slider rendering.

    It handles keyboard rendering properties such as color or padding,
    and provides several rendering methods.

    .. note::
        A DEFAULT and DARK styles are available as class attribute.
    """

    DEFAULT = None
    DARK = None

    def __init__(self,
                 arrow_color,
                 slide_color,
                 selection_color,
                 background_color):
        """VKeyboardStyle default constructor.

        Some parameters take a list of color tuples, one per state.
        The states are: (released, pressed)

        :param arrow_color: RGB tuple for arrow color (one tuple per state).
        :param slide_color: RGB tuple for sldie color (one tuple per state).
        :param selection_color: RGB tuple for selected image color.
        :param background_color: RGB tuple for background color.
        """
        self.arrow_color = arrow_color
        self.slide_color = slide_color
        self.selection_color = selection_color
        self.background_color = background_color

    def draw_arrow(self, surface, texture):
        """

        :param surface: surface background should be drawn in
        :type surface: :py:class:`pygame.Surface`
        :param texture: image of the arrow to draw
        :type texture: :py:class:`pygame.Surface`
        """

    def draw_slide(self, surface, selected):
        """

        :param surface: surface background should be drawn in
        :type surface: :py:class:`pygame.Surface`
        :param selected: the slide is selected/focused
        :type selected: bool
        """

    def draw_background(self, surface):
        """Default drawing method for background.

        Background is drawn as a simple rectangle filled using this
        style background color attribute.

        :param surface: surface background should be drawn in
        :type surface: :py:class:`pygame.Surface`
        """
        surface.fill(self.background_color)
