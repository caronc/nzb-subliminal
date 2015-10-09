#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#
# Subliminal post-processing script for NZBGet
#
# Copyright (C) 2014 Chris Caron <lead2gold@gmail.com>
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with subliminal.  If not, see <http://www.gnu.org/licenses/>.
#

##############################################################################
### NZBGET POST-PROCESSING/SCHEDULER SCRIPT                                ###

# Download Subtitles.
#
# The script searches subtitles on various web-sites and saves them into
# destination directory near video files.
#
# This post-processing script is a wrapper for "Subliminal",
# a python library to search and download subtitles, written
# by Antoine Bertin (Diaoul Ael).
#
# Info about this Subliminal NZB Script:
# Author: Chris Caron (lead2gold@gmail.com).
# Date: Tue, May 30th, 2015.
# License: GPLv3 (http://www.gnu.org/licenses/gpl.html).
# Script Version: 0.9.6
#
# NOTE: This script requires Python to be installed on your system.
#

##############################################################################
### OPTIONS                                                                ###

# List of language codes.
#
# Language code according to ISO 639-1.
# Few examples: English - en, German - de, Dutch - nl, French - fr.
# For the full list of language codes see
#     http://www.loc.gov/standards/iso639-2/php/English_list.php.

# Language Setting
#
# Subtitles for multiple languages can be downloaded. Separate multiple
# languages with some type of delmiter (space, comma, etc)
# codes with commas. Example: en, fr
#Languages=en

# Subliminal Single Mode Setting (yes, no).
#
# Download content without the language code in the subtitles filename.
# Note: this is forced to 'no' in the event more then one Language
# is specified.
#Single=yes

# Subtitle Fetch Mode (ImpairedOnly, StandardOnly, BestScore, ImpairedFirst, StandardFirst).
#
# Define the types of subtitles you would like to scan for, the options
# break down as follows:
#  ImpairedOnly - Only download hearing-impaired subtitles.
#  StandardOnly - Only download non hearing-impaired subtitles.
#  BestScore - Download the best matching subtitles reguardless of if they
#              are flagged for the hearing-impaired or not.
#  ImpairedFirst - Attempt to download the hearing-impaired subtitles
#              first. In the event that they there are not available,
#              then attempt to acquire the non hearing-impaired versions
#              instead.
#  StandardFirst - Attempt to download the standard (non hearing-impaired)
#              subtitles first. In the event that they are not available,
#              then attempt to acquire the the hearing-impaired versions
#              instead.
#FetchMode=BestScore

# Search Mode (basic, advanced).
#
#  basic    - presumed subtitles are guessed based on the (deobsfucated)
#             filename alone.
#  advanced - presumed subtiltes are guessed based on the (deobsfucated)
#             filename (same as basic).  But further processing occurs to
#             help obtain more accurate results. Meta data extracted from
#             the actual video in question such as it's length, FPS, and
#             encoding (including if subs are already included or not).
#             This mode yields the best results but at the cost of additional
#             time and CPU.
#SearchMode=advanced

# Skip Embedded Subtitle Matching (yes, no).
#
# Identify how you want to handle embedded subititles if they are detected
# in the video file being scanned. If you set this value to 'no', you will
# use match embedded subtitles instead and further no further script processing
# will take place.
# If you set this to 'yes', you will ignore the fact that embedded subtitles
# were detected and just continue to exersice this tool to fetch some from
# the providers identified.
# Note: Embedded subtitles can only be detected if you are using the advanced
#       search mode identified above. Therefore this switch has no bearing
#       on a Basic check.
#SkipEmbedded=yes

# Minimum File Size (in MB)
#
# Any video that is equal to this size or larger will not be filtered out from
# having it checked for subtitles. This option prevents unnecessary queries
# to subtitle providers when the video in question is just a sample or preview
# file anyway.  The sample/preview videos will get filtered out by this option
# but still allow for a subtitle checks against the real thing.
# Setting this value to 0 (zero) will disable this filter feature and attempted
# to fetch subtitles on all matched video formats (not recommended).
#MinSize=150

# Minimum File Score
#
# When more then one subtitle is matched against a video, they are individually
# scored based on their likelyhood of being an exact match to the video they
# are being searched on. The highest scored match is the chosen one at the
# end of the day.  A high score (almost perfect) is 50ish, but most videos
# score in the high 30's and low 40's. This score identifies the elimination
# which subtitles should not even be considered if it scores this value or
# lower. If you set this too high, you'll never match any subtitles.  If
# you set this too low, you'll almost always acqurie a subtitle for the video
# in question, but it may not be the correct one.
# If 0 is specified, the default value assigned by the subliminal core
# application will be used.
#MinScore=20

# Default Core Subtitle Providers
#
# Supply a core (master) list of subtitle providers you want to reference
# against each video you scan. The specified subtitle providers should be
# separated by a comma and or a space. The default (if none is
# specified) are used: opensubtitles, tvsubtitles, podnapisi, addic7ed, thesubdb
#Providers=opensubtitles, tvsubtitles, podnapisi, addic7ed, thesubdb

# Movie (Exclusive) Subtitle Providers
#
# Optionally specify Movie Providers you wish to exclusively use when
# a movie is detected.  If nothing is specified, then the Default
# Core Subtitle Providers (identified above) are used instead.
#
# Providers specified should be separated by a comma and or a space. An example
# of what one might specify here is: opensubtitles, podnapisi, thesubdb
#MovieProviders=

# TV Show (Exclusive) Subtitle Providers
#
# Optionally specify TV Show Providers you wish to exclusively use when
# a TV Show is detected.  If nothing is specified, then the Default
# Core Subtitle Providers (identified above) are used instead.
#
# Providers specified should be separated by a comma and or a space.
# An example of what one might specify here is: tvsubtitles, addic7ed
#TVShowProviders=

# File extensions for video files.
#
# Only files with these extensions are processed. Extensions must
# be separated with commas.
# Example=.mkv,.avi,.divx,.xvid,.mov,.wmv,.mp4,.mpg,.mpeg,.vob,.iso
#VideoExtensions=.mkv,.avi,.divx,.xvid,.mov,.wmv,.mp4,.mpg,.mpeg,.vob,.iso

