# QR Filesystem

QrFS is a virtual filesystem where every directory automatically contains a QR code representing its own path.

Browse an endless tree of generated folders and every location instantly becomes a shareable QR code. Nothing is stored on disk; the filesystem is generated entirely on demand.

## Requirements

* Python 3.9 or newer
* FUSE

## Installation

1. Clone the repository:

```bash
git clone https://github.com/anar-bastanov/qr-filesystem.git
cd qr-filesystem
```

2. Install the FUSE library:

```bash
sudo apt update
sudo apt install fuse3
```

3. (Optional) Create a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

4. Install the Python dependencies:

```bash
pip install -r requirements.txt
```

5. Enable `user_allow_other` in `/etc/fuse.conf` by removing the leading `#`:

```bash
sudo nano /etc/fuse.conf
```

6. Create a mount point and start QrFS:

```bash
mkdir drive
python3 src/main.py drive
```

## Usage

After mounting, browse the filesystem with any file manager or terminal. Every directory contains a distinct virtual QR file. Opening it generates a QR code encoding that directory's relative path.

```
drive/
├── qr.png
├── something/
│   ├── qr.png
│   └── ...
├── anything/
│   ├── qr.png
│   └── ...
├── everything/
│   ├── qr.png
│   └── ...
└── ...
```

## Examples

The path between the mount point and the QR file is interpreted as a URL:

```
drive/work/projects/demo/qr.png
# produces a QR code for:
work/projects/demo

drive/www.youtube.com/watch?v=dQw4w9WgXcQ/qr.png
# produces a QR code for:
www.youtube.com/watch?v=dQw4w9WgXcQ

drive/https:\\/github.com/anar-bastanov/qr-filesystem/blob/main/src/main.py/qr.png
# produces a QR code for:
https://github.com/anar-bastanov/qr-filesystem/blob/main/src/main.py
```

The QR output format, image size, border size, and other options can be customized through command-line arguments:

```bash
# Show all options
python3 src/main.py --help

# Generate QR codes as small BMP files
python3 src/main.py --filename qr.bmp --media-type bmp --qr-scale 1 drive

# Customize filesystem name and behavior
python3 src/main.py --max-cache 4096 --fsname MagicFS --subtype magic drive

# Disable generated directories and preserve backslashes
python3 src/main.py --ghost-dirs 0 --allow-backslash --filename qr --media-type raw drive
```

## License

Copyright &copy; 2026 Anar Bastanov <br>
Distributed under the [MIT License](http://www.opensource.org/licenses/mit-license.php).
