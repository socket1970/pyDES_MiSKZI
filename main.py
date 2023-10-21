from src.cipher import Des


if __name__ == "__main__":
    c = Des()
    # пример работы
    key = c.key()  # Генерация ключа
    a = c.encryption("Привет Мир", key)  # Шифрование
    b = c.decryption(a, key)  # Дешифрование
    print(b)