# Force Subtitle Encoding (None, UTF-8, UTF-16, ISO-8859-1, ISO-8859-2).
#
# Force the encoding of a subtitle file to be of a certain type. If set to
# None, then the subtitle will left as it was retrieved.
# - UTF-8: This is the encoding used by most Linux/Unix filesystems. just
#          check the global variable $LANG to see if that's what you are.
# - UTF-16: This is the encoding usually used by OS/X systems and NTFS.
# - ISO-8859-1: Also referred to as Latin-1; Microsoft Windows used this
#               encoding for years (in the past), and still do in some
#               cases. It supports the English, Spanish, and French language
#               character sets.
# - ISO-8859-2: Also referred to as Latin-2; It supports Czech, German,
#               Hungarian, Polish, Romanian, Croatian, Slovak, and
#               Slovene character sets.
#
# If you wish to add another encoding; just email me and i'll add it.
#ForceEncoding=None

# My Systems File Encoding (UTF-8, UTF-16, ISO-8859-1, ISO-8859-2).
#
# All systems have their own encoding; here is a loose guide you can use
# to determine what encoding you are (if you're not sure):
# - UTF-8: This is the encoding used by most Linux/Unix filesystems. just
#          check the global variable $LANG to see if that's what you are.
# - UTF-16: This is the encoding usually used by OS/X systems and NTFS.
# - ISO-8859-1: Also referred to as Latin-1; Microsoft Windows used this
#               encoding for years (in the past), and still do in some
#               cases. It supports the English, Spanish, and French language
#               character sets.
# - ISO-8859-2: Also referred to as Latin-2; It supports Czech, German,
#               Hungarian, Polish, Romanian, Croatian, Slovak, and
#               Slovene character sets.
#
# If you wish to add another encoding; just email me and i'll add it.
# All files that are downloaded will be written to your filesystem using
# the same encoding your operating system uses.  Since there is no way
# to detect this (yet), by specifying it here, you can make it possible
# to handle files with the extended character sets.
#
#SystemEncoding=UTF-8


# Cache Directory
#
# This directory is used for storing temporary cache files created when
# fetching subtitles.
#CacheDir=${TempDir}/subliminal

# Enable debug logging (yes, no).
#
# If subtitles are not downloaded as expected, activate debug logging
# to get a verbose output from subliminal.
#Debug=no

### POST-PROCESSING MODE                                                   ###

# List of TV categories.
#
# Comma separated list of categories for TV. VideoSort automatically
# distinguishes movies from series and dated TV shows. But it needs help
# to distinguish movies from other TV shows because they are named
# using same conventions. If a download has associated category listed in
# option <TvCategories>, Subliminal uses this information to help figure out
# the video being scanned sometimes.
#
# Category names must match categories defined in NZBGet.
#TvCategories=tv, tv2, Series

# Overwrite Mode (yes, no).
#
# Overwrite subtitles even if they previously exist.
#Overwrite=no

# Correct Videos Timestamp (yes, no).
#
# Set this to yes if you want freshly downloaded videos to have their file
# timestamp updated to `now`.
#UpdateTimestamp=yes

# Correct Video Permissions (yes, no).
#
# Set this to yes if you want to adjust the permissions associated with
# all downloaded videos (Unix/Linux only).
#UpdatePermissions=no

# Video Permission Value
#
# Specify the video permissions to set. This is only used if UpdatePermissions
# (identified above) is set to yes.
#VideoPermissions=644

### SCHEDULER MODE                                                         ###

# Directories to Scan
#
# Specify any number of directories this script can (recursively) check
# delimited by a comma and or space. ie: /home/nuxref/mystuff, /path/no3, etc
# For windows users, you can specify: C:\My Downloads, \\My\Network\Path, etc
#ScanDirectories=

# Maximum File Age
#
# The maximum amount of time that can elapse before we can assume that if
# there are still no subtitles after this duration, then there never will
# be.  This option prevents thrashing and requesting subtitles for something
# over and over again for no reason. This value is identified in hours
# relative to each file checked
#MaxAge=24

### NZBGET POST-PROCESSING/SCHEDULER SCRIPT                                ###
##############################################################################

import re
from os.path import join
from shutil import move
from os import getcwd
from os.path import split
from os.path import basename
from os.path import abspath
from os.path import dirname
from os.path import splitext
from os.path import isfile
from os.path import isdir
from os import unlink
from os import chdir
from os import makedirs
import logging

# This is required if the below environment variables
# are not included in your environment already
import sys
sys.path.insert(0, join(dirname(__file__), 'Subliminal'))

# Script dependencies identified below
from guessit import matcher
from datetime import timedelta
from datetime import datetime
from subliminal import Video
from subliminal import Episode
from subliminal import MutexLock
from subliminal import cache_region
from subliminal import scan_video
from subliminal import download_best_subtitles
from chardet import detect
import babelfish

# pynzbget Script Wrappers
from nzbget import PostProcessScript
from nzbget import SchedulerScript
from nzbget import EXIT_CODE
from nzbget import SCRIPT_MODE

class FETCH_MODE(object):
    IMPAIRED_ONLY = "ImpairedOnly"
    STANDARD_ONLY = "StandardOnly"
    BESTSCORE = "BestScore"
    IMPAIRED_FIRST = "ImpairedFirst"
    STANDARD_FIRST = "StandardFirst"

FETCH_MODES = (
    FETCH_MODE.IMPAIRED_ONLY,
    FETCH_MODE.STANDARD_ONLY,
    FETCH_MODE.BESTSCORE,
    FETCH_MODE.STANDARD_FIRST,
    FETCH_MODE.IMPAIRED_FIRST,
)

FETCH_MODE_DEFAULT = FETCH_MODE.BESTSCORE

class SEARCH_MODE(object):
    BASIC = "basic"
    ADVANCED = "advanced"

# Some Default Environment Variables (used with CLI)
DEFAULT_EXTENSIONS = \
        '.mkv,.avi,.divx,.xvid,.mov,.wmv,.mp4,.mpg,.mpeg,.vob,.iso'
DEFAULT_MAXAGE = 24
DEFAULT_LANGUAGE = 'en'
DEFAULT_PROVIDERS = [
    'opensubtitles',
    'tvsubtitles',
    'podnapisi',
    'addic7ed',
    'thesubdb',
]

# System Encodings
DEFAULT_ENCODINGS = (
    # Most Linux Systems
    'UTF-8',
    # NTFS/OS-X
    'UTF-16',
    # Most French/English/Spanish Windows Systems
    'ISO-8859-1',
    # Czech, German, Hungarian, Polish, Romanian,
    # Croatian, Slovak, Slovene.
    'ISO-8859-2',
)

