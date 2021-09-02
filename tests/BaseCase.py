# -*- coding: utf-8 -*-
"""
Requires Python 3.8 or later
"""

__author__ = "Jorge Morfinez Mojica (jorge.morfinez.m@gmail.com)"
__copyright__ = "Copyright 2021"
__license__ = ""
__history__ = """ """
__version__ = "1.21.I02.1 ($Rev: 2 $)"

import unittest

from api_config import *


class BaseCase(unittest.TestCase):

    def setUp(self):

        app, jwt = create_app()

        app.config['TESTING'] = True
        self.app = app.test_client()

        jwt.init_app(app)

