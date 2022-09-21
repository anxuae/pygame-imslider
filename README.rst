pygame-imslider
---------------

|PythonVersions| |PypiPackage| |Downloads|

Flexible images slider for Pygame engine.

Default
^^^^^^^

.. image:: https://raw.githubusercontent.com/anxuae/pygame-imslider/master/screenshots/default.gif
   :align: center
   :alt: default

.. code-block:: python

   slider = ImSlider((800, 300))

Multiple Slides
^^^^^^^^^^^^^^^

.. image:: https://raw.githubusercontent.com/anxuae/pygame-imslider/master/screenshots/multiple.gif
   :align: center
   :alt: multiple

.. code-block:: python

   slider = ImSlider((800, 300), per_page=3, rewind=True)

1 Slide Per Move
^^^^^^^^^^^^^^^^

.. image:: https://raw.githubusercontent.com/anxuae/pygame-imslider/master/screenshots/one_per_move.gif
   :align: center
   :alt: one_per_move

.. code-block:: python

   slider = ImSlider((800, 300), stype=STYPE_LOOP, per_page=3, per_move=1)

Focus Center
^^^^^^^^^^^^

.. image:: https://raw.githubusercontent.com/anxuae/pygame-imslider/master/screenshots/focus.gif
   :align: center
   :alt: focus

.. code-block:: python

   slider = ImSlider((800, 300), stype=STYPE_LOOP, per_page=3, per_move=2, focus='center')

Fade Transition
^^^^^^^^^^^^^^^

.. image:: https://raw.githubusercontent.com/anxuae/pygame-imslider/master/screenshots/fade.gif
   :align: center
   :alt: fade

.. code-block:: python

   slider = ImSlider((800, 300), stype=STYPE_FADE, rewind=True, focus=False)

Install
-------

::

    $ pip3 install pygame-imslider

Basic usage
-----------

``ImSlider`` only require a pygame surface to be displayed on and a index consumer function, as
in the following example :

.. code-block:: python

    from pygame_imslider import *

    def consumer(index):
        print('Current index : %s' % index)

    # Initializes and activates ImSlider
    slider = ImSlider((300, 100), callback=consumer)
    slider.load_images(['image1.png', 'image2.png', 'image3.png',])

The slider has the following optional parameters:

- **stype**: determine a slider type: STYPE_SLIDE, STYPE_LOOP or STYPE_FADE
- **per_page**: determine how many slides should be displayed per page. If
  stype=STYPE_FADE, this option is ignored.
- **per_move**: determine how many slides should be moved when a slider goes
  to next or perv. If stype=STYPE_FADE, this option is ignored.
- **focus**: determine which slide should be focused if there are multiple
  slides in a page. A string "center" is acceptable for centering slides.
- **rewind**: whether to rewind a slider before the first slide or after the
  last one. If stype=STYPE_LOOP, this option is ignored.
- **speed**: transition duration in seconds.
- **renderer**: a ImSliderRenderer to customize colors of the slider
- **callback**: callback called each time the selection is changed.

Event management
----------------

A ``ImSlider`` object handles the following pygame event :

- **MOUSEBUTTONDOWN**
- **MOUSEBUTTONUP**
- **FINGERDOWN**
- **FINGERUP**
- **KEYDOWN**
- **KEYUP**
- **JOYHATMOTION**

In order to process those events, slider instance event handling method should be called like
in the following example:

.. code-block:: python

    while True:

        events = pygame.event.get()

        # Update internal variables
        slider.update(events)

        # Draw the slider
        slider.draw(surface)

        #
        # Perform other tasks here
        #

        # Update the display
        pygame.display.flip()

The **global performances can be improved avoiding to flip the entire display** at each
loop by using the ``pygame.display.update()`` function.

.. code-block:: python

   while True:

       # Draw the slider
       rects = slider.draw(surface)

       # Update only the dirty rectangles of the display
       pygame.display.update(rects)

.. note:: the ``surface`` parameter of the ``draw()`` method is optional, it is used to
          clear/hide the slider when it is necessary and may be mandatory if the surface
          has changed.

Custom rendering using ImSliderRenderer
---------------------------------------

If you want to customize slider rendering you could provide a ``ImSliderRenderer``
instance at ``ImSlider`` construction.

.. code-block:: python

    slider = ImSlider(size, renderer=ImSliderRenderer.DARK)

Here is the list of default renderers provided with ``pygame-imslider``:

- ImSliderRenderer.DEFAULT
- ImSliderRenderer.DARK

A custom ``ImSliderRenderer`` can be built using following constructor :

.. code-block:: python

    renderer = ImSliderRenderer(
        # RGB tuple for arrow color (one per state: released, pressed).
        ((255, 255, 255), (54, 54, 54)),
        # RGB tuple for page-dot color (one tuple per state).
        ((120, 120, 120), (54, 54, 54)),
        # RGB tuple for sldie color.
        (242, 195, 195),
        # RGB tuple for selected image color.
        (245, 95, 76),
        # RGB tuple for selected page-dot color.
        (255, 255, 255),
        # RGB tuple for background color.
        (32, 135, 156)
        )

You can also create your own renderer. Just override ``ImSliderRenderer`` class and
override any of the following methods:

- **draw_arrow(surface, arrow)**: Draw an arrow.
- **draw_arrow_state(surface, arrow)**: Draw arrow state.
- **draw_dot(surface, dot)**: Draw a dot.
- **draw_dot_state(surface, dot)**: Draw page-dot state
- **draw_slide(surface, slide)**: Draw a slide.
- **draw_slide_state(surface, slide)**: Draw slide state.
- **draw_background(surface)**: Draw background.

Getting/Setting data
--------------------

Several information can be retrieved from the slider:

.. code-block:: python

    slider = ImSlider(...)

    # Load a sequence of image files.
    slider.load_images(['image1.png', 'image2.png', 'image3.png'])

    # Get a pygame.Rect object in which the slider is included.
    slider.get_rect()

    # Get the current pygame image (optionally resized).
    slider.get_image()

    # Get the current index.
    slider.get_index()

    # Set the current index.
    slider.set_index(2)
    
    # Hide left and right arrows
    slider.set_arrows_visible(False)


Run examples
------------

Several examples are provided with the **pygame_imslider** library.
To run the examples, simply execute these commands in a terminal:

.. code-block:: bash

    python -m pygame_imslider.examples.default
    python -m pygame_imslider.examples.multiple
    python -m pygame_imslider.examples.one_per_move
    python -m pygame_imslider.examples.small_loop
    python -m pygame_imslider.examples.focus
    python -m pygame_imslider.examples.fade

Contributing
------------

If you develop you own renderer please share it ! I will keep a collection of
rendering class in this repository. Don't hesitate to report bug, feedback,
suggestion into the repository issues section.


.. |PythonVersions| image:: https://img.shields.io/badge/python-3.6+-red.svg
   :target: https://www.python.org/downloads
   :alt: Python 3.6+

.. |PypiPackage| image:: https://badge.fury.io/py/pygame-imslider.svg
   :target: https://pypi.org/project/pygame-imslider
   :alt: PyPi package

.. |Downloads| image:: https://img.shields.io/pypi/dm/pygame-imslider?color=purple
   :target: https://pypi.org/project/pygame-imslider
   :alt: PyPi downloads
