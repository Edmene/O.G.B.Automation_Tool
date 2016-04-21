import requests
import system_info
import re
import bs4
from django.utils.translation import trim_whitespace

class Upload(object):
    
    def __init__(self, params):
        self.data=self._data(params) 
        #When integrated with the other classes the params attribute should be the file path to the benchmark file.    
        
    def _data(self, file):
        username=input("Please insert your user name")
        password=input("Now your password")
        url="http://www.opengamebenchmarks.org/accounts/login/"
        client = requests.session()
        csrf = client.get(url).cookies['csrftoken']
        login_data = dict(username=username, password=password, csrfmiddlewaretoken=csrf)
        client.post(url, data=login_data, headers=dict(Referer=url)) 
              
        linux_systems=['Debian-based (Debian, Ubuntu, Mint, Elementary OS, SteamOS)','Arch-based (Arch, Manjaro)',
                    'Red Hat-based (RedHat, Fedora, CentOS)','Gentoo-based (Gentoo, Chromium, Funtoo)','SUSE-based',
                    'Slackware-based','Mandriva-based','Linux-other'] 
        linux_systems_search=['Debian-based \(Debian\, Ubuntu\, Mint\, Elementary OS\, SteamOS\)','Arch-based \(Arch\, Manjaro\)',
                    'Red Hat-based \(RedHat\, Fedora\, CentOS\)','Gentoo-based \(Gentoo\, Chromium\, Funtoo\)','SUSE-based',
                    'Slackware-based','Mandriva-based','Linux-other']   
        system_information=system_info.SystemInformations()
        system=system_information.system
        if(re.search("Windows", system) == None):
            if(re.search("Debian", system) != None):
                system=[linux_systems[0],linux_systems_search[0]]
            elif(re.search("Ubuntu", system) != None):
                system=[linux_systems[0],linux_systems_search[0]]
            elif(re.search("Mint", system) != None):
                system=[linux_systems[0],linux_systems_search[0]]
            elif(re.search("Elementary", system) != None):
                system=[linux_systems[0],linux_systems_search[0]]
            elif(re.search("Steam", system) != None):
                system=[linux_systems[0],linux_systems_search[0]]
            elif(re.search("Arch", system) != None):
                system=[linux_systems[1],linux_systems_search[1]]
            elif(re.search("Manjaro", system) != None):
                system=[linux_systems[1],linux_systems_search[1]]
            elif(re.search("RedHat", system) != None and re.search("RHEL", system) != None):
                system=[linux_systems[2],linux_systems_search[2]]
            elif(re.search("Fedora", system) != None):
                system=[linux_systems[2],linux_systems_search[2]]
            elif(re.search("Cent", system) != None):
                system=[linux_systems[2],linux_systems_search[2]]
            elif(re.search("Gentoo", system) != None):
                system=[linux_systems[3],linux_systems_search[3]]
            elif(re.search("Chromium", system) != None):
                system=[linux_systems[3],linux_systems_search[3]]
            elif(re.search("Funtoo", system) != None):
                system=[linux_systems[3],linux_systems_search[3]]
            elif(re.search("SUSE", system) != None):
                system=[linux_systems[4],linux_systems_search[4]]
            elif(re.search("Slack", system) != None):
                system=[linux_systems[5],linux_systems_search[5]]
            elif(re.search("Mageia", system) != None):
                system=[linux_systems[6],linux_systems_search[6]]           
            else:
                system=linux_systems[7],linux_systems_search[7]
        kernel_v=system_information.kernelV
        cpu=system_information.cpu
        gpu=system_information.gpu[0]
        driver_type=system_information.gpu[2]
        gpu_ver=system_information.gpu[1]
        desktop=system_information.desktopEnv
        resolution=system_information.resolution
        extras="RAM "+system_information.memory+", VRAM "+system_information.gpu[3]
        url="http://www.opengamebenchmarks.org/accounts/profile/"        
        link=""            
        info=bs4.BeautifulSoup(client.get(url).content, "lxml")
        tr = info.find_all("tr")
        for tr in tr:
            count=0 
            for td in tr.findAll("td", {"class" : ""}):                               
                if(re.search(cpu, str(td)) != None):
                    count=count+1
                if(re.search(gpu, str(td)) != None):
                    count=count+1
                if(re.search(driver_type, str(td)) != None):
                    count=count+1
                if(re.search(system[1], str(td)) != None):
                    count=count+1                
                if(count == 4):
                    link=td.find("a", { "class" : "nounderline label label-xs label-danger" })
                    link=str(link)
            if(len(link) != 0):
                break
        if(len(link) != 0):
            system_id=re.sub("[^0-9]", "", link)
            url="http://www.opengamebenchmarks.org/system_edit/"+system_id
            page=bs4.BeautifulSoup(client.get(url).content, "lxml")
            sys_name = page.find_all("h2")
            sys_name=trim_whitespace(re.sub("Edit system:", "", str(sys_name)))
            csrf=client.get(url).cookies['csrftoken']           
            data = dict(csrfmiddlewaretoken=csrf, descriptive_name=sys_name, cpu_model=cpu, gpu_model=gpu, dual_gpu="None", resolution=resolution, driver=driver_type, operating_system=system[0],
                          desktop_environment=desktop, kernel=kernel_v, gpu_driver_version=gpu_ver, additional_details=extras)
            client.post(url, data=data, headers=dict(Referer=url))
            client.close()
        else:
            system_name=input("Insert a name for your system")
            system_id=re.sub("[^0-9]", "", link)
            url="http://www.opengamebenchmarks.org/system_add/"
            csrf=client.get(url).cookies['csrftoken']        
            data = dict(csrfmiddlewaretoken=csrf, descriptive_name=system_name, cpu_model=cpu,  gpu_model=gpu, dual_gpu="None", resolution=resolution, driver=driver_type, operating_system=system[0],
                          desktop_environment=desktop, kernel=kernel_v, gpu_driver_version=gpu_ver, additional_details=extras)
            client.post(url, data=data, headers=dict(Referer=url))
            client.close()
        
if __name__ == '__main__':
    Upload("")
        
        