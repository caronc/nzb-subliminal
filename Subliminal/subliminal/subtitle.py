# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import logging
import os.path
import babelfish
import pysrt
import re
from .video import Episode, Movie

from chardet import detect as chardet_detect
from chared.detector import get_model_path, EncodingDetector

# Year regular expression checker used in fuzzy searching
DETECTED_YEAR_RE = re.compile('^(?P<title>.+)\s+\(?(?P<year>[123][0-9]{3})\)?\s*$')

SUBTITLE_EXTENSIONS = ('.srt', '.sub', '.smi', '.txt', '.ssa', '.ass', '.mpl')

# A table used to map language codes to their respected chared decoding file
# if a mapping isn't defined on this table, then the code simply falls back
# to chardet encoding detection. chardet is not as accurate as chared, but
# chared has more overhead. The table will be an add on demand (if something
# is missing)
CHARED_LANGUAGE_MAP = {
    u'ar': u'arabic',
    u'hy': u'armenian',
    u'bn': u'bengali',
    u'bg': u'bulgarian',
    u'ca': u'catalan',
    u'hr': u'croatian',
    u'cs': u'czech',
    u'nl': u'dutch',
    u'en': u'english',
    u'et': u'estonian',
    u'fi': u'finnish',
    u'fr': u'french',
    u'de': u'german',
    u'el': u'greek',
    u'gu': u'gujarati',
    u'hi': u'hindi',
    u'hu': u'hungarian',
    u'is': u'icelandic',
    u'id': u'indonesian',
    u'ga': u'irish',
    u'it': u'italian',
    u'ja': u'japanese',
    u'ko': u'korean',
    u'lv': u'latvian',
    u'lt': u'lithuanian',
    u'ml': u'malayalam',
    u'ms': u'malay',
    u'mt': u'maltese',
    u'nb': u'norwegian_bokmal',
    u'fa': u'persian',
    u'pl': u'polish',
    u'pt': u'portuguese',
    u'ro': u'romanian',
    u'ru': u'russian',
    u'sr': u'serbian',
    u'sk': u'slovak',
    u'sl': u'slovene',
    u'es': u'spanish',
    u'sv': u'swedish',
    u'ta': u'tamil',
    u'te': u'telugu',
    u'th': u'thai',
    u'tr': u'turkish',
    u'uk': u'ukrainian',
    u'ur': u'urdu',
    u'vi': u'vietnamese',
    u'cy': u'welsh',
}

