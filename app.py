from flask import Flask, render_template
from stink_calculator import get_stink_value, get_message


app = Flask(__name__)

@app.route('/')
def index():
    stink_value = get_stink_value()
    message = get_message(stink_value)
    return render_template('index.html', stink_value=stink_value, message=message)

if __name__ == '__main__':
    app.run(debug=True)