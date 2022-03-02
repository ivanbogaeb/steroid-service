def usage(Hardware):
    Hardware.Update()
    load = []
    cores = []
    temperature = 0
    for index, Sensor in enumerate(Hardware.Sensors):
        if Sensor.SensorType == 5:
            if "Total" not in Sensor.Name:
                load.append({
                    "name": Sensor.Name,
                    "usage": Sensor.Value
                })
        elif Sensor.SensorType == 3:
            cores.append({
                "name": Sensor.Name,
                "power": Hardware.Sensors[index+2].Value,
                "voltage": Hardware.Sensors[index+3].Value,
            })
        elif Sensor.SensorType == 4:
            temperature = Sensor.Value
    return {
        "name": Hardware.Name,
        "usage": {
            "total": Hardware.Sensors[len(load)].Value,
            "threads": load,
        },
        "package": Hardware.Sensors[len(load)+1].Value,
        "cores": cores,
        "temperature": temperature
    }