DEFAULT_UPDATE_TIMESTAMP = False
DEFAULT_UPDATE_PERMISSIONS = False
DEFAULT_VIDEO_PERMISSIONS = 0o644
DEFAULT_SINGLE = False
DEFAULT_FORCE = 'no'
DEFAULT_SEARCH_MODE = SEARCH_MODE.ADVANCED
DEFAULT_EMBEDDED_SUBS = 'no'
DEFAULT_FORCE_ENCODING = 'None'
DEFAULT_SYSTEM_ENCODING = 'UTF-8'

# A list of compiled regular expressions identifying files to not parse ever
IGNORE_FILELIST_RE = (
    # Samples
    re.compile('^.*[-.]sample(\.[^.]*)?$', re.IGNORECASE),
    re.compile('^sample-.*$', re.IGNORECASE),
)

# The number of MegaBytes the detected video must be (with respect
# to it's filesize). If it is less than this value, then it is presumed
# no subtitles exists for it.
DEFAULT_MIN_VIDEO_SIZE_MB = 150

# The minimum score to accept a potentially matched subtitle that
# was paired against a video.
DEFAULT_MIN_VIDEO_SCORE = 20

# A simple regular expression that scans the video downloaded and
# detects the season/episode information from it.
DETECT_TVSHOW_RE = re.compile(
    r'^.*[^A-Za-z0-9]?S([0-9]{1,4})E([0-9]{1,4}(E[0-9]{1,4})*)[^A-Za-z0-9]',
    re.IGNORECASE,
)

# stat is used to test if the .srt file was fetched okay or not
from os import stat
# used for updating timestamp of the video
from os import utime
# used for updating video permissions
from os import chmod

def decode(str_data, encoding=None):
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
        decoded = detect(str_data)
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


