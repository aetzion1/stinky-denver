from flask import Flask, render_template
from stink_calculator import initialize_client


app = Flask(__name__)
client = initialize_client()

@app.route('/')
def index():
    try:
        stinkiness = client.request_stinkiness()
    except Exception as e:
        stinkiness = client.error_response

    return render_template(
        'index.html',
        stink_value=stinkiness.rating,
        message=stinkiness.poem
    )

if __name__ == '__main__':
    app.run(debug=True)
