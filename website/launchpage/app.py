import subprocess
from flask import Flask, render_template

app = Flask(__name__, static_folder='static')

@app.route('/')
def index():
    try:
        result = subprocess.check_output(['python', 'CNN_DSB.py'], text=True, stderr=subprocess.STDOUT)
        return render_template('ind_ex.html', result=result)
    except subprocess.CalledProcessError as e:
        error_message = f"Error running script: {e.output}"
        return render_template('ind_ex.html', result=error_message)

if __name__ == '__main__':
    app.run(debug=True)
