#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Simple image slider."""

import os
import os.path as osp
import pygame
import pygame_imslider as imslider

HERE = osp.dirname(osp.abspath(__file__))


def consumer(index):
    print('Current index : %s' % index)


def main(test=False, images_nbr=None, parameters={}, resize=False):
    """ Main program.

    :param test: Indicate function is being tested
    :type test: bool
    :return: None
    """
    images = [osp.join(HERE, 'images', name) for name in os.listdir(osp.join(HERE, 'images'))
              if name.endswith('.png')]
    if images_nbr:
        images = images[:images_nbr]

    # Init pygame
    pygame.init()
    if resize:
        screen = pygame.display.set_mode((800, 300), pygame.RESIZABLE)
    else:
        screen = pygame.display.set_mode((800, 300))
    screen.fill((178, 123, 200))

    # Create keyboard
    slider = imslider.ImSlider(screen.get_size(), callback=consumer, **parameters)
    slider.load_images(images)

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
    main(False, 4)
