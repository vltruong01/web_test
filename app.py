import os
import logging
from flask import Flask, request, render_template

# Cấu hình logging
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    result = ''
    if request.method == 'POST':
        user_input = request.form['user_input'].lower()  # Chuyển input về chữ thường
        
        # Ghi lại hành động người dùng nhập
        logging.info(f"User input: {user_input}")
        
        responses = {
            'ngọc ánh': 'Ngọc Ánh Yêu Vương Lộc Trường',
            'vương lộc trường': 'Vương Lộc Trường Yêu Ngọc Ánh',
            'anhsime': 'Ánh Dú Bự',
            'phan quốc huy': 'Ế không ai iu'
        }
        result = responses.get(user_input, 'Không tìm thấy kết quả!')
    return render_template('index.html', result=result)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port, debug=True)
