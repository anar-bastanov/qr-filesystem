import sys
import stat
import errno
from mfusepy import FUSE, Operations, FuseOSError


class QrFS(Operations):
    use_ns = True

    def getattr(self, path, fh=None):
        print("getattr", f"{path = }", f"{fh = }", sep=" | ")
        if path == "/":
            return {
                'st_mode': (stat.S_IFDIR | 0o755),
                'st_nlink': 2,
                'st_size': 4096
            }
        raise FuseOSError(errno.ENOENT)

    def readdir(self, path, fh):
        print("readdir", f"{path = }", f"{fh = }", sep=" | ")
        return ['.', '..']

    def readdir_with_offset(self, path, offset, fh):
        print("readdir_with_offset", f"{path = }", f"{offset = }", f"{fh = }", sep=" | ")
        return ['.', '..']

    def statfs(self, path):
        print("statfs", f"{path = }", sep=" | ")
        return {
            'f_bsize': 4096,
            'f_blocks': 100000,
            'f_bfree': 50000,
            'f_bavail': 50000,
        }

    def access(self, path, amode):
        print("access", f"{path = }", f"{amode = }", sep=" | ")
        return 0

    def chmod(self, path, mode):
        print("chmod", f"{path = }", f"{mode = }", sep=" | ")
        raise FuseOSError(errno.EROFS)

    def chown(self, path, uid, gid):
        print("chown", f"{path = }", f"{uid = }", f"{gid = }", sep=" | ")
        raise FuseOSError(errno.EROFS)

    def utimens(self, path, times=None):
        print("utimens", f"{path = }", f"{times = }", sep=" | ")
        return 0

    def opendir(self, path):
        print("opendir", f"{path = }", sep=" | ")
        return 0

    def releasedir(self, path, fh):
        print("releasedir", f"{path = }", f"{fh = }", sep=" | ")
        return 0

    def mkdir(self, path, mode):
        print("mkdir", f"{path = }", f"{mode = }", sep=" | ")
        raise FuseOSError(errno.EROFS)

    def rmdir(self, path):
        print("rmdir", f"{path = }", sep=" | ")
        raise FuseOSError(errno.EROFS)

    def create(self, path, mode, fi=None):
        print("create", f"{path = }", f"{mode = }", f"{fi = }", sep=" | ")
        raise FuseOSError(errno.EROFS)

    def unlink(self, path):
        print("unlink", f"{path = }", sep=" | ")
        raise FuseOSError(errno.EROFS)

    def rename(self, old, new):
        print("rename", f"{old = }", f"{new = }", sep=" | ")
        raise FuseOSError(errno.EROFS)

    def open(self, path, flags):
        print("open", f"{path = }", f"{flags = }", sep=" | ")
        return 0

    def read(self, path, size, offset, fh):
        print("read", f"{path = }", f"{size = }", f"{offset = }", f"{fh = }", sep=" | ")
        raise FuseOSError(errno.EIO)

    def write(self, path, data, offset, fh):
        print("write", f"{path = }", f"data_len = {len(data)}", f"{offset = }", f"{fh = }", sep=" | ")
        raise FuseOSError(errno.EROFS)

    def truncate(self, path, length, fh=None):
        print("truncate", f"{path = }", f"{length = }", f"{fh = }", sep=" | ")
        raise FuseOSError(errno.EROFS)

    def flush(self, path, fh):
        print("flush", f"{path = }", f"{fh = }", sep=" | ")
        return 0

    def release(self, path, fh):
        print("release", f"{path = }", f"{fh = }", sep=" | ")
        return 0

    def fsync(self, path, datasync, fh):
        print("fsync", f"{path = }", f"{datasync = }", f"{fh = }", sep=" | ")
        return 0

    def fsyncdir(self, path, datasync, fh):
        print("fsyncdir", f"{path = }", f"{datasync = }", f"{fh = }", sep=" | ")
        return 0

    def readlink(self, path):
        print("readlink", f"{path = }", sep=" | ")
        raise FuseOSError(errno.ENOENT)

    def symlink(self, target, source):
        print("symlink", f"{target = }", f"{source = }", sep=" | ")
        raise FuseOSError(errno.EROFS)

    def link(self, target, source):
        print("link", f"{target = }", f"{source = }", sep=" | ")
        raise FuseOSError(errno.EROFS)

    def mknod(self, path, mode, dev):
        print("mknod", f"{path = }", f"{mode = }", f"{dev = }", sep=" | ")
        raise FuseOSError(errno.EROFS)

    def getxattr(self, path, name, position=0):
        print("getxattr", f"{path = }", f"{name = }", f"{position = }", sep=" | ")
        raise FuseOSError(errno.ENOTSUP)

    def listxattr(self, path):
        print("listxattr", f"{path = }", sep=" | ")
        return []

    def setxattr(self, path, name, value, options, position=0):
        print("setxattr", f"{path = }", f"{name = }", f"val_len = {len(value)}", f"{options = }", sep=" | ")
        raise FuseOSError(errno.ENOTSUP)

    def removexattr(self, path, name):
        print("removexattr", f"{path = }", f"{name = }", sep=" | ")
        raise FuseOSError(errno.ENOTSUP)

    def bmap(self, path, blocksize, idx):
        print("bmap", f"{path = }", f"{blocksize = }", f"{idx = }", sep=" | ")
        return 0

    def fallocate(self, path, mode, offset, size, fh):
        print("fallocate", f"{path = }", f"{mode = }", f"{offset = }", f"{size = }", f"{fh = }", sep=" | ")
        raise FuseOSError(errno.ENOSYS)

    def flock(self, path, fh, op):
        print("flock", f"{path = }", f"{fh = }", f"{op = }", sep=" | ")
        raise FuseOSError(errno.ENOSYS)

    def poll(self, path, fh, ph, reventsp):
        print("poll", f"{path = }", f"{fh = }", sep=" | ")
        raise FuseOSError(errno.ENOSYS)

    def read_buf(self, path, bufpp, size, offset, fh):
        print("read_buf", f"{path = }", f"{size = }", f"{offset = }", f"{fh = }", sep=" | ")
        raise FuseOSError(errno.ENOSYS)

    def write_buf(self, path, buf: bytes, offset, fh):
        print("write_buf", f"{path = }", f"buf_len = {len(buf)}", f"{offset = }", f"{fh = }", sep=" | ")
        raise FuseOSError(errno.ENOSYS)

    def ioctl(self, path, cmd, arg, fh, flags, data):
        print("ioctl", f"{path = }", f"{cmd = }", f"{fh = }", f"{flags = }", sep=" | ")
        raise FuseOSError(errno.ENOTTY)

    def lock(self, path, fh, cmd, lock):
        print("lock", f"{path = }", f"{fh = }", f"{cmd = }", sep=" | ")
        raise FuseOSError(errno.ENOSYS)

    def init(self, path):
        print("init", f"{path = }", sep=" | ")
        return None

    def init_with_config(self, conn_info, config_3):
        print("init_with_config", sep=" | ")
        return None

    def destroy(self, path):
        print("destroy", f"{path = }", sep=" | ")
        return None


if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit(1)

    mountpoint = sys.argv[1]

    try:
        FUSE(
            QrFS(),
            mountpoint,
            foreground=True,
            nothreads=True,
            fsname="qrfs",
            subtype="qrfs"
        )
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception:
        sys.exit(1)
