from flask import Blueprint, request
from flask_cors import CORS
import controllers.measurement_controller as controller

app = Blueprint('measurement', __name__)
CORS(app)


@app.route("/measurement", methods=["POST"])
def measurement():
    return controller.register_new_measurement(request.json)
