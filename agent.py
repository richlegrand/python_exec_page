from flask import Flask, Response, request, render_template
import json

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/post_data', methods=['POST'])
def post_data():
    if request.method == "POST":
        data = json.loads(request.data)
        print("posted:", data)
        return  Response(
                json.dumps("hello"),
                mimetype="application/json",
            )
if __name__ == '__main__':
    app.run(port=5000, host="0.0.0.0")