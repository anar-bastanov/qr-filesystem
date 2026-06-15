import io

import qrcode


def path_to_url(path):
    # path = "/abc/def/..."
    #         0^^^^^^^4321
    return path[1:-4]

def path_to_qr_raw(path):
    url = path_to_url(path)
    buffer = io.BytesIO()
    img = qrcode.make(url, border=1)
    for row in img.modules:
        buffer.write(bytes(row))
        buffer.write(b"\n")
    return buffer.getvalue()

def path_to_qr_bmp(path):
    url = path_to_url(path)
    buffer = io.BytesIO()
    img = qrcode.make(url, border=1)
    img.save(buffer, format="BMP")
    return buffer.getvalue()

def path_to_qr_png(path):
    url = path_to_url(path)
    buffer = io.BytesIO()
    img = qrcode.make(url, border=1)
    img.save(buffer, format="PNG")
    return buffer.getvalue()

def get_path_to_qr_converter(media_type):
    match media_type:
        case "raw":
            return path_to_qr_raw
        case "bmp":
            return path_to_qr_bmp
        case "png":
            return path_to_qr_png
        case _:
            raise ValueError("Unsupported media type")
