import os
from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    result = ''
    if request.method == 'POST':
        user_input = request.form['user_input']
        responses = {
            'Ngọc Ánh': 'Ngọc Ánh Yêu Vương Lộc Trường',
            'Vương Lộc Trường': 'Vương Lộc Trường Yêu Ngọc Ánh',
            'anhsime': 'Ánh Dú Bự'
        }
        result = responses.get(user_input, 'Không tìm thấy kết quả!')
    return render_template('index.html', result=result)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port, debug=True)
