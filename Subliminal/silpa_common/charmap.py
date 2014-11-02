#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Indic Language Character Map
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
#
# If you find any bugs or have any suggestions
# email: santhosh.thottingal@gmail.com
# URL: http://www.smc.org.in


__all__ = ['charmap', 'get_language', 'char_compare']

import sys

if sys.version_info.major == 3:
    from functools import lru_cache
else:
    from repoze.lru import lru_cache


charmap = {
    "hi_IN": [u"ँ", u"ं", u"ः", u"ऄ", u"अ", u"आ", u"इ", u"ई", u"उ", u"ऊ", u"ऋ",
              u"ऌ", u"ऍ", u"ऎ", u"ए", u"ऐ", u"ऑ", u"ऒ", u"ओ", u"औ", u"क", u"ख",
              u"ग", u"घ", u"ङ", u"च", u"छ", u"ज", u"झ", u"ञ", u"ट", u"ठ", u"ड",
              u"ढ", u"ण", u"त", u"थ", u"द", u"ध", u"न", u"ऩ", u"प", u"फ", u"ब",
              u"भ", u"म", u"य", u"र", u"ऱ", u"ल", u"ळ", u"ऴ", u"व", u"श", u"ष",
              u"स", u"ह", u"ऺ", u"ऻ", u"़", u"ऽ", u"ा", u"ि", u"ी", u"ु", u"ू",
              u"ृ", u"ॄ", u"ॅ", u"ॆ", u"े", u"ै", u"ॉ", u"ॊ", u"ो", u"ौ", u"्",
              u"ॎ", u"ॏ", u"ॐ", u"॑", u"॒", u"॓", u"॔", u"ॕ", u"ॖ", u"ॗ", u"क़",
              u"ख़", u"ग़", u"ज़", u"ड़", u"ढ़", u"फ़", u"य़", u"ॠ", u"ॡ", u"ॢ", u"ॣ",
              u"।", u"॥", u"०", u"१", u"२", u"३", u"४", u"५", u"६", u"७", u"८",
              u"९", u"॰", u"ॱ", u"ॲ", u"ॳ", u"ॴ", u"ॵ", u"ॶ", u"ॷ", u"ॸ", u"ॹ",
              u"ॺ", u"ॻ", u"ॼ", u"ॽ", u"ॾ", u"ॿ"],
    "bn_IN": [u"ঁ", u"ং", u"ঃ", u"঄", u"অ", u"আ", u"ই", u"ঈ", u"উ", u"ঊ", u"ঋ",
              u"ঌ", u"঍", u"঎", u"এ", u"ঐ", u"঑", u"঒", u"ও", u"ঔ", u"ক", u"খ",
              u"গ", u"ঘ", u"ঙ", u"চ", u"ছ", u"জ", u"ঝ", u"ঞ", u"ট", u"ঠ", u"ড",
              u"ঢ", u"ণ", u"ত", u"থ", u"দ", u"ধ", u"ন", u"঩", u"প", u"ফ", u"ব",
              u"ভ", u"ম", u"য", u"র", u"঱", u"ল", u"঳", u"঴", u"঵", u"শ", u"ষ",
              u"স", u"হ", u"঺", u"঻", u"়", u"ঽ", u"া", u"ি", u"ী", u"ু", u"ূ",
              u"ৃ", u"ৄ", u"৅", u"৆", u"ে", u"ৈ", u"৉", u"৊", u"ো", u"ৌ",
              u"্", u"ৎ", u"৏", u"৐", u"৑", u"৒", u"৓", u"৔", u"৕", u"৖", u"ৗ",
              u"৘", u"৙", u"৚", u"৛", u"ড়", u"ঢ়", u"৞", u"য়", u"ৠ", u"ৡ", u"ৢ",
              u"ৣ", u"৤", u"৥", u"০", u"১", u"২", u"৩", u"৪", u"৫", u"৬", u"৭",
              u"৮", u"৯", u"ৰ", u"ৱ", u"৲", u"৳", u"৴", u"৵", u"৶", u"৷", u"৸",
              u"৹", u"৺", u"৻", u"ৼ", u"৽", u"৾", u"৿"],
    "pa_IN": [u"ਁ", u"ਂ", u"ਃ", u"਄", u"ਅ", u"ਆ", u"ਇ", u"ਈ", u"ਉ", u"ਊ", u"਋",
              u"਌", u"਍", u"਎", u"ਏ", u"ਐ", u"਑", u"਒", u"ਓ", u"ਔ", u"ਕ", u"ਖ",
              u"ਗ", u"ਘ", u"ਙ", u"ਚ", u"ਛ", u"ਜ", u"ਝ", u"ਞ", u"ਟ", u"ਠ", u"ਡ",
              u"ਢ", u"ਣ", u"ਤ", u"ਥ", u"ਦ", u"ਧ", u"ਨ", u"਩", u"ਪ", u"ਫ", u"ਬ",
              u"ਭ", u"ਮ", u"ਯ", u"ਰ", u"਱", u"ਲ", u"ਲ਼", u"਴", u"ਵ", u"ਸ਼", u"਷",
              u"ਸ", u"ਹ", u"਺", u"਻", u"਼", u"਽", u"ਾ", u"ਿ", u"ੀ", u"ੁ", u"ੂ",
              u"੃", u"੄", u"੅", u"੆", u"ੇ", u"ੈ", u"੉", u"੊", u"ੋ", u"ੌ", u"੍",
              u"੎", u"੏", u"੐", u"ੑ", u"੒", u"੓", u"੔", u"੕", u"੖", u"੗", u"੘",
              u"ਖ਼", u"ਗ਼", u"ਜ਼", u"ੜ", u"੝", u"ਫ਼", u"੟", u"੠", u"੡", u"੢", u"੣",
              u"੤", u"੥", u"੦", u"੧", u"੨", u"੩", u"੪", u"੫", u"੬", u"੭", u"੮",
              u"੯", u"ੰ", u"ੱ", u"ੲ", u"ੳ", u"ੴ", u"ੵ", u"੶", u"੷", u"੸", u"੹",
              u"੺", u"੻", u"੼", u"੽", u"੾", u"੿"],
    "gu_IN": [u"ઁ", u"ં", u"ઃ", u"઄", u"અ", u"આ", u"ઇ", u"ઈ", u"ઉ", u"ઊ", u"ઋ",
              u"ઌ", u"ઍ", u"઎", u"એ", u"ઐ", u"ઑ", u"઒", u"ઓ", u"ઔ", u"ક", u"ખ",
              u"ગ", u"ઘ", u"ઙ", u"ચ", u"છ", u"જ", u"ઝ", u"ઞ", u"ટ", u"ઠ", u"ડ",
              u"ઢ", u"ણ", u"ત", u"થ", u"દ", u"ધ", u"ન", u"઩", u"પ", u"ફ", u"બ",
              u"ભ", u"મ", u"ય", u"ર", u"઱", u"લ", u"ળ", u"઴", u"વ", u"શ", u"ષ",
              u"સ", u"હ", u"઺", u"઻", u"઼", u"ઽ", u"ા", u"િ", u"ી", u"ુ", u"ૂ",
              u"ૃ", u"ૄ", u"ૅ", u"૆", u"ે", u"ૈ", u"ૉ", u"૊", u"ો", u"ૌ", u"્",
              u"૎", u"૏", u"ૐ", u"૑", u"૒", u"૓", u"૔", u"૕", u"૖", u"૗", u"૘",
              u"૙", u"૚", u"૛", u"૜", u"૝", u"૞", u"૟", u"ૠ", u"ૡ", u"ૢ", u"ૣ",
              u"૤", u"૥", u"૦", u"૧", u"૨", u"૩", u"૪", u"૫", u"૬", u"૭", u"૮",
              u"૯", u"૰", u"૱", u"૲", u"૳", u"૴", u"૵", u"૶", u"૷", u"૸", u"ૹ",
              u"ૺ", u"ૻ", u"ૼ", u"૽", u"૾", u"૿"],
    "or_IN": [u"ଁ", u"ଂ", u"ଃ", u"଄", u"ଅ", u"ଆ", u"ଇ", u"ଈ", u"ଉ", u"ଊ", u"ଋ",
              u"ଌ", u"଍", u"଎", u"ଏ", u"ଐ", u"଑", u"଒", u"ଓ", u"ଔ", u"କ", u"ଖ",
              u"ଗ", u"ଘ", u"ଙ", u"ଚ", u"ଛ", u"ଜ", u"ଝ", u"ଞ", u"ଟ", u"ଠ", u"ଡ",
              u"ଢ", u"ଣ", u"ତ", u"ଥ", u"ଦ", u"ଧ", u"ନ", u"଩", u"ପ", u"ଫ", u"ବ",
              u"ଭ", u"ମ", u"ଯ", u"ର", u"଱", u"ଲ", u"ଳ", u"଴", u"ଵ", u"ଶ", u"ଷ",
              u"ସ", u"ହ", u"଺", u"଻", u"଼", u"ଽ", u"ା", u"ି", u"ୀ", u"ୁ", u"ୂ",
              u"ୃ", u"ୄ", u"୅", u"୆", u"େ", u"ୈ", u"୉", u"୊", u"ୋ", u"ୌ", u"୍",
              u"୎", u"୏", u"୐", u"୑", u"୒", u"୓", u"୔", u"୕", u"ୖ", u"ୗ", u"୘",
              u"୙", u"୚", u"୛", u"ଡ଼", u"ଢ଼", u"୞", u"ୟ", u"ୠ", u"ୡ", u"ୢ", u"ୣ",
              u"୤", u"୥", u"୦", u"୧", u"୨", u"୩", u"୪", u"୫", u"୬", u"୭", u"୮",
              u"୯", u"୰", u"ୱ", u"୲", u"୳", u"୴", u"୵", u"୶", u"୷", u"୸", u"୹",
              u"୺", u"୻", u"୼", u"୽", u"୾", u"୿"],
    "ta_IN": [u"஁", u"ஂ", u"ஃ", u"஄", u"அ", u"ஆ", u"இ", u"ஈ", u"உ", u"ஊ", u"஋",
              u"஌", u"஍", u"எ", u"ஏ", u"ஐ", u"஑", u"ஒ", u"ஓ", u"ஔ", u"க", u"஖",
              u"஗", u"஘", u"ங", u"ச", u"஛", u"ஜ", u"஝", u"ஞ", u"ட", u"஠", u"஡",
              u"஢", u"ண", u"த", u"஥", u"஦", u"஧", u"ந", u"ன", u"ப", u"஫", u"஬",
              u"஭", u"ம", u"ய", u"ர", u"ற", u"ல", u"ள", u"ழ", u"வ", u"ஶ", u"ஷ",
              u"ஸ", u"ஹ", u"஺", u"஻", u"஼", u"஽", u"ா", u"ி", u"ீ", u"ு", u"ூ",
              u"௃", u"௄", u"௅", u"ெ", u"ே", u"ை", u"௉", u"ொ", u"ோ", u"ௌ", u"்",
              u"௎", u"௏", u"ௐ", u"௑", u"௒", u"௓", u"௔", u"௕", u"௖", u"ௗ", u"௘",
              u"௙", u"௚", u"௛", u"௜", u"௝", u"௞", u"௟", u"௠", u"௡", u"௢", u"௣",
              u"௤", u"௥", u"௦", u"௧", u"௨", u"௩", u"௪", u"௫", u"௬", u"௭", u"௮",
              u"௯", u"௰", u"௱", u"௲", u"௳", u"௴", u"௵", u"௶", u"௷", u"௸", u"௹",
              u"௺", u"௻", u"௼", u"௽", u"௾", u"௿"],
    "te_IN": [u"ఁ", u"ం", u"ః", u"ఄ", u"అ", u"ఆ", u"ఇ", u"ఈ", u"ఉ", u"ఊ", u"ఋ",
              u"ఌ", u"఍", u"ఎ", u"ఏ", u"ఐ", u"఑", u"ఒ", u"ఓ", u"ఔ", u"క", u"ఖ",
              u"గ", u"ఘ", u"ఙ", u"చ", u"ఛ", u"జ", u"ఝ", u"ఞ", u"ట", u"ఠ", u"డ",
              u"ఢ", u"ణ", u"త", u"థ", u"ద", u"ధ", u"న", u"఩", u"ప", u"ఫ", u"బ",
              u"భ", u"మ", u"య", u"ర", u"ఱ", u"ల", u"ళ", u"ఴ", u"వ", u"శ", u"ష",
              u"స", u"హ", u"఺", u"఻", u"఼", u"ఽ", u"ా", u"ి", u"ీ", u"ు", u"ూ",
              u"ృ", u"ౄ", u"౅", u"ె", u"ే", u"ై", u"౉", u"ొ", u"ో", u"ౌ", u"్",
              u"౎", u"౏", u"౐", u"౑", u"౒", u"౓", u"౔", u"ౕ", u"ౖ", u"౗", u"ౘ",
              u"ౙ", u"ౚ", u"౛", u"౜", u"ౝ", u"౞", u"౟", u"ౠ", u"ౡ", u"ౢ", u"ౣ",
              u"౤", u"౥", u"౦", u"౧", u"౨", u"౩", u"౪", u"౫", u"౬", u"౭", u"౮",
              u"౯", u"౰", u"౱", u"౲", u"౳", u"౴", u"౵", u"౶", u"౷", u"౸", u"౹",
              u"౺", u"౻", u"౼", u"౽", u"౾", u"౿"],
    "kn_IN": [u"ಁ", u"ಂ", u"ಃ", u"಄", u"ಅ", u"ಆ", u"ಇ", u"ಈ", u"ಉ", u"ಊ", u"ಋ",
              u"ಌ", u"಍", u"ಎ", u"ಏ", u"ಐ", u"಑", u"ಒ", u"ಓ", u"ಔ", u"ಕ", u"ಖ",
              u"ಗ", u"ಘ", u"ಙ", u"ಚ", u"ಛ", u"ಜ", u"ಝ", u"ಞ", u"ಟ", u"ಠ", u"ಡ",
              u"ಢ", u"ಣ", u"ತ", u"ಥ", u"ದ", u"ಧ", u"ನ", u"಩", u"ಪ", u"ಫ", u"ಬ",
              u"ಭ", u"ಮ", u"ಯ", u"ರ", u"ಱ", u"ಲ", u"ಳ", u"಴", u"ವ", u"ಶ", u"ಷ",
              u"ಸ", u"ಹ", u"಺", u"಻", u"಼", u"ಽ", u"ಾ", u"ಿ", u"ೀ", u"ು", u"ೂ",
              u"ೃ", u"ೄ", u"೅", u"ೆ", u"ೇ", u"ೈ", u"೉", u"ೊ", u"ೋ", u"ೌ", u"್",
              u"೎", u"೏", u"೐", u"೑", u"೒", u"೓", u"೔", u"ೕ", u"ೖ", u"೗", u"೘",
              u"೙", u"೚", u"೛", u"೜", u"ೝ", u"ೞ", u"೟", u"ೠ", u"ೡ", u"ೢ", u"ೣ",
              u"೤", u"೥", u"೦", u"೧", u"೨", u"೩", u"೪", u"೫", u"೬", u"೭", u"೮",
              u"೯", u"೰", u"ೱ", u"ೲ", u"ೳ", u"೴", u"೵", u"೶", u"೷", u"೸", u"೹",
              u"೺", u"೻", u"೼", u"೽", u"೾", u"೿"],
    "ml_IN": [u"ഁ", u"ം", u"ഃ", u"ഄ", u"അ", u"ആ", u"ഇ", u"ഈ", u"ഉ", u"ഊ", u"ഋ",
              u"ഌ", u"഍", u"എ", u"ഏ", u"ഐ", u"഑", u"ഒ", u"ഓ", u"ഔ", u"ക", u"ഖ",
              u"ഗ", u"ഘ", u"ങ", u"ച", u"ഛ", u"ജ", u"ഝ", u"ഞ", u"ട", u"ഠ", u"ഡ",
              u"ഢ", u"ണ", u"ത", u"ഥ", u"ദ", u"ധ", u"ന", u"ഩ", u"പ", u"ഫ", u"ബ",
              u"ഭ", u"മ", u"യ", u"ര", u"റ", u"ല", u"ള", u"ഴ", u"വ", u"ശ", u"ഷ",
              u"സ", u"ഹ", u"ഺ", u"഻", u"഼", u"ഽ", u"ാ", u"ി", u"ീ", u"ു", u"ൂ",
              u"ൃ", u"ൄ", u"൅", u"െ", u"േ", u"ൈ", u"൉", u"ൊ", u"ോ", u"ൌ", u"്",
              u"ൎ", u"൏", u"൐", u"൑", u"൒", u"൓", u"ൔ", u"ൕ", u"ൖ", u"ൗ", u"൘",
              u"൙", u"൚", u"൛", u"൜", u"൝", u"൞", u"ൟ", u"ൠ", u"ൡ", u"ൢ", u"ൣ",
              u"൤", u"൥", u"൦", u"൧", u"൨", u"൩", u"൪", u"൫", u"൬", u"൭", u"൮",
              u"൯", u"൰", u"൱", u"൲", u"൳", u"൴", u"൵", u"൶", u"൷", u"൸", u"൹",
              u"ൺ", u"ൻ", u"ർ", u"ൽ", u"ൾ", u"ൿ"],
    "en_US": [u"a", u"b", u"c", u"d", u"e", u"f", u"g", u"h", u"i", u"j", u"k",
              u"l", u"m", u"n", u"o", u"p", u"q", u"r", u"s", u"t", u"u", u"v",
              u"w", u"x", u"y", u"z"],
}

