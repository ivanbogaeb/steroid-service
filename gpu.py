from flask import jsonify
import types

# Don't ask about the overengineered stuff, okay? Leave it there...
# I need testers to be honest

def usage(Hardware):
    if Hardware is None:
        return {"error": "Not able to fetch GPU sensors."}
    else:
        response = []
        for gpu in Hardware:
            temperature = []
            clock = []
            voltage = []
            load = []
            power = []
            transfer = []
            memory = []
            gpuData = {
                "name": "GPU Name",
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
                "clock": {
                    "core": 0, # AMD / NVIDIA
                    "soc": 0, # AMD
                    "memory": 0 # AMD / NVIDIA
                },
                "voltage": {
                    "core": 0, # AMD
                    "soc": 0, # AMD
                    "memory": 0, # AMD
                },
                "load": {
                    "core": 0, # AMD / NVIDIA / INTEL
                    "memory": 0, # AMD / NVIDIA
                    "videoengine": 0, # NVIDIA
                    "d3d": 0 # NVIDIA
                },
                "power": {
                    "core": 0, # AMD
                    "ppt": 0, # AMD
                    "soc": 0, # AMD
                    "package": 0 # AMD / NVIDIA / INTEL
                },
                "transfer": {
                    "rx": 0, # NVIDIA
                    "tx": 0, # NVIDIA
                },
                "memory": {
                    "free": 0, # NVIDIA
                    "used": 0, # NVIDIA / AMD / INTEL
                    "total": 0, # NVIDIA
                },
            }
            gpu.Update()

            gpuData['name'] = gpu.Name

            if "NVIDIA" in gpu.Name:
                for sensor in gpu.Sensors:
                    if sensor.SensorType == 2:
                        gpuData['power']['package'] = sensor.Value
                    if sensor.SensorType == 3:
                        clock.append(sensor)
                    elif sensor.SensorType == 4:
                        temperature.append(sensor)
                    elif sensor.SensorType == 5:
                        load.append(sensor)
                    elif sensor.SensorType == 13:
                        memory.append(sensor)
                    elif sensor.SensorType == 14:
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

            response.append(gpuData)
            return jsonify(response)
        
    