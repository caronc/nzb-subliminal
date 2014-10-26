Subliminal Processing script for NZBGet
=======================================
This is an NZB  _post-processing_ and _scheduling_ script wrapper for
_Subliminal_. Subliminal was written by Antoine Bertin (Diaoul Ael).
Subliminal is a fantastic tool that can take a file you provide to it and
makes use of a series of websites in efforts to obtain the subtitles
associated with it.

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
| requests **[P]**             | 2.3.0   | https://pypi.python.org/pypi/requests/2.3.0                                      |
| setuptools                   | 0.6.10  | http://svn.python.org/projects/sandbox/branches/setuptools-0.6/pkg_resources.py  |
| six                          | 1.6.1   | https://pypi.python.org/pypi/six/1.6.1                                           |
| stevedore                    | 0.14    | https://pypi.python.org/pypi/stevedore/0.14                                      |
| subliminal **[P]**           | 0.7.4   | https://pypi.python.org/pypi/subliminal/0.7.4                                    |
| urllib3 **[P]**              | 1.9     | https://pypi.python.org/pypi/urllib3/1.9                                         |
| pyxdg                        | 0.25    | https://pypi.python.org/pypi/pyxdg/0.25                                          |
| ordereddict                  | 1.1     | https://pypi.python.org/pypi/ordereddict/1.1                                     |
| ndg-httpsclient              | 0.3.2   | https://pypi.python.org/pypi/ndg-httpsclient/0.3.2                               |
| pyasn1                       | 0.1.7   | https://pypi.python.org/pypi/pyasn1/0.1.7                                        |
| pyOpenSSL                    | 0.14    | https://pypi.python.org/pypi/pyOpenSSL/0.14                                      |

**Note:** I patched (denoted with a **[P]** above) the some of the libraries
mentioned above in efforts to make them compatible with python 2.6 and or
simply fix bugs and add nessesary enhancments.

To be as transparent as possible, all patches have been provided in the
_/patches_ directory.
