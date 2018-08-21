# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import base64
import logging
import os
import re
import xmlrpclib
import zlib
import babelfish
import guessit
from . import Provider
from .. import __version__
from ..exceptions import ProviderError, ProviderNotAvailable, InvalidSubtitle
from ..subtitle import Subtitle, is_valid_subtitle, compute_guess_matches
from ..subtitle import sanitize_string, detect
from ..video import Episode, Movie


logger = logging.getLogger(__name__)


class OpenSubtitlesSubtitle(Subtitle):
    provider_name = 'opensubtitles'
    series_re = re.compile('^"(?P<series_name>.*)" (?P<series_title>.*)$')

    def __init__(self, language, hearing_impaired, id, matched_by, movie_kind, hash, movie_name, movie_release_name,  # @ReservedAssignment
                 movie_year, movie_imdb_id, series_season, series_episode):
        super(OpenSubtitlesSubtitle, self).__init__(language, hearing_impaired)
        self.id = id
        self.matched_by = matched_by
        self.movie_kind = movie_kind
        self.hash = hash
        self.movie_name = movie_name
        self.movie_release_name = movie_release_name
        self.movie_year = movie_year
        self.movie_imdb_id = movie_imdb_id
        self.series_season = series_season
        self.series_episode = series_episode

    @property
    def series_name(self):
        return self.series_re.match(self.movie_name).group('series_name')

    @property
    def series_title(self):
        return self.series_re.match(self.movie_name).group('series_title')

    def compute_matches(self, video):
        matches = set()
        # episode
        if isinstance(video, Episode) and self.movie_kind == 'episode':
            # series
            if video.series and \
                    sanitize_string(self.series_name) == \
                    sanitize_string(video.series):
                matches.add('series')
            # season
            if video.season and self.series_season == video.season:
                matches.add('season')
            # episode
            if video.episode and self.series_episode == video.episode:
                matches.add('episode')
            # guess
            matches |= compute_guess_matches(video, guessit.guess_episode_info(self.movie_release_name + '.mkv'))
        # movie
        elif isinstance(video, Movie) and self.movie_kind == 'movie':
            # year
            if video.year and self.movie_year == video.year:
                matches.add('year')
            # guess
            matches |= compute_guess_matches(video, guessit.guess_movie_info(self.movie_release_name + '.mkv'))
        else:
            logger.info('%r is not a valid movie_kind for %r', self.movie_kind, video)
            return matches
        # hash
        if 'opensubtitles' in video.hashes and self.hash == video.hashes['opensubtitles']:
            matches.add('hash')
        # imdb_id
        if video.imdb_id and self.movie_imdb_id == video.imdb_id:
            matches.add('imdb_id')
        # title
        if video.title and \
                sanitize_string(self.movie_name) == \
                sanitize_string(video.title):
            matches.add('title')
        return matches


class OpenSubtitlesProvider(Provider):
    # Defaults
    username = ''
    password = ''

    server_url = 'http://api.opensubtitles.org/xml-rpc'

    languages = set([babelfish.Language.fromopensubtitles(l) for l in babelfish.language_converters['opensubtitles'].codes])

    def __init__(self, username=None, password=None):
        self.server = None
        self.token = None

        if username and password:
            logger.info('Open Subtitles using authentication serice.')
            self.username = username
            self.password = password

        else:
            logger.info('Open Subtitles using non-authenticated service.')

    def initialize(self):
        self.server = xmlrpclib.ServerProxy(self.server_url)
        try:
            response = self.server.LogIn(
                self.username, self.password, 'eng', 'subliminal v%s' % __version__)

        except xmlrpclib.ProtocolError:
            raise ProviderNotAvailable

        if response['status'].startswith('401'):
            # Unauthorized login attempt
            logger.warning('Failed to authenticate with Open Subtitles!')

            if (self.username or self.password):
                # Reset and recursively try again
                self.username = ''
                self.password = ''
                return self.initialize()

        if response['status'] != '200 OK':
            raise ProviderError('Login failed with status %r' % response['status'])

        self.token = response['token']

        if not self.token:
            raise ProviderError('Failed to acquire a token for Open Subtitles!')

    def terminate(self):

        if self.server is None:
            # Nothing to do
            return

        try:
            response = self.server.LogOut(self.token)
        except xmlrpclib.ProtocolError:
            raise ProviderNotAvailable
        if response['status'] != '200 OK':
            raise ProviderError('Logout failed with status %r' % response['status'])

    def query(self, languages, hash=None, size=None, imdb_id=None, query=None):  # @ReservedAssignment

        if self.server is None:
            # Nothing to do
            return []

        searches = []
        if hash and size:
            searches.append({'moviehash': hash, 'moviebytesize': str(size)})
        if imdb_id:
            searches.append({'imdbid': imdb_id})
        if query:
            searches.append({'query': query})
        if not searches:
            raise ValueError('One or more parameter missing')
        for search in searches:
            search['sublanguageid'] = ','.join(l.opensubtitles for l in languages)
        logger.debug('Searching subtitles %r', searches)
        try:
            response = self.server.SearchSubtitles(self.token, searches)
        except xmlrpclib.ProtocolError:
            raise ProviderNotAvailable
        if response['status'] != '200 OK':
            raise ProviderError('Search failed with status %r' % response['status'])
        if not response['data']:
            logger.debug('No subtitle found')
            return []
        return [OpenSubtitlesSubtitle(babelfish.Language.fromopensubtitles(r['SubLanguageID']),
                                      bool(int(r['SubHearingImpaired'])), r['IDSubtitleFile'], r['MatchedBy'],
                                      r['MovieKind'], r['MovieHash'], r['MovieName'], r['MovieReleaseName'],
                                      int(r['MovieYear']) if r['MovieYear'] else None, int(r['IDMovieImdb']),
                                      int(r['SeriesSeason']) if r['SeriesSeason'] else None,
                                      int(r['SeriesEpisode']) if r['SeriesEpisode'] else None)
                for r in response['data']]

    def list_subtitles(self, video, languages):
        query = None
        if ('opensubtitles' not in video.hashes or not video.size) and not video.imdb_id:
            query = video.name.split(os.sep)[-1]
        return self.query(languages, hash=video.hashes.get('opensubtitles'), size=video.size, imdb_id=video.imdb_id,
                          query=query)

    def download_subtitle(self, subtitle):

        if self.server is None:
            # Nothing to do
            raise ProviderError('Provider not initialized.')

        try:
            response = self.server.DownloadSubtitles(self.token, [subtitle.id])
            logger.debug('Download URL: %s {token=%s, subid:%s}' % (
                self.server_url,
                self.token, subtitle.id,
            ))
        except xmlrpclib.ProtocolError:
            raise ProviderNotAvailable
        if response['status'] != '200 OK':
            raise ProviderError(
                'Download failed with status %s' % str(response['status']))
        if not response['data']:
            raise ProviderError('Nothing to download')
        subtitle_bytes = zlib.decompress(base64.b64decode(response['data'][0]['data']), 47)
        subtitle_text = subtitle_bytes.decode(
            detect(subtitle_bytes, subtitle.language.alpha2)['encoding'], 'replace')
        if not is_valid_subtitle(subtitle_text):
            raise InvalidSubtitle
        return subtitle_text
