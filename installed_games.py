import re
import subprocess
from bs4 import BeautifulSoup
import urllib.request as urllib2


class InstalledGames(object):  
    
    def __init__(self):
        self.games=self._games()     
        
    
    def _games(self):
        gamesString = str(subprocess.getoutput("ls -a /media/Backup/steamapps/ | grep appmanifest"))
        gamesString = re.sub("[^0-9^\n]*", "",gamesString)
        games=gamesString.split("\n")
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
            req = urllib2.Request(url,headers=header)
            page = urllib2.urlopen(req)
            soup = BeautifulSoup(page, "lxml")
            title = str((soup.find("title").text).encode('ascii', 'ignore'))
            title=re.sub("  A.*", "", title)
            title=re.sub("b'", "", title)                    
            gamesNames.insert(i, title)                       
            i=1+i    
        return games, gamesNames  
            
         
      
    
