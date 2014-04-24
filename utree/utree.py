#!/usr/bin/env python
# -*- coding: utf-8 -*-


import urlparse

from node import Node


def sort(urls):
    urls.sort()
    return urls


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
    all_path = parsed_url.path.split('/')[1:]
    parent = root
    for path in all_path:
        node = Node('/'+path, parent)
        parent = node
    return root
