import json
from threading import Timer
import psutil
import platform
from datetime import datetime
import socket
import uuid
import re
import time
import logging
import cpuinfo # este es pip install py-cpuinfo
from psutil import cpu_freq


def get_size(bytes, suffix="B"):
    """
    Scale bytes to its proper format
    e.g:
        1253656 => '1.20MB'
        1253656678 => '1.17GB'
    """
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor

def System_information():  
    uname = platform.uname()
    systemname =uname.system
    node =uname.node
    release  =uname.release
    version =uname.version
    machine =uname.machine
    processor = cpuinfo.get_cpu_info()['brand_raw']
    ip =socket.gethostbyname(socket.gethostname())
    macaddr =':'.join(re.findall('..', '%012x' % uuid.getnode()))
    return {"systemname":systemname, "node":node, "release":release, "version":version, "machine":machine, "processor":processor, "ip":ip, "macaddr":macaddr}

def fullCPU():
    return cpuinfo.get_cpu_info()

def bootTime():
    boot_time_timestamp = psutil.boot_time()
    bt = datetime.fromtimestamp(boot_time_timestamp)  
    return bt.strftime("%Y-%m-%d %H:%M:%S")

def cpuFreq():
    cpu_freq = psutil.cpu_freq()
    maxFreq = cpu_freq.max
    minFreq = cpu_freq.min
    currFreq = cpu_freq.current
    return {"maxFreq":maxFreq, "minFreq":minFreq, "currFreq":currFreq}

def coreInfo():
    phisicalCores=psutil.cpu_count(logical=False)
    totalCores =psutil.cpu_count(logical=True)
    return {"phisicalCores":phisicalCores, "totalCores":totalCores}

def diskSpeed():
    disk_io = psutil.disk_io_counters()
    diskRead = get_size(disk_io.read_bytes)
    diskWrite = get_size(disk_io.write_bytes)
    return {"diskRead":diskRead, "diskWrite":diskWrite}

def diskData():
    # get all disk partitions
    # need to do lambda function
    arr = []
    partitions = psutil.disk_partitions()
    for partition in partitions:
        obj = {}
        obj["device"] = partition.device
        obj["mount"] =partition.mountpoint
        obj["fileSys"] =partition.fstype
        try:
            partition_usage = psutil.disk_usage(partition.mountpoint)
            obj["usage"] = partition_usage
        except PermissionError:
            # this can be catched due to the disk that
            # isn't ready
            continue
        obj["sizeTotal"] =get_size(partition_usage.total)
        obj["sizeUsed"] =get_size(partition_usage.used)
        obj["sizeFree"] =get_size(partition_usage.free)
        obj["sizePercent"] = partition_usage.percent
        arr.append(obj)
    return arr

def networkData():
    net_io = psutil.net_io_counters()
    bytesSent =get_size(net_io.bytes_sent)
    bytesReceived =get_size(net_io.bytes_recv) #todo
    return {"bytesSent":bytesSent, "bytesReceived":bytesReceived}

def networkInterface():
    ## Network information
    ## get all network interfaces (virtual and physical)
    #lambda also
    arr = []
    if_addrs = psutil.net_if_addrs()
    for interface_name, interface_addresses in if_addrs.items():
        for address in interface_addresses:
            obj = {}
            obj["interfaceName"] = interface_name
            if str(address.family) == 'AddressFamily.AF_INET':
                obj["ip"] =address.address
                obj["netmask"] =address.netmask
                obj["broadcast"] =address.broadcast
            elif str(address.family) == 'AddressFamily.AF_PACKET':
               obj["mac"] =address.address
               obj["macnetMask"] =address.netmask
               obj["broadcastMac"] =address.broadcast
            arr.append(obj)

    return arr

def cpuUsageCores():
    arr = []
    for i, percentage in enumerate(psutil.cpu_percent(percpu=True, interval=0.3)):
        obj = {}
        obj.core = percentage
        obj.usage=psutil.cpu_percent()
        arr.append(obj)
    return arr

def cpuUsage():
    arrpercents = psutil.cpu_percent(percpu=True, interval=0.3)
    #sum the arr
    total = 0
    for i in arrpercents:
        total += i
    return total/len(arrpercents)

def swapDataValues():
    swap = psutil.swap_memory()
    total = get_size(swap.total)
    used = get_size(swap.used)
    free = get_size(swap.free)
    percent = swap.percent
    return {"total":total, "used":used, "free":free, "percent":percent}

def ramValues():
    ram = psutil.virtual_memory()
    total = get_size(ram.total)
    used = get_size(ram.used)
    free = get_size(ram.free)
    percent = ram.percent
    return {"total":total, "used":used, "free":free, "percent":percent}

def cpuInfo():
    return cpuinfo.get_cpu_info_json()

   

