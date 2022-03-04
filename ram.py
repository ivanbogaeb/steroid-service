def usage(Hardware):
    Hardware.Update()

    return {
        "name": Hardware.Name,
        "used": Hardware.Sensors[0].Value,
        "free": Hardware.Sensors[1].Value,
        "usage": Hardware.Sensors[2].Value,
    }