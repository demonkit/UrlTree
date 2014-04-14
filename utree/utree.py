#!/usr/bin/env python
# -*- coding: utf-8 -*-


import urlparse


def sort(urls):
    urls.sort()
    return urls


def stripUrl(url):
    """Parse url to remove query parameters and fragment."""
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


if __name__ == '__main__':
    urls = [
            'http://1/2/3?aaa=aa&bb=bb',
            'http://1/3/3?aaa=aa&bb=bb',
            'http://2/2/3?aaa=aa&bb=bb',
            'http://a/2/3?aaa=aa&bb=bb',
            'http://a/a/3?aaa=aa&bb=bb',
            'http://a/2/a?aaa=aa&bb=bb',
            ]
    print sort(map(stripUrl, urls))
