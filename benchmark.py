import os
import time
from subprocess import Popen, PIPE
import threading
import installed_games
import glob

class Benchmark(object):
    '''
    classdocs
    '''


    def __init__(self):
        self.benchmark=self._launch_game()
        '''
        Constructor
        '''
        
    def keypress(self, delay):
        if(delay == "y"):
            time.sleep(50)
        if(delay == "n"):
            time.sleep(20)                                
        keys = '''keydown Shift_L
key F9
keyup Shift_L
'''
        p = Popen(['xte'], stdin=PIPE, shell=True)
        p.stdin.write(bytes(keys.encode(encoding='utf_8', errors='strict')))  
        p.stdin.close()
        os.system("killall xte")
        
    def _launch_game(self):
        g = installed_games.InstalledGames._games(self)
        options=["voglperf","glxosd"]
        wait=""
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
                    print ("Glxosd method have a standard time dalay, 'y' option increment it to 50 seconds")
                    while(wait != "y" and wait != "n"):                    
                        wait = input("Do you want to wait 30 seconds to start? y/n:").lower()                                                                 
                    if(t >= 60 and t <= 300):
                        if(m == 0 and wait == "n"):
                            sb=Popen(['/home/$USER/Downloads/voglperf-master/bin/voglperfrun32 -x -l '+g[0][s]], stdin=PIPE, shell=True)
                            time.sleep(t)
                            os.system("killall xterm")
                        if(m == 0 and wait == "y"):
                            sb=Popen(['/home/$USER/Downloads/voglperf-master/bin/voglperfrun32 -x '+g[0][s]], stdin=PIPE, shell=True)
                            time.sleep(30)
                            sb.stdin.write(bytes(("logfile start "+str(t)).encode("utf-8")))
                            sb.stdin.close()
                            time.sleep(t)
                            os.system("killall xterm")
                        if(m == 1):                       
                            def _glxosd():
                                Popen(["xterm -e glxosd -s steam steam://rungameid/"+g[0][s]], stdin=PIPE, shell=True)                                                             
                            def _kill_glxosd(t):
                                time.sleep(t)
                                Benchmark.keypress("")                                                    
                                os.system("killall xterm")
                            if(wait == "n"):
                                threading.Thread(target=_glxosd())                            
                                Benchmark.keypress(wait)
                                _kill_glxosd(t)                            
                            if(wait == "y"):
                                t=t+30
                                threading.Thread(target=_glxosd())
                                Benchmark.keypress(wait)                            
                                _kill_glxosd(t)
                            
                        benchmark_file = min(glob.iglob("/tmp/*.csv"), key=os.path.getctime)
                        return benchmark_file
                    else:
                        if(t < 60):
                            otherInfo=" Bellow minimal time."
                        else:
                            otherInfo=" Over maximum time."
                        print ("Invalid time."+otherInfo)
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
    
        
      
if __name__ == '__main__':
    bench = Benchmark()
    print (bench)
