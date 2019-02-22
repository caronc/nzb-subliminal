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

### Subliminal v0.7.5
The core app this tool provides a wrapper to

| Patch | Description |
| ----- | ----------- |
| [subliminal-podnapisi.patch](https://github.com/caronc/nzbget-subliminal/blob/master/patches/subliminal-podnapisi.patch) | Podnapisi redesigned their website; this allows 0.7.5 to work with it.
| [subliminal-unicode.patch](https://github.com/caronc/nzbget-subliminal/blob/master/patches/subliminal-unicode.patch) | Added better unicode support
| [subliminal-guessit_requirements.patch](https://github.com/caronc/nzbget-subliminal/blob/master/patches/subliminal-guessit_requirements.patch) | upgraded guessit to a newer version
| [subliminal-better.encoding.patch](https://github.com/caronc/nzbget-subliminal/blob/master/patches/subliminal-better.encoding.patch) | refactored entire encoding backend to do a better job 'guessing' encodings based on the language of the file.
| [subliminal-addic7ed-optional-login.patch](https://github.com/caronc/nzbget-subliminal/blob/master/patches/subliminal-addic7ed-optional-login.patch) | added optional Addic7ed logins


You can apply the patch as follows (Linux example):
```bash
# Assuming you have our dependencies fullfilled
# - RedHat/CentOS/Fedora: yum install -y curl tar patch
# - Ubuntu/Debian: sudo apt-get install curl tar patch
#
# Retrieve the package
curl -L -O https://pypi.python.org/packages/source/s/subliminal/subliminal-0.7.5.tar.gz

# Retrieve the patch
curl -L -O https://raw.githubusercontent.com/caronc/nzbget-subliminal/master/patches/subliminal-podnapisi.patch
curl -L -O https://raw.githubusercontent.com/caronc/nzbget-subliminal/master/patches/subliminal-unicode.patch
curl -L -O https://raw.githubusercontent.com/caronc/nzbget-subliminal/master/patches/subliminal-guessit_requirements.patch
curl -L -O https://raw.githubusercontent.com/caronc/nzbget-subliminal/master/patches/subliminal-better.encoding.patch
curl -L -O https://raw.githubusercontent.com/caronc/nzbget-subliminal/master/patches/subliminal-addic7ed-optional-login.patch

# Extract our downloaded archive
tar xvfz subliminal-0.7.5.tar.gz

# Apply our patch
patch -d subliminal-0.7.5 -p1 < subliminal-podnapisi.patch
patch -d subliminal-0.7.5 -p1 < subliminal-unicode.patch
patch -d subliminal-0.7.5 -p1 < subliminal-guessit_requirements.patch
patch -d subliminal-0.7.5 -p1 < subliminal-better.encoding.patch
patch -d subliminal-0.7.5 -p1 < subliminal-addic7ed-optional-login.patch

# You're done!
```

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
