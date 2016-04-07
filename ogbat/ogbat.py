import argparse
import platform
import system_info
import benchmark
if(platform.system() == "Windows"):
    import benchmark_windows
import subprocess
PIPE=subprocess.PIPE
Popen=subprocess.Popen

parser = argparse.ArgumentParser()
parser.add_argument("option", help="Select what the tool should do (benchmark[b] or sysinfo[s])")
args = parser.parse_args()
if(args.option == "s"):
    system = system_info.SystemInformations()
    print ("CPU: "+str(system.cpu)+"\nSystem: "+str(system.system)+"\nKernel: "+str(system.kernelV)+"\nMemory: "+str(system.memory)+
            "\nGPU: "+str(system.gpu[0])+"\nGPU Driver: "+str(system.gpu[1])+"\nGPU Driver Type: "+str(system.gpu[2])+
            "\nGPU Memory: "+str(system.gpu[3])+"\nDesktop: "+str(system.desktopEnv)+"\nResolution:"+str(system.resolution))
    
elif(args.option == "b"):
    if(platform.system() != "Windows"):
        benchmark_file = benchmark.Benchmark().benchmark     
        print(benchmark_file)
        #upload
        #os.remove("/tmp/"+benchmark_file)
    else:
        benchmark_file = benchmark_windows.Benchmark().benchmark
        print(benchmark_file[0])
        #upload        
        #os.remove(benchmark_file[1]+"/"+benchmark_file[0])  
            