STRING_SANITIZATION = {
    'À': 'A', 'Á': 'A', 'Â': 'A', 'Ã': 'A', 'Ä': 'A', 'Å': 'A',
    'Ǟ': 'A', 'Ǡ': 'A', 'Ȁ': 'A', 'Ȃ': 'A', 'Ǻ': 'A', 'Ǽ': 'AE',
    'à': 'a', 'á': 'a', 'â': 'a', 'ã': 'a', 'ä': 'a', 'å': 'a',
    'ǟ': 'a', 'ǡ': 'a', 'ȁ': 'a', 'ȃ': 'a', 'ǻ': 'a', 'ǽ': 'ae',
    'ç': 'c', 'ć': 'c', 'ĉ': 'c', 'ċ': 'c', 'č': 'c',
    'Ç': 'C', 'Ć': 'C', 'Ĉ': 'C', 'Ċ': 'C', 'Č': 'C',
    'È': 'E', 'É': 'E', 'Ê': 'E', 'Ë': 'E', 'Ē': 'E', 'Ĕ': 'E',
    'Ė': 'E', 'Ę': 'E', 'Ě': 'E', 'Ȅ': 'E', 'Ȇ': 'E',
    'è': 'e', 'é': 'e', 'ê': 'e', 'ë': 'e', 'ē': 'e', 'ĕ': 'e',
    'ė': 'e', 'ę': 'e', 'ě': 'e', 'ǝ': 'e', 'ȅ': 'e', 'ȇ': 'e',
    'Ì': 'I', 'Í': 'I', 'Î': 'I', 'Ï': 'I', 'Ĩ': 'I', 'Ī': 'I',
    'Ĭ': 'I', 'Į': 'I', 'İ': 'I',
    'ì': 'i', 'í': 'i', 'î': 'i', 'ï': 'i', 'ĩ': 'i', 'ī': 'i',
    'ĭ': 'i', 'į': 'i', 'ı': 'i',
    'Ò': 'O', 'Ó': 'O', 'Ô': 'O', 'Õ': 'O', 'Ö': 'O',
    'Ō': 'O', 'Ŏ': 'O', 'Ő': 'O', 'Ǿ': 'O',
    'ò': 'o', 'ó': 'o', 'ô': 'o', 'õ': 'o', 'ö': 'o',
    'ō': 'o', 'ŏ': 'o', 'ő': 'o', 'ǿ': 'o',
    'Ƿ': 'p',
    'Ɲ': 'N', 'ƞ': 'n', 'Ǹ': 'N', 'ǹ': 'n',
    'Ń': 'N', 'ń': 'n', 'Ņ': 'N', 'ņ': 'n', 'Ň': 'N', 'ň': 'n',
    'ŉ': 'n', 'Ŋ': 'N', 'ŋ': 'n',
    'Ŕ': 'R', 'Ŗ': 'R', 'Ř': 'R',
    'ŕ': 'r', 'ŗ': 'r', 'ř': 'r',
    'Ś': 'S', 'Ŝ': 'S', 'Ş': 'S', 'Š': 'S',
    'ś': 's', 'ŝ': 's', 'ş': 's', 'š': 's',
    'Ţ': 'T', 'Ť': 'T', 'Ŧ': 'T',
    'ţ': 't', 'ť': 't', 'ŧ': 't',
    'Ȕ': 'U', 'Ȗ': 'U', 'Ǔ': 'U', 'Ǖ': 'U', 'Ǘ': 'U', 'Ǚ': 'U',
    'Ǜ': 'U',
    'ȕ': 'u', 'ȗ': 'u', 'ǔ': 'u', 'ǖ': 'u', 'ǘ': 'u', 'ǚ': 'u',
    'ǜ': 'u', 'ū': 'u',
}

STRING_SANITIZATION_RE = re.compile(
    r'(' + '|'.join(STRING_SANITIZATION.keys()) + r')',
)

logger = logging.getLogger(__name__)

#  The following characters are always stripped
IGNORED_CHARACTERS_RE = re.compile('[!@#$\'"]')

# non-printable ascii characters
PRINTABLE_ASCII_RE = re.compile(r'[^\x20-\x7E]+')

# Date parsing
STRIP_DATE_RE = re.compile('^\s*([^\[(]+)[\s\[(]?\s*([123][0-9]{3})[\s\])]?\s*$')

def detect(str_data, lang=None):
    """
    A wrapper to encoding detection since we try to make use of both
    chardet and chared together.

    The response is always geared to look like a chardet library call
    thus the output is always like this:
     {
       'encoding': '<encoding type>',
       'confidence': <float value between 0.0 and 100.0>,
     }
    """
    if lang is not None:
        try:
            lang = CHARED_LANGUAGE_MAP[lang]

        except KeyError:
            # No lookup
            lang = None

    if lang is None:
        # Without knowing the language, we need to make our best
        # guess using chardet
        return chardet_detect(str_data)

    # If we reach here, we know the language associated with the str_data
    # being provided.  We can make a better prediction this way.
    try:
        model_file = get_model_path(lang)
    except:
        # Return best guess
        return chardet_detect(str_data)

    try:
        encoding_detector = EncodingDetector.load(model_file)
    except:
        # Return best guess
        return chardet_detect(str_data)

    # Classify our data
    clas = encoding_detector.classify(str_data)
    if not clas:
        # Classification wasn't possible, return best guess
        return chardet_detect(str_data)

    # chared results (return as chardet would)
    return {
       'encoding': clas[0],
       'confidence': 99.999999,
    }


