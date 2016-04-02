import os
import time
from subprocess import Popen, PIPE
import threading
import installed_games
import re

class Benchmark(object):
   
    def __init__(self):
        self.benchmark=self._launch_game()
        
    def keypress(self, delay, extra_time, t):        
        script = win32com.client.Dispatch("WScript.Shell")        
        if(delay == "y"):
            time.sleep(30+extra_time)
        if(delay == "n"):
            time.sleep(30)
        script.SendKeys("{F11}")     
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
                    if(wait == "y"):
                        t=t+delay 
                    game=Popen(["cmd"], stdin=PIPE, shell=True)
                    command=('start steam://rungameid/'+g[0][s]+'\n').encode("utf-8")
                    game.stdin.write(bytes(command))
                    game.stdin.close()
                    Popen([fraps+"fraps.exe"], stdin=PIPE, shell=True)                   
                    threading.Thread(target=Benchmark.keypress("", wait, delay, t))
                            #exit
                    time.sleep(t)
                    threading.Thread(target=Benchmark.keypress("", "", "", t))
                    a=0
                    files=os.listdir(fraps+"benchmarks")
                    benchmark_file=""
                    for a in range (len(files, 0, -1)):
                        if(re.search(".csv", files[a])):
                            benchmark_file = files[a]
                            break                     
                    return benchmark_file, fraps
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
