''' Categorize unicode characters by the code block in which they are found.

    Copyright (c) 2008, Kent S Johnson

    This library is free software; you can redistribute it and/or
    modify it under the terms of the GNU Lesser General Public
    License as published by the Free Software Foundation; either
    version 2.1 of the License, or (at your option) any later version.

    This library is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
    Lesser General Public License for more details.

    You should have received a copy of the GNU Lesser General Public
    License along with this library; if not, write to the Free Software
    Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301
    USA
'''

import os
import re
from bisect import bisect_left


def _loadBlocks():
    ''' Load Blocks.txt.
        Create and return two parallel lists. One has the start and
        end points for codepoint ranges, the second has the corresponding
        block name.
    '''
    # Expects our version of Blocks.txt to be in the same dir as this file
    blocksPath = os.path.join(os.path.dirname(__file__), 'Blocks.txt')
    endpoints = []
    names = []
    splitter = re.compile(r'^(....)\.\.(....); (.*)$')
    for line in open(blocksPath):
        if line.startswith('#'):
            continue
        line = line.strip()
        if not line:
            continue

        m = splitter.match(line)
        assert m
        start = int(m.group(1), 16)
        end = int(m.group(2), 16)
        name = m.group(3)

        endpoints.append(start)
        endpoints.append(end)

        names.append(name)
        names.append(name)

    return endpoints, names

_endpoints, _names = _loadBlocks()


def unicodeBlock(c):
    ''' Returns the name of the unicode block containing c.
        c must be a single character. '''

    ix = bisect_left(_endpoints, ord(c))
    return _names[ix]
