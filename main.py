# s_p_box.py

# Реалізація алгоритмів S-блоку та P-блоку з прямим та зворотним перетворенням
# Автор: [Юрiй]
# Дата: [29.1.2024]

# Таблиця замін для S-блоку (16 елементів для 4-бітових тетрад)
S_BOX = [
    0xE, 0x4, 0xD, 0x1,
    0x2, 0xF, 0xB, 0x8,
    0x3, 0xA, 0x6, 0xC,
    0x5, 0x9, 0x0, 0x7
]

def s_box_encrypt(input_byte):
    """
    Пряме перетворення S-блоку.
    Приймає 8-бітове число, розбиває на дві тетради,
    замінює кожну за таблицею S_BOX і об'єднує результат.
    """
    # Розбиваємо на дві тетради по 4 біти
    high_nibble = (input_byte & 0xF0) >> 4  # Старша тетрада
    low_nibble = input_byte & 0x0F          # Молодша тетрада

    # Заміна за таблицею S_BOX
    high_nibble_sub = S_BOX[high_nibble]
    low_nibble_sub = S_BOX[low_nibble]

    # Об'єднання результату
    output_byte = (high_nibble_sub << 4) | low_nibble_sub
    return output_byte

def generate_inverse_s_box(s_box):
    """
    Генерує зворотну таблицю замін для S-блоку.
    """
    inverse_s_box = [0] * 16
    for i in range(16):
        inverse_s_box[s_box[i]] = i
    return inverse_s_box

# Зворотна таблиця замін для S-блоку
INVERSE_S_BOX = generate_inverse_s_box(S_BOX)

def s_box_decrypt(input_byte):
    """
    Зворотне перетворення S-блоку.
    Використовує зворотну таблицю замін INVERSE_S_BOX.
    """
    # Розбиваємо на дві тетради по 4 біти
    high_nibble = (input_byte & 0xF0) >> 4  # Старша тетрада
    low_nibble = input_byte & 0x0F          # Молодша тетрада

    # Зворотна заміна за таблицею INVERSE_S_BOX
    high_nibble_sub = INVERSE_S_BOX[high_nibble]
    low_nibble_sub = INVERSE_S_BOX[low_nibble]

    # Об'єднання результату
    output_byte = (high_nibble_sub << 4) | low_nibble_sub
    return output_byte

# Таблиця перестановки для P-блоку (8 елементів для 8 бітів)
# Індекси від 0 до 7, де кожне значення вказує на позицію біта у вхідному байті
P_BOX = [1, 5, 2, 0, 3, 7, 4, 6]

def permute(input_byte, permutation):
    """
    Виконує перестановку бітів згідно з таблицею перестановки.
    """
    output_byte = 0
    for i in range(8):
        # Витягуємо біт з вхідної позиції
        bit = (input_byte >> permutation[i]) & 0x01
        # Встановлюємо біт у вихідну позицію
        output_byte |= bit << i
    return output_byte

def p_box_encrypt(input_byte):
    """
    Пряме перетворення P-блоку.
    """
    return permute(input_byte, P_BOX)

def generate_inverse_p_box(permutation):
    """
    Генерує зворотну таблицю перестановки для P-блоку.
    """
    inverse_permutation = [0] * len(permutation)
    for i, p in enumerate(permutation):
        inverse_permutation[p] = i
    return inverse_permutation

# Зворотна таблиця перестановки для P-блоку
INVERSE_P_BOX = generate_inverse_p_box(P_BOX)

def p_box_decrypt(input_byte):
    """
    Зворотне перетворення P-блоку.
    """
    return permute(input_byte, INVERSE_P_BOX)

# Тести для перевірки коректності реалізації
def test_s_box():
    """
    Тестує пряме та зворотне перетворення S-блоку.
    """
    for input_byte in range(256):
        encrypted = s_box_encrypt(input_byte)
        decrypted = s_box_decrypt(encrypted)
        assert input_byte == decrypted, f"S-Box failed at input {input_byte}"
    print("S-Box tests passed.")

def test_p_box():
    """
    Тестує пряме та зворотне перетворення P-блоку.
    """
    for input_byte in range(256):
        encrypted = p_box_encrypt(input_byte)
        decrypted = p_box_decrypt(encrypted)
        assert input_byte == decrypted, f"P-Box failed at input {input_byte}"
    print("P-Box tests passed.")

def main():
    # Демонстрація роботи алгоритмів на прикладі
    input_byte = 0b10110011  # 179 у десятковій системі
    print(f"Вхідний байт: {input_byte:08b}")

    # S-блок
    s_encrypted = s_box_encrypt(input_byte)
    print(f"S-Box зашифровано: {s_encrypted:08b}")
    s_decrypted = s_box_decrypt(s_encrypted)
    print(f"S-Box розшифровано: {s_decrypted:08b}")

    # P-блок
    p_encrypted = p_box_encrypt(input_byte)
    print(f"P-Box зашифровано: {p_encrypted:08b}")
    p_decrypted = p_box_decrypt(p_encrypted)
    print(f"P-Box розшифровано: {p_decrypted:08b}")

    # Тести
    test_s_box()
    test_p_box()

if __name__ == "__main__":
    main()