class Subtitle(object):
    """Base class for subtitle

    :param language: language of the subtitle
    :type language: :class:`babelfish.Language`
    :param bool hearing_impaired: `True` if the subtitle is hearing impaired, `False` otherwise

    """
    def __init__(self, language, hearing_impaired=False):
        #: Language of the subtitle
        self.language = language

        #: URL of the web page from which the subtitle can be downloaded
        self.hearing_impaired = hearing_impaired

        #: Content as bytes
        self.content = None

    def compute_matches(self, video):
        """Compute the matches of the subtitle against the `video`

        :param video: the video to compute the matches against
        :type video: :class:`~subliminal.video.Video`
        :return: matches of the subtitle
        :rtype: set

        """
        raise NotImplementedError

    def compute_score(self, video, hi_score_adjust=0):
        """Compute the score of the subtitle against the `video`

        There are equivalent matches so that a provider can match one element or its equivalent. This is
        to give all provider a chance to have a score in the same range without hurting quality.

        * Matching :class:`~subliminal.video.Video`'s `hashes` is equivalent to matching everything else
        * Matching :class:`~subliminal.video.Episode`'s `season` and `episode`
          is equivalent to matching :class:`~subliminal.video.Episode`'s `title`
        * Matching :class:`~subliminal.video.Episode`'s `tvdb_id` is equivalent to matching
          :class:`~subliminal.video.Episode`'s `series`

        :param video: the video to compute the score against
        :type video: :class:`~subliminal.video.Video`
        :param hi_score_adjust: adjust hearing impaired matched videos by this value
        :return: score of the subtitle
        :rtype: int

        """
        score = 0
        # compute matches
        initial_matches = self.compute_matches(video)
        matches = initial_matches.copy()
        # hash is the perfect match
        if 'hash' in matches:
            score = video.scores['hash']
        else:
            # remove equivalences
            if isinstance(video, Episode):
                if 'imdb_id' in matches:
                    matches -= set(['series', 'tvdb_id', 'season', 'episode', 'title'])
                if 'tvdb_id' in matches:
                    matches -= set(['series',])
                if 'title' in matches:
                    matches -= set(['season', 'episode'])
            # add other scores
            score += sum([video.scores[match] for match in matches])

            # Adjust scoring if hearing impaired subtitles are detected
            if self.hearing_impaired and hi_score_adjust != 0:
                logger.debug('Hearing impaired subtitle score adjusted ' + \
                             'by %d' % hi_score_adjust)
                # Priortization (adjust score)
                score += hi_score_adjust

        logger.debug('Computed score %d with matches %r', score, initial_matches)
        return score

    def __repr__(self):
        return '<%s [%s]>' % (self.__class__.__name__, self.language)

def extract_title_year(str_in):
    """
    If the year can be extracted from the title
    as part of it's name; then it is returned by
    this function
    """
    str_date_re = STRIP_DATE_RE.match(str_in)
    if str_date_re:
        return str(str_date_re.group(2)).strip()
    return ""

def sanitize_string(str_in, strip_date=False):
    """
    Sanitizes a string passed into it by eliminating characters that might
    otherwise cause issues when attempting to locate a match on websites by
    striping out any special characters and forcing a consistent string that
    can be used for caching too.

    :param string str_in: the string to sanitize
    :param bool strip_date: Eliminates trailing dates if found in string
    :return: sanitized string
    :rtype: string
    """
    if not isinstance(str_in, basestring):
        # handle int, float, etc
        str_in = str(str_in)

    # First we do best guess placement of all unicode characters
    # to their ascii equivalent (if it's possible.
    str_out = STRING_SANITIZATION_RE.sub(
        lambda x: STRING_SANITIZATION[x.group()], str_in)

    # Now we strip out anything that isn't printable still
    # lingering
    str_out = PRINTABLE_ASCII_RE.sub('', str_out)

    # Finally eliminate any extra printable characters that
    # really just should't be used.
    str_out = IGNORED_CHARACTERS_RE.sub('', str_out).lower()

    str_date_re = STRIP_DATE_RE.match(str_out)
    if str_date_re:
        str_out = str_date_re.group(1).strip()
        if not strip_date and str_date_re.group(2):
            str_out += ' ' + str_date_re.group(2)

    return str_out.strip()

