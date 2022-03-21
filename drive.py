from flask import jsonify

def usage(Hardware):
    response = [0]
    sensorsLength = 0
    for drive in Hardware:
        drive.Update()
        sensorsLength = len(drive.Sensors)
        response.append({
            "name": drive.Name,
            "temperature": drive.Sensors[0].Value,
            "used": drive.Sensors[sensorsLength - 5].Value,
            "activity": {
                "write": drive.Sensors[sensorsLength - 4].Value,
                "total": drive.Sensors[sensorsLength - 3].Value,
            },
            "rates": {
                "read": drive.Sensors[sensorsLength - 2].Value,
                "write": drive.Sensors[sensorsLength - 1].Value,
            }
        })

    response.pop(0)

    return jsonify(response)