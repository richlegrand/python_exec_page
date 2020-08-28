from flask import Flask, Response, request, render_template
from threading import Lock
import json
import subprocess

app = Flask(__name__)
lock = Lock()

def run_python(code, timeout=5, maxlen=5000):
    proc = subprocess.Popen(['python3'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    try:
        out, err = proc.communicate(bytes(code, 'utf-8'), timeout=timeout)
    except subprocess.TimeoutExpired:
        proc.kill()
        return "Sorry, your program took too long to execute!"
    else:
        out = out.decode('utf-8')
        if len(out)>maxlen:
            return "Sorry, your program's output is too lengthy!"
        return out + err.decode('utf-8')


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/post_data', methods=['POST'])
def post_data():
    if request.method == "POST":
        code = json.loads(request.data)
        # Prevent any imports for our protection
        code = code.replace('import', '')
        # Add any imports that we need here
        #code = "import foo\n" + code
        with lock: # Prevent programs from stepping on each other
            out = run_python(code)
        return Response(json.dumps(out), mimetype="application/json")

if __name__ == '__main__':
    app.run(port=5000, host="0.0.0.0")