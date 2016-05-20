import argparse
import platform
import system_info
import benchmark
#Discover the plataform that is being used to import the windows benchmark class only in the windows enviroment.
if(platform.system() == "Windows"):
    import benchmark_windows
import subprocess
import upload
PIPE=subprocess.PIPE
Popen=subprocess.Popen

parser = argparse.ArgumentParser()
parser.add_argument("option", help="Select what the tool should do (benchmark[b] or sysinfo[s])")
args = parser.parse_args()
#Get the option selected by the user and either show system information or start the benchmark.
if(args.option == "s"):
    system = system_info.SystemInformations()
    print ("CPU: "+str(system.cpu)+"\nSystem: "+str(system.system)+"\nKernel: "+str(system.kernelV)+"\nMemory: "+str(system.memory)+
            "\nGPU: "+str(system.gpu[0])+"\nGPU Driver: "+str(system.gpu[1])+"\nGPU Driver Type: "+str(system.gpu[2])+
            "\nGPU Memory: "+str(system.gpu[3])+"\nDesktop: "+str(system.desktopEnv)+"\nResolution:"+str(system.resolution))
    
elif(args.option == "b"):
    benchmark_info=""
    if(platform.system() != "Windows"):
        benchmark_file = benchmark.Benchmark().benchmark
        benchmark_info=["/tmp/"+benchmark_file[0],benchmark_file[1]]        
    else:
        benchmark_file = benchmark_windows.Benchmark().benchmark
        benchmark_info=[benchmark_file[1]+"/"+benchmark_file[0],benchmark_file[2]]              
    print("\n")
    upload.Upload(benchmark_info)            
