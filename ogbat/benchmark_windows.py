import os
import time
from subprocess import Popen, PIPE
import threading
import installed_games
import re
import pywinauto

class Benchmark(object):
   
    def __init__(self):
        self.benchmark=self._launch_game()
        
    def keypress(self, delay, extra_time, t, path):
        if(delay == "y"):
            time.sleep(30+extra_time)
        if(delay == "n"):
            time.sleep(30)
        p = pywinauto.Application.start(r""+path+"\fraps.exe")        
        p.TypeKeys("{F11}")
        time.sleep(t)
        p.TypeKeys("{F11}")          
        os.system("taskkill /IM fraps.exe") 
        
    def _launch_game(self):
        wait=""
        g = installed_games.InstalledGames._games(self)
        f = open("options.conf", 'r')
        for line in f:
            if(re.match("Seconds",str(line))):
                seconds=str(line)                
                seconds=re.sub("SecondsToDelay:","",seconds)
                delay=int(seconds)
            if(re.match("Fraps",str(line))):
                fraps=str(line)                
                fraps=re.sub("Fraps:","",fraps)
                fraps=re.sub("\n", "",fraps)
        f.close()        
        try:                      
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
                    print ("Fraps method have a standard time dalay, 'y' option increment it to "+str(30+delay)+" seconds")
                    while(wait != "y" and wait != "n"):                    
                        wait = input("Do you want to wait "+str(delay)+" seconds to start? y/n:").lower()
                    game = Popen(["steam steam://rungameid/"+g[0][s]], stdin=PIPE, shell=True)  
                    if(wait == "y"):
                        t=t+delay
                    threading.Thread(target=Benchmark.keypress(self, wait, delay, t, fraps))                    
                    time.sleep(t+2)
                    game.terminate()
                            #exit                        
                    benchmark_file = os.listdir(fraps+"\Benchmarks")[0]                        
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
        except(ValueError):
            print("Appears that you inserted a invalid option.")
            return 0         
        except KeyboardInterrupt:
            return 0
