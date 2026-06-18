from functools import lru_cache
import logging
import random
import stat

from mfusepy import fuse_get_context, log_callback, Operations

from converter import get_path_to_qr_converter


class QrFS(Operations):
    use_ns = True

    _DIRNAME_CHARSET = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-."

    def __init__(
        self,
        filename="...",
        media_type="bmp",
        qr_scale=10,
        qr_border=1,
        ghost_dir_count=100,
        allow_backslash=False,
        max_cache=256,
        debug_mode=False
    ):
        uid, gid, _ = fuse_get_context()

        self._filename = filename
        self._filename_path = "/" + filename
        self._dir_items = [".", "..", filename]
        self._ghost_dir_count = ghost_dir_count
        self._debug_mode = debug_mode
        self._attr_dir = {
            "st_mode": (stat.S_IFDIR | 0o555),
            "st_nlink": 2,
            "st_size": 4096,
            "st_atime": 946684800 * 1e9,
            "st_mtime": 946684800 * 1e9,
            "st_ctime": 946684800 * 1e9,
            "st_birthtime": 946684800 * 1e9,  # Birthtime not supported?
            "st_uid": uid,
            "st_gid": gid,
        }
        self._attr_file = {
            "st_mode": (stat.S_IFREG | 0o444),
            "st_nlink": 1,
            "st_size": 16,
            "st_atime": 946684800 * 1e9,
            "st_mtime": 946684800 * 1e9,
            "st_ctime": 946684800 * 1e9,
            "st_birthtime": 946684800 * 1e9,
            "st_uid": uid,
            "st_gid": gid,
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

        self.get_qr = lru_cache(maxsize=max_cache)(
            get_path_to_qr_converter(
                filename,
                media_type,
                qr_scale,
                qr_border,
                allow_backslash
            )
        )

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
        yield ".", self._attr_dir, 1
        yield "..", self._attr_dir, 2
        yield self._filename, None, 3

        for offset in range(4, self._ghost_dir_count + 4):
            yield QrFS._get_random_dirname(), self._attr_dir, offset

    def readdir_with_offset(self, path, offset, fh):
        if offset < 1: yield ".", self._attr_dir, 1
        if offset < 2: yield "..", self._attr_dir, 2
        if offset < 3: yield self._filename, None, 3

        for offset in range(max(4, offset + 1), self._ghost_dir_count + 4):
            yield QrFS._get_random_dirname(), self._attr_dir, offset

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

    @staticmethod
    def _get_random_dirname():
        # No options to configure this for now
        return "".join(random.choices(QrFS._DIRNAME_CHARSET, k=random.randint(4, 16)))
