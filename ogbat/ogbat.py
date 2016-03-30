import argparse
import system_info
import benchmark
import benchmark_windows
import platform

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
        benchmark = benchmark.Benchmark._launch_game("")
    else:
        benchmark = benchmark_windows.Benchmark._launch_game("")
    