class SubliminalScript(PostProcessScript, SchedulerScript):
    """A wrapper to Subliminal written for NZBGet
    """

    def apply_nzbheaders(self, guess):
        """ Applies NZB headers (if exist) """

        nzb_used = False

        nzb_proper_name = self.nzb_get('propername', '')
        nzb_episode_name = self.nzb_get('episodename', '')
        nzb_movie_year = self.nzb_get('movieyear', '')
        nzb_more_info = self.nzb_get('moreinfo', '')

        if nzb_proper_name != '':
            nzb_used = True
            self.logger.debug('Using DNZB-ProperName')
            if guess['vtype'] == 'series':
                proper_name = nzb_proper_name
                guess['series'] = proper_name
            else:
                guess['title'] = nzb_proper_name

        if nzb_episode_name != '' and guess['vtype'] == 'series':
            nzb_used = True
            self.logger.debug('Using DNZB-EpisodeName')
            guess['title'] = nzb_episode_name

        if nzb_movie_year != '':
            nzb_used = True
            self.logger.debug('Using DNZB-MovieYear')
            guess['year'] = nzb_movie_year

        if nzb_more_info != '':
            nzb_used = True
            self.logger.debug('Using DNZB-MoreInfo')
            if guess['type'] == 'movie':
                regex = re.compile(
                    r'^http://www.imdb.com/title/(tt[0-9]+)/$', re.IGNORECASE)
                matches = regex.match(nzb_more_info)
                if matches:
                    guess['imdb'] = matches.group(1)
                    guess['cpimdb'] = 'cp(' + guess['imdb'] + ')'

        if nzb_used:
            self.logger.debug(guess.nice_string())

    def guess_info(self, filename, shared,
                   deobfuscate=True, use_nzbheaders=True):
        """ Parses the filename using guessit-library """

        tv_categories = [
            cat.lower() for cat in \
            self.parse_list(self.get('TvCategories', [])) ]

        if deobfuscate:
            filename = self.deobfuscate(filename)

        if isinstance(filename, str):
            system_encoding = self.get('SystemEncoding', DEFAULT_SYSTEM_ENCODING)
            _filename = decode(filename, system_encoding)
            if not _filename:
                # could not detect unicode type
                self.logger.debug('Could not detect unicode type.')
            else:
                filename = _filename

        if isinstance(filename, unicode):
            self.logger.debug('Guessing using: %s' % filename.encode('utf-8'))
        else:
            self.logger.debug('Guessing using: %s' % filename)

        # Push Guess to NZBGet
        if shared:
            guess = self.pull_guess()
        else:
            guess = None

        if not guess:
            _matcher = matcher.IterativeMatcher(
                decode(filename),
                filetype='autodetect',
                opts={'nolanguage': True, 'nocountry': True},
            )

            mtree = _matcher.match_tree
            guess = _matcher.matched()

            if self.vdebug:
                # Verbose Mode Only
                self.logger.vdebug(mtree)
                for node in mtree.nodes():
                    if node.guess:
                        self.logger.vdebug(node.guess)
                self.logger.vdebug(guess.nice_string())

            # fix some strange guessit guessing:
            # if guessit doesn't find a year in the file name it
            # thinks it is episode, but we prefer it to be handled
            # as movie instead
            if guess.get('type') == 'episode' and \
                    guess.get('episodeNumber', '') == '':
                guess['type'] = 'movie'
                guess['title'] = guess.get('series')
                guess['year'] = '1900'
                self.logger.debug(
                    'An episode without episode # becomes a movie',
                )
                self.logger.debug(guess.nice_string())

            # detect if year is part of series name
            if guess['type'] == 'episode':
                last_node = None
                for node in mtree.nodes():
                    if node.guess:
                        if last_node != None and \
                                node.guess.get('year') != None and \
                                last_node.guess.get('series') != None:
                            guess['series'] += ' ' + str(guess['year'])
                            self.logger.debug('Detected year as part of title.')
                            self.logger.debug(guess.nice_string())
                            break
                        last_node = node

            if guess['type'] == 'movie':
                category = self.get('CATEGORY', '').lower()
                force_tv = category in tv_categories

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

            elif guess['type'] == 'episode':
                guess['vtype'] = 'series'
        else:
            self.logger.debug('Guessed content already provided by NZBGet!')

        if 'vtype' not in guess:
            raise ValueError("Non-guessable filename.")

        self.logger.debug('Type: %s' % guess['vtype'])

        if use_nzbheaders:
            # Apply nzb meta information to guess if present
            self.apply_nzbheaders(guess)

        if shared:
            # Push Guess to NZBGet
            self.push_guess(guess)

        return guess

    def convert_encoding(self, fname, encoding):
        """Takes a filename and encoding and converts it's contents
        """
        self.logger.debug(
            'Detecting subtitle encoding for %s' % \
            basename(fname),
        )

        tmp_fname = '%s.tmp' % fname
        old_fname = '%s.old' % fname
        try:
            unlink(tmp_fname)
            #self.logger.debug(
            #    'Removed temporary srt re-encode file : %s' % \
            #    basename(tmp_fname),
            #)
        except:
            # no problem
            pass
        try:
            unlink(old_fname)
            #self.logger.debug(
            #    'Removed old srt re-encode file : %s' % \
            #    basename(old_fname),
            #)
        except:
            # no problem
            pass

        try:
            f = open(fname, 'r')
        except IOError:
            self.logger.error(
                'Could not open %s for encoding testing' % \
                basename(fname),
            )
            return False

        try:
            fw = open(tmp_fname, 'w')
        except:
            self.logger.error(
                'Could not create new file %s.' % \
                basename(tmp_fname),
            )
            try:
                f.close()
            except:
                pass
            return False

        def readchunk():
            """Lazy function (generator) to read a file piece by piece.
            Default chunk size: 8096 bytes."""
            return f.read(8096)

        for chunk in iter(readchunk, ''):
            detected = detect(chunk)
            if detected['encoding'] is not None:
                self.logger.debug(
                    "Detecting '%s' (%f confidence) subtitle encoding for %s" % (
                    detected['encoding'],
                    detected['confidence'],
                    basename(fname),
                    )
                )

                if detected['encoding'].lower() not in [ encoding.lower(), 'ascii' ]:
                    try:
                        chunk = chunk.decode(
                            detected['encoding'], errors='replace')\
                                .encode(encoding, errors='replace')
                    except UnicodeError:
                        raise ValueError(
                            '%s contains invalid characters' % (
                                basename(fname),
                        ))
                    except KeyError:
                        raise ValueError(
                            '%s encoding could not be detected ' % (
                                basename(fname),
                        ))

                    except TypeError:
                        try:
                            chunk = chunk.decode(
                            detected['encoding'], 'replace')\
                                .encode(encoding, 'replace')
                        except UnicodeError:
                            raise ValueError(
                                '%s contains invalid characters' % (
                                    basename(fname),
                            ))
                        except KeyError:
                            raise ValueError(
                                '%s encoding could not be detected ' % (
                                    basename(fname),
                            ))

            try:
                fw.write(chunk)
            except:
                self.logger.error(
                    'Could not write to new file %s.' % \
                    basename(tmp_fname),
                )
                try:
                    f.close()
                except:
                    pass
                try:
                    fw.close()
                except:
                    pass
                return False

        try:
            f.close()
        except:
            pass
        try:
            fw.close()
        except:
            pass

        try:
            move(fname, old_fname)
        except OSError:
            self.logger.error(
                'Could not move %s to %s' % (
                    basename(fname),
                    basename(old_fname),
                )
            )
            try:
                unlink(tmp_fname)
            except:
                pass
            return False

        try:
            move(tmp_fname, fname)
        except OSError:
            self.logger.error(
                'Could not move %s to %s' % (
                    basename(tmp_fname),
                    basename(fname),
                )
            )
            try:
                unlink(fname)
            except:
                pass
            try:
                move(old_fname, fname)
            except:
                pass
            try:
                unlink(tmp_fname)
            except:
                pass
            return False

        try:
            unlink(old_fname)
        except:
            pass

        self.logger.info(
            "Converted %s to '%s' encoding." % (
                basename(fname),
                encoding,
            )
        )
        return True

    def subliminal_fetch(self, files, single_mode=True, shared=True,
                         deobfuscate=True, use_nzbheaders=True,
                         overwrite=False):
        """This function fetches the subtitles
        """

        # Get configuration
        cache_dir = self.get('CACHEDIR', self.get('TEMPDIR'))
        cache_file = join(cache_dir, 'subliminal.cache.dbm')

        # Encoding
        force_encoding = self.get('ForceEncoding', DEFAULT_FORCE_ENCODING)
        if force_encoding.lower() == 'none':
            force_encoding = None

        # Minimum Score
        minscore = int(self.get('MinScore', DEFAULT_MIN_VIDEO_SCORE))
        if minscore < 0:
            # Use Default
            minscore = 0

        # Use Embedded Subtitles
        skip_embedded = self.parse_bool(
            self.get('SkipEmbedded', DEFAULT_EMBEDDED_SUBS),
        )

        # Search Mode
        search_mode = self.get('SearchMode', DEFAULT_SEARCH_MODE)
        self.logger.info('Using %s search mode' % search_mode)

        if not isdir(cache_dir):
            try:
                makedirs(cache_dir)
            except:
                self.logger.error('Could not create directory %s' % (
                    cache_dir,
                ))
                return False

        # Change to our cache directory; we do this because subliminal (the one
        # we wrap downloads content to the directory we're standing in at
        # first).  This causes a problem if we're in a system directory which
        # some admin's like to remove write permission from (for good reason
        # too).  Our cache directory acts as a good temporary location to work
        # out of.
        try:
            chdir(cache_dir)
        except OSError:
            self.logger.error('Could not access directory %s' % (
                cache_dir,
            ))
            return False

        # Attempt to detect a category and manage exclusive provider lists (if
        # specified)
        movie_providers = self.parse_list(self.get('MovieProviders', ''))
        if not movie_providers:
            # Handle providers, if list is empty, then use default
            movie_providers = self.parse_list(
                self.get('Providers', DEFAULT_PROVIDERS))

        tvshow_providers = self.parse_list(self.get('TVShowProviders', ''))
        if not tvshow_providers:
            # Handle providers, if list is empty, then use default
            tvshow_providers = self.parse_list(
                self.get('Providers', DEFAULT_PROVIDERS))

        # parse provider list and remove entries that are not valid
        movie_providers = [ p.lower() for p in movie_providers \
                     if p.lower() in DEFAULT_PROVIDERS ]

        # parse provider list and remove entries that are not valid
        tvshow_providers = [ p.lower() for p in tvshow_providers \
                     if p.lower() in DEFAULT_PROVIDERS ]

        if not movie_providers:
            movie_providers = DEFAULT_PROVIDERS
            self.logger.debug('Using default provider list for movies.')
        else:
            self.logger.debug('Using the following movie providers: %s' %(
                ', '.join(movie_providers)
            ))
        if not tvshow_providers:
            tvshow_providers = DEFAULT_PROVIDERS
            self.logger.debug('Using default provider list for movies.')
        else:
            self.logger.debug('Using the following tv show providers: %s' %(
                ', '.join(tvshow_providers)
            ))

        provider_configs = {}

        lang = self.parse_list(self.get('Languages', 'en'))
        if not lang:
            self.logger.error('No valid language was set')
            return False
        if len(lang) > 1 and single_mode:
            # More then 1 language specifies implies not to use single mode
            single_mode = False
            self.logger.warning(
                'SingleMode disabled due to multiple languages specified.',
            )

        # Set up some arguments based on the fetch mode specified
        fetch_mode = self.get('FetchMode', FETCH_MODE_DEFAULT)
        try:
            # Correct ID if required
            fetch_mode = [ m for m in FETCH_MODES \
                          if fetch_mode.upper() == m.upper()][0]
            self.logger.debug('Fetch Mode: %s' % fetch_mode)
        except IndexError:
            self.logger.warning(
                'Invalid FetchMode specified, using default: %s' %\
                FETCH_MODE_DEFAULT,
            )
            fetch_mode = FETCH_MODE_DEFAULT

        hearing_impaired = None
        hi_score_adjust = 0
        if fetch_mode is FETCH_MODE.IMPAIRED_ONLY:
            # Force Hearing-Impaired Only
            hearing_impaired = True

        elif fetch_mode is FETCH_MODE.STANDARD_ONLY:
            # Force Non Hearing-Impaired Only
            hearing_impaired = False

        elif fetch_mode is FETCH_MODE.STANDARD_FIRST:
            # Fetch Non Hearing-Impaired First by lowering the score of
            # matched hearing-impaired subs.
            hi_score_adjust = -3

        elif fetch_mode is FETCH_MODE.IMPAIRED_FIRST:
            # Fetch Hearing-Impaired First by lowering the score of
            # matched non hearing-impaired subs.
            hi_score_adjust = +3

        else: # FETCH_MODE.BESTSCORE
            pass

        try:
            lang = set( babelfish.Language.fromietf(l) for l in lang )
        except babelfish.Error:
            self.logger.error('An error occured processing the language list')

        # Configure cache
        cache_region.configure(
            'dogpile.cache.dbm',
            expiration_time=timedelta(days=30),
            arguments={'filename': cache_file, 'lock_factory': MutexLock},
        )

        # initialize fetch counter
        f_count = 0

        for entry in files:
            if True in [ v.match(entry) is not None \
                        for v in IGNORE_FILELIST_RE ]:
                self.logger.debug('Skipping - Ignored file: %s' % basename(entry))
                continue

            full_path = entry
            if search_mode == SEARCH_MODE.BASIC:
                full_path = join(cache_dir, basename(entry))

            # Create a copy of the lang object
            _lang = set(lang)
            for l in lang:
                # Check that file doesn't already exist
                srt_path = dirname(entry)
                srt_file = basename(splitext(entry)[0])
                srt_file_re = re.escape(srt_file)
                srt_lang = str(l)
                srt_regex = '^(%s\.srt|%s\.%s.srt)$' % (
                    srt_file_re, srt_file_re, srt_lang
                )

                # look in the directory and extract all matches
                _matches = self.get_files(
                    search_dir=srt_path,
                    regex_filter=srt_regex,
                    max_depth=1,
                )
                if not overwrite and len(_matches):
                    self.logger.debug(
                        '%s subtitle match: %s' % (
                            str(l),
                            ', '.join([ basename(_srt) \
                                       for _srt in _matches.keys() ]),
                    ))
                    # File Conversion Option
                    #if force_encoding:
                    #    for _srt in _matches.keys():
                    #        self.convert_encoding(_srt, force_encoding)
                    _lang.remove(l)
                    continue

            if len(_lang) == 0:
                self.logger.debug(
                    'Skipping - Subtitle(s) already exist for: %s' % (
                    basename(entry),
                ))

                continue

            self.logger.debug('Scanning [%s] using %s lang=%s' % (
                search_mode,
                full_path,
                ', '.join([ str(l) for l in _lang ]),
            ))

            try:
                # Add Guessed Information
                video = Video.fromguess(
                    split(entry)[1],
                    self.guess_info(
                        entry,
                        shared=shared,
                        deobfuscate=deobfuscate,
                        use_nzbheaders=use_nzbheaders,
                    ),
                )
            except ValueError as e:
                # fromguess() throws a ValueError if show matches couldn't
                # be detected using the content guessit matched.
                if isinstance(e, basestring):
                    self.logger.debug('Error message: %s' % e)

                self.logger.warning(
                    'Skipping - Invalid file: %s' % basename(entry),
                )
                continue

            if search_mode == SEARCH_MODE.ADVANCED:
                # Deep Enzyme Scan
                video = scan_video(
                    full_path,
                    subtitles=not overwrite,
                    embedded_subtitles=not skip_embedded,
                    video=video,
                )

                if babelfish.Language('und') in video.subtitle_languages:
                    # This means we found embedded subtitles, it causes the
                    # download_best_subtitles() to skip over this because of
                    # this. To alter the default action of ignoring searching
                    # all together, we remove this entry here so we can keep
                    # going.
                    video.subtitle_languages.remove(babelfish.Language('und'))

                    if not skip_embedded:
                        self.logger.debug(
                            'Skipping - unknown embedded subtitle ' + \
                            'language(s) already exist for: %s' % basename(entry),
                        )
                        continue

                # Based on our results, we may need to skip searching
                # further for subtitles
                if not skip_embedded:
                    # clean out languages we have already
                    for l in video.subtitle_languages:
                        if l in _lang:
                            self.logger.debug(
                                'Skipping - Embedded %s subtitle ' % str(l) + \
                                'already exist for: %s' % basename(entry),
                            )
                            _lang.remove(l)

                # One last language check
                if len(_lang) == 0:
                    continue

            # Depending if we are dealing with a TV Show or A Movie, we swap
            # our list of providers
            if isinstance(video, Episode):
                # use TV Series providers
                providers = tvshow_providers
            else:
                # use Movie providers
                providers = movie_providers

            if not len(providers):
                self.logger.warning(
                    'There were no valid providers for this video type.',
                )
                continue

            # download best subtitles
            subtitles = download_best_subtitles(
                [video, ],
                _lang,
                providers=providers,
                provider_configs=provider_configs,
                single=single_mode,
                min_score=minscore,
                hearing_impaired=hearing_impaired,
                hi_score_adjust=hi_score_adjust,
            )

            if not subtitles:
                self.logger.warning('No subtitles were found for %s' % basename(entry))
                continue

            for l in _lang:
                srt_path = abspath(dirname(entry))
                srt_file = basename(splitext(entry)[0])
                srt_lang = str(l)

                if single_mode:
                    expected_file = join(srt_path, '%s.srt' % srt_file)

                else:
                    expected_file = join(srt_path, '%s.%s.srt' % (
                        srt_file, srt_lang,
                    ))

                self.logger.debug('Expecting .srt: %s' % expected_file)

                # Provide other possible locations (unique list)
                potential_files = list(set([ \
                    p for p in [
                        join(abspath(getcwd()), basename(expected_file)),
                        join(cache_dir, basename(expected_file)),
                    ] if isfile(p) and p != expected_file
                ]))

                if self.debug:
                    # Helpful information
                    for potential in potential_files:
                        self.logger.debug(
                            'Potential .srt: %s' % potential
                        )

                if isfile(expected_file):
                    # File was found in the same folder as the movie is
                    # no change is nessisary
                    pass

                elif len(potential_files):
                    # Pop the first item from the potential list
                    while len(potential_files):
                        move_from = potential_files.pop()
                        self.logger.debug(
                            'Expected not found, retrieving: %s' % move_from,
                        )

                        try:
                            # Move our file
                            move(move_from, expected_file)

                            # Move our fetched file to it's final destination
                            self.logger.info('Successfully placed %s' % \
                                             basename(expected_file))
                            # leave loop
                            break

                        except OSError as e:
                            self.logger.error(
                                'Could not move %s to %s' % (
                                    basename(move_from),
                                    expected_file,
                                )
                            )
                            self.logger.debug(
                                'move() exception: %s' % str(e),
                            )

                # Remove any lingering potential files
                try:
                    expected_stat = stat(expected_file)
                except OSError:
                    # weird, expected file was not found..
                    expected_stat = ()

                while len(potential_files):
                    p = potential_files.pop()
                    try:
                        if stat(f) != expected_stat:
                            # non-linked files... proceed
                            unlink(p)
                            self.logger.debug(
                                'Removed lingering extra: %s' % \
                                p,
                            )
                    except:
                        pass

                if not isfile(expected_file):
                    # We can't find anything
                    self.logger.error(
                        'Could not locate a fetched (%s) subtitle.' % l
                    )
                    continue

                # File Conversion Option
                if force_encoding:
                    self.convert_encoding(expected_file, force_encoding)

                # increment counter
                f_count += 1

        # When you're all done handling the file, just return
        # the error code that best represents how everything worked
        if f_count > 0:
            return True

        # Nothing fetched, nothing gained or lost
        return None

    def postprocess_main(self, *args, **kwargs):

        if not self.health_check():
            # No sense scanning something that did not download successfully
            return None

        if not self.validate(keys=(
            'MinSize',
            'MinScore',
            'Single',
            'Overwrite',
            'SkipEmbedded',
            'UpdateTimestamp',
            'UpdatePermissions',
            'VideoPermissions',
            'Providers',
            'MovieProviders',
            'TVShowProviders',
            'SearchMode',
            'FetchMode',
            'TvCategories',
            'VideoExtensions',
            'ForceEncoding',
            'SystemEncoding',
            'Languages')):

            return False

        # Environment
        video_extension = self.get('VideoExtensions', DEFAULT_EXTENSIONS)
        minsize = int(self.get('MinSize', DEFAULT_MIN_VIDEO_SIZE_MB)) * 1048576

        # Overwrite Mode
        overwrite = self.parse_bool(self.get('Overwrite', 'no'))

        # Single Mode (don't download language extension)
        single_mode = self.parse_bool(
            self.get('Single', DEFAULT_SINGLE))

        # Update Timestamp
        update_timestamp = self.parse_bool(
            self.get('UpdateTimestamp', DEFAULT_UPDATE_TIMESTAMP))

        # Update Permissions
        update_permissions = self.parse_bool(
            self.get('UpdatePermissions', DEFAULT_UPDATE_PERMISSIONS))
        try:
            video_permissions = int('0o%d' % self.get(
                'VideoPermissions',
                int(DEFAULT_VIDEO_PERMISSIONS),
            ))
        except (ValueError, TypeError):
            video_permissions = DEFAULT_VIDEO_PERMISSIONS

        # Build file list
        files = self.get_files(suffix_filter=video_extension, fullstats=True)

        # Apply Filters
        _files = dict([ (k, v) for (k, v) in files.items() if \
                      v['filesize'] >= minsize ]).keys()

        if self.debug and len(_files) != len(files):
            # Debug Mode - Print filtered content for peace of mind and
            #              debugging other peoples logs
            for file in list(set(files.keys()) - set(_files)):
                size = 0.0
                if files[file]['filesize'] > 0:
                    size = (float(files[file]['filesize']) / 1048576.0)

                self.logger.debug('Filtered "%s" (%.2f MB)' % (file, size))

        if not _files:
            self.logger.info('There were no files found.')
            return None

        self.logger.info('Found %d matched file(s).' % len(_files))

        for file in _files:
            if self.debug:
                size = 0.0
                if files[file]['filesize'] > 0:
                    size = (float(files[file]['filesize']) / 1048576.0)

                self.logger.debug('Scanning "%s" (%.2f MB)' % (file, size))

            # Update Permissions (if specified to do so)
            if update_permissions:
                try:
                    chmod(file, video_permissions)
                    self.logger.debug(
                        'Video permissions set to 0%o.', video_permissions,
                    )
                except:
                    self.logger.error(
                        'Failed to update video permissions for "%s"' % file,
                    )

            # Update Timestamps (if specified to do so)
            if update_timestamp:
                try:
                    utime(file, None)
                    self.logger.debug('Video timestamp updated.')
                except:
                    self.logger.error(
                        'Failed to update timestamp for "%s"' % file,
                    )

        if _files:
            return self.subliminal_fetch(
                _files,
                single_mode=single_mode,
                deobfuscate=True,
                use_nzbheaders=True,
                overwrite=overwrite,
            )

    def scheduler_main(self, *args, **kwargs):

        if not self.validate(keys=(
            'MaxAge',
            'MinSize',
            'MinScore',
            'Single',
            'SkipEmbedded',
            'Providers',
            'MovieProviders',
            'TVShowProviders',
            'SearchMode',
            'FetchMode',
            'ScanDirectories',
            'VideoExtensions',
            'ForceEncoding',
            'SystemEncoding',
            'Languages')):

            return False

        # Environment
        video_extension = self.get('VideoExtensions', DEFAULT_EXTENSIONS)
        maxage = int(self.get('MaxAge', DEFAULT_MAXAGE))
        minsize = int(self.get('MinSize', DEFAULT_MIN_VIDEO_SIZE_MB)) * 1048576
        paths = self.parse_path_list(self.get('ScanDirectories'))

        # Single Mode (don't download language extension)
        single_mode = self.parse_bool(
            self.get('Single', DEFAULT_SINGLE))

        # Fetch Scan Paths
        files = self.get_files(
            paths,
            suffix_filter=video_extension,
            fullstats=True,
        )

        # Apply Filters
        ref_time = datetime.now() - timedelta(hours=maxage)
        _files = dict([ (k, v) for (k, v) in files.items() if \
                      v['filesize'] >= minsize and \
                      v['modified'] >= ref_time ]).keys()

        if self.debug and len(_files) != len(files):
            # Debug Mode - Print filtered content for peace of mind and
            #              debugging other peoples logs
            for file in list(set(files.keys()) - set(_files)):
                size = 0.0
                if files[file]['filesize'] > 0:
                    size = (float(files[file]['filesize']) / 1048576.0)

                self.logger.debug('Filtered "%s" (%.2f MB)' % (file, size))

        if not _files:
            self.logger.info('There were no files found.')
            return None

        self.logger.info('Found %d matched file(s).' % len(_files))

        if self.debug:
            for file in _files:
                size = 0.0
                if files[file]['filesize'] > 0:
                    size = (float(files[file]['filesize']) / 1048576.0)

                self.logger.debug('Scanning "%s" (%.2f MB)' % (file, size))

        if _files:
            return self.subliminal_fetch(
                _files,
                single_mode=single_mode,
                shared=False,
                deobfuscate=False,
                use_nzbheaders=False,
            )

    def main(self, *args, **kwargs):
        """CLI
        """
        # Environment
        video_extension = self.get('VideoExtensions', DEFAULT_EXTENSIONS)
        maxage = int(self.get('MaxAge', DEFAULT_MAXAGE))
        minsize = int(self.get('MinSize', DEFAULT_MIN_VIDEO_SIZE_MB)) * 1048576
        force = self.parse_bool(self.get('Force', DEFAULT_FORCE))
        paths = self.parse_path_list(self.get('ScanDirectories'))

        # Single Mode (don't download language extension)
        single_mode = self.parse_bool(
            self.get('Single', DEFAULT_SINGLE))

        # Fetch Scan Paths
        files = self.get_files(
            paths,
            suffix_filter=video_extension,
            fullstats=True,
        )

        # Apply Filters
        if not force:
            ref_time = datetime.now() - timedelta(hours=maxage)
            _files = dict([ (k, v) for (k, v) in files.items() if \
                      v['filesize'] >= minsize and \
                          v['modified'] >= ref_time ]).keys()
        else:
            _files = dict([ (k, v) for (k, v) in files.items() if \
                          v['filesize'] >= minsize ]).keys()

        if self.debug and len(_files) != len(files):
            # Debug Mode - Print filtered content for peace of mind and
            #              debugging other peoples logs
            for file in list(set(files.keys()) - set(_files)):
                size = 0.0
                if files[file]['filesize'] > 0:
                    size = (float(files[file]['filesize']) / 1048576.0)

                self.logger.debug('Filtered "%s" (%.2f MB)' % (file, size))

        if not _files:
            self.logger.info('There were no files found.')
            return True

        self.logger.info('Found %d matched file(s).' % len(_files))

        if self.debug:
            for file in _files:
                size = 0.0
                if files[file]['filesize'] > 0:
                    size = (float(files[file]['filesize']) / 1048576.0)

                self.logger.debug('Scanning "%s" (%.2f MB)' % (file, size))

        if files:
            return self.subliminal_fetch(
                _files,
                single_mode=single_mode,
                shared=False,
                deobfuscate=False,
                use_nzbheaders=False,
            )
        else:
            self.logger.warning(
                'There were no files detected less the %dhr(s) ' % maxage +\
                'in age requiring subtitles.')
            self.logger.info(
                'Try adding --force (-f) to force this downloads.'
            )
            return None


