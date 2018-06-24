# -*- coding: utf-8 -*-
from datetime import datetime
import hashlib
import os
import re
import struct
import logging
from guessit import matcher

logger = logging.getLogger(__name__)

# A simple regular expression that scans the video downloaded and
# detects the season/episode information from it.
DETECT_TVSHOW_RE = re.compile(
    r'^.*[^A-Za-z0-9]?S([0-9]{1,4})E([0-9]{1,4}(E[0-9]{1,4})*)[^A-Za-z0-9]',
    re.IGNORECASE,
)

# Year regular expression checker
DETECTED_YEAR_RE = re.compile('^[^(]+\((?P<year>[123][0-9]{3})\).+$')


def hash_opensubtitles(video_path):
    """Compute a hash using OpenSubtitles' algorithm.

    :param str video_path: path of the video.
    :return: the hash.
    :rtype: str

    """
    bytesize = struct.calcsize(b'<q')
    with open(video_path, 'rb') as f:
        filesize = os.path.getsize(video_path)
        filehash = filesize
        if filesize < 65536 * 2:
            return
        for _ in range(65536 // bytesize):
            filebuffer = f.read(bytesize)
            (l_value,) = struct.unpack(b'<q', filebuffer)
            filehash += l_value
            filehash &= 0xFFFFFFFFFFFFFFFF  # to remain as 64bit number
        f.seek(max(0, filesize - 65536), 0)
        for _ in range(65536 // bytesize):
            filebuffer = f.read(bytesize)
            (l_value,) = struct.unpack(b'<q', filebuffer)
            filehash += l_value
            filehash &= 0xFFFFFFFFFFFFFFFF
    returnedhash = '%016x' % filehash

    return returnedhash


def hash_thesubdb(video_path):
    """Compute a hash using TheSubDB's algorithm.

    :param str video_path: path of the video.
    :return: the hash.
    :rtype: str

    """
    readsize = 64 * 1024
    if os.path.getsize(video_path) < readsize:
        return
    with open(video_path, 'rb') as f:
        data = f.read(readsize)
        f.seek(-readsize, os.SEEK_END)
        data += f.read(readsize)

    return hashlib.md5(data).hexdigest()


def hash_napiprojekt(video_path):
    """Compute a hash using NapiProjekt's algorithm.

    :param str video_path: path of the video.
    :return: the hash.
    :rtype: str

    """
    readsize = 1024 * 1024 * 10
    with open(video_path, 'rb') as f:
        data = f.read(readsize)
    return hashlib.md5(data).hexdigest()


def hash_shooter(video_path):
    """Compute a hash using Shooter's algorithm

    :param string video_path: path of the video
    :return: the hash
    :rtype: string

    """
    filesize = os.path.getsize(video_path)
    readsize = 4096
    if os.path.getsize(video_path) < readsize * 2:
        return None
    offsets = (readsize, filesize // 3 * 2, filesize // 3, filesize - readsize * 2)
    filehash = []
    with open(video_path, 'rb') as f:
        for offset in offsets:
            f.seek(offset)
            filehash.append(hashlib.md5(f.read(readsize)).hexdigest())
    return ';'.join(filehash)


def sanitize(string, ignore_characters=None):
    """Sanitize a string to strip special characters.

    :param str string: the string to sanitize.
    :param set ignore_characters: characters to ignore.
    :return: the sanitized string.
    :rtype: str

    """
    # only deal with strings
    if string is None:
        return

    ignore_characters = ignore_characters or set()

    # replace some characters with one space
    characters = {'-', ':', '(', ')', '.'} - ignore_characters
    if characters:
        string = re.sub(r'[%s]' % re.escape(''.join(characters)), ' ', string)

    # remove some characters
    characters = {'\''} - ignore_characters
    if characters:
        string = re.sub(r'[%s]' % re.escape(''.join(characters)), '', string)

    # replace multiple spaces with one
    string = re.sub(r'\s+', ' ', string)

    # strip and lower case
    return string.strip().lower()


def sanitize_release_group(string):
    """Sanitize a `release_group` string to remove content in square brackets.

    :param str string: the release group to sanitize.
    :return: the sanitized release group.
    :rtype: str

    """
    # only deal with strings
    if string is None:
        return

    # remove content in square brackets
    string = re.sub(r'\[\w+\]', '', string)

    # strip and upper case
    return string.strip().upper()


def timestamp(date):
    """Get the timestamp of the `date`, python2/3 compatible

    :param datetime.datetime date: the utc date.
    :return: the timestamp of the date.
    :rtype: float

    """
    return (date - datetime(1970, 1, 1)).total_seconds()


def decode(str_data, encoding=None, lang=None):
    """
    Returns the unicode string of the data passed in
    otherwise it throws a ValueError() exception. This function makes
    use of the chardet library

    If encoding == None then it is attempted to be detected by chardet
    If encoding is a string, then only that encoding is used
    If encoding is a list or tuple, then each item is tried before
                giving up.
    """
    if isinstance(str_data, unicode):
        return str_data

    if encoding is None:
        decoded = detect(str_data, lang)
        encoding = decoded['encoding']

    if isinstance(encoding, str):
        encoding = ( encoding, )

    if not isinstance(encoding, (tuple, list)):
        return str_data

    # Convert to unicode
    for enc in encoding:
        try:
            str_data = str_data.decode(
                enc,
                errors='ignore',
            )
            return str_data
        except UnicodeError:
            raise ValueError(
                '%s contains invalid characters' % (
                    str_data,
            ))
        except KeyError:
            raise ValueError(
                '%s encoding could not be detected ' % (
                    str_data,
            ))
        except TypeError:
            try:
                str_data = str_data.decode(
                    enc,
                    'ignore',
                )
                return str_data
            except UnicodeError:
                raise ValueError(
                    '%s contains invalid characters' % (
                        str_data,
                ))
            except KeyError:
                raise ValueError(
                    '%s encoding could not be detected ' % (
                        str_data,
                ))
    return None

def guess_info(filename, encoding='utf-8'):
    """ Parses the filename using guessit-library """

    if isinstance(filename, str):
        _filename = decode(filename, encoding)
        if not _filename:
            # could not detect unicode type
            logger.debug('Could not detect unicode type.')
        else:
            filename = _filename

    if isinstance(filename, unicode):
        logger.debug(
            'Guessing using: %s' % filename.encode('utf-8'))
    else:
        logger.debug('Guessing using: %s' % filename)

    # Acquire a default year if we can
    result = DETECTED_YEAR_RE.match(filename)
    detected_year = None
    if result:
        detected_year = result.group('year')

    _matcher = matcher.IterativeMatcher(
        decode(filename),
        filetype='autodetect',
        opts={'nolanguage': True, 'nocountry': True},
    )

    mtree = _matcher.match_tree
    guess = _matcher.matched()

    # fix some strange guessit guessing:
    # if guessit doesn't find a year in the file name it
    # thinks it is episode, but we prefer it to be handled
    # as movie instead
    if guess.get('type') == 'episode' and \
            guess.get('episodeNumber', '') == '':
        guess['type'] = 'movie'
        guess['title'] = guess.get('series')
        guess['year'] = '1900'
        logger.debug(
            'An episode without episode # becomes a movie',
        )

    # detect if year is part of series name
    if guess['type'] == 'episode':
        last_node = None
        for node in mtree.nodes():
            if node.guess:
                if last_node != None and \
                        node.guess.get('year') != None and \
                        last_node.guess.get('series') != None:
                    if 'year' in guess:
                        if detected_year != str(guess['year']):
                            logger.debug(
                                'Detected year (%s) updated to %s!' % (
                                    guess['year'], detected_year,
                            ))
                            # Apply override
                            guess['year'] = detected_year

                        guess['series'] += ' ' + str(guess['year'])
                    logger.debug('Detected year as part of title.')
                    break
                last_node = node

        if 'year' not in guess and detected_year:
            logger.debug(
                'Setting detected year %s!' % (
                    detected_year,
            ))

            # Apply override
            guess['year'] = detected_year
            if 'series' in guess:
                guess['series'] += ' ' + str(guess['year'])

    if guess['type'] == 'movie':
        # Enforce TV Show
        force_tv = False
        matches = DETECT_TVSHOW_RE.match(filename)
        if matches:
            # Enforce TV Show
            force_tv = True

            # Help out with guessed info
            _season = int(matches.group(1))
            _episodeList = sorted(re.split('[eE]', matches.group(2)), key=int)
            _episode = int(_episodeList[0])

            if u'episode' not in guess:
                guess[u'episode'] = _episode

            if u'season' not in guess:
                guess[u'season'] = _season

            if len(_episodeList) > 1 and u'episodeList' not in guess:
                guess[u'episodeList'] = _episodeList

        date = guess.get('date')
        if date:
            guess['vtype'] = 'dated'
        elif force_tv:
            guess['vtype'] = 'othertv'
        else:
            guess['vtype'] = 'movie'

        if detected_year:
            if 'year' not in guess:
                logger.debug(
                    'Setting detected year %s!' % (
                        detected_year,
                ))

                # Apply override
                guess['year'] = detected_year

            elif detected_year != str(guess['year']):
                logger.debug(
                    'Detected year (%s) updated to %s!' % (
                        guess['year'], detected_year,
                ))
                # Apply override
                guess['year'] = detected_year

    elif guess['type'] == 'episode':
        guess['vtype'] = 'series'

    logger.debug(guess.nice_string())

    if 'vtype' not in guess:
        raise ValueError("Non-guessable filename.")

    logger.debug('Type: %s' % guess['vtype'])

    return guess
