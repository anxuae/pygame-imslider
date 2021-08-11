#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from io import open
import os.path as osp
from setuptools import setup, find_packages


HERE = osp.abspath(osp.dirname(__file__))
sys.path.insert(0, HERE)
import pygame_imslider  # nopep8 : import shall be done after adding setup to paths


def main():
    setup(
        name=pygame_imslider.__name__,
        version=pygame_imslider.__version__,
        description=pygame_imslider.__doc__,
        long_description=open(osp.join(HERE, 'README.rst'), encoding='utf-8').read(),
        long_description_content_type='text/x-rst',
        classifiers=[
            'Development Status :: 5 - Production/Stable',
            'Environment :: Other Environment',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
            'Operating System :: POSIX :: Linux',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7',
            'Programming Language :: Python :: 3.8',
            'Programming Language :: Python :: 3.9',
            'Natural Language :: English',
            'Topic :: Software Development :: Libraries :: pygame'
        ],
        author="Antoine Rousseaux",
        url="https://github.com/anxuae/pygame-imslider",
        download_url="https://github.com/anxuae/pygame-imslider/archive/{}.tar.gz".format(pygame_imslider.__version__),
        icense='GPLv3',
        platforms=['unix', 'linux'],
        keywords=[
            'pygame',
            'widget'
        ],
        packages=find_packages(),
        package_data={
            'pygame_imslider': ['*.png'],
            'pygame_imslider.examples.images': ['*.png'],
        },
        include_package_data=True,
        python_requires=">=3.6",
        install_requires=[
            'pygame',
        ],
        setup_requires=[
            'setuptools>=41.0.1',
            'wheel>=0.33.4'
        ],
        zip_safe=False,  # Don't install the lib as an .egg zipfile
    )


if __name__ == '__main__':
    main()
