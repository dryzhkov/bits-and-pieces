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
        return bitarray(self.bits, endian='little').tobytes()

    def print(self):
        print(self.bits)
        print(len(self.bits))

    def _int_to_bit(self, integer, bit_count):
        bits = []
        while bit_count > 0:
            bit_count -= 1
            bits.append(integer & 0x1)
            integer = integer >> 1

        return bits


class Unpacker:

    def __init__(self, byte_data):
        self.bits = bitarray(endian='little')
        self.bits.frombytes(byte_data)

    def int32(self):
        return self.bit_to_int(32)

    def int8(self):
        return self.bit_to_int(8)

    def bit_to_int(self, bit_count):
        res = 0
        bits = self.pop_bits(bit_count)
        bits.reverse()

        for bit in bits:
            res = res << 1
            res = res | bit

        return res

    def pop_bits(self, count):
        bits = []
        while count > 0:
            bits.append(self.bits.pop(0))
            count -= 1

        return bits

    def seek(self, count):
        return [x for x in self.bits[0: count]]

    def print(self):
        print(self.bits)
        print(len(self.bits))
