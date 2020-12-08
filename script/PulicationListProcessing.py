import requests
from bs4 import BeautifulSoup as soup
import re
import os
import sys
import os.path
import argparse
from multiprocessing import Queue, Process, cpu_count
import time
import pandas as pd
import time
from requests.adapters import HTTPAdapter
import urllib3.contrib.pyopenssl
s = requests.Session()
s.mount('http', HTTPAdapter(max_retries=3))
s.mount('https', HTTPAdapter(max_retries=3))

'''
Taking Argument
'''
ap = argparse.ArgumentParser()

ap.add_argument("-i", metavar="<File Path>", dest="FilePath",
    help="Enter the path to csv file", required=True)
ap.add_argument("-o", metavar="<OutputFileName>", dest="OutFile",
    help="Enter the File Name Your Output", required=True)
ap.add_argument("-t", metavar="<NumberOfThread>", dest="NumberOfThread",
    help="Enter Number of thread", required=True)


args = vars(ap.parse_args())

#######file Parsing Function To get Require entires
def FileParse(RecieveFilePath):
        FileList=[]
        file=pd.read_excel(RecieveFilePath,sep="\t", header=0)
        file = file[file['DOI'].notna()]### remove all rows whose DOI is not present
        file = file[file['Journal'].notna()]### remove all rows whose Journal name is not present
        file['DOI']=file['DOI'].str.split(' ').str[0]
        file["DOI"] = file["DOI"].str.replace('https://doi.org/', "")# adding https string
        file['DOI'] = 'https://doi.org/'+file['DOI']
        for row in file.iterrows():
            index, data = row
            FileList.append(data['DOI'])
        return FileList #####returning list of DOI


# get detail about the  publication like author institute and country
def JournalDetail(GetLink,q):
    #time.sleep(5)
    try:
        result=[]
        for link in GetLink:# iterating over link
            headers = requests.utils.default_headers()
            headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'
            try:
                r=requests.get(link, headers=headers)
            except requests.exceptions.ConnectionError:
                print("there was a error"+"\t"+link)
            source=soup(r.text,'html.parser')### parsing Html
            keywordlist=['Department','University','College','Institute','Clinica di','研究所','Institut']
            Con =source.find_all(text=re.compile(('|'.join(keywordlist)), re.IGNORECASE))
            text=re.compile('|'.join(keywordlist))# getting requires entries from file
            newlist = list(filter(text.match, Con))
            if not newlist:
                print(link)
                #result.append(link+"\t"+"NA")
            else:
                result.append(link+"\t"+"|".join(newlist))#remove non require entries 
                #print(link+"\t"+"|".join(newlist))
    except:
        q.put([])
        raise
    q.put(result)
####Multi Processing Function
def myMultiprocessing(RecieveFile,RecieveOutFilepath,RecieveThreads):
    files = FileParse(RecieveFile)## to get require entries in a file
    q = Queue()
    procs = []
    for i in range(0,int(RecieveThreads)):
        # Split the source filelist into several sublists.
        lst = [files[j] for j in range(0, len(files)) if j % int(RecieveThreads) == i]
        if len(lst)>0:
            #p = Process(target=FastaDetailProcessor, args=([lst, q,RecieveFilepath]))
            p = Process(target=JournalDetail, args=([lst, q]))
            p.start()
            procs += [p]
    # Collect the results:
    all_results = []
    for i in range(0, len(procs)):
        # Save all results from the queue.
        all_results += q.get()
    file_to_write1=open(RecieveOutFilepath, "w")
    file_to_write1.write("link"+"\t"+"Institute Name"+"\n")
    for item in all_results:
        print(item)
        file_to_write1.write(item+"\n")
    file_to_write1.close()

###### Main Function ######
if __name__ == "__main__":
    myMultiprocessing(args['FilePath'],args['OutFile'],args['NumberOfThread'])