# Call your script as follows:
if __name__ == "__main__":
    from sys import exit
    from optparse import OptionParser

    # Support running from the command line
    parser = OptionParser()
    parser.add_option(
        "-S",
        "--scandir",
        dest="scandir",
        help="The directory to scan against. Note: that by setting this " + \
            "variable, it is implied that you are running this from " + \
            "the command line.",
        metavar="DIR",
    )
    parser.add_option(
        "-a",
        "--maxage",
        dest="maxage",
        help="The maximum age a file can be to be considered searchable. " + \
             "This value is represented in hours. The default value is %d" % \
                DEFAULT_MAXAGE + " hours.",
        metavar="AGE",
    )
    parser.add_option(
        "-n",
        "--encoding",
        dest="encoding",
        help="The system encoding to use (utf-8, ISO-8859-1, etc)." + \
             " The default value is '%s'" % DEFAULT_SYSTEM_ENCODING + ".",
        metavar="ENCODING",
    )
    parser.add_option(
        "-l",
        "--language",
        dest="language",
        help="The language the fetch the subtitles in (en, fr, etc)." + \
             " The default value is '%s'" % DEFAULT_LANGUAGE + ".",
        metavar="LANG",
    )
    parser.add_option(
        "-p",
        "--providers",
        dest="providers",
        help="Specify a list of providers (use commas as delimiters) to " + \
            "identify the providers you wish to use. The following will " + \
            "be used by default: '%s'" % ','.join(DEFAULT_PROVIDERS),
        metavar="PROVIDER1,PROVIDER2,etc",
    )
    parser.add_option(
        "-s",
        "--single",
        action="store_true",
        dest="single_mode",
        help="Download content without the language code in the subtitle " + \
            "filename.",
    )
    parser.add_option(
        "-b",
        "--basic",
        action="store_true",
        dest="basic_mode",
        help="Do not attempt to parse additional information from the " + \
            "video file. Running in a basic mode is much faster but can " + \
            "make it more difficult to determine the correct subtitle if " + \
            "more then one is matched."
    )
    parser.add_option(
        "-z",
        "--minsize",
        dest="minsize",
        help="Specify the minimum size a video must be to be worthy of " + \
        "of checking for subtiles. This value is interpreted in MB " + \
        "(Megabytes) and defaults to %d MB." % DEFAULT_MIN_VIDEO_SIZE_MB,
        metavar="SIZE_IN_MB",
    )
    parser.add_option(
        "-c",
        "--minscore",
        dest="minscore",
        help="When scoring multiple matched subtitles for a video, this " + \
        "value identifies the threshold to assume the subtitle is no good " + \
        "and should be thrown away when being compared against others. " + \
        "It currently defaults to %d." % DEFAULT_MIN_VIDEO_SCORE,
        metavar="MINSCORE",
    )
    parser.add_option(
        "-k",
        "--skip-embedded",
        dest="skip_embedded",
        action="store_true",
        help="If embedded subtitles were detected, choose not to use them " + \
        "and continue to search for the subtitles hosted by the " + \
        "identified provider(s).",
    )
    parser.add_option(
        "-e",
        "--force-encoding",
        dest="force_encoding",
        help="Optionally specify the subtitle's file encoding to" + \
        "a specific type (utf-8, ISO-8859-1, etc). If none is specified " + \
        "then the file is left as is.",
        metavar="ENCODING",
    )
    parser.add_option(
        "-f",
        "--force",
        action="store_true",
        dest="force",
        help="Force a download reguardless of the file age. This " + \
             "switch negates any value specified by the --age (-a) switch.",
    )
    parser.add_option(
        "-o",
        "--overwrite",
        action="store_true",
        dest="overwrite",
        help="Overwrite a subtitle in the event one is already present.",
    )
    parser.add_option(
        "-m",
        "--fetch-mode",
        dest="fetch_mode",
        help="Identify the fetch mode you wish to invoke," + \
        " the options are: '%s'" % "', '".join(FETCH_MODES) + ".  " +\
        "The default value is: %s" % FETCH_MODE_DEFAULT,
        metavar="MODE",
    )
    parser.add_option(
        "-L",
        "--logfile",
        dest="logfile",
        help="Send output to the specified logfile instead of stdout.",
        metavar="FILE",
    )
    parser.add_option(
        "-D",
        "--debug",
        action="store_true",
        dest="debug",
        help="Debug Mode",
    )
    options, _args = parser.parse_args()


    logger = options.logfile
    if not logger:
        # True = stdout
        logger = True
    debug = options.debug

    script_mode = None
    if options.scandir:
        scandir = options.scandir
    elif len(_args):
        # Support command line arguments too
        scandir = ', '.join(_args)
    else:
        # No arguments at all specified
        scandir = ''

    if scandir:
        # By specifying a scandir, we know for sure the user is
        # running this as a standalone script,

        # Setting Script Mode to NONE forces main() to execute
        # which is where the code for the cli() is defined
        script_mode = SCRIPT_MODE.NONE

    script = SubliminalScript(
        logger=logger,
        debug=debug,
        script_mode=script_mode,
    )

    # We always enter this part of the code, so we have to be
    # careful to only set() values that have been set by an
    # external switch. Otherwise we use defaults or what might
    # already be resident in memory (environment variables).
    _encoding = options.encoding
    _language = options.language
    _maxage = options.maxage
    _force_encoding = options.force_encoding
    _minsize = options.minsize
    _minscore = options.minscore
    _single_mode = options.single_mode is True
    _overwrite = options.overwrite is True
    _skip_embedded = options.skip_embedded is True
    _basic_mode = options.basic_mode is True
    _force = options.force is True
    _providers = options.providers
    _fetch_mode = options.fetch_mode

    if _maxage:
        try:
            _maxage = str(abs(int(_maxage)))
            script.set('MaxAge', _maxage)
        except (ValueError, TypeError):
            script.logger.error(
                'An invalid `maxage` (%s) was specified.' % (_maxage)
            )
            exit(EXIT_CODE.FAILURE)

    if _minsize:
        try:
            _minsize = str(abs(int(_minsize)))
            script.set('MinSize', _minsize)
        except (ValueError, TypeError):
            script.logger.error(
                'An invalid `minsize` (%s) was specified.' % (_minsize)
            )
            exit(EXIT_CODE.FAILURE)

    if _minscore:
        try:
            _minscore = str(abs(int(_minscore)))
            script.set('MinScore', _minscore)
        except (ValueError, TypeError):
            script.logger.error(
                'An invalid `minscore` (%s) was specified.' % (_minscore)
            )
            exit(EXIT_CODE.FAILURE)
    if _overwrite:
        script.set('Overwrite', True)

    if _force_encoding:
        script.set('ForceEncoding', _force_encoding.lower())

    if _basic_mode:
        script.set('SearchMode', SEARCH_MODE.BASIC)

    if _skip_embedded:
        script.set('SkipEmbedded', True)

    if _single_mode:
        script.set('Single', True)

    if _force:
        script.set('Force', True)

    if _providers:
        script.set('Providers', _providers)

    if _language:
        script.set('Languages', _language)

    if _encoding:
        script.set('SystemEncoding', _encoding)

    if _fetch_mode:
        if _fetch_mode.upper() in [ f.upper() for f in FETCH_MODES ]:
            script.set('FetchMode', _fetch_mode.upper())
        else:
            script.logger.warning(
                'Invalid FetchMode specified, using default: %s' %\
                FETCH_MODE_DEFAULT)
            script.set('FetchMode', FETCH_MODE_DEFAULT)

    if not script.get('ScanDirectories') and scandir:
        # Set some defaults if they are not already set
        if not _maxage:
            script.set('MaxAge', DEFAULT_MAXAGE)

        if not _minsize:
            script.set('MinSize', DEFAULT_MIN_VIDEO_SIZE_MB)

        if not _minscore:
            script.set('MinScore', DEFAULT_MIN_VIDEO_SCORE)

        if not _language:
            # Force defaults if not set
            script.set('Languages', DEFAULT_LANGUAGE)

        if not _encoding:
            # Force defaults if not set
            script.set('SystemEncoding', DEFAULT_SYSTEM_ENCODING)

        if not _fetch_mode:
            script.set('FetchMode', FETCH_MODE_DEFAULT)

        # Force generic Video Extensions
        script.set('VideoExtensions', DEFAULT_EXTENSIONS)

        # Finally set the directory the user specified for scanning
        script.set('ScanDirectories', scandir)

    if not script.script_mode and not script.get('ScanDirectories'):
        # Provide some CLI help when ScanDirectories has been
        # detected as not being identified
        parser.print_help()
        exit(1)

    # Attach Subliminal logging to output by connecting to its namespace
    logging.getLogger('subliminal').\
            addHandler(script.logger.handlers[0])
    logging.getLogger('subliminal').\
            setLevel(script.logger.getEffectiveLevel())

    # call run() and exit() using it's returned value
    exit(script.run())
