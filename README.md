Subliminal Processing script for NZBGet
=======================================
This is an NZB  _post-processing_ and _scheduling_ script wrapper for
_Subliminal_. Subliminal was written by Antoine Bertin (Diaoul Ael).
Subliminal is a fantastic tool that can take a file you provide to it and
makes use of a series of websites in efforts to obtain the subtitles
associated with it.

Non-NZBGet users can also use this script via a cron (or simply call it
from the command line) to automatically poll directories for the latest
subtitles for the content within it. See __Command Line__ section below.

Installation Instructions
=========================
* Ensure you have a copy of NZBGet v11 or higher which can be retrieved from http://nzbget.net
* Ensure you have Python v2.6 or higher installed onto your system.
* Simply place the _Subliminal.py_ and _Subliminal_ directory together inside
  of your _nzbget/scripts_ directory.

**Note:** The _Subliminal_ directory provides all of the nessisary dependencies
in order for this script to work correctly. The directory is only required
if you do not have the packages already available to your global
environment. These packages are all identified under the _Dependencies_ section
below.

Supported Subtitle Sites
========================
The table below identifies the provider _Subliminal.py_ supports and the
location that content is retrieved from.

| Provider | Source |
| -------- | ------ |
| addic7ed | http://www.addic7ed.com/
| opensubtitles | http://www.opensubtitles.org/
| tvsubtitles | http://www.tvsubtitles.net/
| podnapisi | http://www.podnapisi.net/
| thesubdb | http://thesubdb.com/

Dependencies
============
The following dependencies are already provided for you within the
_Subliminal_ directory and no further effort is required by you. However, it
should be known that Subliminal.py depends on the following packages:

| Name                         | Version | Source                                                                               |
| ---------------------------- |:------- |:------------------------------------------------------------------------------------ |
| pysrt                        | 1.0.1   | https://pypi.python.org/pypi/pysrt/1.0.1                                             |
| babelfish                    | 0.5.3   | https://pypi.python.org/pypi/babelfish/0.5.3                                         |
| backports-ssl_match_hostname | 3.4.0.2 | https://pypi.python.org/pypi/backports.ssl_match_hostname/3.4.0.2                    |
| beautifulsoup4               | 4.3.2   | https://pypi.python.org/pypi/beautifulsoup4/4.3.2                                    |
| charade                      | 1.0.3   | https://pypi.python.org/pypi/charade/1.0.3                                           |
| chardet                      | 2.2.1   | https://pypi.python.org/pypi/chardet/2.2.1                                           |
| python-dateutil              | 2.2     | https://pypi.python.org/packages/source/p/python-dateutil/python-dateutil-2.2.tar.gz |
| dogpile-cache                | 0.5.4   | https://pypi.python.org/pypi/dogpile.cache/0.5.4                                     |
| dogpile-core                 | 0.4.1   | https://pypi.python.org/pypi/dogpile.core/0.4.1                                      |
| enzyme                       | 0.4.1   | https://pypi.python.org/pypi/enzyme/0.4.1                                            |
| guesslanguage                | 0.2.1   | https://pypi.python.org/pypi/guesslanguage/0.2.1                                     |
| guessit                      | 0.9.3   | https://pypi.python.org/pypi/guessit/0.9.3                                           |
| html5lib                     | 0.999   | https://pypi.python.org/pypi/html5lib/0.999                                          |
| ndg-httpsclient              | 0.3.2   | https://pypi.python.org/pypi/ndg-httpsclient/0.3.2                                   |
| ordereddict                  | 1.1     | https://pypi.python.org/pypi/ordereddict/1.1                                         |
| pynzbget                     | 0.2.1   | https://github.com/caronc/pynzbget                                                   |
| repoze.lru                   | 0.6     | https://pypi.python.org/pypi/repoze.lru/0.6                                          |
| requests **[P]**             | 2.3.0   | https://pypi.python.org/pypi/requests/2.3.0                                          |
| setuptools                   | 0.6.10  | http://svn.python.org/projects/sandbox/branches/setuptools-0.6/pkg_resources.py      |
| silpa_common                 | 0.3     | https://pypi.python.org/pypi/silpa_common/0.3                                        |
| six                          | 1.6.1   | https://pypi.python.org/pypi/six/1.6.1                                               |
| stevedore                    | 0.14    | https://pypi.python.org/pypi/stevedore/0.14                                          |
| subliminal **[P]**           | 0.7.4   | https://pypi.python.org/pypi/subliminal/0.7.4                                        |
| pyasn1                       | 0.1.7   | https://pypi.python.org/pypi/pyasn1/0.1.7                                            |
| pyOpenSSL                    | 0.14    | https://pypi.python.org/pypi/pyOpenSSL/0.14                                          |
| pyxdg                        | 0.25    | https://pypi.python.org/pypi/pyxdg/0.25                                              |
| urllib3 **[P]**              | 1.9     | https://pypi.python.org/pypi/urllib3/1.9                                             |

