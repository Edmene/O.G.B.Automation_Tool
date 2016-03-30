import os
import time
from subprocess import Popen, PIPE
import threading
import installed_games
import re

class Benchmark(object):
   
    def __init__(self):
        self.benchmark=self._launch_game()
        
    def keypress(self, delay, extra_time):
        if(delay == "y"):
            time.sleep(30+extra_time)
        if(delay == "n"):
            time.sleep(30)                                
        keys = '''keydown Shift_L
key F9
keyup Shift_L
'''
        p = Popen(['xte'], stdin=PIPE, shell=True)
        p.stdin.write(bytes(keys.encode(encoding='utf_8', errors='strict')))  
        p.stdin.close()
        p.terminate()
        
    def _kill_glxosd(self, duration):
        time.sleep(duration)
        Benchmark.keypress(self, "")                                                    
        os.system("killall xterm")
        
    def _launch_game(self):
        options=["voglperf","glxosd"]
        wait=""
        g = installed_games.InstalledGames._games(self)
        f = open("options.conf", 'r')
        for line in f:
            if(re.match("Seconds",str(line))):
                seconds=str(line)                
                seconds=re.sub("SecondsToDelay:","",seconds)
                delay=int(seconds)
            if(re.match("Voglperf",str(line))):
                voglperf=str(line)                
                voglperf=re.sub("Voglperf:","",voglperf)
                voglperf=re.sub("\n", "",voglperf)
        f.close()        
        print ("Benchmark tools")
        i=0
        for a in range(0, 2):
            print(str(i)+") "+options[a])
            i=i+1
        try:
            method = input("Choice:")
            m=int(method)
            if(m >= 0 and m <= 1): #glxosd selection
            #if(m == 0):            
                print ("Select the game to run")
                i=0
                for a in range(0, len(g[1])):
                    print(str(i)+") "+g[1][a])
                    i=i+1    
                s = input("Choice: ")
                s=int(s)
                if(s >= 0 and s <= len(g[1])):
                    t = input("How long will be the benchmark? (seconds[60-300]):")
                    t=int(t)
                    if(t >= 60 and t <= 300):
                        print ("Glxosd method have a standard time dalay, 'y' option increment it to "+str(30+delay)+" seconds")
                        while(wait != "y" and wait != "n"):                    
                            wait = input("Do you want to wait "+str(delay)+" seconds to start? y/n:").lower()
                        if(m == 0): 
                            if(wait == "n"):
                                sb=Popen([voglperf+' -x -l '+g[0][s]], stdin=PIPE, shell=True)                                
                            if(wait == "y"):
                                sb=Popen([voglperf+' -x '+g[0][s]], stdin=PIPE, shell=True)
                                time.sleep(delay)
                                sb.stdin.write(bytes(("logfile start "+str(t)).encode("utf-8")))
                                sb.stdin.close()
                            time.sleep(t)
                            os.system("killall xterm")
                            #exit
                        if(m == 1):                       
                            def _glxosd():
                                Popen(["xterm -e glxosd -s steam steam://rungameid/"+g[0][s]], stdin=PIPE, shell=True)                                
                            if(wait == "y"):
                                t=t+delay
                            threading.Thread(target=_glxosd())                                                         
                            Benchmark.keypress(self, wait, delay)
                            Benchmark._kill_glxosd(self, t)
                        benchmark_file = os.listdir("/tmp")[0]                        
                        return benchmark_file
                    else:
                        if(t < 60):
                            otherInfo=" Bellow minimal time."
                        else:
                            otherInfo=" Over maximum time."
                        print ("Invalid time."+otherInfo)
                        return 0
                else:
                    print ("Invalid game option.")
                    return 0
            else:
                print ("Invalid tool option.")
                return 0
        except(ValueError):
            print("Appears that you inserted a invalid option.")
            return 0         
        except KeyboardInterrupt:
            return 0
