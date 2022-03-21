import os
import clr
import logging
import multiprocessing
from flask import Flask, request

import cpu as cpuModule
import ram as ramModule
import gpu as gpuModule
import drive as driveModule
import network as networkModule

directory_path = os.getcwd()

clr.AddReference(directory_path+"\\LibreHardwareMonitorLib.dll")
from LibreHardwareMonitor import Hardware
handle = Hardware.Computer()
handle.set_IsStorageEnabled(True)
handle.set_IsNetworkEnabled(True)
handle.set_IsMemoryEnabled(True)
handle.set_IsGpuEnabled(True)
handle.set_IsCpuEnabled(True)
handle.Open()

networkInformation = [0] # In case of multiple connections, initialized to prevent memory leaks
diskInformation = [0] # In case of multiple drives, initialized to prevent memory leaks
gpuInformation = [0] # In case of multiple GPU, initialized to prevent memory leaks

for hardware in handle.Hardware:
    if hardware.HardwareType == Hardware.HardwareType.GpuNvidia or hardware.HardwareType == Hardware.HardwareType.GpuAmd or hardware.HardwareType == Hardware.HardwareType.GpuIntel:
        gpuInformation.append(hardware)
    elif hardware.HardwareType == Hardware.HardwareType.Storage:
        diskInformation.append(hardware)
    elif hardware.HardwareType == Hardware.HardwareType.Network:
        networkInformation.append(hardware)

networkInformation.pop(0) # Removing empty slot
diskInformation.pop(0) # Removing empty slot
gpuInformation.pop(0) # Removing empty slot

app = Flask(__name__)
log = logging.getLogger('werkzeug')
log.disabled = True
app.logger.disabled = True

@app.after_request
def after_request(response):
    response.headers['Access-Control-Allow-Origin'] = "*"
    response.headers['Access-Control-Allow-Methods'] = 'PUT,GET,POST,DELETE'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization'
    return response

@app.route('/', methods=['GET'])
def home():
    return "Use path: /cpu, /gpu, /memory, /network, /filesystem"

@app.route('/cpu', methods=['GET'])
def cpu():
    return cpuModule.usage(handle.Hardware[0], Hardware.SensorType)

@app.route('/memory', methods=['GET'])
def ram():
    return ramModule.usage(handle.Hardware[1])

@app.route('/gpu', methods=['GET'])
def gpu():
    return gpuModule.usage(gpuInformation, Hardware.HardwareType, Hardware.SensorType)

@app.route('/network', methods=['GET'])
def network():
    return networkModule.usage(networkInformation)

@app.route('/filesystem', methods=['GET'])
def filesystem():
    return driveModule.usage(diskInformation)

@app.route('/clear', methods=['GET'])
def clear():
    handle.Close()
    handle.Open()
    return "Resetting hardware..."


if __name__ == '__main__':
    multiprocessing.freeze_support()
    app.run(host="localhost", port=7666, debug=False);