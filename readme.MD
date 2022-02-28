# Steroid Service

Steroid service is the service that provides real time data metrics from your PC to your wallpaper/program.

#### Requirements
- Python 3.9
- PIP

#### Installation
```powershell
    pip install requirements.txt
```

#### How to run
```powershell
    python ./steroid-services.py
```

#### References
Steroid service works as an internal web API hosted on your **localhost** port **7666**, waiting for a **GET method** on these endpoints:

|Endpoint|Query|Return format|
|---|---|---|
|/cpu|?function=minimal|*Object Object*|
||?function=detailed|*Object Object*|
|/gpu||*Object Object*|
|/ram||*Object Object*|
|/filesystem||*Object Object*|

#### Notes
OpenHardwareMonitor sets it's own unique interface, and every sensor has it's own identifier. These are the ones I know by doing reverse engineering:

|Component|SensorType|Description|
|---|---|---|
|**CPU**||||
|**GPU**|1|Clock (Mhz)|
||2|Temperature (C or F)|
||3|Load (%)|
||11|Memory *(GB, MB and KB)*|
|**RAM**||||
|**Filesystem**||||

