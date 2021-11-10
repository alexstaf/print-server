"""Helper module to get package version and distribution."""

import pkg_resources as pkr

__pkg__ = 'print-server'

try:
    __distribution__ = pkr.get_distribution(__pkg__)
    __version__ = __distribution__.version
except pkr.DistributionNotFound:  # pragma: no cover
    # package is not installed
    __distribution__ = pkr.Distribution()
    __version__ = '0.0.0 (source)'
