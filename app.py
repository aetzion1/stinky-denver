from flask import Flask, render_template
import random # remove once we have AI logic

app = Flask(__name__)

@app.route('/')
def index():
    stink_value = random.uniform(0, 1)  # Example: Random value between 0 and 1
    return render_template('index.html', stink_value=stink_value)

if __name__ == '__main__':
    app.run(debug=True)