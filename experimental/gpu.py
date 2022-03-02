from flask import jsonify
import types

def usage(Hardware):
    if Hardware is None:
        return {
            "error": "Not able to fetch GPU sensors."
        }
    else:
        response = []

        temperature = []

        for gpu in Hardware:
            gpu.Update()
            response.append(
                {
                    "name": gpu.Name,
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
                        "videoEngine": 0, # NVIDIA
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
            )
            return jsonify(response)
        
    