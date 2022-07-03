import json

response = "{["
sensorsLength = 0

def usage(Hardware):
    global response
    global sensorsLength

    response = "["

    for index, drive in enumerate(Hardware):
        drive.Update()
        sensorsLength = len(drive.Sensors)

        if index == 0:
            response += json.dumps({
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
        else:
            response += "," + json.dumps({
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

    response += "]"

    return response