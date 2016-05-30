import requests
import system_info
import re
import bs4
from django.utils.translation import trim_whitespace
import sqlite3
import getpass
import platform

class Upload(object):
    
    def __init__(self, params):
        self.upload_data=self._upload_data(params)
        #When integrated with the other classes the params attribute should be the file path to the benchmark file and game steam id.
        
    #Set the system type in the right format for OpenGameBenchmarks.
    def _get_system_information(self):
        linux_distros_types=['Debian-based (Debian, Ubuntu, Mint, Elementary OS, SteamOS)','Arch-based (Arch, Manjaro)',
                    'Red Hat-based (RedHat, Fedora, CentOS)','Gentoo-based (Gentoo, Chromium, Funtoo)','SUSE-based',
                    'Slackware-based','Mandriva-based','Linux-other'] 
        linux_distros_types_search=['Debian-based \(Debian\, Ubuntu\, Mint\, Elementary OS\, SteamOS\)','Arch-based \(Arch\, Manjaro\)',
                    'Red Hat-based \(RedHat\, Fedora\, CentOS\)','Gentoo-based \(Gentoo\, Chromium\, Funtoo\)','SUSE-based',
                    'Slackware-based','Mandriva-based','Linux-other']   
        system_information=system_info.SystemInformations()
        distro_type=system_information.system
        if(re.search("Windows", distro_type) == None):
            if(re.search("Debian", distro_type) != None):
                distro_type=[linux_distros_types[0],linux_distros_types_search[0]]
            elif(re.search("Ubuntu", distro_type) != None):
                distro_type=[linux_distros_types[0],linux_distros_types_search[0]]
            elif(re.search("Mint", distro_type) != None):
                distro_type=[linux_distros_types[0],linux_distros_types_search[0]]
            elif(re.search("Elementary", distro_type) != None):
                distro_type=[linux_distros_types[0],linux_distros_types_search[0]]
            elif(re.search("Steam", distro_type) != None):
                distro_type=[linux_distros_types[0],linux_distros_types_search[0]]
            elif(re.search("Arch", distro_type) != None):
                distro_type=[linux_distros_types[1],linux_distros_types_search[1]]
            elif(re.search("Manjaro", distro_type) != None):
                distro_type=[linux_distros_types[1],linux_distros_types_search[1]]
            elif(re.search("RedHat", distro_type) != None and re.search("RHEL", distro_type) != None):
                distro_type=[linux_distros_types[2],linux_distros_types_search[2]]
            elif(re.search("Fedora", distro_type) != None):
                distro_type=[linux_distros_types[2],linux_distros_types_search[2]]
            elif(re.search("Cent", distro_type) != None):
                distro_type=[linux_distros_types[2],linux_distros_types_search[2]]
            elif(re.search("Gentoo", distro_type) != None):
                distro_type=[linux_distros_types[3],linux_distros_types_search[3]]
            elif(re.search("Chromium", distro_type) != None):
                distro_type=[linux_distros_types[3],linux_distros_types_search[3]]
            elif(re.search("Funtoo", distro_type) != None):
                distro_type=[linux_distros_types[3],linux_distros_types_search[3]]
            elif(re.search("SUSE", distro_type) != None):
                distro_type=[linux_distros_types[4],linux_distros_types_search[4]]
            elif(re.search("Slack", distro_type) != None):
                distro_type=[linux_distros_types[5],linux_distros_types_search[5]]
            elif(re.search("Mageia", distro_type) != None):
                distro_type=[linux_distros_types[6],linux_distros_types_search[6]]           
            else:
                distro_type=linux_distros_types[7],linux_distros_types_search[7]
        system_information.system=distro_type[0]                
        system_specs=[system_information.cpu,trim_whitespace(system_information.gpu[0]),system_information.gpu[2],distro_type[1]]
        return system_specs, system_information
        
        
    #The upload process.
    def _upload_data(self, game_info):
        try:
            login=""
            while(len(login) == 0):
                username=input("User name:")
                password=getpass.getpass("Password:")
                url="http://www.opengamebenchmarks.org/accounts/login/"
                client = requests.session()
                csrf = client.get(url).cookies['csrftoken']
                login_data = dict(username=username, password=password, csrfmiddlewaretoken=csrf)
                client.post(url, data=login_data, headers=dict(Referer=url))
                url="http://www.opengamebenchmarks.org/accounts/profile/"
                if(platform.system() != "Windows"):
                    parser="html.parser"
                else:
                    parser="lxml"
                profile=bs4.BeautifulSoup(client.get(url).content, parser)
                check=profile.find("table")
                if(check != None):
                    login="s"                
            system=Upload._get_system_information("")
            system_specs=system[0]        
            system_id=""
            #Checks if a similar system is registered and return a link id.
            def _system_check(specs):
                link=""
                url="http://www.opengamebenchmarks.org/accounts/profile/"            
                info=bs4.BeautifulSoup(client.get(url).content, parser)
                tr = info.find_all("tr")
                for tr in tr:
                    count=0 
                    for td in tr.findAll("td", {"class" : ""}):                               
                        if(re.search(system_specs[0], str(td)) != None):
                            count=count+1
                        if(re.search(system_specs[1], str(td)) != None):
                            count=count+1
                        if(re.search(system_specs[2], str(td)) != None):
                            count=count+1
                        if(re.search(system_specs[3], str(td)) != None):
                            count=count+1              
                        if(count == 4):
                            link=td.find("a", { "class" : "nounderline label label-xs label-danger" })
                            link=str(link)
                    if(len(link) != 0):
                        break
                return link
            link=_system_check(system_specs)
            if(len(link) != 0):
                system_id=re.sub("[^0-9]", "", link)
                url="http://www.opengamebenchmarks.org/system_edit/"+system_id
                page=bs4.BeautifulSoup(client.get(url).content, parser)
                sys_name = page.find_all("h2")
                sys_name=trim_whitespace(re.sub("Edit system:", "", str(sys_name)))
                sys_name=re.sub("\<\/h2\>\]", "", sys_name)
                sys_name=re.sub("\[\<h2\>", "", sys_name)
                sys_name=trim_whitespace(sys_name)
                csrf=client.get(url).cookies['csrftoken']         
                data = dict(csrfmiddlewaretoken=csrf, descriptive_name=sys_name, cpu_model=system[1].cpu, gpu_model=trim_whitespace(system[1].gpu[0]), dual_gpu="None", resolution=system[1].resolution, driver=system[1].gpu[2],
                         operating_system=system[1].system, desktop_environment=system[1].desktop_env, kernel=system[1].kernel_version, gpu_driver_version=system[1].gpu[1], additional_details="VRAM: "+system[1].gpu[3]+"RAM: "+system[1].memory)
                client.post(url, data=data, headers=dict(Referer=url))
            else:
                print("\n")
                system_name=input("Insert a name for your system:")
                url="http://www.opengamebenchmarks.org/system_add/"
                csrf=client.get(url).cookies['csrftoken']       
                data = dict(csrfmiddlewaretoken=csrf, descriptive_name=system_name, cpu_model=system[1].cpu, gpu_model=system[1].gpu[0], dual_gpu="None", resolution=system[1].resolution, driver=system[1].gpu[2],
                         operating_system=system[1].system, desktop_environment=system[1].desktop_env, kernel=system[1].kernel_version, gpu_driver_version=system[1].gpu[1], additional_details="VRAM: "+system[1].gpu[3]+"RAM: "+system[1].memory)
                client.post(url, data=data, headers=dict(Referer=url))            
                link=_system_check(system_specs)
                system_id=re.sub("[^0-9]", "", link)
                
            #Get the game name to search the id of it in OpenGameBenchmarks.
            conn = sqlite3.connect('ogbatdb.db')
            c=conn.cursor()
            #A special process in case the of the user had choose to use the voglperf filepath game start method.
            if(game_info[1] != "ns"):            
                c.execute("SELECT stdb_game,name_game FROM game WHERE stdb_game=?", [game_info[1]])
                s=0
            else:
                c.execute("SELECT stdb_game,name_game FROM game")
            g=c.fetchall()
            if(game_info == "ns"):
                print ("What game did you benchmarked?")
                i=0
                for a in range(0, len(g)):
                    print(str(i)+") "+g[a][1])
                    i=i+1    
                s = input("Choice: ")
                s=int(s)
            print("\n")
            benchmark_notes=input("Additional information about the benchmark (optional):")
            preset=["Ultra","Very High","High","Medium","Low","n.a."]
            print ("\nWhat game preset was used?")
            i=0
            for a in range(0, len(preset)):
                print(str(i)+") "+preset[a])
                i=i+1   
            p = input("Choice: ")
            p=int(p)
            url="http://www.opengamebenchmarks.org/benchmark_add/"
            csrf=client.get(url).cookies['csrftoken']
            info=bs4.BeautifulSoup(client.get(url).content, parser) 
            select = info.find_all("select", {"id": "id_game"})
            for select in select:
                for option in select.findAll("option"):
                    game_option_name=str(option.encode(encoding='ascii', errors='ignore'))
                    game_option_name=re.sub('<option value.*">', "", game_option_name)
                    game_option_name=re.sub("<\/option>", "", game_option_name)
                    game_option_name=re.sub("b'", "", game_option_name)
                    game_option_name=re.sub("\\\\'s", "'s", game_option_name)
                    game_option_name=re.sub("\\\\'S", "'S", game_option_name)
                    game_option_name=game_option_name[0:len(game_option_name)-1]               
                    game_option=str(option.encode(encoding='ascii', errors='ignore'))
                    game_option=trim_whitespace(re.sub('<option value="', "", game_option))
                    game_option=re.sub('".*', "", game_option)
                    game_option=re.sub("b'", "", game_option)
                    if(re.fullmatch(g[0][1], game_option_name) != None):
                        break
            file=open(game_info[0], 'rb')            
            data = dict(csrfmiddlewaretoken=csrf, game=game_option, user_system=system_id, frames_file={game_info[0]: file}, game_quality_preset=preset[p], additional_notes=benchmark_notes)
            client.post(url, data=data, headers=dict(Referer=url))
            client.close()
        except KeyboardInterrupt:
            pass
        except UnboundLocalError:
            print("Some variable was left empty and produced a error")
        except Exception as e:
            print("A error was occurred: "+str(e))

        
        
