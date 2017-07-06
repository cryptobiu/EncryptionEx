from Crypto.Cipher import AES
from Crypto import Random
# For base conversions:
import codecs

# Block Size (In bytes):
BS = 16

# padding function for AES mode (PKCS5):
pad = lambda s: s + b"".join([bytes(chr(BS - len(s) % BS), 'utf8')]*(BS - len(s) % BS))


# unpadding function:
def unpad(s):
    pad = int(s[len(s) - 1])
    if pad <= 0 or pad > len(s):
        return False
    for i in s[len(s) - pad:]:
        if i != pad:
            return False
    return s[:len(s) - pad]


# AES cipher class.


class AESCipher:
    def __init__(self):
        """
        Requires hex encoded param as a key
        """
        with open('key', 'rb') as key_file:
            self.key = self.iv = key_file.read()

    def encrypt(self, raw):
        """
        Receives input as bytes
        Returns hex encoded encrypted value!
        """
        raw = pad(raw)
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        with open('Ciphertext', 'wb+') as cipher_file:
            cipher_file.write(cipher.encrypt(raw))
        return codecs.encode((cipher.encrypt(raw)), 'hex_codec')

    def decrypt_check(self, enc):
        """
        Requires hex encoded param to decrypt
        """
        enc = codecs.decode(enc, 'hex_codec')
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        plaintext = cipher.decrypt(enc)
        check = type(unpad(plaintext))
        if check == bytes:
            return 1
        else:
            return 0


aes = AESCipher()
with open('Plaintext', 'rb') as data_file:
    msg = data_file.read()

cipher = aes.encrypt(msg)
d1 = aes.decrypt_check(cipher)
print(d1)
tamper_cipher = cipher[0:-1] + b'c'
d2 = aes.decrypt_check(tamper_cipher)
print(d2)
