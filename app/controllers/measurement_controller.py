from models.db import MongoDB
import requests


def register_new_measurement(request):
    fields = [
        'data_hora', 'data'
    ]

    if not all(field in request.keys() for field in fields):
        return {
            "Erro":
            "Todos os campos são obrigatórios"
        }, 400

    if not request["data_hora"]:
        return {"erro": "Data e hora de coleta não informados"}, 400
    if not request["data"]:
        return {"erro": "Medições não enviadas"}, 400

    db = MongoDB()

    connection_is_alive = db.test_connection()
    errors = []

    if connection_is_alive:
        date_time = request['data_hora']
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
