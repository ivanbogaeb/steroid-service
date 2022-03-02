import os
import sys
import clr
from flask import Flask, request
import inspect

import cpu as cpuModule
import ram as ramModule
import gpu as gpuModule
import network as networkModule
import drive as driveModule

#OpenHardwareMonitorLib =  r""+os.getcwd()+"/OpenHardwareMonitorLib.dll"
#MonoPosixNETStandard =  r""+os.getcwd()+"/Mono.Posix.NETStandard.dll"
#HidSharp = r""+os.getcwd()+"/HidSharp.dll"

#sys.path.append(OpenHardwareMonitorLib)
#sys.path.append(MonoPosixNETStandard)
#sys.path.append(HidSharp)

clr.AddReference(r""+os.getcwd()+"\\LibreHardwareMonitorLib.dll")
#clr.AddReference('OpenHardwareMonitorLib')
#clr.AddReference('Mono.Posix.NETStandard')
clr.AddReference(r""+os.getcwd()+"/HidSharp.dll")

from LibreHardwareMonitor import Hardware
#from OpenHardwareMonitor import Hardware as HardwareOpen

handle = Hardware.Computer()
#openHardware = HardwareOpen.Computer()

handle.set_IsStorageEnabled(True)
handle.set_IsNetworkEnabled(True)
handle.set_IsMemoryEnabled(True)
handle.set_IsGpuEnabled(True)
handle.set_IsCpuEnabled(True)
handle.set_IsControllerEnabled(True)
handle.set_IsMotherboardEnabled(True)

#openHardware.HDDEnabled = True

handle.Open()
#openHardware.Open()

networkInformation = [] # In case of multiple connections
diskInformation = [] # In case of multiple drives
gpuInformation = [] # In case of multiple GPU

for hardware in handle.Hardware:
    if hardware.HardwareType == 4: #GPU Variants
        gpuInformation.append(hardware)
    elif hardware.HardwareType == 6: #Storage only works as Admin
        diskInformation.append(hardware)
    elif hardware.HardwareType == 7:
        networkInformation.append(hardware)

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return "Use path: /cpu, /gpu, /ram, /network, /filesystem"

@app.route('/cpu', methods=['GET'])
def cpu():
    return cpuModule.usage(handle.Hardware[0])

@app.route('/ram', methods=['GET'])
def ram():
    return ramModule.usage(handle.Hardware[1])

@app.route('/gpu', methods=['GET'])
def gpu():
    return gpuModule.usage(gpuInformation)

@app.route('/network', methods=['GET'])
def network():
    return networkModule.usage(networkInformation)

@app.route('/filesystem', methods=['GET'])
def filesystem():
    return driveModule.usage(diskInformation)

if __name__ == '__main__':
    app.run(host="localhost", port=7666, debug=True);