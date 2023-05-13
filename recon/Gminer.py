import os
import time
import requests
import threading
from urllib3.exceptions import NewConnectionError
from bs4 import BeautifulSoup
import argparse


parser = argparse.ArgumentParser(description="Gminer is a tool for create passlist")

parser.add_argument("-f", "--filename",
                    required=True,
                    help='file input.')

options = parser.parse_args()
time.sleep(1)

filename = options.filename



List1 = []

f = open(filename,"r")

for i in f:
    List1.append(i.replace("\n",""))
    main = round(len(List1) / 8)


List = []
def final1():

    for i in List1[:main]:
        try:
            if (i[:8] == "https://" or i[:7] == "http://"):
                http = (requests.post(i).content.decode())

            soup = BeautifulSoup(http, 'html.parser')


            for a in soup.find_all(id=True):
                List.append(str(a['id']))

            for a in soup.find_all(rel=True):
                List.append(str(a['rel']))

            for a in soup.find_all(class_=True):
                List.append(str(a['class']))

        except NewConnectionError as nce:
            pass
        except Exception as e:  # there are some other exceptions I want to ignore
            pass


def final2():

    for i in List1[main+main:main+main+main]:
        try:
            if (i[:8] == "https://" or i[:7] == "http://"):
                http = (requests.post(i).content.decode())


            soup = BeautifulSoup(http, 'html.parser')


            for a in soup.find_all(id=True):
                List.append(str(a['id']))

            for a in soup.find_all(rel=True):
                List.append(str(a['rel']))

            for a in soup.find_all(class_=True):
                List.append(str(a['class']))

        except NewConnectionError as nce:
            pass
        except Exception as e:  # there are some other exceptions I want to ignore
            pass


def final3():

    for i in List1[main+main+main:main+main+main+main]:
        try:
            if (i[:8] == "https://" or i[:7] == "http://"):
                http = (requests.post(i).content.decode())

            soup = BeautifulSoup(http, 'html.parser')


            for a in soup.find_all(id=True):
                List.append(str(a['id']))

            for a in soup.find_all(rel=True):
                List.append(str(a['rel']))

            for a in soup.find_all(class_=True):
                List.append(str(a['class']))

        except NewConnectionError as nce:
            pass
        except Exception as e:  # there are some other exceptions I want to ignore
            pass

def final4():

    for i in List1[main+main+main+main:main+main+main+main+main]:
        try:
            if (i[:8] == "https://" or i[:7] == "http://"):
                http = (requests.post(i).content.decode())


            soup = BeautifulSoup(http, 'html.parser')


            for a in soup.find_all(id=True):
                List.append(str(a['id']))

            for a in soup.find_all(rel=True):
                List.append(str(a['rel']))

            for a in soup.find_all(class_=True):
                List.append(str(a['class']))

        except NewConnectionError as nce:
            pass
        except Exception as e:  # there are some other exceptions I want to ignore
            pass


def final5():

    for i in List1[main+main+main+main+main:main+main+main+main+main+main]:
        try:
            if (i[:8] == "https://" or i[:7] == "http://"):
                http = (requests.post(i).content.decode())


            soup = BeautifulSoup(http, 'html.parser')


            for a in soup.find_all(id=True):
                List.append(str(a['id']))

            for a in soup.find_all(rel=True):
                List.append(str(a['rel']))

            for a in soup.find_all(class_=True):
                List.append(str(a['class']))

        except NewConnectionError as nce:
            pass
        except Exception as e:  # there are some other exceptions I want to ignore
            pass


def final6():

    for i in List1[main+main+main+main+main+main:main+main+main+main+main+main+main]:
        try:
            if (i[:8] == "https://" or i[:7] == "http://"):
                http = (requests.post(i).content.decode())


            soup = BeautifulSoup(http, 'html.parser')


            for a in soup.find_all(id=True):
                List.append(str(a['id']))

            for a in soup.find_all(rel=True):
                List.append(str(a['rel']))

            for a in soup.find_all(class_=True):
                List.append(str(a['class']))

        except NewConnectionError as nce:
            pass
        except Exception as e:  # there are some other exceptions I want to ignore
            pass


def final7():

    for i in List1[main+main+main+main+main+main+main:main+main+main+main+main+main+main+main]:
        try:
            if (i[:8] == "https://" or i[:7] == "http://"):
                http = (requests.post(i).content.decode())


            soup = BeautifulSoup(http, 'html.parser')


            for a in soup.find_all(id=True):
                List.append(str(a['id']))

            for a in soup.find_all(rel=True):
                List.append(str(a['rel']))

            for a in soup.find_all(class_=True):
                List.append(str(a['class']))

        except NewConnectionError as nce:
            pass
        except Exception as e:  # there are some other exceptions I want to ignore
            pass

    Gminer3 = open("Gminer3","a")
    for u in List:
        a = (u.replace("['", ""))
        b = (a.replace("']","\n"))
        c = (b.replace("'] ,","\n"))
        d = (c.replace("', '","\n"))
        Gminer3.write(d)
    Gminer3.close()

    os.system("cat Gminer3 | sort -u > Gminer && rm -rf Gminer2 Gminer3")
        


def Threader():

    y = threading.Thread(target=final1, args=())
    y.start()

    z = threading.Thread(target=final2, args=())
    z.start()

    e = threading.Thread(target=final3, args=())
    e.start()

    r = threading.Thread(target=final4, args=())
    r.start()

    m = threading.Thread(target=final5, args=())
    m.start()

    d = threading.Thread(target=final6, args=())
    d.start()

    q = threading.Thread(target=final7, args=())
    q.start()

    print(threading.active_count())
    print(threading.enumerate())
    print(time.perf_counter())


def path():
    
    os.system(f"cat {filename} | unfurl format %p | sort -u > Gminer-params.txt")
    
    f2 = open("Gminer-params.txt","r")
    f3 = open("Gminer-path.txt","w")
    for w in f2:
        f3.write(w.replace("/","\n"))
    f3.close()
    os.system("cat Gminer-path.txt | sort -u > Gminer-path && rm -rf Gminer-params.txt Gminer-path.txt")

Threader()
path()