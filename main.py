import argparse
import errno
import logging
import os
import stat
import sys

from mfusepy import FUSE, FuseOSError, log_callback, Operations


class QrFS(Operations):
    use_ns = True

    def __init__(self, debug_mode=False):
        self._debug_mode = debug_mode
        self._uid = os.getuid() if hasattr(os, 'getuid') else 0
        self._gid = os.getgid() if hasattr(os, 'getgid') else 0
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
            'f_bsize': 4096,
            'f_frsize': 4096,
            'f_blocks': 2**20,
            'f_bfree': 0,
            'f_bavail': 0,
            'f_files': 2**30,
            'f_ffree': 0,
            'f_favail': 0,
            'f_namemax': 255
        }

    @log_callback
    def statfs(self, path):
        return self._stat

    @log_callback
    def getattr(self, path, fh=None):
        if path.endswith("/qr.bmp"):
            return self._attr_file
        return self._attr_dir

    def readdir(self, path, fh):
        return ['.', '..', "qr.bmp"]

    def readdir_with_offset(self, path, offset, fh):
        return ['.', '..', "qr.bmp"]

    @log_callback
    def read(self, path, size, offset, fh):
        return b"a" * 15 + b'\n'

    @log_callback
    def init(self, path):
        if self._debug_mode:
            logging.basicConfig(level=logging.DEBUG)

    def destroy(self, path):
        pass


def main():
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
        "--debug",
        dest="debug_mode",
        action="store_true",
        help="Enable debug messages."
    )

    args = parser.parse_args()

    try:
        FUSE(
            QrFS(args.debug_mode),
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

if __name__ == '__main__':
    main()
