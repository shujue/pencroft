from __future__ import absolute_import

import os
import zipfile


class ZipfileLoader(object):
    """Loads from a zipfile"""

    def __init__(self, path):
        self.path = os.path.realpath(path)
        self._names_to_info = None

    def __getstate__(self):
        """Used for pickling (which is used by multiprocessing)"""
        d = self.__dict__.copy()
        d.pop('_file', None)  # not pickle-able
        return d

    @property
    def file(self):
        """Lazy loading property - helps with multi-processing"""
        try:
            return self._file
        except AttributeError:
            self._file = zipfile.ZipFile(self.path)
            return self._file

    def _set_names_to_info(self):
        assert self._names_to_info is None
        self._names_to_info = dict(
            [(i.filename, i) for i in self.file.infolist()])

    def keys(self):
        if self._names_to_info is None:
            self._set_names_to_info()
        return list(self._names_to_info.keys())

    def exists(self, key):
        if self._names_to_info is None:
            self._set_names_to_info()
        return key in self._names_to_info

    def get(self, key):
        info = self._names_to_info[key]
        return self.file.read(info)