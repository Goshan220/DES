import sys


class LSB:
    def __init__(self):
        self.__mark = '$equr3'
        self.__image = None
        self.__text = ""

    def __to_bin(self, s):
        return str(s) if s <= 1 else self.__to_bin(s >> 1) + str(s & 1)

    def __byte_to_bin(self, bytes):
        for b in bytes:
            yield self.__to_bin(ord(b)).zfill(8)

    def __decrypt_char(self, container):
        str_bits = ''
        for cbits in self.__byte_to_bin(container):
            str_bits += cbits[-1]
            if len(str_bits) == 8:
                yield chr(int(str_bits, 2))
                str_bits = ''

    def __encrypt(self):
        __text_file = open(self.__text, 'rb')
        self.__text = __text_file.read()
        print(self.__text)
        secret_info = self.__mark + self.__text + self.__mark
        __text_file.close()

        __image_file = open(self.__image, 'rb+')
        __image_file.seek(55)
        __container = __image_file.read()

        __need = 8 * len(secret_info) - len(__container)
        if __need > 0:
            print ("Image file so small for text")
            raise -2

        __image_bin = self.__byte_to_bin(__container)
        __encrypted = []
        for text_bin in self.__byte_to_bin(secret_info):
            for bit in text_bin:
                bits = __image_bin.next()
                bits = bits[:-1] + bit
                # bits = bit + bits[1:]
                b = chr(int(bits, 2))
                __encrypted.append(b)
        __image_file.seek(55)
        __image_file.write(''.join(__encrypted))
        __image_file.close()

    def __decrypt(self):
        __image_file = open(self.__image, 'rb')
        __image_file.seek(55)
        container = __image_file.read()
        __image_file.close()

        __decrypted = []
        for b in self.__decrypt_char(container):
            __decrypted.append(b)
            if (len(self.__mark) == len(__decrypted) and
                    self.__mark != ''.join(__decrypted)):
                print "The image does not contain confidential file."
                raise -3

        if len(__decrypted) > len(self.__mark):
            __decrypted = ''.join(__decrypted).split(self.__mark)
            src_data = __decrypted[1]
            src = open('decrypted.txt', 'wb')
            src.write(src_data)
            src.close()

    def run(self, args):
        self.__image = args[1]
        self.__text = args[2]
        self.__encrypt()
        self.__decrypt()


def main(argv=None):
    lsb = LSB()
    if argv is None:
        argv = sys.argv
    lsb.run(argv)


if __name__ == '__main__':
    sys.exit(main())
