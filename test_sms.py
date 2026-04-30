def convert_uid_to_id(uid_hex):
    byte2 = uid_hex[2:4]
    byte3 = uid_hex[4:6]
    byte4 = uid_hex[6:8]
    combined_hex = byte4 + byte3 + byte2
    print("Combined hex:", combined_hex)
    return int(combined_hex, 16)

print(convert_uid_to_id("3D69E9F6"))  # → 21012
