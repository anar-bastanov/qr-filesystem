import argparse
import errno
from functools import lru_cache
import logging
import os
import stat
import sys

from mfusepy import FUSE, FuseOSError, log_callback, Operations


class QrFS(Operations):
    use_ns = True

    def __init__(self, media_type="bmp", max_cache=256, debug_mode=False):
        from encoder import path_to_qr  # Do not directly call path_to_qr elsewhere
        self.get_qr = lru_cache(maxsize=max_cache)(path_to_qr)

        self._media_type = media_type
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
        if path.endswith("/..."):
            qr = self.get_qr(path, self._media_type)
            attrs = self._attr_file.copy()  # Not sure if .copy() can be omitted
            attrs["st_size"] = len(qr)
            return attrs

        if path[-1] == '.' and path.rstrip(".")[-1] == '/':
            raise FuseOSError(errno.ENOENT)

        return self._attr_dir

    def readdir(self, path, fh):
        return [".", "..", "..."]

    def readdir_with_offset(self, path, offset, fh):
        return [".", "..", "..."]

    @log_callback
    def read(self, path, size, offset, fh):
        qr = self.get_qr(path, self._media_type)
        return qr[offset:offset + size]

    @log_callback
    def init(self, path):
        if self._debug_mode:
            logging.basicConfig(level=logging.DEBUG)

    def destroy(self, path):
        if self._debug_mode:
            print("\n--- Cache Stats ---")
            print(self.get_qr.cache_info())
            print("-------------------\n")


def main():
    def int_range(imin, imax):
        def parse(value):
            n = int(value)
            if n < imin:
                raise argparse.ArgumentTypeError(f"value less than {imin}")
            if n > imax:
                raise argparse.ArgumentTypeError(f"value greater than {imax}")
            return n
        return parse

    parser = argparse.ArgumentParser(
        description="Launch the QrFS virtual filesystem."
    )
    parser.add_argument(
        "mountpoint",
        type=str,
        help="The local directory path where the filesystem will be attached."
    )
    parser.add_argument(
        "--fsname",
        type=str,
        default="qrfs",
        help="The filesystem name visible in system mount utilities."
    )
    parser.add_argument(
        "--subtype",
        type=str,
        default="qrfs",
        help="The filesystem subtype classification."
    )
    parser.add_argument(
        "--media-type",
        type=str,
        choices=("raw", "bmp", "png"),
        default="bmp",
        help="File format in which to stream QR codes."
    )
    parser.add_argument(
        "--max-cache",
        type=int_range(0, 2**12),
        default=256,
        help="Number of QR codes to cache in memory."
    )
    parser.add_argument(
        "--debug",
        dest="debug_mode",
        action="store_true",
        help="Enable debug messages."
    )

    args = parser.parse_args()

    try:
        FUSE(
            QrFS(args.media_type, args.max_cache, args.debug_mode),
            args.mountpoint,
            foreground=True,
            nothreads=True,
            fsname=args.fsname,
            subtype=args.subtype,
            ro=True  # Mount as a read-only filesystem
        )
    except RuntimeError as e:
        print("Error:", e)
        sys.exit(1)

if __name__ == "__main__":
    main()
