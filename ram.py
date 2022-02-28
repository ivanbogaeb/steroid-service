def usage(Hardware):
    Hardware[0].Update() # Update this hardware module
    return {
        "name": Hardware[0].Name,
        "usage": Hardware[0].Sensors[0].Value, # Returns in % scale 100
        "usedMemory": Hardware[0].Sensors[1].Value, # Returns in GB
        "freeMemory": Hardware[0].Sensors[2].Value, # Returns in GB
    }