import os
import time
from subprocess import Popen, PIPE
import threading
import installed_games
import re
import win32com.client
import sqlite3

class Benchmark(object):
   
    def __init__(self):
        self.benchmark=self._launch_game()
        
    def keypress(self, delay, extra_time, t):        
        script = win32com.client.Dispatch("WScript.Shell")        
        if(delay == "y"):
            time.sleep(30+extra_time)
        if(delay == "n"):
            time.sleep(30)
        """When using other key combination with fraps change the content of key according with
        the documentation in http://www.developerfusion.com/article/57/sendkeys-command/
        """
        script.SendKeys("{F11}")
        
    #Search for the benchmark file in fraps directory.
    def _benchmark_file(self, fraps):
        files=os.listdir(fraps+"benchmarks")
        for a in range (0, len(files)):
            if(re.search(".csv", files[a])):
                benchmark_file = files[a]
                break
        return benchmark_file
    
    #Get the database game list.
    def _access_db(self):
        installed_games.InstalledGames().games
        conn = sqlite3.connect('ogbatdb.db')
        c=conn.cursor()
        c.execute("SELECT stdb_game,name_game FROM game")
        games=c.fetchall()
        conn.close()
        return games
    
    #Get the option file information.
    def _read_options(self):
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
        return fraps, delay 
         
    #Deals with the user selection of benchmark tool and game, also start the selected game.
    def _launch_game(self):
        wait=""
        g=Benchmark._access_db_db("")        
        options=Benchmark._read_options("")       
        try:                      
            print ("Select the game to run")
            i=0
            for a in range(0, len(g)):
                print(str(i)+") "+g[a][1])
                i=i+1    
            s = input("Choice: ")
            s=int(s)
            if(s >= 0 and s <= len(g)):
                t = input("How long will be the benchmark? (seconds[60-300]):")
                t=int(t)
                if(t >= 60 and t <= 300):
                    print ("Fraps method have a standard time dalay, 'y' option increment it to "+str(30+options[1])+" seconds")
                    while(wait != "y" and wait != "n"):                    
                        wait = input("Do you want to wait "+str(options[1])+" seconds to start? y/n:").lower()
                    if(wait == "y"):
                        t=t+options[1] 
                    game=Popen(["cmd"], stdin=PIPE, shell=True)
                    command=('start steam://rungameid/'+str(g[s][0])+'\n').encode("utf-8")
                    game.stdin.write(bytes(command))
                    game.stdin.close()
                    Popen([options[0]+"fraps.exe"], stdin=PIPE, shell=True)                   
                    threading.Thread(target=Benchmark.keypress("", wait, options[1], t))
                            #exit
                    time.sleep(t)
                    threading.Thread(target=Benchmark.keypress("", "", "", t))
                    benchmark_file=Benchmark._benchmark_file(self, options[0])                                         
                    return benchmark_file, options[0], str(g[s][0])
                else:
                    if(t < 60):
                        additional_info=" Bellow minimal time."
                    else:
                        additional_info=" Over maximum time."
                    print ("Invalid time."+additional_info)
                    return 0
            else:
                print ("Invalid game option.")      
        except ValueError:
            print("Appears that you inserted a invalid option.")
        except UnboundLocalError:
            print("The configuration file appears to be incomplete or don't exists.")      
        except KeyboardInterrupt:
            pass
