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


class TextConverter:
    @staticmethod
    def __bin64list(b: list[str]) \
            -> list[str]:
        """
        Block alignment to 64 bits.
            ---- Takes as input a list, each element of which is an aligned block of 8-bit letters.
            ---- Returns a list where each element is an aligned block of 64 bits

        Выравнивание блока по 64 бит.
            ---- Принимает на вход список, каждый элемент которого представляет собой выровненный блок буквы по 8 бит.
            ---- Возвращает список, каждый элемент которого представляет собой выравненный блок по 64 бита.

        :param list[str] b:
        :return list[str]:
        """
        new_b = []

        for i in range(0, len(b), 8):
            temp_item = "".join(b[i:i + 8])

            if len(temp_item) < 64:
                temp_item += ("0" * (64 - len(temp_item)))

            new_b.append(temp_item)

        return new_b

    @staticmethod
    def __list64bit(b: list[str]) \
            -> list[str]:
        """
        Breaks a block (64 bits) into characters (8 bits).
            ---- Takes as input a list, each element of which is an aligned block of 64 bits.
            ---- Returns a list where each element is a 8-bit aligned block of letters.

        Разбивает блок(64 бита) на символы(8 бит).
            ---- Принимает на вход список, каждый элемент которого представляет собой выравненный блок по 64 бита.
            ---- Возвращает список, каждый элемент которого представляет собой выровненный блок буквы по 8 бит.

        :param list[str] b:
        :return list[str]:
        """
        new_b = []
        for i in b:
            temp_item = [i[j:j + 8] for j in range(0, len(i), 8)]
            new_b += temp_item

        return new_b

    def str2bin(self, t: str) \
            -> list[str]:
        """
        Converting a string to a binary list[str] in cp1251 encoding
            ---- Converts a string to an array, each element of which is a 8-bit aligned cp1251 binary number.

            ---- Конвертирует строку в массив, каждый элемент которого представляет собой двоичное число,
                        кодировки cp1251, выровненное по 8 битам.

        :param str t: string to convert
        :return list(str):
        """
        b = list(map(lambda x: format(x, "b").zfill(8),
                     bytes(t, "cp1251")))
        b = self.__bin64list(b)
        return b

    def bin2str(self, b: list[str]) \
            -> str:
        """
        Converting a binary list[str] to a string in cp1251 encoding

            ---- Converts an array, each element of which is a 8-bit aligned cp1251 binary number, into a string
                        and trims the null character.

            ---- Конвертирует массив, каждый элемент которого представляет собой двоичное число,
                        кодировки cp1251, выровненное по 8 битам, в строку и обрезает нулевой символ.

        :param list[str] b: list to convert
        :return str:
        """
        b = self.__list64bit(b)

        t = "".join(map(lambda x:
                        self.__toBytes(x) if x != "00000000" else "",
                        b))

        return t

    @staticmethod
    def __toBytes(x):
        return int(x, 2).to_bytes().decode(encoding="cp1251")
