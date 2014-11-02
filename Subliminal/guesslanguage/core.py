''' Guess the language of text.

    Based on guesslanguage.cpp by Jacob R Rideout for KDE
    http://websvn.kde.org/branches/work/sonnet-refactoring/common/nlp/guesslanguage.cpp?view=markup
    which itself is based on Language::Guess by Maciej Ceglowski
    http://languid.cantbedone.org/

    Copyright (c) 2008, Kent S Johnson

    C++ version is Copyright (c) 2006 Jacob R Rideout <kde@jacobrideout.net>
    Perl version is (c) 2004-6 Maciej Ceglowski

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

    Note: Language::Guess is GPL-licensed. KDE developers received permission
    from the author to distribute their port under LGPL:
    http://lists.kde.org/?l=kde-sonnet&m=116910092228811&w=2

'''

import codecs
import os
import re
import sys
import unicodedata
from silpa_common.langdetect import detect_lang
__all__ = ["LangGuess", "getInstance"]

try:
    from collections import defaultdict
except:
    class defaultdict(dict):
        def __init__(self, default_factory=None, *a, **kw):
            if (default_factory is not None and
                    not hasattr(default_factory, '__call__')):
                raise TypeError('first argument must be callable')
            dict.__init__(self, *a, **kw)
            self.default_factory = default_factory

        def __getitem__(self, key):
            try:
                return dict.__getitem__(self, key)
            except KeyError:
                return self.__missing__(key)

        def __missing__(self, key):
            if self.default_factory is None:
                raise KeyError(key)
            self[key] = value = self.default_factory()
            return value

        def __reduce__(self):
            if self.default_factory is None:
                args = tuple()
            else:
                args = self.default_factory,
            return type(self), args, None, None, self.items()

        def copy(self):
            return self.__copy__()

        def __copy__(self):
            return type(self)(self.default_factory, self)

        def __deepcopy__(self, memo):
            import copy
            return type(self)(self.default_factory,
                              copy.deepcopy(self.items()))

        def __repr__(self):
            return 'defaultdict(%s, %s)' % (self.default_factory,
                                            dict.__repr__(self))

MIN_LENGTH = 20

BASIC_LATIN = "en_US ceb ha so tlh id haw la sw eu nr nso zu_ZA xh ss st tn ts".split()
EXTENDED_LATIN = "cs af_ZA pl_PL hr_HR ro sk sl tr hu_HU az et sq ca es fr de nl it_IT da is nb sv fi lv pt ve lt tl cy".split()
ALL_LATIN = BASIC_LATIN + EXTENDED_LATIN
CYRILLIC = "ru uk kk uz mn sr mk bg ky".split()
ARABIC = "ar fa ps ur".split()
DEVANAGARI = "hi_IN ne".split()

# NOTE mn appears twice, once for mongolian script and once for CYRILLIC
SINGLETONS = [
    ('Armenian', 'hy'),
    ('Hebrew', 'he'),
    ('Bengali', 'bn_IN'),
    ('Gurmukhi', 'pa'),
    ('Greek', 'el'),
    ('Gujarati', 'gu_IN'),
    ('Oriya', 'or_IN'),
    ('Tamil', 'ta_IN'),
    ('Telugu', 'te_IN'),
    ('Kannada', 'kn_IN'),
    ('Malayalam', 'ml_IN'),
    ('Sinhala', 'si'),
    ('Thai', 'th'),
    ('Lao', 'lo'),
    ('Tibetan', 'bo'),
    ('Burmese', 'my'),
    ('Georgian', 'ka'),
    ('Mongolian', 'mn-Mong'),
    ('Khmer', 'km'),
]

PT = "pt_BR pt_PT".split()

UNKNOWN = 'UNKNOWN'

models = {}

