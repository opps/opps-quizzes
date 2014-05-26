#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pkg_resources

pkg_resources.declare_namespace(__name__)

VERSION = (0, 1, 0)

__version__ = ".".join(map(str, VERSION))
__status__ = "Development"
__description__ = u"quizzes App for Opps CMS"

__author__ = u"YACOWS"
__credits__ = []
__email__ = u""
__license__ = u""
__copyright__ = u"Copyright 2014, YACOWS"
