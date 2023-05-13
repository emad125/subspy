import os
import time
import argparse
import requests
from waybackpy import WaybackMachineCDXServerAPI
import re

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'




print (bcolors.FAIL + " ____       _           _____ _           _")
print (bcolors.FAIL + "|  _ \ ___ | |__   ___ |  ___(_)_ __   __| | ___ _ __")
print (bcolors.OKGREEN + "| |_) / _ \| '_ \ / _ \| |_  | | '_ \ / _` |/ _ \ '__|")
print (bcolors.ENDC + "|  _ < (_) | |_) | (_) |  _| | | | | | (_| |  __/ |")
print (bcolors.OKBLUE + "|_| \_\___/|_.__/ \___/|_|   |_|_| |_|\__,_|\___|_|")
time.sleep(1)
print(bcolors.BOLD+"********** Made by debug **********\n")


parser = argparse.ArgumentParser(description="RoboFinder is a tool for get robots.txt content")

parser.add_argument("-u", "--url",
                    help='url input.')

parser.add_argument("-f", "--filename",
                    help='file input.')


options = parser.parse_args()
time.sleep(1)

url = options.url
filename = options.filename

def Robourl():
    user_agent = "Mozilla/5.0 (Windows NT 5.1; rv:40.0) Gecko/20100101 Firefox/40.0"

    cdx = WaybackMachineCDXServerAPI(url+"/robots.txt", user_agent, start_timestamp=2016, end_timestamp=2022)

    file = open("result.txt","w")
    try:
        for item in cdx.snapshots():

            x = requests.post(item.archive_url)
            # print(item.archive_url)
            file.writelines(x.text+"\n")

        file.close()
    except requests.exceptions.SSLError:
        print("Turn on vpn. This part need vpn")
    except requests.exceptions.ConnectionError:
        print("Connection eroor")

    os.system("sort result.txt | uniq > Robots.txt && rm -rf result.txt")


    f = open("Robots.txt","r")
    f2 = open("test.txt","w")

    content = f.read()

    disallowed_paths = re.findall(r'Disallow:\s+(.*)', content)
    disallowed_urls = []

    for path in disallowed_paths:
        disallowed_urls.append(url + path)

    f2.write('\n'.join(disallowed_urls))

    allowed_paths = re.findall(r'Allow:\s+(.*)', content)
    allowed_urls = []

    for path in allowed_paths:
        allowed_urls.append(url + path)

    f2.write('\n'.join(allowed_urls))

    pattern = rf'{url}[\w\./-]*'

    # Find all occurrences of the pattern in the file content
    urls = re.findall(pattern, content)

    # Print the extracted URLs
    for url2 in urls:
        f2.write(f"{url2}\n")

def Robofile():
    user_agent = "Mozilla/5.0 (Windows NT 5.1; rv:40.0) Gecko/20100101 Firefox/40.0"

    file = open(filename,"r")
    
    for u in file:
        match = re.match(r'^https?://([^/]+)\..*', u)
        sub = match.group(1)
        
        cdx = WaybackMachineCDXServerAPI(u+"/robots.txt", user_agent, start_timestamp=2016, end_timestamp=2022)

        file = open("result.txt","w")
        try:
            for item in cdx.snapshots():

                x = requests.post(item.archive_url)
                print(item.archive_url)
                file.writelines(x.text+"\n")

            file.close()
        except requests.exceptions.SSLError:
            print("Turn on vpn. This part need vpn")
        except requests.exceptions.ConnectionError:
            print("Connection eroor")

        os.system(f"sort result.txt | uniq > **{sub}**")


        f = open(f"**{sub}**","r")
        f2 = open(sub,"w")

        content = f.read()

        disallowed_paths = re.findall(r'Disallow:\s+(.*)', content)
        disallowed_urls = []

        for path in disallowed_paths:
            disallowed_urls.append(u + path)

        f2.write('\n'.join(disallowed_urls))

        allowed_paths = re.findall(r'Allow:\s+(.*)', content)
        allowed_urls = []

        for path in allowed_paths:
            allowed_urls.append(u + path)

        f2.write('\n'.join(allowed_urls))

        pattern = rf'{u}[\w\./-]*'

        # Find all occurrences of the pattern in the file content
        urls = re.findall(pattern, content)

        # Print the extracted URLs
        for url2 in urls:
            f2.write(f"{url2}\n")
        
        os.system(f"rm -rf **{sub}**")

if options.url != None:
    Robourl()

if options.filename != None:
    Robofile()
    os.system("rm -rf Robots.txt result.txt")