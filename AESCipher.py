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
            cipher_file.write(self.iv + cipher.encrypt(raw))
        return codecs.encode((self.iv + cipher.encrypt(raw)), 'hex_codec')

    def decrypt_check(self, enc):
        """
        Requires hex encoded param to decrypt
        """
        enc = codecs.decode(enc, 'hex_codec')
        iv = enc[:16]
        enc = enc[16:]
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        plaintext = cipher.decrypt(enc)
        check = type(unpad(plaintext))
        if check == bytes:
            return 0
        else:
            return 1


aes = AESCipher()
with open('Plaintext', 'rb') as data_file:
    msg = data_file.read()

d = aes.decrypt_check(aes.encrypt(msg))
print(d)
