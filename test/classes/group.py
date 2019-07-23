import unittest

import svd.classes

class group_attributes(svd.classes.group):

    attributes = ['extra']

    def __init__(self, parent, node):
        svd.classes.group.__init__(self, parent, node)