NAME_MAP = {
    "ab": "Abkhazian",
    "af_ZA": "Afrikaans",
    "ar": "Arabic",
    "az": "Azeri",
    "be": "Byelorussian",
    "bg": "Bulgarian",
    "bn": "Bengali",
    "bo": "Tibetan",
    "br": "Breton",
    "ca": "Catalan",
    "ceb": "Cebuano",
    "cs": "Czech",
    "cy": "Welsh",
    "da": "Danish",
    "de_DE": "German",
    "el": "Greek",
    "en": "English",
    "en_US": "English",
    "eo": "Esperanto",
    "es": "Spanish",
    "et": "Estonian",
    "eu": "Basque",
    "fa": "Farsi",
    "fi": "Finnish",
    "fo": "Faroese",
    "fr": "French",
    "fy": "Frisian",
    "gd": "Scots Gaelic",
    "gl": "Galician",
    "gu_IN": "Gujarati",
    "ha": "Hausa",
    "haw": "Hawaiian",
    "he": "Hebrew",
    "hi_IN": "Hindi",
    "hr_HR": "Croatian",
    "hu_HU": "Hungarian",
    "hy": "Armenian",
    "id": "Indonesian",
    "is": "Icelandic",
    "it_IT": "Italian",
    "ja_JP": "Japanese",
    "ka": "Georgian",
    "kk": "Kazakh",
    "kn_IN": "Kannada",
    "km": "Cambodian",
    "ko": "Korean",
    "ku": "Kurdish",
    "ky": "Kyrgyz",
    "la": "Latin",
    "lt": "Lithuanian",
    "lv": "Latvian",
    "mg": "Malagasy",
    "mk": "Macedonian",
    "ml_IN": "Malayalam",
    "mn": "Mongolian",
    "mr_IN": "Marathi",
    "ms": "Malay",
    "nd": "Ndebele",
    "ne": "Nepali",
    "nl": "Dutch",
    "nn": "Nynorsk",
    "no": "Norwegian",
    "or_IN": "Oriya(Odiya)",
    "nso": "Sepedi",
    "pa_IN": "Punjabi",
    "pl_PL": "Polish",
    "ps": "Pashto",
    "pt": "Portuguese",
    "ro": "Romanian",
    "ru": "Russian",
    "sa_IN": "Sanskrit",
    "sh": "Serbo-Croatian",
    "sk": "Slovak",
    "sl": "Slovene",
    "so": "Somali",
    "sq": "Albanian",
    "sr": "Serbian",
    "sv": "Swedish",
    "sw": "Swahili",
    "ta_IN": "Tamil",
    "te_IN": "Telugu",
    "th": "Thai",
    "tl": "Tagalog",
    "tlh": "Klingon",
    "tn": "Setswana",
    "tr": "Turkish",
    "ts": "Tsonga",
    "tw": "Twi",
    "uk": "Ukrainian",
    "uk": "Ukranian",
    "ur": "Urdu",
    "uz": "Uzbek",
    "ve": "Venda",
    "vi": "Vietnamese",
    "xh": "Xhosa",
    "zh": "Chinese",
    "zh-tw": "Traditional Chinese (Taiwan)",
    "zu_ZA": "Zulu",
}

IANA_MAP = {
    "ab": 12026,
    "af_ZA": 40,
    "ar": 26020,
    "az": 26030,
    "be": 11890,
    "bg": 26050,
    "bn": 26040,
    "bo": 26601,
    "br": 1361,
    "ca": 3,
    "ceb": 26060,
    "cs": 26080,
    "cy": 26560,
    "da": 26090,
    "de_DE": 26160,
    "el": 26165,
    "en": 26110,
    "eo": 11933,
    "es": 26460,
    "et": 26120,
    "eu": 1232,
    "fa": 26130,
    "fi": 26140,
    "fo": 11817,
    "fr": 26150,
    "fy": 1353,
    "gd": 65555,
    "gl": 1252,
    "gu": 26599,
    "ha": 26170,
    "haw": 26180,
    "he": 26592,
    "hi_IN": 26190,
    "hr_HR": 26070,
    "hu_HU": 26200,
    "hy": 26597,
    "id": 26220,
    "is": 26210,
    "it_IT": 26230,
    "ja": 26235,
    "ka": 26600,
    "kk": 26240,
    "km": 1222,
    "ko": 26255,
    "ku": 11815,
    "ky": 26260,
    "la": 26280,
    "lt": 26300,
    "lv": 26290,
    "mg": 1362,
    "mk": 26310,
    "ml": 26598,
    "mn": 26320,
    "mr": 1201,
    "ms": 1147,
    "ne": 26330,
    "nl": 26100,
    "nn": 172,
    "no": 26340,
    "pa": 65550,
    "pl": 26380,
    "ps": 26350,
    "pt": 26390,
    "ro": 26400,
    "ru": 26410,
    "sa": 1500,
    "sh": 1399,
    "sk": 26430,
    "sl": 26440,
    "so": 26450,
    "sq": 26010,
    "sr": 26420,
    "sv": 26480,
    "sw": 26470,
    "ta": 26595,
    "te": 26596,
    "th": 26594,
    "tl": 26490,
    "tlh": 26250,
    "tn": 65578,
    "tr": 26500,
    "tw": 1499,
    "uk": 26510,
    "uk": 26520,
    "ur": 26530,
    "uz": 26540,
    "vi": 26550,
    "zh": 26065,
    "zh-tw": 22,
}


