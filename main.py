import random
class EKeys:
    def __init__(self, PrivKey):
        self.PrivKey = PrivKey
        self.PubKey = [None]*len(self.PrivKey)
        self.p = 0
        self.r = 0
    def DefPR(self):
        sum = 0
        for i in self.PrivKey:
            sum += i
        self.p = random.randint(sum, sum*3)
        self.r = random.randint(sum, self.p - 1)
        cDiv = self.r
        while cDiv != 1:
            for i in range(self.r):
                if self.p % (self.r - i) == 0 and self.r % (self.r - i) == 0:
                    cDiv = self.r - i
                    break
            if cDiv != 1:
                self.r = random.randint(sum, self.p - 1)
                cDiv = self.r
    def MPubK(self):
        self.DefPR()
        for i in range(len(self.PrivKey)):
            self.PubKey[i] = (self.r*self.PrivKey[i]) % self.p
class ECnDC:
    def __init__(self, PrivKeys):
        self.key = EKeys(PrivKeys)
        self.key.MPubK()
        self.r2 = 0
    def encode(self, char):
        binary = bin(ord(char))[2:]
        ecVal = 0
        if len(binary) < 7:
            for i in range(7-len(binary)):
                binary = "0"+binary
        for i in range(len(binary)):
            ecVal += self.key.PubKey[i]*int(binary[i])
        return ecVal
    def decode(self, value):
        self.r2 = self.modInverse(self.key.r, self.key.p)
        sum = (value*self.r2)%self.key.p
        binary = ""
        for i in range(1, len(self.key.PrivKey)+1):
            if self.key.PrivKey[len(self.key.PrivKey)-i] <= sum:
                sum -= self.key.PrivKey[len(self.key.PrivKey)-i]
                binary = "1"+binary
            else:
                binary = "0"+binary
        return binary
    def modInverse(self, a, m):
        for x in range(1, m):
            if (((a % m) * (x % m)) % m == 1):
                return x
        return -1
    def encodeStr(self, str):
        array = []
        for i in str:
            array.append(self.encode(i))
        return array
    def decodeArray(self, array):
        string = ""
        for i in array:
            string += self.decode(i)+" "
        return string
pKey = [2, 5, 18, 26, 82, 135, 280]
hello = ECnDC(pKey)
print(hello.encode("A"))
print(hello.decode(hello.encode("A")))
print(hello.key.PubKey)
string = "And they sang a new song, saying: 'You are worthy to take the scroll and to open its seals, because you were slain, and with your blood you purchased for God persons from every tribe and language and people and nation."
tranStr = hello.encodeStr(string)
print(tranStr)
binary = hello.decodeArray(tranStr)
print(binary)