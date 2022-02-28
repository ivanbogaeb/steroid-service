# MINIMAL OUTPUT FOR CPU USAGE
def minimal(Hardware):
    Hardware[0].Update() # Update this hardware module
    cores = 0;
    for data in Hardware[0].Sensors:
        if "CPU Core" in data.Name: # If this sensor is named CPU Core
            cores += 1 # Count one core
    return {
        "name": Hardware[0].Name,
        "usage": Hardware[0].Sensors[cores].Value, # The position of CPU Usage is at the end
    }

# DETAILED INFORMATION OF CPU USAGE
def detailed(Hardware):
    Hardware[0].Update()
    coresData = [];
    for data in Hardware[0].Sensors:
        if "CPU Core" in data.Name:
            coresData.append({
                "name": data.Name,
                "usage": data.Value,
            })
    return {
        "name": Hardware[0].Name,
        "usage": Hardware[0].Sensors[len(coresData)].Value,
        "cores": coresData,
    }
