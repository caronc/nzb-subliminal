# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import logging
import babelfish
import bs4
import requests
from . import Provider
from ..cache import region
from ..exceptions import ProviderConfigurationError, ProviderNotAvailable, InvalidSubtitle
from ..subtitle import Subtitle, is_valid_subtitle, sanitize_string, extract_title_year, detect
from ..video import Episode


logger = logging.getLogger(__name__)


class Addic7edSubtitle(Subtitle):
    """Addic7ed Subtitle."""

    provider_name = 'addic7ed'

    def __init__(self, language, series, season, episode, title, version, hearing_impaired, download_link, referer):
        super(Addic7edSubtitle, self).__init__(language, hearing_impaired)
        self.series = series
        self.season = season
        self.episode = episode
        self.title = title
        self.version = version
        self.download_link = download_link
        self.referer = referer

    @property
    def id(self):
        return self.download_link

    def compute_matches(self, video):
        matches = set()
        # series
        if video.series and self.series == video.series:
            matches.add('series')
        # season
        if video.season and self.season == video.season:
            matches.add('season')
        # episode
        if video.episode and self.episode == video.episode:
            matches.add('episode')
        # title
        if video.title and self.title.lower() == video.title.lower():
            matches.add('title')
        # release_group
        if video.release_group and self.version and video.release_group.lower() in self.version.lower():
            matches.add('release_group')
        # resolution
        if video.resolution and self.version and video.resolution in self.version.lower():
            matches.add('resolution')
        return matches


