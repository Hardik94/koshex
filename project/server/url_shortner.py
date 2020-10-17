import string, random
import base64

def make_shorten(size=6, chars=string.ascii_uppercase + string.digits + string.ascii_lowercase):
    return ''.join(random.choice(chars) for _ in range(size))

def custom_shorten(key=''):
    if len(key) < 7:
        key = make_shorten(size=50)
    message_bytes = key.encode('ascii')
    base64_bytes = base64.b64encode(message_bytes)
    base64_message = base64_bytes.decode('ascii')
    return make_shorten(size=6, chars=base64_message)
