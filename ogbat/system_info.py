import re
import subprocess
from django.utils.translation import trim_whitespace

class SystemInformations:           
    
    def __init__(self):        
        self.kernelV = self._kernel()
        self.cpu = self._cpu()
        self.gpu = self._gpu()        
        self.desktopEnv = self._desktop()
        self.memory = self._memory()
        self.resolution = self._resolution()            
        
    def _kernel(self):
        kernelV = str(subprocess.getoutput("uname -s")) + " "
        kernelV = kernelV + str(subprocess.getoutput("uname -r")) + " "
        kernelV = kernelV + str(subprocess.getoutput("uname -m"))
        return kernelV       
        
    def _cpu(self):
        f = open("/proc/cpuinfo", 'r')
        for line in f:     
            if(re.match("model name",str(line))):
                cpuM=str(line)
        f.close()
        cpuM=re.sub("model name *.: ", "", cpuM)
        cpuM=re.sub(" CPU.*", "", cpuM)
        cpuM=re.sub("(.(R)).", "", cpuM)
        cpuM=re.sub("(.(TM).)", "", cpuM)
        return cpuM
    
    def _memory(self):
        f = open("/proc/meminfo", 'r')
        for line in f:     
            if(re.match("MemTotal:",str(line))):
                mem=str(line)
        f.close()
        mem=re.sub("MemTotal: *. ", "", mem)
        mem=re.sub(" [a-z].*", "", mem)
        mem = str(round(int(mem)/1024))+"MB"
        return mem
        
    def _gpu(self):
        vendor=str(subprocess.getoutput("grep 'Creating default' /var/log/Xorg.0.log"))
        if(re.findall("NVIDIA", vendor)):
            vendorMemory=vendor="NVIDIA"
        elif(re.findall("Advanced", vendor)):
            vendorMemory=vendor="AMD"
        elif(re.findall("intel", vendor)):
            vendor="Intel"
            vendorMemory=vendor.lower()
        gpuMem = str(subprocess.getoutput("grep '"+vendorMemory+"(0): Memory' /var/log/Xorg.0.log"))        
        gpuMem=re.sub("\[.* [0-9].\.[0-9]*]", "", gpuMem)
        gpuMem=re.sub("\(.*\):", "", gpuMem)
        gpuMem=trim_whitespace(re.sub("Memory: ", "", gpuMem))
        gpuMem=re.sub("k.*", "", gpuMem)
        gpuMem=str(int(gpuMem)/1024)+"MB"        
        try:            
            '''
            vendor = str(subprocess.getoutput("lspci -v | grep 'VGA compatible controller:'"))
            vendor = re.sub("0[0-9].[0-9].\.[0-9] VGA compatible controller*: ", "", vendor)
            vendor = vendor[0:8]
            vendor = re.sub(" .*","",vendor)       
            '''            
            if(vendor == "Intel"):
                gpuCard=str(subprocess.getoutput("grep 'Integrated' /var/log/Xorg.0.log"))
                gpuCard=re.sub("Integrated Graphics Chipset: ","",gpuCard)
                gpuCard=re.sub("\(R\)","",gpuCard)
                driverType="Opensource"                
            if(vendor == "NVIDIA"):
                gpuCard=str(subprocess.getoutput("grep 'NVIDIA GPU GeF' /var/log/Xorg.0.log"))
                gpuCard=gpuCard[40:56]                                
                if(subprocess.getoutput("command -v nvidia-smi >/dev/null 2>&1 || { return 0; }") != 0):
                    gpu = str(subprocess.getoutput("nvidia-smi | grep Driver"))
                    gpuDriver = gpu[12:20]
                    gpuDriver=trim_whitespace(gpuDriver)
                    '''    
                    gpu = str(subprocess.getoutput("nvidia-smi | grep GeForce"))
                    gpuCard = gpu[5:27]
                    gpuCard="NVidia "+trim_whitespace(gpuCard)
                    '''
                    driverType="Proprietary"
                else:
                    gpuDriver=""
                    driverType="Opensource"  
            else:
                if(subprocess.getoutput("command -v fglrxinfo >/dev/null 2>&1 || { return 0; }") != 0):
                    gpu = str(subprocess.getoutput("fglrxinfo | grep Radeon"))
                    gpuCard = gpu[28]
                    gpuCard=trim_whitespace(gpuCard)
                    driverType="Proprietary"
                    gpu = str(subprocess.getoutput("fglrxinfo | grep version"))
                    gpuDriver = gpu[23:37]
                    gpuDriver = re.sub("[a-z].*[A-Z].*","", gpuDriver)
                    gpuDriver=trim_whitespace(gpuDriver)                
                else:
                    gpu=str(subprocess.getoutput("lspci -v | grep Radeon"))
                    gpu=re.sub("^(\[Radeon .*\] )", "", gpu)
                    gpuCard=re.sub("$\[\]","",gpu)
                    driverType="Opensource"
                    gpuDriver=""                                        
        except:
            if(vendor != "AMD"):
                vendor = "NVIDIA"    
            else:
                vendor = "AMD"                
                print ("Error while executing a gpu detection function of "+vendor)        
        return gpuCard,gpuDriver,driverType,gpuMem
    
    def _desktop(self):
        desktopEnv = str(subprocess.getoutput("env | grep 'DESKTOP_SESSION'"))
        desktopEnv = re.sub("DESKTOP_SESSION=", "", desktopEnv)
        return desktopEnv
    
    def _resolution(self):
        width=0
        heigth=0
        resolution = str(subprocess.getoutput("xrandr | grep connected"))
        resolution = re.sub("[a-z]*-[0-9]*", "", resolution)
        resolution = re.sub("\).*", "", resolution)
        resolution = re.sub("\+.* ", "", resolution)
        resolution = re.sub("[^0-9^\n]*", "", resolution)
        parseResolution = resolution.split("\n")
        for x in range(0, len(parseResolution)):
            if(width != 0):
                if(parseResolution[x][0:4] != ""):
                    width=width+int(parseResolution[x][0:4])
            else:
                if(parseResolution[x][0:4] != ""):
                    width=int(parseResolution[x][0:4])
                    
            if(heigth != 0):
                if(parseResolution[x][4:9] != ""):
                    if(heigth < int(parseResolution[x][4:9])):
                        heigth = int(parseResolution[x][4:9])
            else:
                if(parseResolution[x][4:9] != ""):
                    heigth=int(parseResolution[x][4:9])
        totalResolution = str(width)+"x"+str(heigth)
        return totalResolution
    
if __name__ == '__main__':
        s = SystemInformations()        
        
    