def _load_models():
    modelsDir = os.path.join(os.path.dirname(__file__), 'trigrams')
    modelsList = os.listdir(modelsDir)
    lineRe = re.compile(r"(.{3})\s+(.*)")
    for modelFile in modelsList:
        modelPath = os.path.join(modelsDir, modelFile)
        if os.path.isdir(modelPath):
            continue
        f = codecs.open(modelPath, 'r', 'utf-8')
        model = {}  # QHash<QString,int> model
        for line in f:
            m = lineRe.search(line)
            if m:
                model[m.group(1)] = int(m.group(2))

        models[modelFile.lower()] = model


def guessLanguage(text):
    ''' Returns the language code, i.e. 'en' '''
    if not text:
        return UNKNOWN

    if isinstance(text, str):
        text = unicode(text, 'utf-8')

    text = normalize(text)

    return _identify(text, find_runs(text))


def guessLanguageInfo(text):
    """
        Returns (tag, id, name)  i.e. ('en', 26110, 'english')
    """
    tag = guessLanguage(text)

    if tag == UNKNOWN:
        return UNKNOWN, UNKNOWN, UNKNOWN

    id = _getId(tag)
    name = _getName(tag)
    return tag, id, name


# An alias for guessLanguage
guessLanguageTag = guessLanguage


def guessLanguageId(text):
    """
        Returns the language id.  i.e. 26110
    """
    lang = guessLanguage(text)
    return _getId(lang)


def guessLanguageName(text):
    """
        Returns the language name.  i.e. 'english'
    """
    lang = guessLanguage(text)
    return _getName(lang)


def _getId(iana):
    return IANA_MAP.get(iana, UNKNOWN)


def _getName(iana):
    return NAME_MAP.get(iana, UNKNOWN)


def find_runs(text):
    ''' Count the number of characters in each character block '''
    run_types = defaultdict(int)

    totalCount = 0
    from blocks import unicodeBlock
    for c in text:
        if c.isalpha():
            block = unicodeBlock(c)
            run_types[block] += 1
            totalCount += 1

#    pprint.pprint(run_types)

    # return run types that used for 40% or more of the string
    # always return basic latin if found more than 15%
    # and extended additional latin if over 10% (for Vietnamese)
    relevant_runs = []
    for key, value in run_types.items():
        pct = (value*100) / totalCount
        if pct >= 40:
            relevant_runs.append(key)
        elif key == "Basic Latin" and (pct >= 15):
            relevant_runs.append(key)
        elif key == "Latin Extended Additional" and (pct >= 10):
            relevant_runs.append(key)

    return relevant_runs


def _identify(sample, scripts):
    if len(sample) < 3:
        return UNKNOWN

    if "Hangul Syllables" in scripts or "Hangul Jamo" in scripts \
            or "Hangul Compatibility Jamo" in scripts or "Hangul" in scripts:
        return "ko"

    if "Greek and Coptic" in scripts:
        return "el"

    if "Katakana" in scripts or "Hiragana" in scripts or "Katakana Phonetic Extensions" in scripts:
        return "ja"

    if "CJK Unified Ideographs" in scripts or "Bopomofo" in scripts \
            or "Bopomofo Extended" in scripts or "KangXi Radicals" in scripts:

