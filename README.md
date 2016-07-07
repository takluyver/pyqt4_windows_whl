This machinery downloads PyQt4 windows binary installers from Sourceforge, reassembles the contents into Python wheel packages, and uploads the results to PyPI. This allows PyQt4 to be installed with pip, and also to be used by other tools such as [Pynsist](http://pynsist.readthedocs.io/en/latest/).

The script runs [on Travis CI](https://travis-ci.org/takluyver/pyqt4_windows_whl), uploading when I include `+UPLOAD` in the commit message.

The resulting wheels can be found here: https://pypi.io/project/PyQt4_windows_whl/
