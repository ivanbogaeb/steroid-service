## Steroid Service

Hardware  monitor web application made for [Steroid](https://steroid-app.github.io), providing real time usage metrics from your PC to your wallpaper.

### Requirements:

- .NET 4.7.X (Latest if possible)
- Python 3.8.X (Above will run with `--pre` version of pythonnet but might cause memory leaks)
- PIP

### Installation:

```shell
    pip install -r requirements.txt
```

### How to run:
> Must run under Root/Administrator/System.

If not built with PyInstaller
```shell
    python ./steroid-service.py
```

If built or downloaded the latest release, `you must open a terminal as Administrator in the steroid folder`, and then:
```shell
    cd dist/steroid-service
    start steroid-service.exe
```

> CTRL + C to exit.

### Compile:

```shell
    pyinstaller steroid-service.spec --collect-data pythonnet
```

### References:

Steroid service works as an internal web API hosted on **http://localhost:7666**, waiting for a **GET method** on these paths:

|Endpoint|Return format|
|---|---|
|<center>/cpu</center>|<center>*Object Object*</center>|
|<center>/gpu</center>|<center>*Array Object*</center>|
|<center>/network</center>|<center>*Array Object*</center>|
|<center>/memory</center>|<center>*Object Object*</center>|
|<center>/filesystem</center>|<center>*Array Object*</center>|

> This service application can run both UAC enabled or disabled.

> GPU is **UNFISHED** and needs AMD testers to provide console output.


### Development Notes:
LibreHardwareMonitor sets it's own unique interface, and every hardware has it's own `HardwareType` and `Name`:

**Hardware**:
|HardwareType|Name|Privileges|
|---|---|---|
|<center>0</center>|<center>Motherboard</center>|<center>User</center>|
|<center>1</center>|<center>SuperIO</center>|<center>Admin</center>|
|<center>2</center>|<center>CPU</center>|<center>User</center>|
|<center>3</center>|<center>Memory</center>|<center>User</center>|
|<center>4</center>|<center>GpuNvidia</center>|<center>User</center>|
|<center>4</center>|<center>GpuAmd</center>|<center>User</center>|
|<center>4</center>|<center>GpuIntel</center>|<center>User</center>|
|<center>6</center>|<center>Storage</center>|<center>Admin</center>|
|<center>7</center>|<center>Network</center>|<center>User</center>|
|<center>?</center>|<center>Cooler</center>|<center>Admin</center>|
|<center>?</center>|<center>EmbeddedController</center>|<center>Admin</center>|
|<center>?</center>|<center>Psu</center>|<center>Admin</center>|
|<center>?</center>|<center>Battery</center>|<center>Admin</center>|

> Hardware components marked as **Admin** are requested under Administrator privileges.

**Sensors**:
|SensorType|Value|Format|Privileges|
|---|---|---|---|
|<center>0</center>|<center>Voltage</center>|<center>V</center>|<center>Admin</center>|
|<center>1</center>|<center>Current</center>|<center>A</center>|<center>Admin</center>|
|<center>2</center>|<center>Power</center>|<center>W</center>|<center>User/Admin</center>|
|<center>3</center>|<center>Clock</center>|<center>Mhz</center>|<center>User/Admin</center>|
|<center>4</center>|<center>Temperature</center>|<center>°C</center>|<center>User/Admin</center>|
|<center>5</center>|<center>Load</center>|<center>%</center>|<center>User</center>|
|<center>6</center>|<center>Frequency</center>|<center>Hz</center>|<center>User</center>|
|<center>7</center>|<center>Fan</center>|<center>RPM</center>|<center>Admin</center>|
|<center>8</center>|<center>Flow</center>|<center>L/h</center>|<center>Admin</center>|
|<center>9</center>|<center>Control</center>|<center>%</center>|<center>User</center>|
|<center>10</center>|<center>Level</center>|<center>%</center>|<center>User</center>|
|<center>11</center>|<center>Factor</center>|<center>1</center>|<center>Admin</center>|
|<center>12</center>|<center>Data</center>|<center>GB</center>|<center>User</center>|
|<center>13</center>|<center>SmallData</center>|<center>MB</center>|<center>User</center>|
|<center>14</center>|<center>Throughput</center>|<center>B/s</center>|<center>User</center>|
|<center>15</center>|<center>TimeSpan</center>|<center>Seconds</center>|<center>User</center>|
|<center>16</center>|<center>Energy</center>|<center>mWh</center>|<center>Admin</center>|

> **User/Admin** privileges means it is only available for Users under determined conditions, like the GPU.

### Credits:

Brought to you thanks to [flask](https://github.com/pallets/flask), [pythonnet](http://pythonnet.github.io/), [pyinstaller](https://github.com/pyinstaller/pyinstaller) and [LibreHardwareMonitor](https://github.com/librehardwaremonitor/librehardwaremonitor) libraries.
