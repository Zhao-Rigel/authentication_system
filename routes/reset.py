from flask import Blueprint, request, render_template, redirect, url_for, flash
from extensions import db
from utils import generate_totp_secret, generate_reset_token, verify_reset_token, hash_password
reset_bp = Blueprint('reset', __name__)

# 延迟导入
def get_user_model():
    from models import User
    return User

@reset_bp.route('/reset', methods=['GET', 'POST'])
def reset_request():
    User = get_user_model()
    if request.method == 'POST':
        email = request.form['email']
        user = User.query.filter_by(email=email).first()
        if user:
            token = generate_reset_token(email)
            reset_url = url_for('reset.reset_token', token=token, _external=True)
            print(reset_url)# Replace with email sending
            
        return redirect(url_for('auth.login'))

    return render_template('reset.html')

@reset_bp.route('/reset/<token>', methods=['GET', 'POST'])
def reset_token(token):
    User = get_user_model()
    email = verify_reset_token(token)
    if not email:
        return 'Invalid or expired token', 400

    if request.method == 'POST':
        user = User.query.filter_by(email=email).first()
        if user:
            user.password = hash_password(request.form['password'])

            totp_secret=generate_totp_secret()

            user.totp_secret=totp_secret
            db.session.commit()

            import pyotp
            import qrcode
            totp = pyotp.TOTP(user.totp_secret)
            # 生成一个 TOTP 二维码（可以扫描并添加到 Google Authenticator 等应用中）
            uri = totp.provisioning_uri(user.username, issuer_name="身份鉴别系统_赵君灏")
            img = qrcode.make(uri)  # 生成二维码
            img.save("static/totp_qr.png")  # 保存二维码图像
            return redirect(url_for('auth.setup_totp'))

    return render_template('reset_password.html')