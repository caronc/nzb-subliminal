Common functions for SILPA
##########################

.. image::
   https://travis-ci.org/Project-SILPA/silpa-common.svg
   :target: https://travis-ci.org/Project-SILPA/silpa-common


.. image::
   https://coveralls.io/repos/Project-SILPA/silpa-common/badge.png?branch=master
   :target: https://coveralls.io/r/Project-SILPA/silpa-common?branch=master 


This package provides common functions needed by SILPA web application
itself and modules which are hosted by SILPA. There are 2 submodules
provided by this package

* charmap - provides character mapping for Indic and other languages
* langdetect - module provides language detecting capabilities
* Also provides a decorator servicemethod, this should be used by
  modules which want to expose their methods via JSONRPC modules
