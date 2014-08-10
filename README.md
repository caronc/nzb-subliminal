Subliminal Processing script for NZBGet
=======================================
This is an NZB  _post-processing_ and _scan_ script wrapper for "Subliminal",
Subliminal was written by Antoine Bertin (Diaoul Ael). It' is a fantastic
tool that can take a file, parse it of it's meta information and attempt
to fetch subtitles for it.

Subliminal Details
==================
* Author: Antoine Bertin (diaoulael@gmail.com).
* Web-site: http://subliminal.readthedocs.org.
* Source code: http://github.com/Diaoul/subliminal.
* License: GPLv3 (http://www.gnu.org/licenses/gpl.html).
* Version: 0.7.4 (release date: 2014-01-27).

Installation Instructions
=========================
* Simply place the _Subliminal.py_ and _Subliminal_ directory together inside
  of your NZBGets nzbget/scripts directory.

Note: The _Subliminal_ directory provides all of the nessisary dependencies
in order for this script to work correctly. The directory is only required
if you do not have the following packages already available to you global
environment:

Dependencies
============
This script requires Python v2.6+ to be installed on your system.

The following dependencies are already provided for you within the
_Subliminal_ directory and no further effort is required by you. However, it
should be known that Subliminal.py depends on the following packages:

| Name                         | Version | Source                                                                           |
| ---------------------------- |:------- |:-------------------------------------------------------------------------------- |
| pysrt                        | 1.0.1   | https://pypi.python.org/pypi/pysrt/1.0.1                                         |
| babelfish                    | 0.5.1   | https://pypi.python.org/pypi/babelfish/0.5.1                                     |
| backports-ssl_match_hostname | 3.4.0.2 | https://pypi.python.org/pypi/backports.ssl_match_hostname/3.4.0.2                |
| beautifulsoup4               | 4.3.2   | https://pypi.python.org/pypi/beautifulsoup4/4.3.2                                |
| charade                      | 1.0.3   | https://pypi.python.org/pypi/charade/1.0.3                                       |
| chardet                      | 2.2.1   | https://pypi.python.org/pypi/chardet/2.2.1                                       |
| dogpile-cache                | 0.5.4   | https://pypi.python.org/pypi/dogpile.cache/0.5.4                                 |
| dogpile-core                 | 0.4.1   | https://pypi.python.org/pypi/dogpile.core/0.4.1                                  |
| enzyme                       | 0.4.1   | https://pypi.python.org/pypi/enzyme/0.4.1                                        |
| guessit                      | 0.7.1   | https://pypi.python.org/pypi/guessit/0.7.1                                       |
| html5lib                     | 0.999   | https://pypi.python.org/pypi/html5lib/0.999                                      |
| pynzbget                     | 0.1.0   | https://github.com/caronc/pynzbget                                               |
| requests _[p]_               | 2.3.0   | https://pypi.python.org/pypi/requests/2.3.0                                      |
| setuptools                   | 0.6.10  | http://svn.python.org/projects/sandbox/branches/setuptools-0.6/pkg_resources.py  |
| six                          | 1.6.1   | https://pypi.python.org/pypi/six/1.6.1                                           |
| stevedore                    | 0.14    | https://pypi.python.org/pypi/stevedore/0.14                                      |
| subliminal _[p]_             | 0.7.4   | https://pypi.python.org/pypi/subliminal/0.7.4                                    |
| urllib3 _[p]_                | 1.9     | https://pypi.python.org/pypi/urllib3/1.9                                         |
| pyxdg                        | 0.25    | https://pypi.python.org/pypi/pyxdg/0.25                                          |
| ordereddict                  | 1.1     | https://pypi.python.org/pypi/ordereddict/1.1                                     |

Note: I patched (denoted with a _[p]_ above) the some of the libraries
mentioned above in efforts to make them compatible with python 2.6.

To be as transparent as possible, they have been provided in the _/patches_ directory.
