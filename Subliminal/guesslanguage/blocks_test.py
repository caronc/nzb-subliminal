''' Copyright (c) 2008, Kent S Johnson

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
    Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA
'''

import unittest

from blocks import unicodeBlock

class blocks_test(unittest.TestCase):
    def test_unicodeBlock(self):
        for c in range(128):
            self.assertBlock('Basic Latin', c)

        for c in range(0x80, 0x180) + range(0x250, 0x2B0):
            self.assertBlock('Extended Latin', c)

        self.assertBlock('Thai', 0xE00)
        self.assertBlock('Thai', 0xE7F)
        self.assertBlock('Lao', 0xE80)
        self.assertBlock('Lao', 0x0EFF)
        self.assertBlock('Tibetan', 0xF00)
        self.assertBlock('Tibetan', 0xFFF)
        self.assertBlock('Cyrillic', 0x421)

    def assertBlock(self, name, c):
        c = unichr(c)
        block = unicodeBlock(c)
        self.assertEquals(name, unicodeBlock(c), '%s != %s for %r' % (name, block, c))


    def setUp(self):
        pass


if __name__ == '__main__':
    unittest.main()