# This is in both Ceglowski and Rideout
# I can't imagine why...
#            or "Arabic Presentation Forms-A" in scripts
        return "zh"

    if "Cyrillic" in scripts:
        return check(sample, CYRILLIC)

    if "Arabic" in scripts or "Arabic Presentation Forms-A" in scripts or "Arabic Presentation Forms-B" in scripts:
        return check(sample, ARABIC)

    if "Devanagari" in scripts:
        return check(sample, DEVANAGARI)

    # Try languages with unique scripts
    for blockName, langName in SINGLETONS:
        if blockName in scripts:
            return langName

    if "Latin Extended Additional" in scripts:
        return "vi"

    if "Extended Latin" in scripts:
        latinLang = check(sample, EXTENDED_LATIN)
        if latinLang == "pt":
            return check(sample, PT)
        else:
            return latinLang

    if "Basic Latin" in scripts:
        return check(sample, ALL_LATIN)

    return UNKNOWN


def check(sample, langs):
    if len(sample) < MIN_LENGTH:
        return UNKNOWN

    scores = []
    model = createOrderedModel(sample)  # QMap<int,QString>

    for key in langs:
        lkey = key.lower()

        if lkey in models:
            scores.append((distance(model, models[lkey]), key))

    if not scores:
        return UNKNOWN

    # we want the lowest score, less distance = greater chance of match
#    pprint(sorted(scores))
    return min(scores)[1]


def createOrderedModel(content):
    ''' Create a list of trigrams in content sorted by frequency '''
    trigrams = defaultdict(int)    # QHash<QString,int>
    content = content.lower()

    for i in xrange(0, len(content)-2):
        trigrams[content[i:i+3]] += 1

    return sorted(trigrams.keys(), key=lambda k: (-trigrams[k], k))


spRe = re.compile(r"\s\s", re.UNICODE)
MAXGRAMS = 300


def distance(model, knownModel):
    dist = 0

    for i, value in enumerate(model[:MAXGRAMS]):
        if not spRe.search(value):
            if value in knownModel:
                dist += abs(i - knownModel[value])
            else:
                dist += MAXGRAMS

    return dist


def _makeNonAlphaRe():
    nonAlpha = [u'[^']
    for i in range(sys.maxunicode):
      c = unichr(i)
      if c.isalpha(): nonAlpha.append(c)
    nonAlpha.append(u']')
    nonAlpha = u"".join(nonAlpha)
    return re.compile(nonAlpha)


spaceRe = re.compile('\s+', re.UNICODE)


def normalize(u):
    ''' Convert to normalized unicode.
        Remove non-alpha chars and compress runs of spaces.
    '''
    nonAlphaRe = _makeNonAlphaRe()
    u = unicodedata.normalize('NFC', u)
    u = nonAlphaRe.sub(' ', u)
    u = spaceRe.sub(' ', u)
    return u


class LangGuess:
    def __init__(self):
        _load_models()

    def guessLanguage(self, text):
        lang = guessLanguageName(text)
        if lang == 'UNKNOWN':
            firstWord = text.split()[0]
            lang = detect_lang(firstWord)[firstWord]
            lang = _getName(lang.split("_")[0])
        return lang

    def guessLanguageId(self, text):
        lang = guessLanguage(text)
        if lang == 'UNKNOWN':
            firstWord = text.split()[0]
            lang = detect_lang(firstWord)[firstWord]
        return lang

    def getScriptName(self, text):
        return dumps(detect_lang(text))

    def get_module_name(self):
        return "Guess Language"

    def get_info(self):
        return "Guess the language of given text. This module can detect more than 50 languages. Based on Language::Guess by Maciej Ceglowski(http://languid.cantbedone.org/)"


def getInstance():
    return LangGuess()
