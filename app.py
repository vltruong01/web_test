import os
import logging
from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from unidecode import unidecode  # Thêm import thư viện unidecode

# Cấu hình logging
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

# Cấu hình PostgreSQL (Render)
database_uri = os.environ.get('DATABASE_URI', 'postgresql://web_test_olxc_user:eqI93uS1LWJS9qdzFn5GNR4Q91V1H34C@dpg-cv3h6uan91rc739ftn20-a:5432/web_test_olxc')  # Đường dẫn Persistent Storage
app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Model cho từ điển
class Dictionary(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(100), unique=True, nullable=False)
    value = db.Column(db.String(255), nullable=False)

# Tạo database nếu chưa có
with app.app_context():
    db.create_all()

# Trang chính
@app.route('/', methods=['GET', 'POST'])
def index():
    result = ''
    if request.method == 'POST':
        user_input = request.form['user_input'].lower()
        logging.info(f"User input: {user_input}")

        # Loại bỏ dấu và chuyển thành chữ thường
        user_input_no_accent = unidecode(user_input)  # Loại bỏ dấu

        # Sử dụng like để tìm kiếm không phân biệt chữ hoa chữ thường và tìm giống như LIKE SQL
        word = Dictionary.query.filter(Dictionary.key.ilike(f'%{user_input_no_accent}%')).first()  # Sử dụng `ilike` để tìm kiếm không phân biệt chữ hoa chữ thường
        
        if word:
            result = word.value
        else:
            result = 'Không tìm thấy kết quả!'

        # Ghi log cả input và output
        logging.info(f"User output: {result}")
    
    return render_template('index.html', result=result)

# Trang quản lý từ điển
@app.route('/admin', methods=['GET', 'POST'])
def admin():
    message = ''
    if request.method == 'POST':
        key = request.form['key'].lower()
        value = request.form['value']

        # Kiểm tra xem từ đã tồn tại chưa
        existing_entry = Dictionary.query.filter_by(key=key).first()
        if existing_entry:
            existing_entry.value = value  # Cập nhật từ điển
            message = "Cập nhật thành công!"
        else:
            new_entry = Dictionary(key=key, value=value)
            db.session.add(new_entry)
            db.session.commit()
            message = "Thêm thành công!"
    
    # Lấy tất cả các từ trong từ điển
    dictionary = Dictionary.query.all()
    return render_template('admin.html', dictionary=dictionary, message=message)

# Route để xóa từ điển
@app.route('/delete/<int:id>', methods=['GET'])
def delete(id):
    word = Dictionary.query.get(id)
    if word:
        db.session.delete(word)
        db.session.commit()
    return redirect(url_for('admin'))

if __name__ == '__main__':
    # Cấu hình port từ môi trường (Render uses 10000 by default)
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port, debug=True)
