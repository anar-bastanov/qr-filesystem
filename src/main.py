import argparse
import sys

from mfusepy import FUSE

import argparse_types
from qrfs import QrFS


def main():
    parser = argparse.ArgumentParser(
        description="Launch the QrFS virtual filesystem."
    )
    parser.add_argument(
        "mountpoint",
        type=str,
        help="local directory path where the filesystem will be attached"
    )
    parser.add_argument(
        "--filename",
        type=argparse_types.str_except("\0/"),
        default="...",
        help="name of the special QR file"
    )
    parser.add_argument(
        "--media-type",
        type=str,
        choices=("raw", "bmp", "png"),
        default="bmp",
        help="file format in which to stream QR codes"
    )
    parser.add_argument(
        "--qr-border",
        type=argparse_types.int_range(0, 16),
        default=1,
        help="size of borders around the images in pixels"
    )
    parser.add_argument(
        "--max-cache",
        type=argparse_types.int_range(0, 2**12),
        default=256,
        help="number of QR codes to cache in memory"
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
        "--debug",
        dest="debug_mode",
        action="store_true",
        help="enable debug messages"
    )

    args = parser.parse_args()

    try:
        FUSE(
            QrFS(
                args.filename,
                args.media_type,
                args.qr_border,
                args.max_cache,
                args.debug_mode
            ),
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