**Note:** I patched (denoted with a **[P]** above) the some of the libraries
mentioned above in efforts to:
- Make their libaries compatible with Python 2.6
- Fix bugs to add stability to the overall functionality
- Add nessesary enhancments that benifit the Subliminal.py (NZBGet PostProcess/Scan Script)

To be as transparent as possible, all patches have been provided in the
[_/patches_](https://github.com/caronc/nzbget-subliminal/tree/master/patches) directory.

Command Line
============
Subliminal.py has a built in command line interface that can be easily tied
to a cron entry or can be easilly called from the command line to automate
the fetching of subtitles.

Here are the switches available to you:
```
Usage: Subliminal.py [options]

Options:
  -h, --help            show this help message and exit
  -S DIR, --scandir=DIR
                        The directory to scan against. Note: that by setting
                        this variable, it is implied that you are not running
                        this from the command line.
  -a AGE, --maxage=AGE  The maximum age a file can be to be considered
                        searchable. This value is represented in hours. The
                        default value is 24 hours.
  -l LANG, --language=LANG
                        The language the fetch the subtitles in (en, fr, etc).
                        The default value is 'en'.
  -p PROVIDER1,PROVIDER2,etc, --providers=PROVIDER1,PROVIDER2,etc
                        Specify a list of providers (use commas as delimiters)
                        to identify the providers you wish to use. The
                        following will be used by default: 'opensubtitles,tvsu
                        btitles,podnapisi,addic7ed,thesubdb'
  -s, --single          Download content without the language code in the
                        subtitle filename.
  -b, --basic           Do not attempt to parse additional information from
                        the video file. Running in a basic mode is much faster
                        but can make it more difficult to determine the
                        correct subtitle if more then one is matched.
  -z SIZE_IN_MB, --minsize=SIZE_IN_MB
                        Specify the minimum size a video must be to be worthy
                        of of checking for subtiles. This value is interpreted
                        in MB (Megabytes) and defaults to 150 MB.
  -f, --force           Force a download reguardless of the file age. This
                        switch negates any value specified by the --age (-a)
                        switch.
  -o, --overwrite       Overwrite a subtitle in the event one is already
                        present.
  -m MODE, --fetch-mode=MODE
                        Identify the fetch mode you wish to invoke, the
                        options are: 'ImpairedOnly', 'StandardOnly',
                        'BestScore', 'StandardFirst', 'ImpairedFirst'.  The
                        default value is: 'BestScore'
  -U USERNAME, --addic7ed-username=USERNAME
                        You must specify a Addic7ed username if you wish to
                        use them as one of your chosen providers.
  -P PASSWORD, --addic7ed-password=PASSWORD
                        You must specify a Addic7ed password if you wish to
                        use them as one of your chosen providers.
  -L FILE, --logfile=FILE
                        Send output to the specified logfile instead of
                        stdout.
  -D, --debug           Debug Mode
```

Here is simple example:
```bash
# Scan a single directory (recursively) for english subtitles
python2 Subliminal.py -s -f -S /usr/share/TVShows
```

You can scan multiple directories with the following command:
```bash
# Scan a single directory (recursively) for english subtitles
python2 Subliminal.py -s -f -S "/usr/share/TVShows, /usr/share/Movies"
```

Another nice feature this tool offers is the ability to _expire_ the
need to check certain content over and over again.  Considering that most of
us keep all our videos in one common location.  It would be excessive overkill
to poll the internet each and every time for each and every file we have (for
subtitles) over and over again.  We can assume, that if there are no subtitles for
a given video within the _last 24 hours_ of it's existance on our system, then there
simply aren't going to be any later. _I realize this isn't always the case; but
for most situations it will be._

In the above examples, I provided a __--force__ (__-f__) switch which bypasses
this feature. But if you want to set up a cron entry to scan your library on
a regular basis, this feature can save you time and effort. A cron could be
easily configured to scan your library every hour as so:
```bash
# $> crontab -e
0 * * * * /path/to/Subliminal.py -s -S "/usr/share/TVShows, /usr/share/Movies"
```
If 24 hours seems to short of a window for you, then just specify the
__--age__ (-a) switch and adjust the time to your needs (it's value is represented
in hours).
