pygame-imslider
---------------

|PythonVersions| |PypiPackage| |Downloads|

Flexible images slider for Pygame engine.

.. image:: https://raw.githubusercontent.com/anxuae/pygame-imslider/master/docs/pygame-imslider.png
   :align: center
   :alt: pygame-imslider

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

The slider has the following optional parameters:

- **size**: size of the image slider surface
- **stype**: determine a slider type: STYPE_SLIDE, STYPE_LOOP or STYPE_FADE
- **per_page**: determine how many slides should be displayed per page. In
  "fade" stype, this option is ignored.
- **per_move**: determine how many slides should be moved when a slider goes
  to next or perv. In "fade" stype, this option is ignored.
- **focus**: determine which slide should be focused if there are multiple
  slides in a page. A string "center" is acceptable for centering slides.
- **rewind**: whether to rewind a slider before the first slide or after the
  last one. In "loop" stype, this option is ignored.
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
- **JOYBUTTONDOWN**
- **JOYBUTTONUP**

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

The global performances can be improved avoiding to flip the entire display at each loop by
using the ``pygame.display.update()`` function.

.. code-block:: python

   while True:

       # Draw the slider
       rects = slider.draw(surface)

       # Update only the dirty rectangles of the display
       pygame.display.update(rects)
   ```

.. note:: the ``surface`` parameter of the ``draw()`` method is optional, it is used to
          clear/hide the slider when it is necessary and may be mandatory if the surface
          has changed.

Run examples
------------

Several examples are provided with the **pygame_imslider** library.
To run the examples, simply execute these commands in a terminal:

.. code-block:: bash

    python -m pygame_imslider.examples.default
    python -m pygame_imslider.examples.multiple
    python -m pygame_imslider.examples.one_per_move
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
