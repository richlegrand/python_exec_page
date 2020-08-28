from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/post_data', methods=['POST'])
def post_data():
    if request.method == "POST":
        print("posted:", request.data)
        #perform action here
        return "OK"

if __name__ == '__main__':
    app.run(port=5000, host="0.0.0.0")