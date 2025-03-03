import os
import logging
import unicodedata
from flask import Flask, request, render_template

# Cấu hình logging
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

def normalize_input(input_str):
    # Chuyển input về chữ thường và loại bỏ dấu
    return ''.join(
        c for c in unicodedata.normalize('NFD', input_str.lower())
        if unicodedata.category(c) != 'Mn'
    )

@app.route('/', methods=['GET', 'POST'])
def index():
    result = ''
    if request.method == 'POST':
        user_input = normalize_input(request.form['user_input'])
        
        # Ghi lại hành động người dùng nhập
        logging.info(f"User input: {user_input}")
        
        responses = {
            'ngoc anh': 'Ngọc Ánh Yêu Vương Lộc Trường',
            'vuong loc truong': 'Vương Lộc Trường Yêu Ngọc Ánh',
            'anhsime': 'Ánh Đẹp Gái',
            'phan quoc huy': 'Ế không ai iu'
        }
        result = responses.get(user_input, 'Không tìm thấy kết quả!')
    return render_template('index.html', result=result)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port, debug=True)