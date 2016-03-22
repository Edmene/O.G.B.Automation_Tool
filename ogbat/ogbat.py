import argparse
import system_info
import benchmark

parser = argparse.ArgumentParser()
parser.add_argument("option", help="Select what the tool should do (benchmark[b] or sysinfo[s])")
args = parser.parse_args()
if(args.option == "s"):
    system = system_info.SystemInformations()
    print ("CPU: "+system.cpu+"Kernel: "+system.kernelV+"\nMemory: "+system.memory+
           "\nGPU: "+system.gpu[0]+"\nGPU Driver: "+system.gpu[1]+"\nGPU Driver Type: "+system.gpu[2]+
           "\nGPU Memory: "+system.gpu[3]+"\nDesktop: "+system.desktopEnv+"\nResolution:"+system.resolution)
    
elif(args.option == "b"):
    benchmark = benchmark.Benchmark._launch_game("")
    
