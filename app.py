import os
import logging
from flask import Flask, request, render_template, redirect, url_for

app = Flask(__name__)

# Cấu hình logging
logging.basicConfig(level=logging.INFO)

# Bộ nhớ tạm lưu từ điển (có thể thay bằng database sau này)
dictionary = {
    'Ngọc Ánh': 'Ngọc Ánh Yêu Vương Lộc Trường',
    'Vương Lộc Trường': 'Vương Lộc Trường Yêu Ngọc Ánh',
    'anhsime': 'Ánh Dú Bự'
}

@app.route('/', methods=['GET', 'POST'])
def index():
    result = ''
    if request.method == 'POST':
        user_input = request.form['user_input'].strip().lower()
        
        # Ghi lại hành động người dùng nhập
        logging.info(f"User input: {user_input}")
        
        result = dictionary.get(user_input, 'Không tìm thấy kết quả!')
    return render_template('index.html', result=result)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    message = ''
    if request.method == 'POST':
        key = request.form['key'].strip().lower()
        value = request.form['value'].strip()
        
        if key and value:
            dictionary[key] = value
            message = f'Từ "{key}" đã được thêm với nghĩa "{value}"'
            logging.info(f'Admin added: {key} -> {value}')
        else:
            message = 'Vui lòng nhập đầy đủ thông tin!'
    
    return render_template('admin.html', message=message, dictionary=dictionary)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port, debug=True)
