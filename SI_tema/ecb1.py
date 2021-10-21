def _xor(block1, block2):
    a_list = [chr(ord(a) ^ ord(b)) for a, b in zip(block1, block2)]
    rezult = "".join(a_list)
    return rezult


class ECB:
    def __init__(self, key):
        self.key = key
        self.block_size = 16

    def encrypt(self, plaintext):

        split_text = [plaintext[i:i + self.block_size] for i in range(0, len(plaintext), self.block_size)]
        ciphertext = [plaintext[i:i + self.block_size] for i in range(0, len(plaintext), self.block_size)]
        n = 0
        for block in split_text:
            # block = block.encode('utf-8')
            ciphertext[n] = _xor(block, self.key)
            n += 1
        return ciphertext

    def decrypt(self, ciphertext):
            return _xor(ciphertext, self.key)
