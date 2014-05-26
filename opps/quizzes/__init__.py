#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pkg_resources

pkg_resources.declare_namespace(__name__)

VERSION = (0, 1, 0)

__version__ = ".".join(map(str, VERSION))
__status__ = "Development"
__description__ = u"quizzes App for Opps CMS"

__author__ = u"Bruno Rocha"
__credits__ = []
__email__ = u"rochacbruno@gmail.com"
__license__ = u""
__copyright__ = u"Copyright 2013, Bruno Rocha"
