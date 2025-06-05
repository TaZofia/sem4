import binascii

ESC_SEQ = '01111110'      # znacznik końca/początku ramki
ESC_NUM = 5               # liczba kolejnych jedynek, po których nastąpi wstawienie 0


def crc32_bits(data_bits: str) -> str:
    # Konwersja binarnego stringa na bajty
    byte_data = int(data_bits, 2).to_bytes((len(data_bits) + 7) // 8, byteorder='big')
    crc = binascii.crc32(byte_data) & 0xffffffff
    return format(crc, '032b')  # 32-bitowa binarna reprezentacja


def encode(data: str) -> str:
    # Dodanie CRC
    data += crc32_bits(data)
    output = ESC_SEQ
    one_counter = 0

    for c in data:
        output += c
        if c == '1':
            one_counter += 1
            if one_counter == ESC_NUM:
                output += '0'  # bit stuffing
                one_counter = 0
        else:
            one_counter = 0

    output += ESC_SEQ
    return output


def decode(data: str) -> str:
    if not (data.startswith(ESC_SEQ) and data.endswith(ESC_SEQ)):
        raise ValueError('Błąd: brak znaczników ramki (ESC_SEQ)')

    data = data[len(ESC_SEQ):-len(ESC_SEQ)]  # Usuń znaczniki
    output = ''
    one_counter = 0
    skip_next = False

    for c in data:
        if skip_next:
            skip_next = False
            continue

        output += c
        if c == '1':
            one_counter += 1
            if one_counter == ESC_NUM:
                skip_next = True  # usuń wstawione 0
                one_counter = 0
        else:
            one_counter = 0

    payload = output[:-32]
    received_crc = output[-32:]
    expected_crc = crc32_bits(payload)

    if received_crc != expected_crc:
        raise ValueError('Błąd: CRC się nie zgadza')

    return payload


def main():
    # Odczytaj dane z pliku Z
    with open('Z.txt', 'r') as f:
        original_data = f.read().strip()

    print("Odczytano dane z Z.txt")


    encoded_data = encode(original_data)
    # Zakodowane dane zapisz do W
    with open('W.txt', 'w') as f:
        f.write(encoded_data)

    print("Zapisano zakodowane dane do W.txt")

    # Dekoduj z W i sprawdź poprawność CRC - uzyskaj z powrotem Z
    with open('W.txt', 'r') as f:
        coded_data = f.read().strip()

    decoded_data = decode(coded_data)

    with open('Z_recovered.txt', 'w') as f:
        f.write(decoded_data)

    print("Zapisano zdekodowane dane do Z_recovered.txt")


if __name__ == '__main__':
    main()
