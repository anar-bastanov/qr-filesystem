import argparse
import errno
import logging
import stat
import sys

from mfusepy import FUSE, FuseOSError, log_callback, Operations


class QrFS(Operations):
    use_ns = True

    def __init__(self, debug_mode=False):
        self.debug_mode = debug_mode

    @log_callback
    def getattr(self, path, fh=None):
        if path == "/":
            return {
                'st_mode': (stat.S_IFDIR | 0o755),
                'st_nlink': 2,
                'st_size': 4096
            }
        raise FuseOSError(errno.ENOENT)

    def readdir(self, path, fh):
        return ['.', '..']

    def readdir_with_offset(self, path, offset, fh):
        return ['.', '..']

    def statfs(self, path):
        return {
            'f_bsize': 4096,
            'f_blocks': 100000,
            'f_bfree': 50000,
            'f_bavail': 50000,
        }

    def access(self, path, amode):
        return 0

    def chmod(self, path, mode):
        raise FuseOSError(errno.EROFS)

    def chown(self, path, uid, gid):
        raise FuseOSError(errno.EROFS)

    def utimens(self, path, times=None):
        return 0

    def opendir(self, path):
        return 0

    def releasedir(self, path, fh):
        return 0

    def mkdir(self, path, mode):
        raise FuseOSError(errno.EROFS)

    def rmdir(self, path):
        raise FuseOSError(errno.EROFS)

    def create(self, path, mode, fi=None):
        raise FuseOSError(errno.EROFS)

    def unlink(self, path):
        raise FuseOSError(errno.EROFS)

    def rename(self, old, new):
        raise FuseOSError(errno.EROFS)

    def open(self, path, flags):
        return 0

    def read(self, path, size, offset, fh):
        raise FuseOSError(errno.EIO)

    def write(self, path, data, offset, fh):
        raise FuseOSError(errno.EROFS)

    def truncate(self, path, length, fh=None):
        raise FuseOSError(errno.EROFS)

    def flush(self, path, fh):
        return 0

    def release(self, path, fh):
        return 0

    def fsync(self, path, datasync, fh):
        return 0

    def fsyncdir(self, path, datasync, fh):
        return 0

    def readlink(self, path):
        raise FuseOSError(errno.ENOENT)

    def symlink(self, target, source):
        raise FuseOSError(errno.EROFS)

    def link(self, target, source):
        raise FuseOSError(errno.EROFS)

    def mknod(self, path, mode, dev):
        raise FuseOSError(errno.EROFS)

    def getxattr(self, path, name, position=0):
        raise FuseOSError(errno.ENOTSUP)

    def listxattr(self, path):
        return []

    def setxattr(self, path, name, value, options, position=0):
        raise FuseOSError(errno.ENOTSUP)

    def removexattr(self, path, name):
        raise FuseOSError(errno.ENOTSUP)

    def bmap(self, path, blocksize, idx):
        return 0

    def fallocate(self, path, mode, offset, size, fh):
        raise FuseOSError(errno.ENOSYS)

    def flock(self, path, fh, op):
        raise FuseOSError(errno.ENOSYS)

    def poll(self, path, fh, ph, reventsp):
        raise FuseOSError(errno.ENOSYS)

    def read_buf(self, path, bufpp, size, offset, fh):
        raise FuseOSError(errno.ENOSYS)

    def write_buf(self, path, buf: bytes, offset, fh):
        raise FuseOSError(errno.ENOSYS)

    def ioctl(self, path, cmd, arg, fh, flags, data):
        raise FuseOSError(errno.ENOTTY)

    def lock(self, path, fh, cmd, lock):
        raise FuseOSError(errno.ENOSYS)

    def init(self, path):
        if self.debug_mode:
            logging.basicConfig(level=logging.DEBUG)

    # def init_with_config(self, conn_info, config_3):
    #     pass

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
            subtype=args.subtype
        )
    except RuntimeError as e:
        print("Error:", e)
        sys.exit(1)

if __name__ == '__main__':
    main()
