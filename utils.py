import pyotp
from flask_bcrypt import Bcrypt
from itsdangerous import URLSafeTimedSerializer

bcrypt = Bcrypt()
serializer = URLSafeTimedSerializer('your_secret_key')

# 密码处理
def hash_password(password):
    return bcrypt.generate_password_hash(password).decode('utf-8')

def check_password(password, hashed_password):
    return bcrypt.check_password_hash(hashed_password, password)

# TOTP
def generate_totp_secret():
    return pyotp.random_base32()

def verify_totp(secret, token):
    totp = pyotp.TOTP(secret)
    return totp.verify(token)

# 重置令牌
def generate_reset_token(email):
    return serializer.dumps(email, salt='reset-password')

def verify_reset_token(token, max_age=3600):
    try:
        return serializer.loads(token, salt='reset-password', max_age=max_age)
    except Exception:
        return None
