#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Simple image slider."""

import pygame
import pygame_imslider as imslider


def main(test=False, images=[], parameters={}):
    """ Main program.

    :param test: Indicate function is being tested
    :type test: bool
    :return: None
    """

    # Init pygame
    pygame.init()
    screen = pygame.display.set_mode((800, 300))
    screen.fill((178, 123, 200))

    # Create keyboard
    slider = imslider.ImSlider(screen.get_size(), **parameters)
    slider.load_images(images, True)

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
    main(False, ["a", "b", "c", "d"])
