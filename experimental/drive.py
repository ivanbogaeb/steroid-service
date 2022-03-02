from flask import jsonify
import types

def usage(Hardware):

    response = []

    for drive in Hardware:
        drive.Update()
        response.append({
            "name": drive.Name,
            "temperature": drive.Sensors[0].Value,
            "used": drive.Sensors[1].Value,
            "activity": {
                "write": drive.Sensors[2].Value,
                "total": drive.Sensors[3].Value,
            },
            "rates": {
                "read": drive.Sensors[4].Value,
                "write": drive.Sensors[5].Value,
            }
        })

    return jsonify(response)