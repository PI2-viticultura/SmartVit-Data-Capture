from models.db import MongoDB
import requests
import re
from datetime import datetime


def register_new_measurement(request):
    # Validade data
    sensor_labels = [
        "vento_MS", 
        "vento_direcao",
        "qtd_chuva",
        "temp_celsius",
        "humidity_percent",
        "pressure_hPa",
        "sensor_ph",
        "moist_percent_1",
        "moist_percent_2",
        "moist_percent_3"
    ]

    if not 'data' in request.keys():
        return {
            "Erro":
            "Dado dos sensores não enviados"
        }, 400

    for sensor_id, sensor_values  in request['data'].items(): 
        for label in sensor_values.keys():
            if not label in sensor_labels:
                return {
                    "Erro":
                    "Dado inválido! Dado não autorizado enviado!"
                }, 400

        for values in sensor_values.values(): 
            if (isinstance(values, list) and any([re.search("^\s*$", elem) for elem in values])) or (not values):
                return {
                    "Erro":
                    "Dado inválido!" + str(values)
                }, 400
       
    db = MongoDB()

    connection_is_alive = db.test_connection()
    errors = []

    if connection_is_alive:
        date_time = datetime.now()
        measurements_sent = request['data']

        for sensor_id, data in measurements_sent.items():
            sensor = db.get_one_by_identifier(sensor_id, 'sensor')

            if not sensor:
                return {'error': 'Sensor ' +
                        sensor_id + ' doesn\'t exist'}, 500

            elif 'measurements' not in sensor.keys():
                sensor['measurements'] = []
            elif len(sensor['measurements']) == 0:
                sensor['measurements'] = []
            
            # Register automatic irrigation
            if (
                "moist_percent_1" in data.keys()
                and "moist_percent_2" in data.keys()
                and "moist_percent_3" in data.keys()
            ):

                if (
                  data["moist_percent_1"] +
                  data["moist_percent_2"] +
                  data["moist_percent_3"]
                )/3 <= 0.3:
                    system = db.get_system_by_sensor_id(sensor['_id'])
                    winery = db.get_winery_by_system_id(system['_id'])
                    data = dict()
                    data['type'] = 'water'
                    data['title'] = 'Sistema de Irrigacao'
                    data['winery'] = str(winery['_id'])
                    data['message'] = 'Sistema de Irrigacao Ativado'
                    url = "https://smartvit-notification-dev.herokuapp.com"
                    requests.post(
                      url + "/notification",
                      json=data
                    )
            
            # Update sensor with data
            for label, value in data.items():
                request_sent = {"sensor_id": sensor_id,
                                "value": value,
                                "date_time": date_time,
                                "type": label}
                sensor_data = {'value': value,
                               'date_time': date_time,
                               'type': label}

                measurement = db.insert_one(request_sent, 'measurement')

                if not measurement:
                    errors.append('Something gone wrong saving ' +
                                  label +
                                  ' measurement')

                sensor['measurements'].append(sensor_data)

                if not (db.update_one(sensor, 'sensor')):
                    errors.append(
                        'Something gone wrong updating measurements from '
                        + sensor_id)

        if len(errors) == 0:
            return {"message": "success"}, 200
        else:
            return{"Error": errors}, 500

    return {'error': 'Something gone wrong with database connection'}, 500
