# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import logging
import babelfish
import requests
from . import Provider
from .. import __version__
from ..exceptions import InvalidSubtitle, ProviderNotAvailable, ProviderError
from ..subtitle import Subtitle, is_valid_subtitle, detect


logger = logging.getLogger(__name__)


class TheSubDBSubtitle(Subtitle):
    provider_name = 'thesubdb'

    def __init__(self, language, hash):  # @ReservedAssignment
        super(TheSubDBSubtitle, self).__init__(language)
        self.hash = hash

    @property
    def id(self):
        return self.hash + '-' + str(self.language)

    def compute_matches(self, video):
        matches = set()
        # hash
        if 'thesubdb' in video.hashes and video.hashes['thesubdb'] == self.hash:
            matches.add('hash')
        return matches


class TheSubDBProvider(Provider):
    languages = set([babelfish.Language.fromalpha2(l) for l in ['en', 'es', 'fr', 'it', 'nl', 'pl', 'pt', 'ro', 'sv', 'tr']])
    required_hash = 'thesubdb'

    def initialize(self):
        self.session = requests.Session()
        self.session.headers = {
            'User-Agent': self.primary_user_agent,
        }

    def terminate(self):
        self.session.close()

    def get(self, params):
        """Make a GET request on the server with the given parameters

        :param params: params of the request
        :return: the response
        :rtype: :class:`requests.Response`
        :raise: :class:`~subliminal.exceptions.ProviderNotAvailable`

        """
        try:
            r = self.session.get('http://api.thesubdb.com', params=params, timeout=10)
        except requests.Timeout:
            raise ProviderNotAvailable('Timeout after 10 seconds')
        return r

    def query(self, hash):  # @ReservedAssignment
        params = {'action': 'search', 'hash': hash}
        logger.debug('Searching subtitles %r', params)
        r = self.get(params)
        if r.status_code == 404:
            logger.debug('No subtitle found')
            return []
        elif r.status_code != 200:
            raise ProviderError('Request failed with status code %d' % r.status_code)
        return [TheSubDBSubtitle(language, hash) for language in
                set([babelfish.Language.fromalpha2(l) for l in r.content.split(',')])]

    def list_subtitles(self, video, languages):
        return [s for s in self.query(video.hashes['thesubdb']) if s.language in languages]

    def download_subtitle(self, subtitle):
        params = {'action': 'download', 'hash': subtitle.hash, 'language': subtitle.language.alpha2}
        r = self.get(params)
        if r.status_code != 200:
            raise ProviderError('Request failed with status code %d' % r.status_code)
        logger.debug('Download URL: %s {hash=%s, lang=%s}' % (
            'http://api.thesubdb.com', subtitle.hash, subtitle.language.alpha2,
        ))
        subtitle_text = r.content.decode(
            detect(r.content, subtitle.language.alpha2)['encoding'], 'replace')
        if not is_valid_subtitle(subtitle_text):
            raise InvalidSubtitle
        return subtitle_text
