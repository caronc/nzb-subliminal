# -*- coding: utf-8 -*-
from os.path import basename, splitext
from io import BytesIO
from logging import getLogger
from zipfile import ZipFile

from babelfish import Language, language_converters
from requests import Session
from ..utils import guess_info
import bs4
import requests

from . import Provider
from ..subtitle import Subtitle
from ..utils import guess_info
from ..video import Video, Episode, Movie
from ..converters.subscene import supported_languages
from ..exceptions import ProviderNotAvailable, InvalidSubtitle
from ..subtitle import sanitize_string
from ..subtitle import compute_guess_matches
from ..subtitle import is_valid_subtitle
from ..subtitle import detect


logger = getLogger(__name__)

language_converters.register('subscene = subliminal.converters.subscene:SubsceneConverter')

language_ids = {
        'ara':  2, 'dan': 10, 'nld': 11, 'eng': 13, 'fas': 46, 'fin': 17,
        'fra': 18, 'heb': 22, 'ind': 44, 'ita': 26, 'msa': 50, 'nor': 30,
        'ron': 33, 'spa': 38, 'swe': 39, 'vie': 45, 'sqi':  1, 'hye': 73,
        'aze': 55, 'eus': 74, 'bel': 68, 'ben': 54, 'bos': 60, 'bul':  5,
        'mya': 61, 'cat': 49, 'hrv':  8, 'ces':  9, 'epo': 47, 'est': 16,
        'kat': 62, 'deu': 19, 'ell': 21, 'kal': 57, 'hin': 51, 'hun': 23,
        'isl': 25, 'jpn': 27, 'kor': 28, 'kur': 52, 'lav': 29, 'lit': 43,
        'mkd': 48, 'mal': 64, 'mni': 65, 'mon': 72, 'pus': 67, 'pol': 31,
        'por': 32, 'pan': 66, 'rus': 34, 'srp': 35, 'sin': 58, 'slk': 36,
        'slv': 37, 'som': 70, 'tgl': 53, 'tam': 59, 'tel': 63, 'tha': 40,
        'tur': 41, 'ukr': 56, 'urd': 42, 'yor': 71
}



class SubsceneSubtitle(Subtitle):
    """Subscene Subtitle."""
    provider_name = 'subscene'
    server = 'https://subscene.com'

    def __init__(self,  language, id, release, hearing_impaired, link,
                 series=None, season=None, episode=None,
                 title=None, year=None):
        super(SubsceneSubtitle, self).__init__(language, hearing_impaired)
        self.id = id
        self.hearing_impaired = hearing_impaired
        self.link = link
        self.release = release

        # Calculate the remaining fields
        self.series = series
        self.season = season
        self.episode = episode
        self.title = title
        self.year = year

    def compute_matches(self, video):
        matches = set()
        matches |= compute_guess_matches(video, guess_info(self.release + '.mkv'))

        return matches

class SubsceneProvider(Provider):
    """Subscene Provider."""

    server = 'https://subscene.com'
    languages = supported_languages
    video_types = (Episode, Movie)

    def initialize(self):
        self.session = Session()
        self.session.headers = {
            'User-Agent': self.random_user_agent,
            'Referer': self.server,
        }

    def terminate(self):
        self.session.close()

    def query(self, video):
        """
        Preforms a query for a show on subscene.com
        """
        subtitles = self._simple_query(splitext(basename(video.name))[0])

        if not subtitles:
            subtitles = self._extended_query(video)

        return subtitles

    def list_subtitles(self, video, languages):
        self._create_filters(languages)
        self._enable_filters()
        return [s for s in self.query(video) if s.language in languages]

    def download_subtitle(self, subtitle):
        logger.debug("Downloading subscene subtitle %r", str(subtitle.id))
        soup = self.get(subtitle.link)
        url = soup.find("div", "download").a.get("href")
        r = self.session.get(self.server + url)

        with ZipFile(BytesIO(r.content)) as zf:
            fn = [n for n in zf.namelist() if n.endswith('.srt')][0]
            subtitle_bytes = zf.read(fn)

        subtitle_text = subtitle_bytes.decode(
            detect(subtitle_bytes, subtitle.language.alpha2)['encoding'], 'replace')
        if not is_valid_subtitle(subtitle_text):
            raise InvalidSubtitle
        return subtitle_text

    def _simple_query(self, name):
        subtitles = []

        # set language
        parms = {
            'q': name,
            'l': '',
        }

        logger.debug('Searching subscene for "%s"' % name)
        soup = self.get('/subtitles/title', parms)

        if 'Subtitle search by' in str(soup):
            subtitles = self._subtitles_from_soup(soup)

        if not subtitles:
            search_result = soup.find("div", "search-results")
            if search_result is not None:
                for a in search_result.ul.find_all("a"):
                    logger.debug("Extracting subscene subtitles for '%s'" % a.text)
                    soup = self.get(a.get("href"))
                    subtitles.extend(self._subtitles_from_soup(soup))

        return subtitles

    def _extended_query(self, video):
        # find a subtitle only with correct name, and then from it's page find correct video page
        logger.debug("Using extended search algorithm")

        self._disable_filters()

        video_title = video.title.lower()
        subtitles = self._simple_query(video_title)

        video_page = None
        for subtitle in subtitles:
            if subtitle.title.lower() == video_title:
                try:
                    video_page = self.get(subtitle.link).find("div", "bread").a.get("href")
                    break
                except AttributeError:
                    continue

        if video_page is None:
            return []

        self._enable_filters()
        return self._subtitles_from_soup(self.get(video_page))

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

    def _subtitles_from_soup(self, soup):
        subtitles = []

        # Defaults
        year = None
        language = None

        try:
            year = int(soup.find("div", "header").strong.parent.text.strip()[5:].strip())
        except AttributeError:
            pass

        for tr in soup.table.tbody.find_all("tr"):
            try:
                language = Language.fromsubscene(tr.span.text.strip())
            except NotImplementedError:
                continue

            link = tr.a.get("href")
            id = int(link[link.rindex('/') + 1:])

            release = tr.span.find_next("span").text.strip()
            hearing_impaired = bool(tr.find("td", "a41"))
            subtitles.append(SubsceneSubtitle(
                language=language,
                id=id,
                release=release,
                hearing_impaired=hearing_impaired,
                link=link,
                year=year,
            ))

        logger.debug("%s subtitles found" % len(subtitles))
        return subtitles

    def _create_filters(self, languages):
        self.filters = dict(ForeignOnly="False", HearingImpaired="2")

        self.filters["LanguageFilter"] = ",".join((str(language_ids[l.alpha3]) for l in languages))

        logger.debug("Subscene Filter created: '%s'" % self.filters)

    def _enable_filters(self):
        self.session.cookies.update(self.filters)
        logger.debug("Subscene Filters applied")

    def _disable_filters(self):
        for key in self.filters:
            self.session.cookies.pop(key)
        logger.debug("Subscene Filters discarded")