charmap_transphon = {
    "ISO15919": ["m̐", "ṁ", "ḥ", "", "a", "ā", "i", "ī", "u", "ū", "ṛ", "ḷ",
                 "ê", "e", "ē", "ai", "ô", "o", "ō", "au", "ka", "kha", "ga",
                 "gha", "ṅa", "ca", "cha", "ja", "jha", "ña", "ṭa", "ṭha",
                 "ḍa", "ḍha", "ṇa", "ta", "tha", "da", "dha", "na", "ṉa",
                 "pa", "pha", "ba", "bha", "ma", "ya", "ra", "ṟa", "la", "ḷa",
                 "ḻa", "va", "śa", "ṣa", "sa", "ha", "", "", "", "'", "ā", "i",
                 "ī", "u", "ū", "ṛ", "ṝ", "ê", "e", "ē", "ai", "ô", "o", "ō",
                 "au", "", "", "", "oṃ", "", "", "", "", "", "", "", "qa",
                 "ḵẖa", "ġ", "za", "ṛa", "ṛha", "fa", "ẏa", "ṝ", "ḹ", "ḷ",
                 "ḹ", ".", "..", "0", "1", "2", "3", "4", "5", "6", "7", "8",
                 "9", "…", "", "", "", "", "", "", "", "", "", "", "", "", "",
                 "", "", "", ""],
    "IPA": ["m", "m", "", "", "ə", "aː", "i", "iː", "u", "uː", "r̩", "l̩", "æ",
            "e", "eː", "ɛː", "ɔ", "o", "oː", "ow", "kə", "kʰə", "gə", "gʱə",
            "ŋə", "ʧə", "ʧʰə", "ʤə", "ʤʱə", "ɲə", "ʈə", "ʈʰə", "ɖə", "ɖʱə",
            "ɳə", "t̪ə", "t̪ʰə", "d̪ə", "d̪ʱə", "n̪ə", "nə", "pə", "pʰə", "bə",
            "bʱə", "mə", "jə", "ɾə", "rə", "lə", "ɭə", "ɻə", "ʋə", "ɕə", "ʂə",
            "sə", "ɦə", "", "", "", "ഽ", "aː", "i", "iː", "u", "uː", "r̩",
            "l̩", "e", "eː", "ɛː", "ɔ", "o", "oː", "ow", "", "", "", "", "",
            "", "", "", "", "", "ow", "", "", "", "", "", "", "", "", "r̩ː",
            "l̩ː", "", "", "", "", "0", "1", "2", "3", "4", "5", "6", "7", "8",
            "9", "൰", "", "", "", "", "", "", "", "", "", "", "", "", "", "",
            ""]
}


