import argparse
import system_info
import benchmark
import benchmark_windows
import platform
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
        benchmark_file = benchmark.Benchmark._launch_game("")
        #upload
        subprocess.call("rm /tmp/"+benchmark_file)
    else:
        benchmark_file = benchmark_windows.Benchmark._launch_game("")
        #upload
        print(benchmark_file[0])
        game=Popen(["cmd"], stdin=PIPE, shell=True)
        command=('del '+benchmark_file[1]+"/"+benchmark_file[0]+"\n").encode("utf-8")
        game.stdin.write(bytes(command))
        selection=input("Please select the answer equivalent to yes")
        command2=(str(selection)+"\n").encode("utf-8")
        game.stdin.write(bytes(command2))
        game.stdin.close()
            
