from Crypto.Cipher import AES
from base64 import b64encode, b64decode

from django.conf import settings
import hashlib
key = "0e2E4i6ka6ridR+arMqWeNQgRySPZMtO"

def gen_key(key):
    return key


def decrypt(data):
    raw = b64decode(data)
    obj = AES.new(gen_key(key))
    real = obj.decrypt(raw)
    return real

def encrypt(real):
    if len(real)%16 != 0:
        blank = ' '* (16-len(real)%16)
        real += blank

    print "real,len" ,len(real)
    obj = AES.new(gen_key(key))
    raw = obj.encrypt(real)
    data = b64encode(raw)
    return data 


if __name__ == "__main__":
    d = encrypt("rick")
    print d
    print decrypt(d)


