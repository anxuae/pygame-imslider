#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pygame_imslider as imslider
from .default import main


if __name__ == '__main__':
    main(False, ["a", "b", "c", "d", "e", "f", "g", "h", "i"],
         {'stype': imslider.STYPE_FADE, 'rewind': True})
