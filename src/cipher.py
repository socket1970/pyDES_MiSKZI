#         @@@     @@@     @@
#          &@.      @@     @@
#          @@      @@      (@#
#        @@      @@        @@
#       @@      @@       @@
#       @@      @@      @@
# @@     @@@     @@     @@     @@@
#    @@@@@@@*        ,&@@@@@@@*
#   @                         @@     @@
#   @@                       ,@#    @@
#   @@@                     @@@  &@#
#     @@@&                @@@
#        @@@@@@@@@@@@@@@@@


import secrets

from src.box import *
from src.textConverter import TextConverter


class Des:
    @staticmethod
    def key() \
            -> str:
        """
        Generating a 64-bit key with a parity bit

            ---- Генерация 64-битного ключа с битом четности
        :return str:
        """
        key = ""

        for _ in range(8):
            pieceKey = format(secrets.randbits(7), "b").zfill(7)

            match pieceKey.count("1") % 2:
                case 0:
                    pieceKey += "1"
                case _:
                    pieceKey += "0"
            key += pieceKey

        return key

    def encryption(self, message: str, key: str) \
            -> list[str]:
        """
        String encryption, cp1251 encoding, returns an array, each element of which is converted to binary format and
                                                                                                            encrypted.
            ---- Шифрование строки, кодировка cp1251, возвращает массив, каждый элемент которого переведем в
                                                                                        двоичный формат и зашифрован.
        :param str message:
        :param str key:
        :return list[str]:
        """
        t = TextConverter()

        message = t.str2bin(message)
        message = self.__initial_per(message)
        key = self.__round_key(key)

        enc = []

        for i in message:
            L, R = i[:32],  i[32:]

            L, R = self.__Feistel_cipher(L, R, key)

            enc.append(self.__final_per(L + R))

        return enc

    def decryption(self, message: list[str], key: str) \
            -> str:
        """
        Decryption, the input is an array with a binary block aligned to 64 bits, the output is a string with
                                                                                                        decryption.
            ---- Дешифрование, на вход подается массив с двоичным, выравненным по 64 бита блок, на выходе строка с
                                                                                                        расшифровкой.
        :param list[str] message:
        :param str key:
        :return str:
        """
        t = TextConverter()

        dec = []

        message = self.__initial_per(message)
        key = self.__round_key(key)[::-1]

        for i in message:
            L, R = i[:32], i[32:]
            L, R = self.__Feistel_cipher(L, R, key)

            dec.append(self.__final_per(L + R))

        return t.bin2str(dec)

    def __Feistel_cipher(self, L: str, R: str, key: list[str]) \
            -> tuple[str, str]:
        """
        Feistel Network. The first two blocks are the input - left and right, the final blocks are the output
                                                                                                    after 16 iterations.
            ---- Сеть Фейстеля. На вход первые два блока - левый и правый, на выход конечные блоки после 16 итераций.
        :param str L:
        :param str R:
        :param list[str] key:
        :return str:
        """
        for i in range(16):

            new_L = self.__e_box(R)

            new_L = self.__XOR(new_L, key[i], 48)
            new_L = self.__s_box(new_L)
            new_L = self.__p_box(new_L)

            L, R = R, self.__XOR(new_L, L, 32)

        return R, L

    def __round_key(self, key: str) \
            -> list[str]:
        """
        Generation of round keys. The input is a string with a 64-bit key. The output is an array with 48bit round keys.
            ---- Генерация раундовых ключей. На вход подается строка с 64 битным ключом. На выходе -
                                                                                массив с 48 битными раудновыми ключами.
        :param key:
        :return list[str]:
        """
        all_key = []

        C = self.__key_initial(key, "C")
        D = self.__key_initial(key, "D")

        for i in range(16):
            C = self.__key_shift(C, i)
            D = self.__key_shift(D, i)

            r_key = C + D
            r_key = self.__key_final(r_key)

            all_key.append(r_key)

        return all_key

    @staticmethod
    def __key_shift(key: str, r: int) \
            -> str:
        """
        Key shift.
            ---- Сдвиг ключа.
        :param str key:
        :param int r:
        :return str:
        """
        match r:
            case 0 | 1 | 8 | 15: r = 1
            case _: r = 2

        return key[r:] + key[:r]

    def __XOR(self, x: str, y: str, leveling: int) \
            -> str:
        """
        Addition modulo 2 and leveling the result.
            --- Сложение по модулю 2 и выравнивание результата.
        :param str x:
        :param str y:
        :param int leveling:
        :return str:
        """
        x = self.__dec(x)
        y = self.__dec(y)

        return self.__bin(x ^ y, leveling)

    @staticmethod
    def __key_initial(key: str, side: str) \
            -> str:
        """
        Initial permutation table for the key.
            ---- Таблица первичной перестановки для ключа.
        :param str key:
        :param int side:
        :return str:
        """
        match side:
            case "C" | "c":
                side = 0
            case "D" | "d":
                side = 1

        return "".join([key[j - 1] for j in permutation_key_initial[side]])

    @staticmethod
    def __key_final(key: str) \
            -> str:
        """
        Final key permutation table.
            ---- Таблица конечной перестановки ключа.
        :param str key:
        :return str :
        """
        return "".join([key[j - 1] for j in permutation_key_final])

    @staticmethod
    def __e_box(L: str) \
            -> str:
        """
        Extension E block.
            ---- Расширение E блоком.
        :param str L:
        :return str:
        """
        return "".join([L[j - 1] for j in expansion_func_E])

    def __s_box(self, L: str) \
            -> str:
        """
        S lookup table.
            ---- S таблица подстановки.
        :param str L:
        :return str:
        """
        L = [L[j:j+6] for j in range(0, 48, 6)]

        L_new = ""

        for i in range(8):
            x = self.__dec(L[i][0] + L[i][-1])
            y = self.__dec(L[i][1:5])

            L_new += self.__bin(s_blocks[i][x][y], 4)

        return L_new

    @staticmethod
    def __p_box(L: str) \
            -> str:
        """
        P permutation table.
            ---- Таблица перестановки P.
        :param str L:
        :return str:
        """
        return "".join([L[j - 1] for j in permutation_P])

    @staticmethod
    def __initial_per(mess: list[str]) \
            -> list[str]:
        """
        Primary rearrangement.
            ---- Первичная перестановка.
        :param mess:
        :return:
        """
        new_b = []
        for i in mess:
            temp_item = "".join([i[j - 1] for j in initial_permutation_table])
            new_b.append(temp_item)

        return new_b

    @staticmethod
    def __final_per(mes: str) \
            -> str:
        """
        Final permutation.
            ---- Конечная перестановка.
        :param str mes:
        :return str:
        """
        return "".join([mes[j - 1] for j in final_permutation_table])

    @staticmethod
    def __bin(number: int, leveling: int) \
            -> str:
        """
        Decimal to binary conversion and block alignment.
            ---- Перевод из десятичной в двоичную и выравнивание блока.
        :param int number:
        :param int leveling:
        :return str:
        """
        return format(number, "b").zfill(leveling)

    @staticmethod
    def __dec(number: str) \
            -> int:
        """
        Conversion from binary to decimal number system.
            --- Перевод из двоичной в десятичную систему счисления.
        :param str number:
        :return int:
        """
        return int(number, 2)
