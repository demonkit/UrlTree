#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

import utree


class BaseNode(object):

    out = sys.stdout


class Node(BaseNode):

    def __init__(self, path, parent=None):
        self.path = path
        self.parent = parent
        if parent:
            self.level = parent.level + 1
            self.parent.appendChild(self)
        else:
            self.level = 0
        self.children = []

    def __cmp__(self, other):
        if self.parent != other.parent:
            raise ValueError("two operands' parent not equal")
        return cmp(self.path,  other.path)

    def isRoot(self):
        return self.parent is None

    def iterChildren(self):
        for node in self.children:
            yield node

    def appendChild(self, node):
        self.children.append(node)

    def display(self):
        self.out.write( "    " * self.level + self.path + '\n')


def displayAll(node):
    node.display()
    for child in node.iterChildren():
        displayAll(child)
