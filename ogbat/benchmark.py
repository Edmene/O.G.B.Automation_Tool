import os
import time
from subprocess import Popen, PIPE
import threading
import sqlite3
import re
import installed_games
import platform
if(platform.system() == "Windows"):
    import win32com.client

class Benchmark(object):
   
    def __init__(self):
        self.benchmark=self._launch_game()
        
    def keypress(self, delay, extra_time):
        if(delay == "y"):
            time.sleep(30+extra_time)
        if(delay == "n"):
            time.sleep(30)                                
        """When using other key combination to glxosd, change the content of key according with
        the documentation in http://linux.die.net/man/1/xte.
        
        When using other key combination with fraps, change the content of key according with
        the documentation in http://www.developerfusion.com/article/57/sendkeys-command/
        """        
        #Call xte and insert the key combination that is sended system wide.
        if(platform.system() != "Windows"):
            keys = '''keydown Shift_L
key F9
keyup Shift_L
'''
            p = Popen(['xte'], stdin=PIPE, shell=True)
            p.stdin.write(bytes(keys.encode(encoding='utf_8', errors='strict')))  
            p.stdin.close()
        else:
            keys="{F11}"
            script = win32com.client.Dispatch("WScript.Shell")
            script.SendKeys(keys)
        
    #End the glxosd benchmark and closes it.
    def _kill_glxosd(self, duration):
        time.sleep(duration)
        Benchmark.keypress(self, "", "")                                                    
        os.system("killall xterm")
        
    def _benchmark_file(self, tool_path):
        if(platform.system() == "Windows"):
            benchmark_path=tool_path+"benchmarks"
        else:
            benchmark_path="/tmp"
        files=os.listdir(benchmark_path)
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
            if(re.match("Voglperf",str(line))):
                voglperf=str(line)                
                voglperf=re.sub("Voglperf:","",voglperf)
                voglperf=re.sub("\n", "",voglperf)
            if(re.match("Fraps",str(line))):
                fraps=str(line)                
                fraps=re.sub("Fraps:","",fraps)
                fraps=re.sub("\n", "",fraps)            
        f.close()
        if(platform.system() != "Windows"):
            tool_path=voglperf
        else:
            tool_path=fraps
        return tool_path, delay
        
    #Deals with the user selection of benchmark tool and game, also start the selected game.
    def _launch_game(self):
        options=["voglperf","glxosd","voglperf executable"]        
        wait=""
        m=-1
        installed_games.InstalledGames().games        
        try:
            g=Benchmark._access_db(self)
            file_content=Benchmark._read_options(self)
            if(platform.system() == "Windows"):
                pass
            else:
                print ("Benchmark tools")
                i=0
                for a in range(0, len(options)):
                    print(str(i)+") "+options[a])
                    i=i+1        
                method = input("Choice:")
                m=int(method)
            if((m >= 0 and m <= 2) or platform.system() == "Windows"):
                s=0
                if(m != 2):            
                    print ("Select the game to run")
                    i=0
                    for a in range(0, len(g)):
                        print(str(i)+") "+g[a][1])
                        i=i+1    
                    s = input("Choice: ")
                    s=int(s)
                if((s >= 0 and s <= len(g)) or m == 2):
                    t = input("How long will be the benchmark? (seconds[60-300]):")
                    t=int(t)
                    if(t >= 60 and t <= 300):
                        print ("Glxosd method have a standard time dalay, 'y' option increment it to "+str(30+file_content[1])+" seconds")
                        while(wait != "y" and wait != "n"):                    
                            wait = input("Do you want to wait "+str(file_content[1])+" seconds to start? y/n:").lower()
                        if(platform.system() != "Windows"):
                            if(m == 0):
                                game_id=str(g[s][0]) 
                                if(wait == "n"):
                                    sb=Popen([file_content[0]+' -x -l '+str(g[s][0])], stdin=PIPE, shell=True)                                
                                if(wait == "y"):
                                    sb=Popen([file_content[0]+' -x '+str(g[s][0])], stdin=PIPE, shell=True)
                                    time.sleep(file_content[1])
                                    sb.stdin.write(bytes(("logfile start "+str(t)).encode("utf-8")))
                                    sb.stdin.close()
                                time.sleep(t)
                                sb.terminate()
                                os.system("killall xterm")
                            if(m == 1):
                                game_id=str(g[s][0])                                                   
                                def _glxosd():
                                    Popen(["xterm -e glxosd -s steam steam://rungameid/"+str(g[s][0])], stdin=PIPE, shell=True)                                                      
                                if(wait == "y"):
                                    t=t+file_content[1]
                                threading.Thread(target=_glxosd())                                                         
                                Benchmark.keypress(self, wait, file_content[1])
                                threading.Thread(target=Benchmark._kill_glxosd(self, t))
                            if(m == 2):
                                game_id="ns"
                                exec_path=input("Type the path to the game executable:") 
                                if(wait == "n"):
                                    sb=Popen([file_content[0]+' -x -l '+exec_path], stdin=PIPE, shell=True)                                
                                if(wait == "y"):
                                    sb=Popen([file_content[0]+' -x '+exec_path], stdin=PIPE, shell=True)
                                    time.sleep(file_content[1])
                                    sb.stdin.write(bytes(("logfile start "+str(t)).encode("utf-8")))
                                    sb.stdin.close()
                                time.sleep(t)
                                sb.terminate()
                                os.system("killall xterm")
                        else:
                            game_id=str(g[s][0])
                            if(wait == "y"):
                                t=t+file_content[1] 
                            game=Popen(["cmd"], stdin=PIPE, shell=True)
                            command=('start steam://rungameid/'+str(g[s][0])+'\n').encode("utf-8")
                            game.stdin.write(bytes(command))
                            game.stdin.close()
                            Popen([file_content[0]+"fraps.exe"], stdin=PIPE, shell=True)                   
                            threading.Thread(target=Benchmark.keypress("", wait, file_content[1]))
                            time.sleep(t)
                            threading.Thread(target=Benchmark.keypress("", "", ""))
                        benchmark_file=Benchmark._benchmark_file(self, file_content[0])                                                   
                        return benchmark_file,file_content[0],game_id
                    else:
                        if(t < 60):
                            otherInfo=" Bellow minimal time."
                        else:
                            otherInfo=" Over maximum time."
                        print ("Invalid time."+otherInfo)
                else:
                    print ("Invalid game option.")
            else:
                print ("Invalid tool option.")
        except UnboundLocalError:
            print("The configuration file appears to be incomplete or don't exists.")
        except ValueError:
            print("Appears that you inserted a invalid option.")                
        except KeyboardInterrupt:
            pass          
