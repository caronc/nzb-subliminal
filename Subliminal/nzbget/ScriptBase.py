# -*- encoding: utf-8 -*-
#
# A base scripting class for NZBGet
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
"""
This script provides a base for all NZBGet Scripts and provides
functionality such as:
 * validate() - handle environment checking, correct versioning as well
                as if the expected configuration variables you specified
                are present.

 * push()     - pushes a variables to the NZBGet server


 * set()/get()- Hash table get/set attributes that can be set in one script
                and then later retrieved from another. get() can also
                be used to fetch content that was previously pushed using
                the push() tool. You no longer need to work with environment
                variables. If you enable the SQLite database, set content is
                put here as well so that it can be retrieved by another
                script.

 * get_api()  - Retreive a simple API/RPC object built from the global
                variables NZBGet passes into an external program when
                called.

 * get_files()- list all files in a specified directory as well as fetching
                their details such as filesize, modified date, etc in an
                easy to reference dictionary.  You can provide a ton of
                different filters to minimize the content returned. Filters
                can by a regular expression, file prefixes, and/or suffixes.

 * parse_nzbfile() - Parse an NZB-File and extract all of its meta
                     information from it. lxml must be installed on your
                     system for this to work correctly

 * parse_list() - Takes a string (or more) as well as lists of strings as
                  input. It then cleans it up and produces an easy to
                  manage list by combining all of the results into 1.
                  Hence: parse_list('.mkv, .avi') returns:
                      [ '.mkv', '.avi' ]

 * parse_path_list() - Very smilar to parse_list() except that it is used
                  to handle directory paths while cleaning them up at the
                  same time.

 * parse_bool() - Handles all of NZBGet's configuration options such as
                  'on' and 'off' as well as 'yes' or 'no', or 'True' and
                  'False'.  It greatly simplifies the checking of these
                  variables passed in from NZBGet

 * push_guess() - You can push a guessit dictionary (or one of your own
                  that can help identify your release for other scripts
                  to use later after yours finishes

 * pull_guess() - Pull a previous guess pushed by another script.
                  why redo grunt work if it's already done for you?
                  if no previous guess content was pushed, then an
                  empty dictionary is returned.

Ideally, you'll write your script using this class as your base wrapper
requiring you to only define a main() function and call run().
You no longer need to manage the different return codes NZBGet uses,
instead you can just return True, False and None from your main()
function and let the wrappers transform that to the proper return code.

Logging is automatically initialized and works right away.
When you define your logging, you can prepare in the following ways:
   logging=True
        All output will be redirected to stdout

   logging=False
        All output will be redirected to stderr
   logging=None
        No logging will take place
   logging=Logger()
        If you pass a Logger object (you already set up yourself), then
        logging will just reference that instance.
   logging=string
        The string you identify will be the log file content is written to
        with self rotating capabilties built in.  Man... life is so easy...

Additionally all exception handling is wrapped to make debugging easier.
"""

import re
from tempfile import gettempdir
from os import environ
from os import makedirs
from os import chdir
from os import walk
from os import access
from os import W_OK
from os import R_OK
from os import X_OK
from os.path import isdir
from os.path import isfile
from os.path import join
from os.path import dirname
from os.path import basename
from os.path import normpath
from os.path import splitext
from getpass import getuser
from logging import Logger
from datetime import datetime
from Utils import tidy_path

# Relative Includes
from NZBGetAPI import NZBGetAPI
from Logger import init_logger
from Logger import destroy_logger
from Utils import ESCAPED_PATH_SEPARATOR
from Utils import ESCAPED_WIN_PATH_SEPARATOR
from Utils import ESCAPED_NUX_PATH_SEPARATOR

# NZB Processing Support if lxml is installed
try:
    from lxml import etree
    from lxml.etree import XMLSyntaxError
except ImportError:
    # No panic, we just can't use nzbfile parsing
    pass

# Database Support if sqllite is installed
try:
    from Database import Database
    from Database import Category
except ImportError:
    # No panic, we just can't use database
    pass

# File Stats
from stat import ST_ATIME
from stat import ST_CTIME
from stat import ST_MTIME
from stat import ST_SIZE

from os import stat

# Some booleans that are read to and from nzbget
NZBGET_BOOL_TRUE = 'yes'
NZBGET_BOOL_FALSE = 'no'

class EXIT_CODE(object):
    """List of exit codes for post processing
    """
    PARCHECK_CURRENT = 91
    # Request NZBGet to do par-check/repair for current nzb-file.
    # This code can be used by pp-scripts doing unpack on their own.
    PARCHECK_ALL = 92
    # Post-process successful
    SUCCESS = 93
    # Post-process failed
    FAILURE = 94
    # Process skipped. Use this code when your script determines that it is
    # neither a success or failure. Perhaps your just not processing anything
    # due to how content was parsed.
    NONE = 95

EXIT_CODES = (
   EXIT_CODE.PARCHECK_CURRENT,
   EXIT_CODE.PARCHECK_ALL,
   EXIT_CODE.SUCCESS,
   EXIT_CODE.FAILURE,
   EXIT_CODE.NONE,
)

class PRIORITY(object):
    """Although priority can be any integer value, the web-interface operates
    with six predefined priorities.
    """
    VERY_LOW = -100
    LOW = -50
    NORMAL = 0
    HIGH = 50
    VERY_HIGH = 100
    FORCE = 900

# A list of priorities makes it easier to validate them
# for each priority added above, make sure you also update this list.
PRIORITIES = (
    PRIORITY.VERY_LOW,
    PRIORITY.LOW,
    PRIORITY.NORMAL,
    PRIORITY.HIGH,
    PRIORITY.VERY_HIGH,
    PRIORITY.FORCE,
)

# Environment variables that identify specific configuration for scripts
SYS_ENVIRO_ID = 'NZBOP_'

# Script options
CFG_ENVIRO_ID = 'NZBPO_'

# Shared configuration options passed through NZBGet and push(); if these
# are found in the environment, they are saved to the `config` dictionary
SHR_ENVIRO_ID = 'NZBR_'

# Environment ID used when pushing common variables to the server
PUSH_ENVIRO_ID = 'NZBPR_'

# DNZB is an environment variable sometimes referenced by other scripts
SHR_ENVIRO_DNZB_ID = '_DNZB_'

# GUESS is an environment variable sometimes referenced by other scripts
# it provides the guessed information for other scripts to save them
# from re-guessing all over again.
SHR_ENVIRO_GUESS_ID = '_GUESS_'

# NZBGet Internal Message Passing Prefix
NZBGET_MSG_PREFIX = '[NZB] '

# Precompile regular expressions for speed
SYS_OPTS_RE = re.compile('^%s([A-Z0-9_]+)$' % SYS_ENVIRO_ID)
CFG_OPTS_RE = re.compile('^%s([A-Z0-9_]+)$' % CFG_ENVIRO_ID)
SHR_OPTS_RE = re.compile('^%s([A-Z0-9_]+)$' % SHR_ENVIRO_ID)
DNZB_OPTS_RE = re.compile('^%s%s([A-Z0-9_]+)$' % (
    SHR_ENVIRO_ID,
    SHR_ENVIRO_DNZB_ID,
))

