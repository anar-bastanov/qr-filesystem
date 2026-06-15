import io

import qrcode


def path_to_url(path):
    return path  # For now

def url_to_qr(url):
    buffer = io.BytesIO()
    # img = qrcode.make(url)
    # img.save(buffer, format="PNG")
    # buffer.seek(0)
    # raw_bytes = buffer.getvalue()
    buffer.write(url.encode())
    raw_bytes = buffer.getvalue()
    return raw_bytes

def path_to_qr(path):
    url = path_to_url(path)
    qr = url_to_qr(url)
    return qr
