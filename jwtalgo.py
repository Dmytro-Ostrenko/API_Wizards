import secrets

# Генеруємо 32 байти (256 біт) як випадковий секретний ключ
secret_key = secrets.token_hex(32)
print(secret_key)