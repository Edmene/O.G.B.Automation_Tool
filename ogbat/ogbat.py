import argparse
import system_info
import benchmark

parser = argparse.ArgumentParser()
parser.add_argument("option", help="Select what the tool should do (benchmark[b] or sysinfo[s])")
args = parser.parse_args()
if(args.option == "s"):
    system = system_info.SystemInformations()
    print (system.cpu)
    
elif(args.option == "b"):
    benchmark = benchmark.Benchmark._launch_game("")
    