class Addic7edProvider(Provider):
    # Defaults
    username = None
    password = None

    languages = set([babelfish.Language('por', 'BR')]) | set([babelfish.Language(l)
                 for l in ['ara', 'aze', 'ben', 'bos', 'bul', 'cat', 'ces', 'dan', 'deu', 'ell', 'eng', 'eus', 'fas',
                           'fin', 'fra', 'glg', 'heb', 'hrv', 'hun', 'hye', 'ind', 'ita', 'jpn', 'kor', 'mkd', 'msa',
                           'nld', 'nor', 'pol', 'por', 'ron', 'rus', 'slk', 'slv', 'spa', 'sqi', 'srp', 'swe', 'tha',
                           'tur', 'ukr', 'vie', 'zho']])
    video_types = (Episode,)
    server = 'http://www.addic7ed.com'

    def __init__(self, username=None, password=None):

        self.logged_in = None
        if username and password:
            logger.info('Addic7ed using authentication serice.')
            self.username = username
            self.password = password
            self.logged_in = False
        else:
            logger.info('Addic7ed using non-authenticated service.')


    def initialize(self):
        self.session = requests.Session()
        self.session.headers = {
            'User-Agent': self.random_user_agent,
            'Referer': self.server,
        }
        if self.logged_in is False:
            # Attempt to log in
            logger.debug('Preparing to log into Addic7ed...')
            data = {
                'username': self.username,
                'password': self.password,
                'Submit': 'Log in',
            }
            try:
                r = self.session.post(
                    self.server + '/dologin.php', data, timeout=10,
                    allow_redirects=False,
                )
            except requests.Timeout:
                raise ProviderNotAvailable(
                    'Addic7ed Authentication timeout',
                )

            if r.status_code == 302:
                logger.debug('Successfully authenticated with Addic7ed.')
                self.logged_in = True
            else:
                logger.warning('Failed to authenticate with Addic7ed!')

    def terminate(self):
        # logout
        if self.logged_in:

            # Toggle our flag reguardless of our success
            self.logged_in = False
            try:
                r = self.session.get(self.server + '/logout.php', timeout=10)
                logger.debug('Successfully logged out of Addic7ed.')
            except requests.Timeout:
                # No problem... we're done anyway
                logger.warning('A timeout occured logging out of Addic7ed!')
                return

            if r.status_code != 200:
                logger.warning(
                    'Addic7ed returned the error code %d while logging out' %\
                    r.status_code,
                )
                return

        # Close our session
        self.session.close()

    def get(self, url, params=None):
        """Make a GET request on `url` with the given parameters

        :param string url: part of the URL to reach with the leading slash
        :param params: params of the request
        :return: the response
        :rtype: :class:`bs4.BeautifulSoup`
        :raise: :class:`~subliminal.exceptions.ProviderNotAvailable`

        """
        try:
            r = self.session.get(self.server + url, params=params, timeout=10)
        except requests.Timeout:
            raise ProviderNotAvailable('Timeout after 10 seconds')
        if r.status_code != 200:
            raise ProviderNotAvailable('Request failed with status code %d' % r.status_code)
        return bs4.BeautifulSoup(r.content, ['permissive'])

    @region.cache_on_arguments()
    def get_show_ids(self):
        """Load the shows page with default series to show ids mapping

        :return: series to show ids
        :rtype: dict

        """
        soup = self.get('/shows.php')
        show_ids = {}
        for html_show in soup.select('td.version > h3 > a[href^="/show/"]'):
            try:
                show_ids[sanitize_string(html_show.string)] = \
                        int(html_show['href'][6:])

            except ValueError:
                logger.debug("Invalid ID(%s) for show: %s" % (
                    html_show['href'][6:],
                    html_show.string,
                ))

        return show_ids

    @region.cache_on_arguments()
    def find_show_id(self, series):
        """Find a show id from the series

        Use this only if the series is not in the dict returned by :meth:`get_show_ids`

        :param string series: series of the episode
        :return: the show id, if any
        :rtype: int or None

        """
        params = {'search': series, 'Submit': 'Search'}
        logger.debug('Searching series %r', params)
        suggested_shows = self.get('/search.php', params).select('span.titulo > a[href^="/show/"]')
        if not suggested_shows:
            logger.info('Series %r not found', series)
            return None

        try:
            return int(suggested_shows[0]['href'][6:])

        except ValueError:
            # Lookup failed
            logger.debug("Invalid ID(%s) for series search: %s" % (
                suggested_shows[0]['href'][6:],
                series,
            ))
        return None

    def query(self, series, season):
        show_ids = self.get_show_ids()
        sanitized_series = sanitize_string(series)
        if sanitized_series in show_ids:
            show_id = show_ids[sanitized_series]
        else:
            show_id = self.find_show_id(sanitized_series)
            if show_id is None:
                if extract_title_year(sanitized_series):
                    logger.debug('Date detected in series title; adjusting search.')
                    # Attempt to search again without the date
                    sanitized_series = sanitize_string(
                        sanitized_series,
                        strip_date=True,
                    )
                    show_id = self.find_show_id(sanitized_series)
                    if show_id is None:
                        return []
        params = {'show_id': show_id, 'season': season}
        logger.debug('Searching subtitles %r', params)
        link = '/show/{show_id}&season={season}'.format(**params)
        soup = self.get(link)
        subtitles = []
        for row in soup('tr', class_='epeven completed'):
            cells = row('td')
            if cells[5].string != 'Completed':
                logger.debug('Skipping incomplete subtitle')
                continue
            if not cells[3].string:
                logger.debug('Skipping empty language')
                continue
            subtitles.append(Addic7edSubtitle(babelfish.Language.fromaddic7ed(cells[3].string), series, season,
                                              int(cells[1].string), cells[2].string, cells[4].string,
                                              bool(cells[6].string), cells[9].a['href'], link))
        return subtitles

    def list_subtitles(self, video, languages):
        return [s for s in self.query(video.series, video.season)
                if s.language in languages and s.episode == video.episode]

    def download_subtitle(self, subtitle):
        try:
            r = self.session.get(self.server + subtitle.download_link, timeout=10,
                                 headers={'Referer': self.server + subtitle.referer})
            logger.debug('Download URL: %s' % (self.server + subtitle.download_link))
        except requests.Timeout:
            raise ProviderNotAvailable('Timeout after 10 seconds')
        if r.status_code != 200:
            raise ProviderNotAvailable('Request failed with status code %d' % r.status_code)
        if r.headers['Content-Type'] == 'text/html':
            raise ProviderNotAvailable('Download limit exceeded')
        subtitle_text = r.content.decode(
            detect(r.content, subtitle.language.alpha2)['encoding'], 'replace')
        if not is_valid_subtitle(subtitle_text):
            raise InvalidSubtitle
        return subtitle_text
