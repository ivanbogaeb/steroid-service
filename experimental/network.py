from flask import jsonify

def usage(Hardware):
    response = []
    sensorsLength = 0
    for connection in Hardware:
        sensorsLength = len(connection.Sensors)
        connection.Update()
        response.append({
            "name": connection.Name,
            "usage": connection.Sensors[sensorsLength - 1].Value,
            "speed": {
                "download": connection.Sensors[sensorsLength - 2].Value,
                "upload": connection.Sensors[sensorsLength - 3].Value,
            },
            "data": {
                "downloaded": connection.Sensors[sensorsLength - 4].Value,
                "uploaded": connection.Sensors[sensorsLength - 5].Value,
            },
        })

    return jsonify(response)