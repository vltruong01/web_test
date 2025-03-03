from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    result = ''
    if request.method == 'POST':
        user_input = request.form['user_input']
        if user_input == 'Ngọc Ánh':
            result = 'Ngọc Ánh Yêu Vương Lộc Trường'
        if user_input == 'Vương Lộc Trường':
            result = 'Vương Lộc Trường Yêu Ngọc Ánh'
        if user_input == 'anhsime':
            result = 'Ánh Dú Bự'
    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)