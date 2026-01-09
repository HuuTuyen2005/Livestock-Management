# import bcrypt

# def check_password(plain, hashed):
#     return bcrypt.checkpw(plain.encode(), hashed.encode())
import bcrypt
import random
import string

# -------------------------------
# 1. Kiểm tra password nhập vào
# -------------------------------
def check_password(plain: str, hashed: str) -> bool:
    """
    Kiểm tra mật khẩu plaintext với hash lưu trong DB.
    """
    return bcrypt.checkpw(plain.encode(), hashed.encode())

# -------------------------------
# 2. Hash password
# -------------------------------
def hash_password(plain: str) -> str:
    """
    Tạo hash từ mật khẩu plaintext để lưu vào DB.
    """
    hashed = bcrypt.hashpw(plain.encode(), bcrypt.gensalt())
    return hashed.decode()  # Lưu dưới dạng string

# -------------------------------
# 3. Sinh mật khẩu mới ngẫu nhiên
# -------------------------------
def generate_password(length: int = 8, use_special: bool = True) -> str:
    """
    Sinh mật khẩu ngẫu nhiên gồm chữ hoa, chữ thường, số và ký tự đặc biệt.
    
    Parameters:
    - length: độ dài password
    - use_special: có thêm ký tự đặc biệt hay không
    """
    letters = string.ascii_letters  # a-zA-Z
    digits = string.digits          # 0-9
    specials = "!@#$%^&*()-_=+"
    
    chars = letters + digits
    if use_special:
        chars += specials

    # Đảm bảo ít nhất 1 ký tự từ mỗi nhóm (letters, digits, specials)
    password = [
        random.choice(string.ascii_lowercase),
        random.choice(string.ascii_uppercase),
        random.choice(string.digits),
    ]
    if use_special:
        password.append(random.choice(specials))

    # Điền phần còn lại
    while len(password) < length:
        password.append(random.choice(chars))

    random.shuffle(password)
    return ''.join(password)
