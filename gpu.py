from flask import jsonify

# Don't ask about the overengineered stuff, okay? Leave it there...
# I need testers to be honest

def usage(Hardware, HardwareType, SensorType):
    response = []
    if Hardware is None:
        response.append({"error": "Not able to fetch GPU sensors."})
    else:
        for gpu in Hardware:
            voltage = []
            power = []
            clock = []
            temperature = []
            load = []
            memory = []
            transfer = []
            gpuData = {
                "name": "GPU Name",
                "voltage": {
                    "core": 0, # AMD
                    "soc": 0, # AMD
                    "memory": 0, # AMD
                },
                "power": {
                    "core": 0, # AMD
                    "ppt": 0, # AMD
                    "soc": 0, # AMD
                    "package": 0 # AMD / NVIDIA / INTEL
                },
                "clock": {
                    "core": 0, # AMD / NVIDIA
                    "soc": 0, # AMD
                    "memory": 0 # AMD / NVIDIA
                },
                "temperature": {
                    "core": 0, # AMD  / NVIDIA calls junction
                    "memory": 0, # AMD
                    "vddc": 0, # AMD
                    "mvdd": 0, # AMD
                    "soc": 0, # AMD
                    "liquid": 0, # AMD
                    "plx": 0, # AMD
                    "hotspot": 0, # AMD / NVIDIA
                },
                "load": {
                    "core": 0, # AMD / NVIDIA / INTEL
                    "memory": 0, # AMD / NVIDIA
                    "videoengine": 0, # NVIDIA
                    "d3d": 0 # NVIDIA
                },
                "memory": {
                    "free": 0, # NVIDIA
                    "used": 0, # NVIDIA / AMD / INTEL
                    "total": 0, # NVIDIA
                },
                "transfer": {
                    "rx": 0, # NVIDIA
                    "tx": 0, # NVIDIA
                },
                
            }
            gpu.Update()
            gpuData['name'] = gpu.Name
            if gpu.HardwareType == HardwareType.GpuNvidia:
                for sensor in gpu.Sensors:
                    if sensor.SensorType == SensorType.Power:
                        gpuData['power']['package'] = sensor.Value
                    elif sensor.SensorType == SensorType.Clock:
                        clock.append(sensor)
                    elif sensor.SensorType == SensorType.Temperature:
                        temperature.append(sensor)
                    elif sensor.SensorType == SensorType.Load:
                        load.append(sensor)
                    elif sensor.SensorType == SensorType.SmallData:
                        memory.append(sensor)
                    elif sensor.SensorType == SensorType.Throughput:
                        transfer.append(sensor)
                gpuData['clock']['core'] = clock[0].Value
                gpuData['clock']['memory'] = clock[1].Value
                gpuData['temperature']['core'] = temperature[0].Value
                gpuData['temperature']['hotspot'] = temperature[1].Value
                gpuData['load']['core'] = load[0].Value
                gpuData['load']['memory'] = load[1].Value
                gpuData['load']['videoengine'] = load[2].Value
                gpuData['load']['d3d'] = load[6].Value
                gpuData['memory']['free'] = memory[1].Value
                gpuData['memory']['used'] = memory[2].Value
                gpuData['memory']['total'] = memory[0].Value
                gpuData['transfer']['rx'] = transfer[0].Value
                gpuData['transfer']['tx'] = transfer[1].Value
            elif gpu.HardwareType == HardwareType.GpuAmd:
                for sensor in gpu.Sensors:
                    print(sensor.SensorType, sensor.Name, sensor.Value)
                    if sensor.SensorType == SensorType.Voltage:
                        voltage.append(sensor)
                    elif sensor.SensorType == SensorType.Power:
                        power.append(sensor)
                    elif sensor.SensorType == SensorType.Clock:
                        clock.append(sensor)
                    elif sensor.SensorType == SensorType.Temperature:
                        temperature.append(sensor)
                    elif sensor.SensorType == SensorType.Load:
                        load.append(sensor)
                    elif sensor.SensorType == SensorType.SmallData:
                        memory.append(sensor)
            elif gpu.HardwareType == HardwareType.GpuIntel:
                for sensor in gpu.Sensors:
                    print(sensor.SensorType, sensor.Name, sensor.Value)
                    if sensor.SensorType == SensorType.Power:
                        gpuData['power']['package'] = sensor.Value
                    elif sensor.SensorType == SensorType.Load:
                        load.append(sensor)
                    elif sensor.SensorType == SensorType.SmallData:
                        gpuData['memory']['used'] = sensor.Value
                gpuData['load']['d3d'] = load[0].Value
                gpuData['load']['videoengine'] = load[3].Value

            response.append(gpuData)

    return jsonify(response)
        
    