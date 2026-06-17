import argparse
import sys

from mfusepy import FUSE

import argparse_types
from qrfs import QrFS


def main():
    parser = argparse.ArgumentParser(
        description="Launch the QrFS virtual filesystem.",
        formatter_class=argparse_types.CustomFormatter
    )
    parser.add_argument(
        "mountpoint",
        type=str,
        help="local directory path where the filesystem will be attached"
    )
    parser.add_argument(
        "-f", "--filename",
        type=argparse_types.str_except("\0/"),
        default="...",
        help="name of the special QR file"
    )
    parser.add_argument(
        "-t", "--media-type",
        type=str,
        choices=("raw", "bmp", "png"),
        default="png",
        help=(
            "file format for the QR stream:\n"
            "  raw : newline-separated rows of \\x00/\\x01 bytes; ignores QR_SCALE and QR_BORDER\n"
            "  bmp : uncompressed Bitmap image format\n"
            "  png : compressed PNG image format"
        )
    )
    parser.add_argument(
        "-s", "--qr-scale",
        type=argparse_types.int_range(1, 32),
        default=10,
        help="pixel width and height of each cell in QR codes"
    )
    parser.add_argument(
        "-b", "--qr-border",
        type=argparse_types.int_range(0, 16),
        default=1,
        help="number of padding cells to add around QR codes"
    )
    parser.add_argument(
        "-c", "--max-cache",
        type=argparse_types.int_range(0, 2**12),
        default=256,
        help="number of most recent QR codes to cache in memory"
    )
    parser.add_argument(
        "--no-allow-other",
        action="store_true",
        help="restrict filesystem access exclusively to the current user"
    )
    parser.add_argument(
        "--fsname",
        type=str,
        default="qrfs",
        help="filesystem name visible in system mount utilities"
    )
    parser.add_argument(
        "--subtype",
        type=str,
        default="qrfs",
        help="filesystem subtype classification"
    )
    parser.add_argument(
        "-d", "--debug",
        dest="debug_mode",
        action="store_true",
        help="enable debug messages"
    )

    args = parser.parse_args()
    allow_other = not args.no_allow_other

    try:
        FUSE(
            QrFS(
                args.filename,
                args.media_type,
                args.qr_scale,
                args.qr_border,
                args.max_cache,
                args.debug_mode
            ),
            args.mountpoint,
            foreground=True,
            nothreads=True,
            fsname=args.fsname,
            subtype=args.subtype,
            ro=True,  # Mount as a read-only filesystem
            allow_other=allow_other,
            default_permissions=allow_other,
            kernel_cache=True
        )
    except RuntimeError as e:
        print("Error:", e)
        sys.exit(1)


if __name__ == "__main__":
    main()
