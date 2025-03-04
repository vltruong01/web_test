import os
import json
import logging
from flask import Flask, request, render_template

# Cấu hình logging
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

# Đường dẫn file JSON để lưu từ điển
DICTIONARY_FILE = "dictionary.json"

# **Hàm đọc từ điển từ JSON**
def load_dictionary():
    if os.path.exists(DICTIONARY_FILE):
        with open(DICTIONARY_FILE, 'r', encoding='utf-8') as file:
            return json.load(file)
    return {}  # Trả về từ điển rỗng nếu chưa có file JSON

# **Hàm ghi từ điển vào JSON**
def save_dictionary():
    with open(DICTIONARY_FILE, 'w', encoding='utf-8') as file:
        json.dump(dictionary, file, ensure_ascii=False, indent=4)

# **Khởi tạo từ điển**
dictionary = load_dictionary()

@app.route('/', methods=['GET', 'POST'])
def index():
    result = ''
    if request.method == 'POST':
        user_input = request.form['user_input'].strip().lower()
        
        # Ghi log input của người dùng
        logging.info(f"User input: {user_input}")
        
        # Kiểm tra từ điển
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
            save_dictionary()  # Lưu vào file JSON
            message = f'Từ "{key}" đã được thêm với nghĩa "{value}"'
            logging.info(f'Admin added: {key} -> {value}')
        else:
            message = 'Vui lòng nhập đầy đủ thông tin!'
    
    return render_template('admin.html', message=message, dictionary=dictionary)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port, debug=True)
