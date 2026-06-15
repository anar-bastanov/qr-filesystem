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

    def write(self, path, data, offset, fh): return 0
    def chmod(self, path, mode): return 0
    def chown(self, path, uid, gid): return 0
    def mkdir(self, path, mode): return 0
    def rmdir(self, path): return 0
    def create(self, path, mode, fi=None): return 0
    def rename(self, old, new): return 0
    def truncate(self, path, length, fh=None): return 0
    def unlink(self, path): return 0

    def access(self, path, amode): return 0
    def opendir(self, path): return 0
    def releasedir(self, path, fh): return 0
    def open(self, path, flags): return 0
    def flush(self, path, fh): return 0
    def release(self, path, fh): return 0
    def fsync(self, path, datasync, fh): return 0
    def fsyncdir(self, path, datasync, fh): return 0
    def utimens(self, path, times=None): return 0

    def readlink(self, path): raise FuseOSError(errno.ENOENT)
    def symlink(self, target, source): raise FuseOSError(errno.ENOSYS)
    def link(self, target, source): raise FuseOSError(errno.ENOSYS)
    def mknod(self, path, mode, dev): raise FuseOSError(errno.ENOSYS)
    def getxattr(self, path, name, position=0): raise FuseOSError(errno.ENOTSUP)
    def listxattr(self, path): return []
    def setxattr(self, path, name, value, options, position=0): raise FuseOSError(errno.ENOTSUP)
    def removexattr(self, path, name): raise FuseOSError(errno.ENOTSUP)
    def bmap(self, path, blocksize, idx): raise FuseOSError(errno.ENOSYS)
    def fallocate(self, path, mode, offset, size, fh): raise FuseOSError(errno.ENOSYS)
    def flock(self, path, fh, op): raise FuseOSError(errno.ENOSYS)
    def poll(self, path, fh, ph, reventsp): raise FuseOSError(errno.ENOSYS)
    # def read_buf(self, path, bufpp, size, offset, fh):
    # def write_buf(self, path, buf, offset, fh):
    def ioctl(self, path, cmd, arg, fh, flags, data): raise FuseOSError(errno.ENOTTY)
    # def lock(self, path, fh, cmd, lock): raise FuseOSError(errno.ENOSYS)

    @log_callback
    def init(self, path):
        if self._debug_mode:
            logging.basicConfig(level=logging.DEBUG)

    # Only one init method should be overridden
    # def init_with_config(self, conn_info, config_3):

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
