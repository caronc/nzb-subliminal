__Note:__ This script was intended to be an [NZBGet](http://nzbget.net) _post-processing_
and _scheduling_ script wrapper for _Subliminal_. However, it also works
perfectly fine as a standalone script for others too.
See the _Command Line_ section below for details how you can easily use this on it's own (without NZBGet).

Subliminal Scheduling and Processing Script
===========================================
[Subliminal](https://github.com/Diaoul/subliminal) was originally written by Antoine
Bertin (Diaoul Ael). This tool I'm hosting here merely acts as a wrapper to it
by enhancing the great functionality it already provides. Subliminal
allows us to take a video file (and/or a directory containing videos) you
provide it. From there it makes use of a series of websites in efforts to
obtain the subtitles associated with the videos it scanned. This wrapper
extends this functionallity by controlling how many interenet requests are made
for videos without subtitles. This script will prevents querying videos over
and over again that simply don't have subtitles at all.

I do however maintain a [fork](https://github.com/caronc/subliminal/tree/0.7.x) of the
Subliminal 0.7.x branch here where I've added my own enhancements to help make
this tool do what I want to. Enhancments such as:
* The script pays attention to the date of the files and only acts on those that are within a certain (configurable) timeframe; _the default age is 24 hours_. This works really amazing for NZBGet users, but for those using this tool in it's standalone version may find it works for them too. This feature allows you to control how many times the internet is polled against a video that has never had subtitles posted for it.  There is more detail on this below in the __Command Line__ section on how to use _(or disable)_ this feature.
* The script can operate in one of 5 modes:
   * __ImpairedOnly__: Only attempt to fetch subtitles that are identified as supporting the hearing impaired. _Note: This is not an enhancment and exists in the current version of subliminal._
   * __StandardOnly__: Only attempt to fetch subtitles that are _NOT_ identified as supporting the hearing impaired. _Note: This is not an enhancment and exists in the current version of subliminal._
   * __BestScore__: Just download the best matched subtitles reguardless of whether they are for the hearing impaired or not. _Note: This is the default option._
   * __ImpairedFirst__: This is similar to the __BestScore__ mode above; except the script scores (weighs) the hearing impaired matches a bit higher in efforts to make them be priority over any other subtitles matched.
   * __StandardFirst__: This is similar to the __BestScore__ mode above; except the script scores (weighs) the hearing impaired matches a bit lower in efforts to make them be the last to be considered as a match.
* Python v2.6 Support in efforts to target a broader audience.

Most of my changes actually made it back into the original source code ([pull request #404](https://github.com/Diaoul/subliminal/pull/404)). However I still like to maintain my own fork in case of an unforseen enhancment gets pushed upstream that breaks this wrapper.

Installation Instructions
=========================
1. Ensure you have at least Python v2.6 or higher installed onto your system.
2. Simply place the __Subliminal.py__ and __Subliminal__ directory together.
   * __NZBGet users__: you'll want to place these inside of your _nzbget/scripts_ directory. Please ensure you are running _(at least)_ NZBGet v11.0 or higher. You can acquire the latest version of of it from [here](http://nzbget.net/download).

The Non-NZBGet users can also use this script via a cron (or simply call it
from the command line) to automatically poll directories for the latest
subtitles for the video content within it. See the __Command Line__ section
below for more instructions on how to do this.

**Note:** The _Subliminal_ directory provides all of the nessisary dependencies
in order for this script to work correctly. The directory is only required
if you do not have the packages already available to your global
environment. These dependant packages are all identified under the
_Dependencies_ section below.

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
| babelfish                    | 0.5.4   | https://pypi.python.org/pypi/babelfish/0.5.4                                         |
| backports-ssl_match_hostname | 3.4.0.2 | https://pypi.python.org/pypi/backports.ssl_match_hostname/3.4.0.2                    |
| beautifulsoup4               | 4.3.2   | https://pypi.python.org/pypi/beautifulsoup4/4.3.2                                    |
| charade                      | 1.0.3   | https://pypi.python.org/pypi/charade/1.0.3                                           |
| chardet                      | 2.2.1   | https://pypi.python.org/pypi/chardet/2.2.1                                           |
| python-dateutil              | 2.2     | https://pypi.python.org/packages/source/p/python-dateutil/python-dateutil-2.2.tar.gz |
| dogpile-cache                | 0.5.4   | https://pypi.python.org/pypi/dogpile.cache/0.5.4                                     |
| dogpile-core                 | 0.4.1   | https://pypi.python.org/pypi/dogpile.core/0.4.1                                      |
| enzyme                       | 0.4.1   | https://pypi.python.org/pypi/enzyme/0.4.1                                            |
| guesslanguage                | 0.2.1   | https://pypi.python.org/pypi/guesslanguage/0.2.1                                     |
| guessit                      | 0.10.3  | https://pypi.python.org/pypi/guessit/0.10.3                                          |
| html5lib                     | 0.999   | https://pypi.python.org/pypi/html5lib/0.999                                          |
| ndg-httpsclient              | 0.3.2   | https://pypi.python.org/pypi/ndg-httpsclient/0.3.2                                   |
| ordereddict                  | 1.1     | https://pypi.python.org/pypi/ordereddict/1.1                                         |
| pynzbget                     | 0.2.3   | https://pypi.python.org/pypi/pynzbget/0.2.3                                          |
| repoze.lru                   | 0.6     | https://pypi.python.org/pypi/repoze.lru/0.6                                          |
| requests **[P]**             | 2.3.0   | https://pypi.python.org/pypi/requests/2.3.0                                          |
| setuptools                   | 0.6.10  | http://svn.python.org/projects/sandbox/branches/setuptools-0.6/pkg_resources.py      |
| silpa_common                 | 0.3     | https://pypi.python.org/pypi/silpa_common/0.3                                        |
| six                          | 1.6.1   | https://pypi.python.org/pypi/six/1.6.1                                               |
| stevedore                    | 0.14    | https://pypi.python.org/pypi/stevedore/0.14                                          |
| subliminal **[P]**           | 0.7.5   | https://pypi.python.org/pypi/subliminal/0.7.5                                        |
| pyasn1                       | 0.1.7   | https://pypi.python.org/pypi/pyasn1/0.1.7                                            |
| pyOpenSSL                    | 0.14    | https://pypi.python.org/pypi/pyOpenSSL/0.14                                          |
| pyxdg                        | 0.25    | https://pypi.python.org/pypi/pyxdg/0.25                                              |
| urllib3 **[P]**              | 1.9     | https://pypi.python.org/pypi/urllib3/1.9                                             |

**Note:** The items above denoted with a **[P]** were patched in efforts to:
- Make their libaries compatible with Python v2.6.
- Fix bugs to add stability to the overall functionality.
- Add the nessesary enhancments that benifit this wrapper tool.

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
                        this variable, it is implied that you are running this
                        from the command line.
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
  -c MINSCORE, --minscore=MINSCORE
                        When scoring multiple matched subtitles for a video,
                        this value identifies the threshold to assume the
                        subtitle is no good and should be thrown away when
                        being compared against others. It currently defaults
                        to 20.
  -k, --skip-embedded   If embedded subtitles were detected, choose not to use
                        them and continue to search for the subtitles hosted
                        by the identified provider(s).
  -f, --force           Force a download reguardless of the file age. This
                        switch negates any value specified by the --age (-a)
                        switch.
  -o, --overwrite       Overwrite a subtitle in the event one is already
                        present.
  -m MODE, --fetch-mode=MODE
                        Identify the fetch mode you wish to invoke, the
                        options are: 'ImpairedOnly', 'StandardOnly',
                        'BestScore', 'StandardFirst', 'ImpairedFirst'.  The
                        default value is: BestScore
  -L FILE, --logfile=FILE
                        Send output to the specified logfile instead of
                        stdout.
  -D, --debug           Debug Mode
```

Here is simple example:
```bash
# Scan a single directory (recursively) for english subtitles
python Subliminal.py -s -f -S /usr/share/TVShows

# Or just omit the (recently) depricated -S switch to achive the same
# results:
python Subliminal.py -s -f /usr/share/TVShows

```


You can scan multiple directories with the following command:
```bash
# Scan a single directory (recursively) for english subtitles
python Subliminal.py -s -f -S "/usr/share/TVShows, /usr/share/Movies"

# Or just omit the (recently) depricated -S switch to achive the same
# results:
python Subliminal.py -s -f /usr/share/TVShows /usr/share/Movies
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
0 * * * * /path/to/Subliminal.py -s /usr/share/TVShows /usr/share/Movies
```
If 24 hours seems to short of a window for you, then just specify the
__--age__ (__-a__) switch and adjust the time to your needs. Remember: it's
value is represented in hours.
