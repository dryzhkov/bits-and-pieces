from bitarray import bitarray

class Packer:

    def __init__(self):
        self.bits = []


    def int8(self, integer):
        self.bits += self._int_to_bit(integer, 8)


    def int32(self, integer):
        self.bits += self._int_to_bit(integer, 32)


    def addBits(self, bits):
        self.bits += bits


    def pack(self):
        return bitarray(self.bits).tobytes()


    def print(self):
        print(self.bits)
        print(len(self.bits))

    def _int_to_bit(self, integer, bit_count):
        bits = []
        count = 0
        while count < bit_count:
            count += 1
            bits.append(integer & 0x1)
            integer = integer >> 1

        return bits