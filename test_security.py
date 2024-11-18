# from werkzeug.security import generate_password_hash, check_password_hash

# password = 'mysecretpassword'
# # hashed_password = generate_password_hash(password, method='sha256')
# hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
# print(f'Hashed password: {hashed_password}')

# is_valid = check_password_hash(hashed_password, password)
# print(f'Password is valid: {is_valid}')

from werkzeug.security import generate_password_hash, check_password_hash

test_password = 'testpassword'
hashed = generate_password_hash(test_password, method='pbkdf2:sha256')
print(f'Hashed Password: {hashed}')
print(f'Check Password: {check_password_hash(hashed, test_password)}')
