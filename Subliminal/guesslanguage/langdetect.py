#! /usr/bin/env python
# -*- coding: utf-8 -*-
#Language Detection based on unicode range
# Copyright 2008 Santhosh Thottingal <santhosh.thottingal@gmail.com>
# http://www.smc.org.in
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.

import string


def _detect_lang(text):
    """
    Detect the language of the given text using the unicode range.
    This function can take a chunk of text and return a dictionary
    containing word-language key-value pairs.
    """
    words = text.split(" ")
    word_count = len(words)
    word_iter = 0
    word = ""
    result_dict = dict()
    while word_iter < word_count:
        word = words[word_iter]
        if(word):
            orig_word = word
            #remove the punctuations
            for punct in string.punctuation:
                word = word.replace(punct, " ")
            length = len(word)
            index = 0
            # scan left to write, skip any punctuations,
            # the detection stops in the first match itself.
            while index < length:
                letter = word[index]
                if not letter.isalpha():
                    index = index + 1
                    continue
                if ((ord(letter) >= 0x0D00) & (ord(letter) <= 0x0D7F)):
                    result_dict[orig_word] = "ml_IN"
                    break
                if ((ord(letter) >= 0x0980) & (ord(letter) <= 0x09FF)):
                    result_dict[orig_word] = "bn_IN"
                    break
                if ((ord(letter) >= 0x0900) & (ord(letter) <= 0x097F)):
                    result_dict[orig_word] = "hi_IN"
                    break
                if ((ord(letter) >= 0x0A80) & (ord(letter) <= 0x0AFF)):
                    result_dict[orig_word] = "gu_IN"
                    break
                if ((ord(letter) >= 0x0A00) & (ord(letter) <= 0x0A7F)):
                    result_dict[orig_word] = "pa_IN"
                    break
                if ((ord(letter) >= 0x0C80) & (ord(letter) <= 0x0CFF)):
                    result_dict[orig_word] = "kn_IN"
                    break
                if ((ord(letter) >= 0x0B00) & (ord(letter) <= 0x0B7F)):
                    result_dict[orig_word] = "or_IN"
                    break
                if ((ord(letter) >= 0x0B80) & (ord(letter) <= 0x0BFF)):
                    result_dict[orig_word] = "ta_IN"
                    break
                if ((ord(letter) >= 0x0C00) & (ord(letter) <= 0x0C7F)):
                    result_dict[orig_word] = "te_IN"
                    break
                if ((letter <= u'z')):  # this is fallback case.
                    result_dict[orig_word] = "en_US"
                    break
                index = index + 1
        word_iter = word_iter + 1
    return result_dict
