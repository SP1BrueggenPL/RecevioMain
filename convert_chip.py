def convert_uid_to_id(uid_hex):
    # Wyciągnij odpowiednie bajty ręcznie (jako stringi, nie binarnie!)
    byte2 = uid_hex[2:4]
    byte3 = uid_hex[4:6]
    byte4 = uid_hex[6:8]

    print(f"DEBUG → byte2: {byte2}, byte3: {byte3}, byte4: {byte4}")

    # Składamy w kolejności little endian
    combined_hex = byte4 + byte3 + byte2
    print(f"DEBUG → combined_hex: {combined_hex}")

    result = int(combined_hex, 16)
    print(f"DEBUG → result: {result}")
    return result


# TESTY
print("Result 1:", convert_uid_to_id("3D69E9F6"))  # ➜ 21012
print("Result 2:", convert_uid_to_id("3CC8C41F"))  # ➜ 21194
print("Result 3:", convert_uid_to_id("3C3FB023"))  # ➜ 21197
print("Result 4:", convert_uid_to_id("3CEDA123"))  # ➜ 21198)
