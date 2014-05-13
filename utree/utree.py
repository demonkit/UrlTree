#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import urlparse


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
        self.children = set()

    def __str__(self):
        paths = [self.path, ]
        parent = self.parent
        while parent is not None:
            paths.append(parent.path)
            parent = parent.parent
        paths.reverse()
        return ''.join(paths)

    def __cmp__(self, other):
        if self.parent != other.parent:
            raise ValueError("two operands' parent not equal")
        return cmp(self.path,  other.path)

    def __eq__(self, other):
        return str(self) == str(other)

    def isRoot(self):
        return self.parent is None

    def iterChildren(self):
        for node in self.children:
            yield node

    def appendChild(self, node):
        self.children.add(node)

    def extendChild(self, nodes):
        if isinstance(nodes, set):
            nodes = set(nodes)
        self.children = self.children.union(nodes)

    def display(self):
        self.out.write("    " * self.level + self.path + '\n')


def stripUrl(url):
    """Parse url to remove query parameters and fragment."""
    url = url.strip()
    if not url.startswith('http://') and not url.startswith('https://'):
        url = 'http://' + url
    parsed_url = urlparse.urlparse(url)
    return urlparse.urlunparse(
                (
                    parsed_url.scheme,
                    parsed_url.netloc,
                    parsed_url.path,
                    '',
                    '',
                    '',
                )
            )


def splitPath(url):
    url = stripUrl(url)
    parsed_url = urlparse.urlparse(url)
    domain = parsed_url.netloc
    root = Node(domain)
    parent = root

    all_path = parsed_url.path.split('/')[1:]
    for path in all_path:
        node = Node('/'+path, parent)
        parent = node
    return root


def displayAll(node):
    node.display()
    for child in node.iterChildren():
        displayAll(child)


def mapNodesDict(nodes):
    path_dict = {}
    for node in nodes:
        _key = str(node)
        if _key in path_dict:
            path_dict[_key].extendChild(node.children)
        else:
            path_dict[_key] = node
    return path_dict


def main():
    urls = []
    with open('../../urls.txt') as fin:
        urls = fin.readlines()
    nodes = []
    for url in urls:
        nodes.append(splitPath(url))
    path_dict = mapNodesDict(nodes)
    for value in path_dict.values():
        displayAll(value)
    # next, try to remove the duplicated ones


if __name__ == '__main__':
    main()
