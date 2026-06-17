import io

import qrcode


def get_path_to_qr_converter(filename, media_type, qr_scale, qr_border):
    offset = -(len(filename) + 1)

    def path_to_url(path):
        return path[1:offset]

    def path_to_qr_raw(path):
        url = path_to_url(path)
        buffer = io.BytesIO()
        img = qrcode.make(url, box_size=qr_scale, border=qr_border)
        for row in img.modules:
            buffer.write(bytes(row))
            buffer.write(b"\n")
        return buffer.getvalue()

    def path_to_qr_bmp(path):
        url = path_to_url(path)
        buffer = io.BytesIO()
        img = qrcode.make(url, box_size=qr_scale, border=qr_border)
        img.save(buffer, format="BMP")
        return buffer.getvalue()

    def path_to_qr_png(path):
        url = path_to_url(path)
        buffer = io.BytesIO()
        img = qrcode.make(url, box_size=qr_scale, border=qr_border)
        img.save(buffer, format="PNG")
        return buffer.getvalue()

    match media_type:
        case "raw":
            return path_to_qr_raw
        case "bmp":
            return path_to_qr_bmp
        case "png":
            return path_to_qr_png
        case _:
            raise ValueError("unsupported media type")
