#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pygame_imslider as imslider
from .default import main


if __name__ == '__main__':
    main(False, ["a", "b", "c", "d"],
         {'stype': imslider.STYPE_LOOP, 'per_page': 3, 'per_move': 1, 'focus': 'center'})
