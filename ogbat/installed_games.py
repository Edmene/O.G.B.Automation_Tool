import re
import subprocess
from bs4 import BeautifulSoup
import urllib.request as request
import platform
import sqlite3

class InstalledGames(object):  
    
    def __init__(self):
        self.games=self._games()
    
    def _games(self):
        conn = sqlite3.connect('ogbatdb.db')
        c=conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS
        game (id_game INTEGER PRIMARY KEY,
        stdb_game INTEGER,
        name_game BLOB);       
        ''')
        conn.commit()        
        games=""
        f = open("options.conf", 'r')
        for line in f:
            if(re.match("Steam",str(line))):
                directories=str(line) 
                directories=re.sub("SteamDirectories:", "", directories)
                directory=directories.split(",")               
        f.close()
        for a in range(0, len(directory)):
            if(platform.system() != "Windows"):
                command="ls "+directory[a]+" | grep appmanifest"
            else:
                command='dir '+directory[a]+' | find "appmanifest"'
            command=re.sub("\n", "", command)
            gamesString = str(subprocess.getoutput(command))
            if(platform.system() != "Windows"):
                gamesString = re.sub("[^0-9^\n]*", "",gamesString)
            else:
                gamesString = re.sub("[0-9][0-9]\/[0-9][0-9]\/[0-9][0-9][0-9][0-9]  ", "",gamesString)
                gamesString = re.sub("[0-9][0-9]:[0-9][0-9]", "",gamesString)
                gamesString = re.sub(" *", "",gamesString)
                gamesString = re.sub("[0-9]*a", "",gamesString)
                gamesString = re.sub("[^0-9^\n]*", "",gamesString)
            if(len(games) == 0):
                games=gamesString.split("\n")
            else:
                games=games+gamesString.split("\n")        
                
        c.execute('SELECT stdb_game FROM game')        
        dbIds=c.fetchall()
        dbIds=list(dbIds)
            
        for a in range(0, len(dbIds)):
            fail=0
            dbIds[a]=re.sub(",\)","",str(dbIds[a]))
            dbIds[a]=re.sub("\(","",dbIds[a])
            for game in games:
                if(game != dbIds[a]):
                    fail=fail+1
            if(fail == len(games)):
                c.execute("DELETE FROM game WHERE stdb_game=?", [dbIds[a]])
                conn.commit()
        
        gamesIds=list()   
        for o in range(0,len(games)):                               
            gamesIds.insert(o, games[o])
                
        for o in range(0,len(gamesIds)):                               
            c.execute("SELECT stdb_game FROM game WHERE stdb_game=?", [gamesIds[o]])
            if(c.fetchone() != None):
                games.remove(gamesIds[o])             
            
        gamesNames = list()
        i=0
        while i < len(games):            
            url = "https://steamdb.info/app/"+games[i]+"/"
            header = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
                        'Accept-Encoding': 'none',
                        'Accept-Language': 'en-US,en;q=0.8',
                        'Connection': 'keep-alive'}            
            try:
                req = request.Request(url,headers=header)
                page = request.urlopen(req)            
                if(platform.system() != "Windows"):
                    soup = BeautifulSoup(page, "lxml")
                else:
                    soup = BeautifulSoup(page, "html.parser")
                title = str((soup.find("title").text).encode('ascii', 'ignore'))
                title=re.sub("  A.*", "", title)
                title=re.sub("b'", "", title)                    
                gamesNames.insert(i, title)                                    
                i=1+i
            except:
                pass
                games.remove(games[i])
        for o in range(0,len(games)):                 
            c.execute("INSERT INTO game VALUES(NULL,"+games[o]+",'"+gamesNames[o]+"');")
            conn.commit()           
        conn.close()