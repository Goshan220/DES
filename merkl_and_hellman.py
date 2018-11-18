
class MerklHellman:
    def __init__(self):
        # self.closed_key = [2, 3, 6, 13, 27, 52]
        # self.m = 105
        # self.n = 31
        self.closed_key = [2, 4, 7, 17, 33, 70]
        self.m = 120
        self.n = 37
        self.open_key = list()
        self.message = []

    def __evklid(self, a, b):
        if a == 0:
            return (b, 0, 1)
        else:
            g, x, y = self.__evklid(b % a, a)
            return (g, y - (b // a) * x, x)

    def __reverse(self, b, n):
        g, x, _ = self.__evklid(b, n)
        if g == 1:
            return x % n

    def __string_to_bit(self, text):  # Convert a string into a list of bits
        array = list()
        for char in text:
            binval = self.__binvalue(char, 8)  # Get the char value on one byte
            array.extend([int(x) for x in list(binval)])  # Add the bits to the final list
        return array

    def __n_split(self, s, n):  # Split a list into sublists of size "n"
        return [s[k:k + n] for k in range(0, len(s), n)]

    def __bit_to_string(self, array):  # Recreate the string from the bit array
        res = ''.join([chr(int(y, 2)) for y in [''.join([str(x) for x in bytes]) for bytes in self.__n_split(array, 8)]])
        return res

    def __binvalue(self, val, bitsize):  # Return the binary value as a string of the given size
        binval = bin(val)[2:] if isinstance(val, int) else bin(ord(val))[2:]
        if len(binval) > bitsize:
            raise ("binary value larger than the expected size")
        while len(binval) < bitsize:
            binval = "0" + binval  # Add as many 0 as needed to get the wanted size
        return binval

    def __create_norm_p(self):
        for i in self.closed_key:
            self.open_key.append(i * self.n % self.m)

    def encrypt(self, text):
        self.__create_norm_p()
        len_norm = len(self.open_key)
        binary = self.__string_to_bit(text)
        binary = self.__n_split(binary, len_norm)
        len_bin = len(binary)
        for i in range(len_bin):
            temp_block = binary[i]
            temp = 0
            res = 0
            for j in temp_block:
                if j == 1:
                    res = res + self.open_key[temp]
                temp += 1
            self.message.append(res)
        return self.message

    def decrypt(self):
        print("________decrypt__________")
        # print(self.message)
        n_1 = self.__reverse(self.n, self.m)
        decrypted = ""
        for i in self.message:
            # print("+++++++ new number ++++++++")
            temp = i*n_1 % self.m
            # print(temp)
            bag = temp
            result = ""
            reverse_closed_key = self.closed_key[::-1]
            for i in reverse_closed_key:
                # print("  i = ", i)
                # print("bag = ", bag)
                if i <= bag:
                    result += "1"
                    bag = bag - i
                else:
                    result += "0"
            result = result[::-1]
            decrypted = decrypted + result
        return self.__bit_to_string(decrypted)


if __name__ == '__main__':
    d = MerklHellman()
    t = d.encrypt("Hello world!")
    print(t)
    x = d.decrypt()
    print(x)