def get_subtitle_path(video_path, language=None):
    """Create the subtitle path from the given `video_path` and `language`

    :param string video_path: path to the video
    :param language: language of the subtitle to put in the path
    :type language: :class:`babelfish.Language` or None
    :return: path of the subtitle
    :rtype: string

    """
    subtitle_path = os.path.splitext(video_path)[0]
    if isinstance(subtitle_path, str):
        try:
            subtitle_path = subtitle_path.decode('utf-8', errors='ignore')
        except TypeError:
            # python <= 2.6
            subtitle_path = subtitle_path.decode('utf-8', 'ignore')

    if language is not None:
        try:
            return subtitle_path + '.%s.%s' % (language.alpha2, 'srt')
        except babelfish.LanguageConvertError:
            return subtitle_path + '.%s.%s' % (language.alpha3, 'srt')
    return subtitle_path + '.srt'


def is_valid_subtitle(subtitle_text):
    """Check if a subtitle text is a valid SubRip format

    :return: `True` if the subtitle is valid, `False` otherwise
    :rtype: bool

    """
    try:
        pysrt.from_string(subtitle_text, error_handling=pysrt.ERROR_RAISE)
        return True
    except pysrt.Error as e:
        if e.args[0] > 80:
            return True
    except:
        logger.exception('Unexpected error when validating subtitle')
    return False


def compute_guess_matches(video, guess, fuzzy=True):
    """Compute matches between a `video` and a `guess`

    :param video: the video to compute the matches on
    :type video: :class:`~subliminal.video.Video`
    :param guess: the guess to compute the matches on
    :type guess: :class:`guessit.Guess`
    :param bool fuzzy: whether to be less strict on possible matches
    :return: matches of the `guess`
    :rtype: set

    """
    matches = set()
    if isinstance(video, Episode):
        # Series
        if video.series and 'series' in guess:
            if guess['series'].lower() == video.series.lower():
                matches.add('series')

            elif fuzzy:
                # Disregard trailing years and test again
                _vresult = DETECTED_YEAR_RE.match(video.series)
                _gresult = DETECTED_YEAR_RE.match(guess['series'])

                if _vresult:
                    _vresult = _vresult.group('title').lower()
                else:
                    _vresult = video.series.lower()

                if _gresult:
                    _gresult = _gresult.group('title').lower()
                else:
                    _gresult = guess['series'].lower()

                if _vresult == _gresult:
                    matches.add('series')

        # Season
        if video.season and 'seasonNumber' in guess and guess['seasonNumber'] == video.season:
            matches.add('season')

        elif video.season and 'season' in guess and guess['season'] == video.season:
            # Support season keyword too which comes out of older versions of guessit
            matches.add('season')

        # Episode
        if video.episode and 'episodeNumber' in guess and guess['episodeNumber'] == video.episode:
            matches.add('episode')

    elif isinstance(video, Movie):
        # Year
        if video.year and 'year' in guess and guess['year'] == video.year:
            matches.add('year')
    # Title
    if video.title and 'title' in guess and guess['title'].lower() == video.title.lower():
        matches.add('title')
    # Release group
    if video.release_group and 'releaseGroup' in guess and guess['releaseGroup'].lower() == video.release_group.lower():
        matches.add('release_group')
    # Screen size
    if video.resolution and 'screenSize' in guess and guess['screenSize'] == video.resolution:
        matches.add('resolution')
    # Video codec
    if video.video_codec and 'videoCodec' in guess and guess['videoCodec'] == video.video_codec:
        matches.add('video_codec')
    # Audio codec
    if video.audio_codec and 'audioCodec' in guess and guess['audioCodec'] == video.audio_codec:
        matches.add('audio_codec')
    return matches
