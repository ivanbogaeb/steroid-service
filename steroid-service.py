import os
import sys
import clr
from flask import Flask, request

import cpu as cpuModule
import ram as ramModule
import gpu as gpuModule

OpenHardwareMonitorLib = r""+os.getcwd()+"/OpenHardwareMonitorLib.dll"
MonoPosixNETStandard =  r""+os.getcwd()+"C:/Users/N0XT/Desktop/steroid-service/Mono.Posix.NETStandard.dll"

sys.path.append(OpenHardwareMonitorLib)
sys.path.append(MonoPosixNETStandard)

clr.AddReference('OpenHardwareMonitorLib')
clr.AddReference('Mono.Posix.NETStandard')

from OpenHardwareMonitor import Hardware

computer = Hardware.Computer()
computer.MainboardEnabled = True
computer.CPUEnabled = True
computer.RAMEnabled = True
computer.GPUEnabled = True
computer.HDDEnabled = True

computer.Open()

cpuInformation = []
ramInformation = []
gpuInformation = []
diskInformation = []

for hardware in computer.Hardware:
    if hardware.HardwareType ==  2:
        cpuInformation.append(hardware)
    elif hardware.HardwareType == 3:
        ramInformation.append(hardware)
    elif hardware.HardwareType == 4:
        gpuInformation.append(hardware)
    elif hardware.HardwareType == 8:
        diskInformation.append(hardware)

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return "Use path: /cpu, /gpu, /ram, /filesystem"

@app.route('/cpu', methods=['GET'])
def cpu():
    args = request.args
    function = args.get("function")
    if function is None:
        return "Query parameter named 'function' is missing, try using 'minimal', 'detailed'"
    elif "minimal" in function:
        return cpuModule.minimal(cpuInformation)
    elif "detailed" in function:
        return cpuModule.detailed(cpuInformation)

@app.route('/ram', methods=['GET'])
def ram():
    return ramModule.usage(ramInformation)

@app.route('/gpu', methods=['GET'])
def gpu():
    return gpuModule.usage(gpuInformation)

@app.route('/disk', methods=['GET'])
def disk():
    return diskModule.usage(diskInformation)

if __name__ == '__main__':
    app.run(host="localhost", port=7666, debug=True);