# Precompile Guess Fetching
SHR_GUESS_OPTS_RE = re.compile('^%s([A-Z0-9_]+)$' % SHR_ENVIRO_GUESS_ID)

# This is used as a mapping table so when we fetch content later
# at another time we can map them to the same format commonly
# used.
GUESS_KEY_MAP = {
    'AUDIOCHANNELS': 'audioChannels', 'AUDIOCODEC': 'audioCodec',
    'AUDIOPROFILE': 'audioProfile', 'BONUSNUMBER':'bonusNumber',
    'BONUSTITLE': 'bonusTitle', 'CONTAINER':'container', 'DATE': 'date',
    'EDITION': 'edition', 'EPISODENUMBER': 'episodeNumber',
    'FILMNUMBER': 'filmNumber', 'FILMSERIES': 'filmSeries',
    'FORMAT': 'format', 'LANGUAGE': 'language',
    'RELEASEGROUP': 'releaseGroup',  'SCREENSIZE': 'screenSize',
    'SEASON': 'season', 'SERIES': 'series', 'SPECIAL': 'special',
    'SUBTITLELANGUAGE': 'subtitleLanguage', 'TITLE': 'title',
    'TYPE': 'type', 'VIDEOCODEC': 'videoCodec','VTYPE': 'vtype',
    'WEBSITE': 'website', 'YEAR': 'year',
}

# keys should not be complicated... make it so they aren't
VALID_KEY_RE = re.compile('[^a-zA-Z0-9_.-]')

# delimiters used to separate values when content is passed in by string
# This is useful when turning a string into a list
STRING_DELIMITERS = r'[%s\[\]\:;,\s]+' % \
        ESCAPED_PATH_SEPARATOR

# For speparating paths
PATH_DELIMITERS = r'([%s]+[%s;\|,\s]+|[;\|,\s%s]+[%s]+)' % (
        ESCAPED_NUX_PATH_SEPARATOR,
        ESCAPED_NUX_PATH_SEPARATOR,
        ESCAPED_NUX_PATH_SEPARATOR,
        ESCAPED_NUX_PATH_SEPARATOR,
)

# SQLite Database
NZBGET_DATABASE_FILENAME = "nzbget/nzbget.db"

class SCRIPT_MODE(object):
    # After the download of nzb-file is completed NZBGet can call
    # post-processing scripts (pp-scripts). The scripts can perform further
    # processing of downloaded files such es delete unwanted files
    # (*.url, etc.), send an e-mail notification, transfer the files to other
    # application and do any other things.
    POSTPROCESSING = 'postprocess'

    # Scan scripts are called when a new file is found in the incoming nzb
    # directory (option `NzbDir`). If a file is being added via web-interface
    # or via RPC-API from a third-party app the file is saved into nzb
    # directory and then processed. NZBGet loads only files with nzb-extension
    # but it calls the scan scripts for every file found in the nzb directory.
    # This allows for example for scan scripts which unpack zip-files
    # containing nzb-files.

    # To activate a scan script or multiple scripts put them into `ScriptDir`,
    # then choose them in the option `ScanScript`.
    SCAN = 'scan'

    # Queue scripts are called after the download queue was changed. In the
    # current version the queue scripts are called only after an nzb-file was
    # added to queue. In the future they can be calledon other events too.

    # To activate a queue script or multiple scripts put them into `ScriptDir`,
    # then choose them in the option `QueueScript`.
    QUEUE = 'queue'

    # Scheduler scripts are called by scheduler tasks (setup by the user).

    # To activate a scheduler script or multiple scripts put them into
    # `ScriptDir`, then choose them in the option `TaskX.Script`.
    SCHEDULER = 'scheduler'

    # None is detected if you aren't using one of the above types
    NONE = ''

# Depending on certain environment variables, a mode can be detected
# a mode can be used to. When using a MultiScript
SCRIPT_MODES = (
    # The order these are listed is very important,
    # it identifies the order when preforming sanity
    # checking
    SCRIPT_MODE.POSTPROCESSING,
    SCRIPT_MODE.SCAN,
    SCRIPT_MODE.QUEUE,
    SCRIPT_MODE.SCHEDULER,
    SCRIPT_MODE.NONE,
)

