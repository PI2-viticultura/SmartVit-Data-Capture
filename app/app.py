from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app, automatic_options=True)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8000)
