# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import babelfish
from ..video import Episode, Movie
from .. import __version__
from random import randint
from os.path import exists
from os.path import join
from hashlib import md5
import requests
import logging

logger = logging.getLogger(__name__)

# Agent List
AGENT_LIST = (
    'Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.0',
    'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.1 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10; rv:33.0) Gecko/20100101 Firefox/33.0',
    'Mozilla/5.0 (X11; Linux i586; rv:31.0) Gecko/20100101 Firefox/31.0',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:31.0) Gecko/20130401 Firefox/31.0',
    'Mozilla/5.0 (Windows NT 5.1; rv:31.0) Gecko/20100101 Firefox/31.0',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36',
    'Mozilla/5.0 (compatible, MSIE 11, Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A',
    'Mozilla/5.0 (iPad; CPU OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5355d Safari/8536.25',
    'Mozilla/5.0 (X11; Linux x86_64; rv:31.0) Gecko/20100101 Firefox/31.0',
)

class Provider(object):
    """Base class for providers

    If any configuration is possible for the provider, like credentials, it must take place during instantiation

    :param \*\*kwargs: configuration
    :raise: :class:`~subliminal.exceptions.ProviderConfigurationError` if there is a configuration error

    """
    #: Supported BabelFish languages
    languages = set()

    #: Supported video types
    video_types = (Episode, Movie)

    #: Required hash, if any
    required_hash = None

    # Returns a random agent to use from the list above
    random_user_agent = AGENT_LIST[randint(0, len(AGENT_LIST)-1)]

    # Defines the ideal user agent to use for all providers otherwise
    primary_user_agent = 'Subliminal/%s' % __version__


    def __init__(self, **kwargs):
        pass

    def __enter__(self):
        self.initialize()
        return self

    def __exit__(self, *args):
        self.terminate()

    def initialize(self):
        """Initialize the provider

        Must be called when starting to work with the provider. This is the place for network initialization
        or login operations.

        .. note:
            This is called automatically if you use the :keyword:`with` statement


        :raise: :class:`~subliminal.exceptions.ProviderNotAvailable` if the provider is unavailable

        """
        pass

    def terminate(self):
        """Terminate the provider

        Must be called when done with the provider. This is the place for network shutdown or logout operations.

        .. note:
            This is called automatically if you use the :keyword:`with` statement

        :raise: :class:`~subliminal.exceptions.ProviderNotAvailable` if the provider is unavailable
        """
        pass

    @classmethod
    def check(cls, video):
        """Check if the `video` can be processed

        The video is considered invalid if not an instance of :attr:`video_types` or if the :attr:`required_hash` is
        not present in :attr:`~subliminal.video.Video`'s `hashes` attribute.

        :param video: the video to check
        :type video: :class:`~subliminal.video.Video`
        :return: `True` if the `video` and `languages` are valid, `False` otherwise
        :rtype: bool

        """
        if not isinstance(video, cls.video_types):
            return False
        if cls.required_hash is not None and cls.required_hash not in video.hashes:
            return False
        return True

    def query(self, languages, *args, **kwargs):
        """Query the provider for subtitles

        This method arguments match as much as possible the actual parameters for querying the provider

        :param languages: languages to search for
        :type languages: set of :class:`babelfish.Language`
        :param \*args: other required arguments
        :param \*\*kwargs: other optional arguments
        :return: the subtitles
        :rtype: list of :class:`~subliminal.subtitle.Subtitle`
        :raise: :class:`~subliminal.exceptions.ProviderNotAvailable` if the provider is unavailable
        :raise: :class:`~subliminal.exceptions.ProviderError` if something unexpected occured

        """
        raise NotImplementedError

    def list_subtitles(self, video, languages):
        """List subtitles for the `video` with the given `languages`

        This is a proxy for the :meth:`query` method. The parameters passed to the :meth:`query` method may
        vary depending on the amount of information available in the `video`

        :param video: video to list subtitles for
        :type video: :class:`~subliminal.video.Video`
        :param languages: languages to search for
        :type languages: set of :class:`babelfish.Language`
        :return: the subtitles
        :rtype: list of :class:`~subliminal.subtitle.Subtitle`
        :raise: :class:`~subliminal.exceptions.ProviderNotAvailable` if the provider is unavailable
        :raise: :class:`~subliminal.exceptions.ProviderError` if something unexpected occured

        """
        raise NotImplementedError

    def download_subtitle(self, subtitle):
        """Download the `subtitle`

        :param subtitle: subtitle to download
        :type subtitle: :class:`~subliminal.subtitle.Subtitle`
        :return: the subtitle text
        :rtype: string
        :raise: :class:`~subliminal.exceptions.ProviderNotAvailable` if the provider is unavailable
        :raise: :class:`~subliminal.exceptions.InvalidSubtitle` if the downloaded subtitle is invalid
        :raise: :class:`~subliminal.exceptions.ProviderError` if something unexpected occured

        """
        raise NotImplementedError

    def debug_url(self, url, session=None, params=None, headers=None,
                      timeout=10, get=True):
        """A simple wrapper that should only be used for developers who
        are testing new providers or debuging old ones.

        Instead of calling self.session.get() or self.session.post()
        where session is a requests.Session() object.

        Just pass the URL and the content will be fetched and stored
        to the /tmp folder.  Subsequent calls will read from the
        file previously fetched instead of getting the data again.

        This allows one to test the server without hitting it
        over and over again.

        If session isn't specified, then a request.Session() instance
        is automatically created in it's stead.  If you've already
        preconfigured a session variable, then pass it in as well
        with this function so it'll use it's prepared data.
        """
        # Temporary debug path
        path = '/tmp'

        # hash by url to keep results unique
        m = md5()
        m.update(url)
        result_file = join(path, '%s.tmp' % m.hexdigest())

        if exists(result_file):
            # Cache file exists, so lets use it
            class DummyResponse(object):
                def __init__(self, result_file):
                    self.status_code = 200
                    self.url = url
                    self.content = ''

                    # Retrieve Data
                    fd = open(result_file, 'r')
                    self.content = fd.read()
                    logger.info('Using cached results for %s', url)
                    fd.close()
            return DummyResponse(result_file=result_file)

        # If we get here we need to fetch the data for ourselves
        if not session:
            session = requests.Session()
            self.session.headers = {
               'User-Agent': self.random_user_agent,
           }

        r = session.get(
            url,
            params=params,
            headers=headers,
            timeout=timeout,
        )

        if r.status_code == 200:
            fd = open(result_file, 'w')
            fd.write(r.content)
            fd.close()
            logger.info('Caching results for url %s (%s).' % (
                url, result_file,
            ))

        return r


    def __repr__(self):
        return '<%s [%r]>' % (
            self.__class__.__name__, self.video_types,
        )