class ScriptBase(object):
    """The intent is this is the script you run from within your script
       after overloading the main() function of your class
    """

    def __init__(self, logger=True, debug=False, script_mode=None,
                 database_key=None, tempdir=None, *args, **kwargs):

        # logger identifier
        self.logger_id = __name__
        self.logger = logger
        self.debug = debug

        # for extra verbosity
        # This is set by just additionally passing in _dev_debug=True
        # into the initialization of your scripts
        self._dev_debug = kwargs.get('_dev_debug')

        # Script Mode
        self.script_mode = None
        if not hasattr(self, 'script_dict'):
            # Only define once
            self.script_dict = {}

        # For Database Handling
        self.database = None
        self.database_key = database_key

        # Fetch System Environment (passed from NZBGet)
        self.system = dict([(SYS_OPTS_RE.match(k).group(1), v.strip()) \
            for (k, v) in environ.items() if SYS_OPTS_RE.match(k)])

        # Fetch/Load Script Specific Configuration
        self.config = dict([(CFG_OPTS_RE.match(k).group(1), v.strip()) \
            for (k, v) in environ.items() if CFG_OPTS_RE.match(k)])

        # Fetch/Load Shared Configuration through push()
        self.shared = dict([(SHR_OPTS_RE.match(k).group(1), v.strip()) \
            for (k, v) in environ.items() if SHR_OPTS_RE.match(k)])

        # Preload nzbheaders based on any DNZB environment variables
        self.nzbheaders = self.pull_dnzb()

        # self.tempdir
        # path to temporary directory to work from
        if tempdir is None:
            self.tempdir = self.system.get('TEMPDIR')
        else:
            self.tempdir = tempdir

        # version detection
        try:
            self.version = '%s.' % self.system.get('VERSION')
            self.version = int(self.version.split('.')[0])
        except (TypeError, ValueError):
            self.version = 11

        # Enabling DEBUG as a flag by specifying  near in the configuration
        # section of your script
        #Debug=no
        if self.debug is None:
            # Check Script Environments
            for k in SCRIPT_MODES:
                # Initialize all script types
                if hasattr(self, '%s_%s' % (k, 'debug')):
                    if getattr(self, '%s_%s' % (k, 'debug'))(*args, **kwargs):
                        self.debug = True
                        break
            if self.debug is None:
                self.debug = False

        if isinstance(self.logger, basestring):
            # Use Log File
            self.logger = init_logger(
                name=self.logger_id,
                logger=logger,
                debug=debug,
                nzbget_mode=False,
            )

        elif not isinstance(self.logger, Logger):
            # handle all other types
            if logger is None:
                # None means don't log anything
                self.logger = init_logger(
                    name=self.logger_id,
                    logger=None,
                    debug=debug,
                    nzbget_mode=True,
                )
            else:
                # Use STDOUT for now
                self.logger = init_logger(
                    name=self.logger_id,
                    logger=True,
                    debug=debug,
                    nzbget_mode=True,
                )
        else:
            self.logger_id = None

        # enforce temporary directory
        if not self.tempdir:
            self.tempdir = join(
                gettempdir(),
                'nzbget-%s' % getuser(),
            )
            # Force environment to be the same
            self.system['TEMPDIR'] = self.tempdir
            environ['%sTEMPDIR' % SYS_ENVIRO_ID] = self.tempdir

        if not isdir(self.tempdir):
            try:
                makedirs(self.tempdir, 0700)
            except:
                self.logger.warning(
                    'Temporary directory could not be ' + \
                    'created: %s' % self.system['TEMPDIR'],
                )

        if self._dev_debug and self.debug:
            # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
            # Print Global System Varables to help debugging process
            #
            # Note: This is a very verbose process, so it is only performed
            #       if both the debug and _dev_debug flags are set.
            # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
            for k, v in self.system.items():
                self.logger.debug('SYS %s=%s' % (k, v))

            for k, v in self.config.items():
                self.logger.debug('CFG %s=%s' % (k, v))

            for k, v in self.shared.items():
                self.logger.debug('SHR %s=%s' % (k, v))

        # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
        # Enforce system/global variables for script processing
        # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
        self.system['DEBUG'] = self.debug

        # Set environment variable how NZBGet Would have done so
        if self.debug:
            environ['%sDEBUG' % SYS_ENVIRO_ID] = NZBGET_BOOL_TRUE
        else:
            environ['%sDEBUG' % SYS_ENVIRO_ID] = NZBGET_BOOL_FALSE

        if script_mode is not None:
            if script_mode in self.script_dict.keys() + [SCRIPT_MODE.NONE,]:
                self.script_mode = script_mode
                if self.script_mode is SCRIPT_MODE.NONE:
                    self.logger.debug('Script mode forced off.')
                else:
                    self.logger.debug(
                        'Script mode forced to: %s' % self.script_mode,
                    )
            else:
                self.logger.warning(
                    'Could not force script mode to: %s' % script_mode,
                )
        else:
            # An NZBGet Mode means we should work out of a writeable directory
            try:
                chdir(self.tempdir)
            except OSError:
                self.logger.warning(
                    'Temporary directory is not ' + 'accessible: %s' % \
                    self.tempdir,
                )

        # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
        # Detect the mode we're running in
        # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
        if self.script_mode is None:
            self.detect_mode()

        if self.script_mode == SCRIPT_MODE.NONE:
            # Reload logging without NZBGet mode configured
            self.logger = init_logger(
                name=self.logger_id,
                logger=self.logger,
                debug=debug,

                # NZBGet mode disabled
                nzbget_mode=False,
            )

        # Initialize the chosen script mode
        if hasattr(self, '%s_%s' % (self.script_mode, 'init')):
            getattr(
                self, '%s_%s' % (self.script_mode, 'init')
            )(*args, **kwargs)

    def __del__(self):
        if self.logger_id:
            destroy_logger(self.logger_id)

    def _push(self, key, value):
        """NZBGet has the ability to process certain messages
        delivered to it via stdout. This is just a wrapper
        script to ease this process

        This version of push is just used internally. It's designed
        To update system variables and only supports a specific
        set of commands which are predefined in the scripts that
        inherit this base class.

        users should be utlizing the push() command instead of
        this one.
        """
        # Content is only pushable in certain modes
        if self.script_mode is SCRIPT_MODE.NONE:
            # if there is no script mode, then the calling
            # function isn't supported by NZBGet (or this
            # framework)
            return True

        elif value is None:
            # Never print... well.. nothing, you can acomplish
            # this by passing in an empty string ('')
            return False

        # clean key
        key = VALID_KEY_RE.sub('', key).upper()

        if isinstance(value, bool):
            # convert boolean's to int's for consistency
            value = str(int(value))

        elif not isinstance(value, basestring):
            value = str(value)

        # Push message on to nzbget (by simply sending it to
        # stdout)
        print('%s%s=%s' % (NZBGET_MSG_PREFIX, key, value))

        # No reason to fail if we make it this far
        return True

    def push(self, key, value, use_env=True):
        """Pushes a key/value pair to NZBGet Server

        The content pushed can be retrieved from
        self.config in scripts called after this one
        by the same key you specified in this script.
        """
        # clean key
        key = VALID_KEY_RE.sub('', key).upper()

        # Accomodate other environmental variables
        self.shared[key] = value
        if isinstance(value, bool):
            # convert boolean's to int's for consistency
            value = str(int(value))

        elif not isinstance(value, basestring):
            value = str(value)

        if use_env:
            # Save environment variable
            environ['%s%s' % (SHR_ENVIRO_ID, key)] = value

        # Alert NZBGet of variable being set
        return self._push('%s%s' % (PUSH_ENVIRO_ID, key), value)

    def push_dnzb(self, nzbheaders=None):
        """pushes meta information to NZBGet Server as DNZB content
           if no `nzbheaders` (dictionary) is defined, then the
           default one is used instead.
        """
        if nzbheaders is None:
            nzbheaders = self.nzbheaders

        if not isinstance(nzbheaders, dict):
            return False

        for k, v in nzbheaders.items():
            # Push content to NZB Server
            self.push('%s%s' % (
                SHR_ENVIRO_DNZB_ID,
                k.upper(),
            ), v.strip())

        return True

    def pull_dnzb(self):
        """pulls meta information stored in the DNZB environment
           variables and returns a dictionary
        """
        # Preload nzbheaders based on any DNZB environment variables
        return dict([(DNZB_OPTS_RE.match(k).group(1).upper(), v.strip()) \
            for (k, v) in environ.items() if DNZB_OPTS_RE.match(k)])

    def push_guess(self, guess):
        """pushes guess results to NZBGet Server. The function was
        initially intended to provide a simply way of passing content
        from guessit(), but it can be used by any dictionary with
        common elements used to identify releases
        """

        if not isinstance(guess, dict):
            # A guess is a 'dict' type, so handle the common elements
            # if set.
            return False

        for key in guess.keys():
            if key.upper() in GUESS_KEY_MAP.keys():
                # Push content to NZB Server
                self.push('%s%s' % (
                    SHR_ENVIRO_GUESS_ID,
                    key.upper(),
                ), str(guess[key]).strip())

        return True

    def pull_guess(self):
        """Retrieves guess content in a dictionary
        """
        # Fetch/Load Guess Specific Content
        return dict([
            (GUESS_KEY_MAP[SHR_GUESS_OPTS_RE.match(k).group(1)], v.strip()) \
            for (k, v) in self.shared.items() \
                if SHR_GUESS_OPTS_RE.match(k) and \
                SHR_GUESS_OPTS_RE.match(k).group(1) in GUESS_KEY_MAP])

    def parse_nzbfile(self, nzbfile, check_queued=False):
        """Parse an nzbfile specified and return just the
        meta information within the <head></head> tags

        """
        results = {}
        if not isinstance(nzbfile, basestring):
            # Simple check for nothing found
            self.logger.debug('NZB-File not defined; parse skipped.')
            return results

        if isfile(nzbfile):
            # Nothing expensive to do with i/o; just move along
            pass

        elif check_queued and isdir(dirname(nzbfile)):
            # the specified nzbfile doesn't exist, but that doesn't mean
            # it hasn't been picked up and is been picked up and nzbget
            # renamed it to .queued
            # .processed nzb files can be a result of a scan scripts handling
            # .nzb_processed are also used during the pre-scanning in scan
            #                scripts.
            # .error may be corrupted, but it does't mean we can't attempt
            #        to parse content from it.
            file_escaped = re.escape(basename(nzbfile))
            file_regex = r'^%s|%s' % (file_escaped, file_escaped) + \
                r'(' + \
                r'|\.queued|\.[0-9]+\.queued' + \
                r'|\.processed|\.[0-9]+\.processed' + \
                r'|\.nzb_processed|\.[0-9]+\.nzb_processed' + \
                r'|\.error|\.[0-9]+\.error' + \
                r')$'

            # look in the directory and extract all matches
            _filenames = self.get_files(
                search_dir=dirname(nzbfile),
                regex_filter=file_regex,
                fullstats=True,
                max_depth=1,
            )

            if len(_filenames):
                # sort our results by access time
                _files = sorted (
                    _filenames.iterkeys(),
                    key=lambda k: (
                        # Sort by Accessed time first
                        _filenames[k]['accessed'],
                        # Then sort by Created Date
                        _filenames[k]['created'],
                        # Then sort by filename length
                        # file.nzb.2.queued > file.nzb.queued
                        len(k)),
                    reverse=True,
                )
                if self.debug:
                    for _file in _files:
                        self.logger.debug('NZB-Files located: %s (%s)' % (
                            basename(_file),
                            _filenames[_file]['accessed']\
                                .strftime('%Y-%m-%d %H:%M:%S'),
                        ))
                # Assign first file (since we've listed by access time)
                nzbfile = _files[0]
                self.logger.info(
                    'NZB-File detected: %s' % basename(nzbfile),
                )

        try:
            for event, element in etree.iterparse(
                nzbfile, tag="{http://www.newzbin.com/DTD/2003/nzb}head"):
                for child in element:
                    if child.tag == "{http://www.newzbin.com/DTD/2003/nzb}meta":
                        if child.text.strip():
                            # Only store entries with content
                            results[child.attrib['type'].upper()] = \
                                child.text.strip()

                element.clear()
            self.logger.info(
                'NZBParse - NZB-File parsed %d meta entries' % len(results),
            )

        except NameError:
            self.logger.warning('NZBParse - Skipped; lxml is not installed')

        except IOError:
            self.logger.warning(
                'NZBParse - NZB-File is missing: %s' % basename(nzbfile))

        except XMLSyntaxError, e:
            if e[0] is None:
                # this is a bug with lxml in earlier versions
                # https://bugs.launchpad.net/lxml/+bug/1185701
                # It occurs when the end of the file is reached and lxml
                # simply just doesn't handle the closure properly
                # it was fixed here:
                # https://github.com/lxml/lxml/commit\
                #       /19f0a477c935b402c93395f8c0cb561646f4bdc3
                # So we can relax and return ok results here
                self.logger.info(
                    'NZBParse - NZB-File parsed %d meta entries' % \
                    len(results),
                )
            else:
                # This is the real thing
                self.logger.error(
                    'NZBParse - NZB-File is corrupt: %s' % nzbfile,
                )
                self.logger.debug('NZBParse - Exception %s' % str(e))

        return results

    # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
    # set() and get() wrappers
    # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
    def unset(self, key, use_env=True, use_db=True):
        """Unset a variable, this also occurs if you call set() with a value
            set to None.
        """
        return self.set(key, None, use_env=use_env, use_db=use_db)

    def set(self, key, value, use_env=True, use_db=True):
        """Sets a key/value pair into the configuration

            if use_env is True, then content is additionaly set in the
            local environment variables.

            if use_db is True, then content is additionally set in a sqlite
            database.
        """
        # clean key
        key = VALID_KEY_RE.sub('', key).upper()
        if not key:
            return False

        if key in self.system:
            self.logger.warning('set() called using a system key (%s)' % key)

        # Save content to database
        if use_db and self.database is None and self.database_key:
            try:
                # Connect to database on first use only
                self.database = Database(
                    container=self.database_key,
                    database=join(
                        self.tempdir,
                        NZBGET_DATABASE_FILENAME,
                    ),
                    logger=self.logger,
                )

                # Database is ready to go
                if value is None:
                    # Remove Entry if it's set to None
                    self.database.unset(key=key)
                    self.logger.debug('unset(database) %s"' % key)

                elif isinstance(value, bool):
                    # Convert boolean to integer (change True to 1 or False to 0)
                    self.database.set(key=key, value=int(value))
                    self.logger.debug('set(database) %s="%s"' % (
                        key,
                        int(value)),
                    )

                else:
                    self.database.set(key=key, value=value)
                    self.logger.debug('set(database) %s="%s"' % (key, value))

            except NameError:
                # Sqlite wasn't installed
                # set the dbstore to false so it isn't used anymore
                self.database = False

        elif use_db and self.database:
            # Database is ready to go
            if value is None:
                # Remove Entry if it's set to None
                self.database.unset(key=key)
                self.logger.debug('unset(database) %s"' % key)

            elif isinstance(value, bool):
                # Convert boolean to integer (change True to 1 or False to 0)
                self.database.set(key=key, value=int(value))
                self.logger.debug('set(database) %s="%s"' % (
                    key,
                    int(value),
                ))

            else:
                self.database.set(key=key, value=value)
                self.logger.debug('set(database) %s="%s"' % (key, value))

        if value is None:
            # Remove Entry if it's set to None
            # This also touches the shared dictionary as well.
            # This is intentional as it gives people who push() content
            # a way of unsettting the local variable the set (in the event
            # they should want to)
            if key in self.config:
                del self.config[key]
                self.logger.debug('unset(config) %s' % key)
            if key in self.shared:
                del self.shared[key]
                self.logger.debug('unset(shared) %s' % key)

        else:
            # Set config variables
            self.config[key] = value
            self.logger.debug('set(config) %s="%s"' % (key, value))

        if use_env:
            # convert boolean's to int's for consistency
            if value is None:
                # Remove entry
                if '%s%s' % (CFG_ENVIRO_ID, key) in environ:
                    self.logger.debug('unset(environment) %s' % key)
                    del environ['%s%s' % (CFG_ENVIRO_ID, key)]

            elif isinstance(value, bool):
                # Convert boolean to integer (change True to 1 or False to 0)
                environ['%s%s' % (CFG_ENVIRO_ID, key)] = str(int(value))
                self.logger.debug('set(environment) %s="%s"' % (
                    key,
                    str(int(value))),
                )

            else:
                environ['%s%s' % (CFG_ENVIRO_ID, key)] = str(value)
                self.logger.debug('set(environment) %s="%s"' % (key, value))

        return True

    def get(self, key, default=None, check_system=True,
            check_shared=True, use_db=True):
        """works with set() operation making it easy to retrieve set()
        content
        """

        # clean key
        key = VALID_KEY_RE.sub('', key).upper()
        if not key:
            return False

        if check_system:
            # System variables over-ride all
            value = self.system.get('%s' % key)
            if value is not None:
                # only return if a key was found
                self.logger.debug('get(system) %s="%s"' % (key, value))
                return value

        value = self.config.get('%s' % key)
        if value is not None:
            # only return if a key was found
            self.logger.debug('get(config) %s="%s"' % (key, value))
            return value

        # Fetch content from database
        if use_db and self.database is None and self.database_key:
            try:
                # Connect to database on first use only
                self.database = Database(
                    container=self.database_key,
                    database=join(
                        self.tempdir,
                        NZBGET_DATABASE_FILENAME,
                    ),
                    logger=self.logger,
                )

                # Database is ready to go
                value = self.database.get(key=key)
                if value is not None:
                    # only return if a key was found
                    self.logger.debug('get(database) %s="%s"' % (key, value))
                    return value

            except NameError:
                # Sqlite wasn't installed
                # set the dbstore to false so it isn't used anymore
                self.database = False

        elif use_db and self.database:
            value = self.database.get(key=key)
            if value is not None:
                # only return if a key was found
                self.logger.debug('get(database) %s="%s"' % (key, value))
                return value

        # If we reach here, the content wasn't found in the database
        # or the database simply isn't enabled. We now fetch attempt to
        # fetch the content from it's shared variable now

        # We still haven't found the variable requested
        if check_shared:
            # We'll look for the shared environment variable now
            # These are set by the push() methods
            value = self.shared.get('%s' % key)
            if value is not None:
                self.logger.debug('get(shared) %s="%s"' % (key, value))
                return value

        if default is not None:
            self.logger.debug('get(default) %s="%s"' % (key, str(default)))
        else:
            self.logger.debug('get(default) %s=None' % key)

        return default

    def items(self, check_system=True, check_shared=True, use_db=True):
        """
        This lets you utilize for-loops by returning you a list of keys

        """
        items = list()
        if use_db and self.database is None and self.database_key:
            try:
                # Connect to database on first use only
                self.database = Database(
                    container=self.database_key,
                    database=join(
                        self.tempdir,
                        NZBGET_DATABASE_FILENAME,
                    ),
                    logger=self.logger,
                )

                # Fetch from database first
                items = self.database.items()
            except NameError:
                # Sqlite wasn't installed
                # set the dbstore to false so it isn't used anymore
                self.database = False

        elif use_db and self.database:
            # Fetch from database first
            items = self.database.items()

        if check_shared:
            # Shared values trump any database set ones
            items = dict(items + self.shared.items()).items()

        # configuration trumps shared values
        items = dict(items + self.config.items()).items()

        if check_system:
            # system trumps all values
            items = dict(items + self.system.items()).items()

        return items

    # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
    # nzb_set() and nzb_get() wrappers
    # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
    def nzb_unset(self, key, use_env=True, use_db=True):
        """Unset a variable, this also occurs if you call nzb_set() with a
            value set to None.
        """
        return self.nzb_set(key, None, use_env=use_env, use_db=use_db)

    def nzb_set(self, key, value, use_env=True, use_db=True):
        """Sets a key/value pair into the nzb headers

            if use_env is True, then content is additionaly set in the
            local environment variables.
        """
        # clean key
        key = VALID_KEY_RE.sub('', key).upper()
        if not key:
            return False

        # Save content to database
        if use_db and self.database is None and self.database_key:
            try:
                # Connect to database on first use only
                self.database = Database(
                    container=self.database_key,
                    database=join(
                        self.tempdir,
                        NZBGET_DATABASE_FILENAME,
                    ),
                    logger=self.logger,
                )

                # Database is ready to go
                if value is None:
                    # Remove Entry if it's set to None
                    self.database.unset(key=key, category=Category.NZB)
                    self.logger.debug('nzb_unset(database) %s"' % key)

                elif isinstance(value, bool):
                    # Convert boolean to integer (change True to 1 or False to 0)
                    self.database.set(
                        key=key, value=int(value), category=Category.NZB)
                    self.logger.debug('nzb_set(database) %s="%s"' % (
                        key,
                        int(value)),
                    )

                else:
                    self.database.set(
                        key=key, value=value, category=Category.NZB)
                    self.logger.debug('nzb_set(database) %s="%s"' % (key, value))

            except NameError:
                # Sqlite wasn't installed
                # set the dbstore to false so it isn't used anymore
                self.database = False

        elif use_db and self.database:
            # Database is ready to go
            if value is None:
                # Remove Entry if it's set to None
                self.database.unset(key=key, category=Category.NZB)
                self.logger.debug('nzb_unset(database) %s"' % key)

            elif isinstance(value, bool):
                # Convert boolean to integer (change True to 1 or False to 0)
                self.database.set(key=key, value=int(value), category=Category.NZB)
                self.logger.debug('nzb_set(database) %s="%s"' % (
                    key,
                    int(value),
                ))

            else:
                self.database.set(key=key, value=value, category=Category.NZB)
                self.logger.debug('nzb_set(database) %s="%s"' % (key, value))

        if value is None:
            # Remove Entry if it's set to None
            # This also touches the shared dictionary as well.
            # This is intentional as it gives people who push() content
            # a way of unsettting the local variable the set (in the event
            # they should want to)
            if key in self.nzbheaders:
                del self.nzbheaders[key]
                self.logger.debug('nzb_unset(config) %s' % key)

            # Remove entry from environment too
            if use_env and '%s%s%s' % (
                    CFG_ENVIRO_ID,
                    SHR_ENVIRO_DNZB_ID,
                    key) in environ:
                del environ['%s%s%s' % (
                    SHR_ENVIRO_ID,
                    SHR_ENVIRO_DNZB_ID,
                    key)]
                self.logger.debug('nzb_unset(environment) %s' % key)
        else:
            # Set config variables
            self.nzbheaders[key] = value

            self.logger.debug('nzb_set(config) %s="%s"' % (key, str(value)))

            if use_env:
                if isinstance(value, bool):
                    # Convert boolean to integer (change True to 1 or False to 0)
                    value = str(int(value))

                elif not isinstance(value, basestring):
                    value = str(value)

                environ['%s%s%s' % (
                    SHR_ENVIRO_ID,
                    SHR_ENVIRO_DNZB_ID,
                    key)] = value

                self.logger.debug('nzb_set(environment) %s="%s"' % (
                    key, value),
                )

        return True

    def nzb_get(self, key, default=None, use_db=True):
        """works with nzb_set() operation making it easy to retrieve
        content
        """
        # clean key
        key = VALID_KEY_RE.sub('', key).upper()
        if not key:
            return False

        value = self.nzbheaders.get(key)
        if value is not None:
            # only return if a key was found
            self.logger.debug('nzb_get(config) %s="%s"' % (key, value))
            return value

        # Fetch content from database
        if use_db and self.database is None and self.database_key:
            try:
                # Connect to database on first use only
                self.database = Database(
                    container=self.database_key,
                    database=join(
                        self.tempdir,
                        NZBGET_DATABASE_FILENAME,
                    ),
                    logger=self.logger,
                )

                # Database is ready to go
                value = self.database.get(key=key, category=Category.NZB)
                if value is not None:
                    # only return if a key was found
                    self.logger.debug('nzb_get(database) %s="%s"' % (key, value))
                    return value

            except NameError:
                # Sqlite wasn't installed
                # set the dbstore to false so it isn't used anymore
                self.database = False

        elif use_db and self.database:
            value = self.database.get(key=key, category=Category.NZB)
            if value is not None:
                # only return if a key was found
                self.logger.debug('nzb_get(database) %s="%s"' % (key, value))
                return value

        if default is not None:
            self.logger.debug('get(default) %s="%s"' % (key, str(default)))
        else:
            self.logger.debug('get(default) %s=None' % key)

        return default

    def items(self, check_system=True, check_shared=True, use_db=True):
        """
        This lets you utilize for-loops by returning you a list of keys

        """
        items = []
        if use_db and self.database is None and self.database_key:
            try:
                # Connect to database on first use only
                self.database = Database(
                    container=self.database_key,
                    database=join(
                        self.tempdir,
                        NZBGET_DATABASE_FILENAME,
                    ),
                    logger=self.logger,
                )

                # Fetch from database first
                items = self.database.items()
            except NameError:
                # Sqlite wasn't installed
                # set the dbstore to false so it isn't used anymore
                self.database = False

        elif use_db and self.database:
            # Fetch from database first
            items = self.database.items()

        if check_shared:
            # Shared values trump any database set ones
            items = dict(items + self.shared.items()).items()

        # configuration trumps shared values
        items = dict(items + self.config.items()).items()

        if check_system:
            # system trumps all values
            items = dict(items + self.system.items()).items()

        return items

    # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
    # Sanity
    # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
    def _sanity_check(self):
        """Sanity checks on a base class are always successful
        """
        return True

    # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
    # Validatation
    # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
    def validate(self, *args, **kwargs):
        """A system wrapper to _validate() allowing a mult-script environment
        """
        # Default
        core_function = self._validate
        if hasattr(self, '%s_%s' % (self.script_mode, 'validate')):
            core_function = getattr(
                self, '%s_%s' % (self.script_mode, 'validate'))

        # Execute
        return core_function(*args, **kwargs)

    def _validate(self, keys=None, min_version=11, *args, **kwargs):
        """validate against environment variables
        """

        # Initialize a global variable, we run through the entire function
        # so all errors can be caught to make it easier for debugging
        is_okay = True

        if keys:
            missing = []
            if isinstance(keys, basestring):
                keys = self.parse_list(keys)

            missing = [
                k for k in keys \
                        if not (k.upper() in self.system \
                             or k.upper() in self.config)
            ]

            if missing:
                self.logger.error('Validation - Directives not set: %s' % \
                      ', '.join(missing))
                is_okay = False

        # We should fail if the temporary directory is not accessible
        if not access(self.tempdir, (R_OK|W_OK|X_OK)):
            self.logger.error(
                'Validation - Temporary directory is not accessible %s' % \
                self.tempdir,
            )
            is_okay = False

        if self.script_mode == SCRIPT_MODE.NONE:
            # Nothing more to process if not utilizaing
            # NZBGet environment
            return is_okay

        if min_version > self.version:
            self.logger.error(
                'Validation - detected version %d, (min expected=%d)' % (
                    self.version, min_version)
            )
            is_okay = False

        # Always a bad thing if SCRIPTDIR doesn't work since that is
        # introduced in v11 (the minimum version we support)
        if not 'SCRIPTDIR' in self.system:
            self.logger.error(
                'Validation - (<v11) Directive not set: %s' % 'SCRIPTDIR',
            )
            is_okay = False

        return is_okay

    def get_api(self):
        """This function can be used to return a XML-RCP server
        object using the server variables defined
        """

        # System Options required for RPC calls to work
        required_opts = set((
            'CONTROLIP',
            'CONTROLPORT',
            'CONTROLUSERNAME',
            'CONTROLPASSWORD',
        ))
        # Fetch standard RCP information to simplify future commands
        if set(self.system) & required_opts != required_opts:
            # Not enough options to extract RCP information
            return None

        # if we reach here, we have enough data to build an RCP connection
        host = self.system['CONTROLIP']
        if host == "0.0.0.0":
            host = "127.0.0.1"

        # Return API Controller
        return NZBGetAPI(
            self.system['CONTROLUSERNAME'],
            self.system['CONTROLPASSWORD'],
            host,
            self.system['CONTROLPORT'],
        )

    # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
    # File Retrieval
    # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
    def get_files(self, *args, **kwargs):
        """A system wrapper to _get_files() allowing a mult-script environment
        """

        # Default
        core_function = self._get_files
        if self.script_mode is not None and \
           hasattr(self, '%s_%s' % (self.script_mode, 'get_files')):
            core_function = getattr(
                self, '%s_%s' % (self.script_mode, 'get_files'))

        # Execute
        return core_function(*args, **kwargs)

    def _get_files(self, search_dir, regex_filter=None, prefix_filter=None,
                    suffix_filter=None, fullstats=False,
                   followlinks=False, min_depth=None, max_depth=None,
                  case_sensitive=False):
        """Returns a dict object of the files found in the download
           directory. You can additionally pass in filters as a list or
           string) to filter the results returned.
              ex:
              {
                 '/full/path/to/file.mkv': {
                     'basename': 'file.mkv',
                     'dirname': '/full/path/to',
                     # always tolower() applied to:
                     'extension': mkv,

                     # If fullstatus == True then the following additional
                     # content is provided.

                     # filesize is in bytes
                     'filesize': 10000,
                     # accessed date
                     'accessed': datetime(),
                     # created date
                     'created': datetime(),
                     # created date
                     'modified': datetime(),
                 }
              }

        """

        # Build file list
        files = {}
        if isinstance(search_dir, (list, tuple)):
            for _dir in search_dir:
                # use recursion to build a master (unique) list
                files = dict(files.items() + self._get_files(
                    search_dir=_dir,
                    regex_filter=regex_filter,
                    prefix_filter=prefix_filter,
                    suffix_filter=suffix_filter,
                    fullstats=fullstats,
                    followlinks=followlinks,
                    min_depth=min_depth,
                    max_depth=max_depth,
                    case_sensitive=case_sensitive,
                ).items())
            return files

        elif not isinstance(search_dir, basestring):
            # Unsupported
            return {}

        # Change all filters strings lists (if they aren't already)
        if regex_filter is None:
            regex_filter = tuple()
        if isinstance(regex_filter, basestring):
            regex_filter = (regex_filter,)
        elif isinstance(regex_filter, re._pattern_type):
            regex_filter = (regex_filter,)
        if suffix_filter is None:
            suffix_filter = tuple()
        if isinstance(suffix_filter, basestring):
            suffix_filter = (suffix_filter, )
        if prefix_filter is None:
            prefix_filter = tuple()
        if isinstance(prefix_filter, basestring):
            prefix_filter = (prefix_filter, )

        # clean prefix list
        if prefix_filter:
            prefix_filter = self.parse_list(prefix_filter)

        # clean up suffix list
        if suffix_filter:
            suffix_filter = self.parse_list(suffix_filter)

        # Precompile any defined regex definitions
        if regex_filter:
            _filters = []
            for f in regex_filter:
                if not isinstance(f, re._pattern_type):
                    flags = re.MULTILINE
                    if not case_sensitive:
                        flags |= re.IGNORECASE
                    try:
                        _filters.append(re.compile(f, flags=flags))
                        self.logger.debug('Compiled regex "%s"' % f)
                    except:
                        self.logger.error(
                            'invalid regular expression: "%s"' % f,
                        )
                        return {}
                else:
                    # precompiled already
                    _filters.append(f)
            # apply
            regex_filter = _filters

        if isfile(search_dir):
            fname = basename(search_dir)
            dname = dirname(search_dir)
            filtered = False
            if regex_filter:
                filtered = True
                for regex in regex_filter:
                    if regex.search(fname):
                        self.logger.debug('Allowed %s (regex)' % fname)
                        filtered = False
                        break
                if filtered:
                    self.logger.debug('Denied %s (regex)' % fname)

            if not filtered and prefix_filter:
                filtered = True
                for prefix in prefix_filter:
                    if case_sensitive:
                        if fname[0:len(prefix)] == prefix:
                            self.logger.debug('Allowed %s (prefix)' % fname)
                            filtered = False
                            break
                    else:
                        # Not Case Sensitive
                        if fname[0:len(prefix)].lower() == prefix.lower():
                            self.logger.debug('Allowed %s (prefix)' % fname)
                            filtered = False
                            break
                if filtered:
                    self.logger.debug('Denied %s (prefix)' % fname)

            if not filtered and suffix_filter:
                filtered = True
                for suffix in suffix_filter:
                    if case_sensitive:
                        if fname[-len(suffix):] == suffix:
                            self.logger.debug('Allowed %s (suffix)' % fname)
                            filtered = False
                            break
                    else:
                        # Not Case Sensitive
                        if fname[-len(suffix):].lower() == suffix.lower():
                            self.logger.debug('Allowed %s (suffix)' % fname)
                            filtered = False
                            break
                if filtered:
                    self.logger.debug('Denied %s (suffix)' % fname)

            if filtered:
                # File does not meet implied filters
                return {}

            # If we reach here, we can prepare a file using the data
            # we fetch
            _file = {
                search_dir: {
                'basename': fname,
                'dirname': dname,
                'extension': splitext(basename(fname))[1].lower(),
                }
            }
            if fullstats:
                stat_obj = stat(search_dir)
                _file[search_dir]['modified'] = \
                    datetime.fromtimestamp(stat_obj[ST_MTIME])
                _file[search_dir]['accessed'] = \
                    datetime.fromtimestamp(stat_obj[ST_ATIME])
                _file[search_dir]['created'] = \
                    datetime.fromtimestamp(stat_obj[ST_CTIME])
                _file[search_dir]['filesize'] = stat_obj[ST_SIZE]
            return _file

        elif not isdir(search_dir):
            return {}

        # For depth matching
        search_dir = normpath(search_dir)
        depth_offset = len(re.split('[%s]' % ESCAPED_PATH_SEPARATOR, search_dir)) - 1
        self.logger.debug('File depth offset %d' % depth_offset)

        for dname, dnames, fnames in walk(
            search_dir, followlinks=followlinks):

            # Depth handling
            current_depth = \
                    len(re.split('[%s]' % ESCAPED_PATH_SEPARATOR, dname))\
                    - depth_offset

            # Min and Max depth handling
            if max_depth and max_depth < current_depth:
                continue
            if min_depth and min_depth > current_depth:
                continue

            self.logger.debug('CUR depth %d (MAX=%s, MIN=%s)' % \
                              (current_depth, str(max_depth), str(min_depth)))

            for fname in fnames:
                filtered = False

                # Apply filters
                if regex_filter:
                    filtered = True
                    for regex in regex_filter:
                        if regex.search(fname):
                            self.logger.debug('Allowed %s (regex)' % fname)
                            filtered = False
                            break
                    if filtered:
                        self.logger.debug('Denied %s (regex)' % fname)
                        continue

                if not filtered and prefix_filter:
                    filtered = True
                    for prefix in prefix_filter:
                        if fname[0:len(prefix)] == prefix:
                            self.logger.debug('Allowed %s (prefix)' % fname)
                            filtered = False
                            break
                    if filtered:
                        self.logger.debug('Denied %s (prefix)' % fname)
                        continue

                if not filtered and suffix_filter:
                    filtered = True
                    for suffix in suffix_filter:
                        if fname[-len(suffix):] == suffix:
                            self.logger.debug('Allowed %s (suffix)' % fname)
                            filtered = False
                            break
                    if filtered:
                        self.logger.debug('Denied %s (suffix)' % fname)
                        continue

                # If we reach here, we store the file found
                extension = splitext(fname)[1].lower()
                _file = join(dname, fname)
                files[_file] = {
                    'basename': fname,
                    'dirname': dname,
                    'extension': extension,
                }

                if fullstats:
                    # Extend file information
                    stat_obj = stat(_file)
                    files[_file]['modified'] = \
                        datetime.fromtimestamp(stat_obj[ST_MTIME])
                    files[_file]['accessed'] = \
                        datetime.fromtimestamp(stat_obj[ST_ATIME])
                    files[_file]['created'] = \
                        datetime.fromtimestamp(stat_obj[ST_CTIME])
                    files[_file]['filesize'] = stat_obj[ST_SIZE]
        # Return all files
        return files

    def run(self, *args, **kwargs):
        """The intent is this is the script you run from within your script
        after overloading the main() function of your class
        """
        import traceback
        from sys import exc_info

        # Default
        main_function = self.main

        # Determine the function to use
        # multi-scripts need to define a
        #  - postprocess_main()
        #  - scan_main()
        #  - schedule_main()
        #  - queue_main()
        #
        # otherwise main() is executed
        if hasattr(self, '%s_%s' % (self.script_mode, 'main')):
            main_function = getattr(
                self, '%s_%s' % (self.script_mode, 'main'))

        try:
            exit_code = main_function(*args, **kwargs)
        except:
            # Try to capture error
            exc_type, exc_value, exc_traceback = exc_info()
            lines = traceback.format_exception(
                     exc_type, exc_value, exc_traceback)
            if self.script_mode != SCRIPT_MODE.NONE:
                # NZBGet Mode enabled
                for line in lines:
                    self.logger.error(line)
            else:
                # Display error as is
                self.logger.error('Fatal Exception:\n%s' % \
                    ''.join('  ' + line for line in lines))
            exit_code = EXIT_CODE.FAILURE

        # Simplify return codes for those who just want to use
        # True/False/None
        if exit_code is None:
            exit_code = EXIT_CODE.NONE

        elif exit_code is True:
            exit_code = EXIT_CODE.SUCCESS

        elif exit_code is False:
            exit_code = EXIT_CODE.FAILURE

        # Otherwise Be specific and if the code is not a valid one
        # then simply swap it with the FAILURE one
        if exit_code not in EXIT_CODES:
            self.logger.error(
                'The exit code %d is not valid, ' % exit_code + \
                'changing response to a failure (%d).' % (EXIT_CODE.FAILURE),
            )
            exit_code = EXIT_CODE.FAILURE
        return exit_code

    # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
    # Simplify Parsing
    # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
    def parse_list(self, *args):
        """
        Take a string list and break it into a delimited
        list of arguments. This funciton also supports
        the processing of a list of delmited strings and will
        always return a unique set of arguments. Duplicates are
        always combined in the final results.

        You can append as many items to the argument listing for
        parsing.

        Hence: parse_list('.mkv, .iso, .avi') becomes:
            ['.mkv', '.iso', '.avi']

        Hence: parse_list('.mkv, .iso, .avi', ['.avi', '.mp4') becomes:
            ['.mkv', '.iso', '.avi', '.mp4']

        The parsing is very forgiving and accepts spaces, slashes, comma's
        semicolons, colons, and pipes as delimiters
        """

        result = []
        for arg in args:
            if isinstance(arg, basestring):
                result += re.split(STRING_DELIMITERS, arg)

            elif isinstance(arg, (list, tuple)):
                for _arg in arg:
                    if isinstance(arg, basestring):
                        result += re.split(STRING_DELIMITERS, arg)
                    # A list inside a list? - use recursion
                    elif isinstance(_arg, (list, tuple)):
                        result += self.parse_list(_arg)
                    else:
                        # Convert whatever it is to a string and work with it
                        result += self.parse_list(str(_arg))
            else:
                # Convert whatever it is to a string and work with it
                result += self.parse_list(str(arg))

        # apply as well as make the list unique by converting it
        # to a set() first. filter() eliminates any empty entries
        return filter(bool, list(set(result)))

    def parse_path_list(self, *args):
        """
        Very similar to the parse_list() however this parses a listing of
        provided directories.  The difference is that white space is
        treated a bit more strictly since directory paths can contain
        spaces in them. Trailing (back)slashes are always removed from
        results. Duplicates are always combined in final results.

        Hence: parse_path_list('C:\\test dir\\, D:\\test2') becomes:
            [ 'C:\\test dir', D:\\test2' ]

        Hence: parse_path_list('C:\\test dir\\, D:\\test2',
            [ 'H:\\test 4', 'C:\\test dir', 'D:\\test2' ]
        becomes:
            [ 'C:\\test dir', D:\\test2', 'H:\\test 4' ]
        """

        if not hasattr(self, '_path_delimiter_re'):
            # Compile for speed on first pass though
            self._path_delimiter_re = re.compile(PATH_DELIMITERS)

            # Compile for speed on first pass though
            # This separates D:\entry E:\entry2 by forcing a delimiter
            # that will be caught with the _path_delimiter_re is ran
            # afterwards
            self._path_win_drive_re = re.compile(
                r'[\s,\|]+([A-Za-z]):+(%s)%s*' % (
                    ESCAPED_WIN_PATH_SEPARATOR,
                    ESCAPED_WIN_PATH_SEPARATOR,
            ))

            self._path_win_re = re.compile(
                r'[%s]+[\s,\|]+([%s]{2}%s*|[^%s])' % (
                    ESCAPED_WIN_PATH_SEPARATOR,
                    ESCAPED_WIN_PATH_SEPARATOR,
                    ESCAPED_WIN_PATH_SEPARATOR,
                    ESCAPED_WIN_PATH_SEPARATOR,
            ))

        result = []
        for arg in args:
            if isinstance(arg, basestring):
                cleaned = self._path_delimiter_re.sub('|', tidy_path(arg))
                cleaned = self._path_win_re.sub('|\\1', cleaned)
                cleaned = self._path_win_drive_re.sub('|\\1:\\2', cleaned)
                result += cleaned.split('|')

            elif isinstance(arg, (list, tuple)):
                for _arg in arg:
                    if isinstance(_arg, basestring):
                        cleaned = self._path_delimiter_re.sub('|', tidy_path(_arg))
                        cleaned = self._path_win_re.sub('|\\1', cleaned)
                        cleaned = self._path_win_drive_re.sub('|\\1:\\2', cleaned)
                        result += cleaned.split('|')

                    # A list inside a list? - use recursion
                    elif isinstance(_arg, (list, tuple)):
                        result += self.parse_path_list(_arg)
                    else:
                        # unsupported content
                        continue
            else:
                # unsupported content (None, bool's, int's, floats, etc)
                continue

        # apply as well as make the list unique by converting it
        # to a set() first. filter() eliminates any empty entries
        return filter(bool, list(set([tidy_path(p) for p in result])))

    def parse_bool(self, arg, default=False):
        """
        NZBGet uses 'yes' and 'no' as well as other strings such
        as 'on' or 'off' etch to handle boolean operations from
        it's control interface.

        This method can just simplify checks to these variables.

        If the content could not be parsed, then the default is
        returned.
        """

        if isinstance(arg, basestring):
            # no = no - False
            # of = short for off - False
            # 0  = int for False
            # fa = short for False - False
            # f  = short for False - False
            # n  = short for No - False
            if arg.lower()[0:2] in ('f', 'n', 'no', 'of', '0', 'fa'):
                return False
            # ye = yes - True
            # on = short for off - True
            # 1  = int for True
            # tr = short for True - True
            # t  = short for True - True
            elif arg.lower()[0:2] in ('t', 'y', 'ye', 'on', '1', 'tr'):
                return True
            # otherwise
            return default

        # Handle other types
        return bool(arg)

    def detect_mode(self):
        """
        Attempt to detect the script mode based on environment variables
        The modes are defied at the top and are determined by a certain
        set of global variables defined.
        """
        if self.script_mode is not None:
            return self.script_mode

        if len(self.script_dict):
            self.logger.debug('Detecting possible script mode from: %s' % \
                         ', '.join(self.script_dict.keys()))

        if len(self.script_dict.keys()) > 1:
            for k in [ v for v in SCRIPT_MODES \
                      if v in self.script_dict.keys() + [SCRIPT_MODE.NONE,]]:
                if hasattr(self, '%s_%s' % (k, 'sanity_check')):
                    if getattr(self, '%s_%s' % (k, 'sanity_check'))():
                        self.script_mode = k
                        if self.script_mode != SCRIPT_MODE.NONE:
                            self.logger.info(
                                'Script Mode: %s' % self.script_mode.upper())
                            return self.script_mode

        elif len(self.script_dict.keys()) == 1:
            self.script_mode = self.script_dict.keys()[0]
            if self.script_mode != SCRIPT_MODE.NONE:
                self.logger.info('Script Mode: %s' % self.script_mode.upper())
                return self.script_mode

        self.logger.warning('Script Mode: <Standalone>')
        self.script_mode = SCRIPT_MODE.NONE

        return self.script_mode

    def main(self, *args, **kwargs):
        """Write all of your code here making uses of your functions while
        returning your exit code
        """
        if not self.validate():
            # We're running a version < v11
            return False

        return True
