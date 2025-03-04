import os
import json
import logging
from flask import Flask, request, render_template

# Cấu hình logging
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

# Tệp JSON lưu từ điển
DICTIONARY_FILE = "dictionary.json"

# Load từ điển từ file JSON
def load_dictionary():
    if os.path.exists(DICTIONARY_FILE):
        with open(DICTIONARY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

# Lưu từ điển vào file JSON
def save_dictionary(dictionary):
    with open(DICTIONARY_FILE, "w", encoding="utf-8") as f:
        json.dump(dictionary, f, ensure_ascii=False, indent=4)

# Khởi tạo từ điển
dictionary = load_dictionary()

@app.route('/', methods=['GET', 'POST'])
def index():
    result = ''
    if request.method == 'POST':
        user_input = request.form['user_input'].lower()
        logging.info(f"User input: {user_input}")
        result = dictionary.get(user_input, 'Không tìm thấy kết quả!')
    return render_template('index.html', result=result)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    message = ""
    
    if request.method == 'POST':
        key = request.form.get('key', '').strip().lower()
        value = request.form.get('value', '').strip()
        action = request.form.get('action')

        if action == "add":
            if key and value:
                dictionary[key] = value
                save_dictionary(dictionary)
                message = "Thêm thành công!"
            else:
                message = "Vui lòng nhập đầy đủ thông tin."
        
        elif action == "update":
            if key in dictionary:
                dictionary[key] = value
                save_dictionary(dictionary)
                message = "Cập nhật thành công!"
            else:
                message = "Từ không tồn tại!"
        
        elif action == "delete":
            if key in dictionary:
                del dictionary[key]
                save_dictionary(dictionary)
                message = "Xóa thành công!"
            else:
                message = "Từ không tồn tại!"
    
    return render_template('admin.html', dictionary=dictionary, message=message)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port, debug=True)
