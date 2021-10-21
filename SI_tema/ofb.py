def _xor(block1, block2):
    a_list = [chr(ord(a) ^ ord(b)) for a, b in zip(block1, block2)]
    rezult = "".join(a_list)
    return rezult

def rotate_to_left(left, right, j):
    # Slice string in two parts for left and right
    Lfirst = left[j: len(left)]
    Lsecond = right[0: j]
    #Rfirst = input[0: len(input) - j]
    #Rsecond = input[len(input) - d:]
    return  Lfirst + Lsecond
    #print("Right Rotation : ", (Rsecond + Rfirst))
    # Driver program
#d=2
#cuvant = "pythonprogram"
#test = "madihdwhe"
#cuvant = rotate_to_left(cuvant,test,d)
#print(cuvant)

class OFB:
    def __init__(self, vi, key, j):
        self.key = key
        self.j = j
        self.vi = vi
        self.VI = vi
        self.vi1 = ''



    def encrypt(self, plaintext):
        split_text = [plaintext[i:i + self.j] for i in range(0, len(plaintext), self.j)]
        ciphertext = [plaintext[i:i + self.j] for i in range(0, len(plaintext), self.j)]
        n = 0
        for block in split_text:
            self.vi1 = _xor(self.vi, self.key)
            ciphertext[n] = _xor(block, self.vi1)
            self.vi = rotate_to_left(self.vi, self.vi1, self.j)
            n += 1
        return ciphertext

    def decrypt(self, ciphertext):
        plaintext = [''] * 1000
        n = 0
        self.vi = self.VI
        print("vi: ", self.vi)
        self.vi1 = ''
        for block in ciphertext:
            self.vi1 = _xor(self.vi, self.key)
            block = str(block)
            block = block[2:len(block)-1]
            print(block)
            plaintext[n] = _xor(str(block), self.vi1)
            self.vi = rotate_to_left(self.vi, self.vi1, self.j)
            n += 1
        return plaintext


#iv = '0102030405060708AABBCCDDEEFF'
#K1 = 'Olmv5OmjCqwhrMMFA_fa-PhUPLBVBnxAfxJiZrFmP3k='
#ofb = OFB(iv, K1, 10)
#cipher = ofb.encrypt("ana are mere jsda djasdg hjsdadvhje hjdiuaaebddeiagdagdyv dyegdad")
#print(cipher)
#print(ofb.decrypt(cipher))

