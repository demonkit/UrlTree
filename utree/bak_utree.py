#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import urlparse


class BaseNode(object):

    out = sys.stdout


class NodeSet(object):

    def __init__(self, nodes=None):
        self._node_dict = {}
        if nodes is not None:
            self.__initNodes(nodes)

    def __initNodes(self, nodes):
        for node in nodes:
            node_str = str(node)
            if node_str not in self._node_dict:
                self._node_dict[node_str] = node

    def __contains__(self, node):
        return str(node) in self._node_dict

    def __iter__(self):
        for node in self._node_dict.itervalues():
            yield node

    def _add(self, node):
        self._node_dict[str(node)] = node

    def _delete(self, node):
        del self._node_dict[str(node)]

    def __unionChild(self, node):
        for child in node.children:
            if child not in self:
                self._add(node)

    def add(self, node):
        if node not in self:
            self._add(node)
        else:
            # if node already in the set, we should handle its children
            self.__unionChild(node)

    def delete(self, node):
        if node not in self:
            self._delete(node)

    def union(self, nodes):
        for node in nodes:
            node_str = str(node)
            if node not in self:
                self._add(node)


class Node(BaseNode):

    def __init__(self, path, parent=None):
        self.path = path
        self.parent = parent
        if parent:
            self.level = parent.level + 1
            self.parent.appendChild(self)
        else:
            self.level = 0
        # print '======================================='
        # self.children = NodeSet()
        # print self.children
        # print '======================================='

    def setOupputStream(self, output):
        self.out = output

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
        if not isinstance(nodes, NodeSet):
            nodes = NodeSet(nodes)
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
        print node.children
        continue
        if _key in path_dict:
            path_dict[_key].extendChild(node.children)
        else:
            path_dict[_key] = node
    return path_dict


def main():
    urls = []
    with open('../../u.txt') as fin:
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
