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
        "videoencode": 0, # AMD / NVIDIA
        "videodecode": 0 # AMD / NVIDIA
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
def usage(Hardware, HardwareType, SensorType):
    if Hardware is None:
        return {"error": "Not able to fetch GPU sensors."}
    else:
        for gpu in Hardware:
            clock = [0]
            temperature = [0]
            load = [0]
            memory = [0]
            transfer = [0]
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

                clock.pop(0)
                temperature.pop(0)
                load.pop(0)
                memory.pop(0)
                transfer.pop(0)
                
                gpuData['clock']['core'] = clock[0].Value
                gpuData['clock']['memory'] = clock[1].Value
                gpuData['temperature']['core'] = temperature[0].Value
                gpuData['temperature']['hotspot'] = temperature[1].Value
                gpuData['load']['core'] = load[0].Value
                gpuData['load']['memory'] = load[1].Value
                gpuData['load']['videoengine'] = load[2].Value
                gpuData['load']['d3d'] = load[6].Value
                gpuData['load']['decode'] = load[9].Value
                gpuData['load']['encode'] = load[13].Value
                gpuData['memory']['free'] = memory[1].Value
                gpuData['memory']['used'] = memory[2].Value
                gpuData['memory']['total'] = memory[0].Value
                gpuData['transfer']['rx'] = transfer[0].Value
                gpuData['transfer']['tx'] = transfer[1].Value

            elif gpu.HardwareType == HardwareType.GpuAmd:
                for sensor in gpu.Sensors:
                    if sensor.SensorType == SensorType.Power:
                        gpuData['power']['package'] = sensor.Value
                    elif sensor.SensorType == SensorType.Clock:
                        clock.append(sensor)
                    elif sensor.SensorType == SensorType.Temperature:
                        gpuData['temperature']['core'] = sensor.Value
                    elif sensor.SensorType == SensorType.Load:
                        load.append(sensor)
                    elif sensor.SensorType == SensorType.SmallData:
                        memory.append(sensor)

                temperature.pop(0)
                load.pop(0)
                memory.pop(0)
                transfer.pop(0)

                gpuData['memory']['used'] = memory[0].Value
                gpuData['load']['d3d'] = load[0].Value
                if clock[0] != 0: # Not integrated
                    gpuData['clock']['core'] = clock[0].Value
                    gpuData['clock']['memory'] = clock[1].Value
                    gpuData['load']['decode'] = load[11].Value
                    gpuData['load']['encode'] = load[14].Value
                    gpuData['load']['core'] = load[load.len()].Value
                else: # Integrated
                    gpuData['load']['decode'] = load[6].Value
                    gpuData['load']['encode'] = load[8].Value

                clock.pop(0)

            elif gpu.HardwareType == HardwareType.GpuIntel:
                for sensor in gpu.Sensors:
                    if sensor.SensorType == SensorType.Power:
                        gpuData['power']['package'] = sensor.Value
                    elif sensor.SensorType == SensorType.Load:
                        load.append(sensor)
                    elif sensor.SensorType == SensorType.SmallData:
                        gpuData['memory']['used'] = sensor.Value

                load.pop(0)
                
                gpuData['load']['d3d'] = load[0].Value
                gpuData['load']['videoengine'] = load[3].Value

        return gpuData
    