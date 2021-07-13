#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Simple image slider."""

import pygame
import pygame_imslider as imslider


def on_slide_event(index):
    """ Print the current text. """
    print('Current index:', index)


def main(test=False):
    """ Main program.

    :param test: Indicate function is being tested
    :type test: bool
    :return: None
    """

    # Init pygame
    pygame.init()
    screen = pygame.display.set_mode((500, 400))

    # Create keyboard
    slider = imslider.ImageSlider(screen.get_size())

    clock = pygame.time.Clock()

    # Main loop
    while True:
        clock.tick(100)  # Ensure not exceed 100 FPS

        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                print("Average FPS: ", clock.get_fps())
                exit()

        slider.update(events)
        rects = slider.draw(screen)

        # Flip only the updated area
        pygame.display.update(rects)

        # At first loop returns
        if test:
            break


if __name__ == '__main__':
    main()
