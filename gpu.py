from flask import jsonify
import types

def usage(Hardware):
    if Hardware is None:
        return {
            "error": "Not able to fetch GPU sensors."
        }
    elif len(Hardware) > 1:
        response = []
        for gpu in Hardware:
            gpu.Update()
            response.append(
                {
                    "name": gpu.Name,
                    "core": {
                        "temperature": gpu.Sensors[0].Value,
                        "usage": gpu.Sensors[4].Value,
                        "frequency": gpu.Sensors[1].Value,
                    },
                    "memory": {
                        "usage": gpu.Sensors[10].Value,
                        "controller": {
                            "usage": gpu.Sensors[5].Value,
                        },
                        "frequency": gpu.Sensors[2].Value,
                        "total": gpu.Sensors[7].Value, # Outputs in Kb
                        "used": gpu.Sensors[8].Value,
                        "free": gpu.Sensors[9].Value,
                    },
                    "shader": {
                        "usage": gpu.Sensors[3].Value,
                    },
                    "video": {
                        "usage": gpu.Sensors[6].Value,
                    },
                }
            )
            return jsonify(response)
    
    else:
        Hardware[0].Update()
        for sensor in Hardware[0].Sensors:
                print(sensor.SensorType, " - ", sensor.Identifier)
        # gpuData = types.SimpleNamespace()
        # gpuData.name = Hardware[0].Name,
        return {
            "name": Hardware[0].Name,
            "core": {
                "temperature": Hardware[0].Sensors[0].Value,
                "usage": Hardware[0].Sensors[4].Value,
                "frequency": Hardware[0].Sensors[1].Value,
            },
            "memory": {
            "usage": Hardware[0].Sensors[10].Value,
            "controller": {
                    "usage": Hardware[0].Sensors[5].Value,
                },
                "frequency": Hardware[0].Sensors[2].Value,
                "total": Hardware[0].Sensors[7].Value, # Outputs in Kb
                "used": Hardware[0].Sensors[8].Value,
                "free": Hardware[0].Sensors[9].Value,
            },
            "shader": {
                "usage": Hardware[0].Sensors[3].Value,
            },
            "video": {
                 "usage": Hardware[0].Sensors[6].Value,
            }, 
        }
        
    