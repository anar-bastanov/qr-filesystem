from functools import lru_cache
import logging
import os
import stat

from mfusepy import log_callback, Operations

from converter import get_path_to_qr_converter


class QrFS(Operations):
    use_ns = True

    def __init__(
        self,
        filename="...",
        media_type="bmp",
        qr_scale=10,
        qr_border=1,
        allow_backslash=False,
        max_cache=256,
        debug_mode=False
    ):
        self.get_qr = lru_cache(maxsize=max_cache)(
            get_path_to_qr_converter(
                filename,
                media_type,
                qr_scale,
                qr_border,
                allow_backslash
            )
        )

        self._filename = filename
        self._filename_path = "/" + filename
        self._directory = [".", "..", filename]
        self._debug_mode = debug_mode
        self._uid = os.getuid() if hasattr(os, "getuid") else 0
        self._gid = os.getgid() if hasattr(os, "getgid") else 0
        self._attr_dir = {
            "st_mode": (stat.S_IFDIR | 0o555),
            "st_nlink": 2,
            "st_size": 4096,
            "st_atime": 946684800 * 1e9,
            "st_mtime": 946684800 * 1e9,
            "st_ctime": 946684800 * 1e9,
            "st_birthtime": 946684800 * 1e9,  # Birthtime not supported?
            "st_uid": self._uid,
            "st_gid": self._gid,
        }
        self._attr_file = {
            "st_mode": (stat.S_IFREG | 0o444),
            "st_nlink": 1,
            "st_size": 16,
            "st_atime": 946684800 * 1e9,
            "st_mtime": 946684800 * 1e9,
            "st_ctime": 946684800 * 1e9,
            "st_birthtime": 946684800 * 1e9,
            "st_uid": self._uid,
            "st_gid": self._gid,
        }
        self._stat =  {
            "f_bsize": 4096,
            "f_frsize": 4096,
            "f_blocks": 2**20,
            "f_bfree": 0,
            "f_bavail": 0,
            "f_files": 2**30,
            "f_ffree": 0,
            "f_favail": 0,
            "f_namemax": 255
        }

    @log_callback
    def statfs(self, path):
        return self._stat

    @log_callback
    def getattr(self, path, fh=None):
        if path.endswith(self._filename_path):
            qr = self.get_qr(path)
            attrs = self._attr_file.copy()  # Not sure if .copy() can be omitted
            attrs["st_size"] = len(qr)
            return attrs

        return self._attr_dir

    def readdir(self, path, fh):
        return self._directory

    def readdir_with_offset(self, path, offset, fh):
        return self._directory

    @log_callback
    def read(self, path, size, offset, fh):
        qr = self.get_qr(path)
        return qr[offset:offset + size]

    @log_callback
    def init(self, path):
        if self._debug_mode:
            logging.basicConfig(level=logging.DEBUG)

    def destroy(self, path):
        if self._debug_mode:
            print("\nCache Stats:", self.get_qr.cache_info())
