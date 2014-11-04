## Patching
Please note that all of the patches identified here have already been applied
to the libraries included with nzbget-subliminal (this repository).  Hence If you
are (or have already) downloading nzbget-subliminal, then you do not need to keep
this directory at all.

The only reason this __patches__ directory exists for developer transparency.
The content in this directory is just a means of sharing changes I made with other
developers who may be otherwise interested.

There were several libraries patched for various reasons:
* To allow systems running Python v2.6 to still take advantage of the libraries. Previously most of these python libraries only worked with Python v2.7 or higher. This grants us access to a larger audience.
* To add enhancements and/or to address outstanding bugfixes that I felt were nessisary to apply.

The patches identified are exclusive the version they were created against and
will most likely not work if applied against anything else.

### Enzyme v0.4.1
Enzyme is a powerful library writting by the creator of the Subliminal
library. It can open and scan existing video files to extract the metadata
from within it. Subliminal uses this to determine if the video already has
subtitles or not.

| Patch | Description |
| ----- | ----------- |
| [enzyme-python.26.support.patch](https://github.com/caronc/nzbget-subliminal/blob/master/patches/enzyme-python.26.support.patch) | Eliminates reference to logging.NullHandler() which isn't available until Python 2.7. The patch allows the library to be used with systems running Python v2.4 - v2.6.

| Enzyme v0.4.1 Sources |
| --------------------- |
| https://pypi.python.org/packages/source/e/enzyme/enzyme-0.4.1.tar.gz |
| https://github.com/Diaoul/enzyme/archive/0.4.1.zip |

You can apply the patch as follows (Linux example):
```bash
# Assuming you have our dependencies fullfilled
# - RedHat/CentOS/Fedora: yum install -y curl tar patch
# - Ubuntu/Debian: sudo apt-get install curl tar patch
#
# Retrieve the package
curl -L -O https://pypi.python.org/packages/source/e/enzyme/enzyme-0.4.1.tar.gz

# Retrieve the patch
curl -L -O https://raw.githubusercontent.com/caronc/nzbget-subliminal/master/patches/enzyme-python.26.support.patch

# Extract our downloaded archive
tar xvfz enzyme-0.4.1.tar.gz

# Apply our patch
patch -d enzyme-0.4.1 -p1 < enzyme-python.26.support.patch

# You're done!
```

### Requests v2.3.0
Requests greatly simplifies webpage interaction and content extraction in
python. The actual retreival of subtitles is through this library itself.

| Patch | Description |
| ----- | ----------- |
| [requests-use.global.deps.patch](https://github.com/caronc/nzbget-subliminal/blob/master/patches/requests-use.global.deps.patch) | A patch put in place to eliminate reference to the extra libraries this package includes. This way we can use the ones we're already providing and maintaining instead.

| Request v2.3.0 Source |
| --------------------- |
| https://pypi.python.org/packages/source/r/requests/requests-2.3.0.tar.gz |

You can apply the patch as follows (Linux example):
```bash
# Assuming you have our dependencies fullfilled
# - RedHat/CentOS/Fedora: yum install -y curl tar patch
# - Ubuntu/Debian: sudo apt-get install curl tar patch
#
# Retrieve the package
curl -L -O https://pypi.python.org/packages/source/r/requests/requests-2.3.0.tar.gz

# Retrieve the patch
curl -L -O https://raw.githubusercontent.com/caronc/nzbget-subliminal/master/patches/requests-use.global.deps.patch

# Extract our downloaded archive
tar xvfz requests-2.3.0.tar.gz

# Apply our patch
patch -d requests-2.3.0 -p1 < requests-use.global.deps.patch

# You're done!
```

### Subliminal v0.7.4
The foundation of the nzbget-subliminal wrapper. This is the core application
which makes use of all of the libraries hosted so that subtitles can be
fetched based on Movie and TV Series titles it is fed.

There were a lot of changes made to this library in efforts to satisfy needs
and incoming requests from the users of NZBGet (via their forum).

I have an ongoing pull request to Subliminal's v0.7.4 branch in efforts to
push the major changes I've added to it [here](https://github.com/Diaoul/subliminal/pull/404).

| Subliminal v0.7.4 Source |
| --------------------- |
| https://pypi.python.org/packages/source/s/subliminal/subliminal-0.7.4.tar.gz |

All of the patches identified below must be applied in the order they are
listed since some alter files previously changed by another.

| Patch | Description |
| ----- | ----------- |
| [subliminal-reqfix.patch](https://github.com/caronc/nzbget-subliminal/blob/master/patches/subliminal-reqfix.patch) | Update guessit and babelfish requirements to support the newer versions.
| [subliminal-python.26.support.patch](https://github.com/caronc/nzbget-subliminal/blob/master/patches/subliminal-python.26.support.patch) | Python v2.6 support by eliminating reference to [PEP 274](http://legacy.python.org/dev/peps/pep-0274/) (Dict Comprehensions) and reference to logging.NullHandler(). Some Babelfish adjustments were also lumped into this patch.
| [subliminal-guessit07.support.patch](https://github.com/caronc/nzbget-subliminal/blob/master/patches/subliminal-guessit07.support.patch) | Updated some guessit references to accomodate the library version packaged.
| [subliminal-hearing_impaired.ignore.option.patch](https://github.com/caronc/nzbget-subliminal/blob/master/patches/subliminal-hearing_impaired.ignore.option.patch) | Make it so we don't have to exclusively download hearing-impared or non-hearing impaired subtitles. This gives us the flexability to download whatever best matches.
| [subliminal-double.download.patch](https://github.com/caronc/nzbget-subliminal/blob/master/patches/subliminal-double.download.patch) | Eliminates a bug that seems to cause Subliminal to download more then one subtitle (overwriting the last) when there is multiple matched ones.
| [subliminal-prioritize.patch](https://github.com/caronc/nzbget-subliminal/blob/master/patches/subliminal-prioritize.patch) | Introduce a priortization of which subtitle to choose when both hearing-impared and/or non-hearing impaired subtitles are found.
| [subliminal-offline_providers.patch](https://github.com/caronc/nzbget-subliminal/blob/master/patches/subliminal-offline_providers.patch) | Handle subtitle providers that aren't responding to web requests (do to maintenance or whatever) more gracefully. Prior to this patch; subliminal crashes if a provider goes offline or fails to respond.
| [subliminal-podnapisi.patch](https://github.com/caronc/nzbget-subliminal/blob/master/patches/subliminal-podnapisi.patch) | In Aug 2014, podnapisi changed their web page structure around which effectively broke this as a viable provider to search. This patch allows subliminal to successfully search and fetch content from this location again.
| [subliminal-quote_support.patch](https://github.com/caronc/nzbget-subliminal/blob/master/patches/subliminal-quote_support.patch) | Some TV Shows and Movies have quotes in their title. These quotes were interfering with the potential matches on providers when being queried for subtitles.  This patch resolves this dillema.
| [subliminal-addic7ed.logging.patch](https://github.com/caronc/nzbget-subliminal/blob/master/patches/subliminal-addic7ed.logging.patch) | Login and Logoff of Addic7ed server made just a bit more obvious

```bash
# Assuming you have our dependencies fullfilled
# - RedHat/CentOS/Fedora: yum install -y curl tar patch
# - Ubuntu/Debian: sudo apt-get install curl tar patch
#
# Retrieve the package
curl -L -O https://pypi.python.org/packages/source/s/subliminal/subliminal-0.7.4.tar.gz

# Retrieve the patch
curl -L -O https://raw.githubusercontent.com/caronc/nzbget-subliminal/master/patches/subliminal-reqfix.patch
curl -L -O https://raw.githubusercontent.com/caronc/nzbget-subliminal/master/patches/subliminal-python.26.support.patch
curl -L -O https://raw.githubusercontent.com/caronc/nzbget-subliminal/master/patches/subliminal-guessit07.support.patch
curl -L -O https://raw.githubusercontent.com/caronc/nzbget-subliminal/master/patches/subliminal-hearing_impaired.ignore.option.patch
curl -L -O https://raw.githubusercontent.com/caronc/nzbget-subliminal/master/patches/subliminal-double.download.patch
curl -L -O https://raw.githubusercontent.com/caronc/nzbget-subliminal/master/patches/subliminal-prioritize.patch
curl -L -O https://raw.githubusercontent.com/caronc/nzbget-subliminal/master/patches/subliminal-offline_providers.patch
curl -L -O https://raw.githubusercontent.com/caronc/nzbget-subliminal/master/patches/subliminal-podnapisi.patch
curl -L -O https://raw.githubusercontent.com/caronc/nzbget-subliminal/master/patches/subliminal-quote_support.patch
curl -L -O https://raw.githubusercontent.com/caronc/nzbget-subliminal/master/patches/subliminal-addic7ed.logging.patch

# Extract our downloaded archive
tar xvfz subliminal-0.7.4.tar.gz

# Apply our patches
patch -d subliminal-0.7.4 -p1 < subliminal-reqfix.patch
patch -d subliminal-0.7.4 -p1 < subliminal-python.26.support.patch
patch -d subliminal-0.7.4 -p1 < subliminal-guessit07.support.patch
patch -d subliminal-0.7.4 -p1 < subliminal-hearing_impaired.ignore.option.patch
patch -d subliminal-0.7.4 -p1 < subliminal-double.download.patch
patch -d subliminal-0.7.4 -p1 < subliminal-prioritize.patch
patch -d subliminal-0.7.4 -p1 < subliminal-offline_providers.patch
patch -d subliminal-0.7.4 -p1 < subliminal-podnapisi.patch
patch -d subliminal-0.7.4 -p1 < subliminal-quote_support.patch
patch -d subliminal-0.7.4 -p1 < subliminal-addic7ed.logging.patch

# You're done!
```

### Urllib3 v1.9
Urllib3 is a dependency of Requests (identified above).  It provides web page
interaction simplifying some common steps (which requests then further takes
to another level).

| Patch | Description |
| ----- | ----------- |
| [urllib3-use.global.deps.patch](https://github.com/caronc/nzbget-subliminal/blob/master/patches/urllib3-use.global.deps.patch) | A patch put in place to eliminate reference to the extra libraries this package includes. This way we can use the ones we're already providing and maintaining instead.

| Request v1.9 Source |
| --------------------- |
| https://pypi.python.org/packages/source/u/urllib3/url.ib3-1.9.tar.gz |

You can apply the patch as follows (Linux example):
```bash
# Assuming you have our dependencies fullfilled
# - RedHat/CentOS/Fedora: yum install -y curl tar patch
# - Ubuntu/Debian: sudo apt-get install curl tar patch
#
# Retrieve the package
curl -L -O https://pypi.python.org/packages/source/u/urllib3/urllib3-1.9.tar.gz

# Retrieve the patch
curl -L -O https://raw.githubusercontent.com/caronc/nzbget-subliminal/master/patches/urllib3-use.global.deps.patch

# Extract our downloaded archive
tar xvfz urllib3-1.9.tar.gz

# Apply our patch
patch -d urllib3-1.9 -p1 < urllib3-use.global.deps.patch

# You're done!
```
