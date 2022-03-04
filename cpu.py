def usage(Hardware):
    Hardware.Update()
    load = []
    cores = []
    loadLen = 0
    temperature = 0

    for index, Sensor in enumerate(Hardware.Sensors):
        if Sensor.SensorType == 5:
            if "Total" not in Sensor.Name:
                load.append({
                    "name": Sensor.Name,
                    "usage": Sensor.Value
                })
        elif Sensor.SensorType == 3 and "Core" in Sensor.Name:
            cores.append({
                "name": Sensor.Name,
                "frequency": Sensor.Value,
                "voltage": Hardware.Sensors[index+3].Value,
                "power": Hardware.Sensors[index+2].Value,
            })
        elif Sensor.SensorType == 4:
            temperature = Sensor.Value

    loadLen = len(load)

    return {
        "name": Hardware.Name,
        "usage": {
            "total": Hardware.Sensors[loadLen].Value,
            "threads": load,
        },
        "package": Hardware.Sensors[loadLen+1].Value,
        "cores": cores,
        "temperature": temperature
    }
