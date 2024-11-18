import secrets

# Generate a random secret key
secret_key = secrets.token_hex(16)
print(f'Your new secret key: {secret_key}')

# Your new secret key: a6f526bd162387bc46a607363cd45483