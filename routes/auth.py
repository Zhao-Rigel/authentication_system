from flask import Blueprint, request, render_template, redirect, url_for, session
from extensions import db, bcrypt
from utils import hash_password, check_password, generate_totp_secret, verify_totp

auth_bp = Blueprint('auth', __name__)

# 延迟导入
def get_user_model():
    from models import User
    return User

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    User = get_user_model()  # 延迟获取 User 模型
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = hash_password(request.form['password'])
        totp_secret = generate_totp_secret()

        user = User(username=username, email=email, password=password, totp_secret=totp_secret)
        db.session.add(user)
        db.session.commit()
        import pyotp
        import qrcode
        totp = pyotp.TOTP(user.totp_secret)
        # 生成一个 TOTP 二维码（可以扫描并添加到 Google Authenticator 等应用中）
        uri = totp.provisioning_uri(user.username, issuer_name="身份鉴别系统_赵君灏")
        img = qrcode.make(uri)  # 生成二维码
        img.save("static/totp_qr.png")  # 保存二维码图像
        return redirect(url_for('auth.setup_totp'))

    return render_template('register.html')


@auth_bp.route('/setup_totp')
def setup_totp():
    return render_template('setup_totp.html', qr_image='static/totp_qr.png')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    User = get_user_model()
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        token = request.form['token']

        user = User.query.filter_by(email=email).first()
        if user and check_password(password, user.password) and verify_totp(user.totp_secret, token):
            session['user_id'] = user.id
            session['username'] = user.username
            return redirect(url_for('auth.dashboard'))

        return 'Invalid credentials or token', 401

    return render_template('login.html')


@auth_bp.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    username = session.get('username', 'Guest')
    return render_template('dashboard.html', username=username)

@auth_bp.route('/logout')
def logout():
    # 清除 session 中的所有数据
    session.clear()
    return redirect(url_for('auth.login'))  # 跳转到登录页面

@auth_bp.route('/')
def root():
    return redirect(url_for('auth.dashboard'))