@lru_cache(maxsize=1024)
def char_compare(char1, char2):
    ''' Check if 2 characters are similar

        This function checks if given 2 characters are similar but are
        from 2 different languages.

        :param char1: First character for comparison
        :param char2: Second character for comparison

        :return: 0 if both characters are same, 1 if both characters
                 are similar but from different language and -1 if any
                 one or both characters are not found
    '''
    if char1 == char2:
        return 0

    char1_index = -1
    char2_index = -1

    char1_lang = get_language(char1)
    char2_lang = get_language(char2)

    if char1_lang is not None and char2_lang is not None:
        # Is this IPA or ISO15919 char?
        if char1_lang in ["ISO15919", "IPA"]:
            char1_index = charmap_transphon[char1_lang].index(char1)

        if char2_lang in ["ISO15919", "IPA"]:
            char2_index = charmap_transphon[char2_lang].index(char2)

        # Still index not found?
        if char1_index == -1:
            char1_index = charmap[char1_lang].index(char1)

        if char2_index == -1:
            char2_index = charmap[char2_lang].index(char2)

        # is char index similar?
        if char1_index == char2_index:
            return 1

    # char's are not similar
    return -1


@lru_cache(maxsize=1024)
def get_language(char):
    ''' Get the language of given `char'

       Return the language of given character, if character language
       is not found `None' is returned.

       :param char:
           The char whose language is to be detected
       :return: string representing language or None if char not found
           in our mapping.
    '''
    if sys.version_info.major == 2:
        tmpchr = char.decode('utf-8') if type(char).__name__ == 'str' else char
    else:
        tmpchr = char
    for lang in charmap:
        if tmpchr.lower() in charmap[lang]:
                return lang

    if sys.version_info.major == 2:
        tmpchr = char.encode('utf-8') if type(char).__name__ == 'unicode'\
            else char
    else:
        tmpchr = char

    # Reached here means no language is found check in ISO and IPA set
    for lang in charmap_transphon:
        if tmpchr in charmap_transphon[lang]:
            return lang

    # Nothing found!
    return None
