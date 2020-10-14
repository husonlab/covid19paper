import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
import os
import sys
import re
import os.path
import argparse
from multiprocessing import Queue, Process, cpu_count
import time

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

#ap.print_help()

args = vars(ap.parse_args())

link='http://biorxiv.org/cgi/content/short/2020.04.01.020966'+'.article-info'
'''
Getting driver
'''
def GetBrowser():
    #PROXY = "http://23.23.23.23:312"  # IP:PORT or HOST:PORT
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('blink-settings=imagesEnabled=false')
    #options.add_argument('--proxy-server={PROXY}')
    browser = webdriver.Chrome(options=options,  executable_path=r'PathToChromedriver')# add path to chrome driver
    return browser

def FileParse(RecieveFilePath):
        FileList=[]
        file=pd.read_csv(RecieveFilePath,sep="\t", header=0)
        #file.columns = ['one', 'two','three','four','five','six']
        #file=file[file['title'].str.contains("COVID", na=False)]
        file['rel_link'] = file['rel_link'].astype(str)+'.article-info'
        #col_three_list = file[[3]].tolist()
        for row in file.iterrows():
            index, data = row
            FileList.append(data['rel_link'])
        return FileList
        #grouped = file.groupby('source_x')
        #print(grouped.describe().head())
        #for name_of_the_group, group in grouped:
            #print (name_of_the_group)
           # print (group)

def JournalDetail(GetLink,q,TakeOutputFile):
    driver=GetBrowser()
    #time.sleep(5)
    try:
        result=[]
        file_to_write1=open(TakeOutputFile, "a")
        for link in GetLink:
            #print(link)
            driver.get(str(link))
            time.sleep(5)
            content = driver.find_elements_by_class_name('aff')
            time.sleep(5)
            arrayAppendForResult=[]
            for data in content:
                arrayAppendForResult.append(data.text)
            listToStr = "#".join(arrayAppendForResult)
            #print(listToStr)
            file_to_write1.write(str(link)+"\t"+str(listToStr.encode(encoding='UTF-8',errors='strict'))+"\n")
            # arrayAppendForResult[:] = []
        result.append("Done")
        file_to_write1.close()
        driver.close()
#Medrxiv(link)
    except:
        q.put([])
        raise
    q.put(result)

def myMultiprocessing(RecieveFile,RecieveOutFilepath,RecieveThreads):
#def myMultiprocessing(folder):
    '''
    Splits the source filelist into sublists according to the number of CPU cores and provides multiprocessing of them.
    '''
    file_to_write1=open(RecieveOutFilepath, "w")
    file_to_write1.write("link"+"\t"+"Institute Name"+"\n")
    file_to_write1.close()
    files = FileParse(RecieveFile)
    q = Queue()
    procs = []
    for i in range(0,int(RecieveThreads)):
        # Split the source filelist into several sublists.
        lst = [files[j] for j in range(0, len(files)) if j % int(RecieveThreads) == i]
        if len(lst)>0:
            #p = Process(target=FastaDetailProcessor, args=([lst, q,RecieveFilepath]))
            p = Process(target=JournalDetail, args=([lst, q,RecieveOutFilepath]))
            p.start()
            procs += [p]
    # Collect the results:
    all_results = []
    for i in range(0, len(procs)):
        # Save all results from the queue.
        all_results += q.get()

    # Output results into the file.
    #log = open("logfile.log", "w")
    #print >>file_to_write1, all_results
    #print(all_results, end="", file=file_to_write1)
    # file_to_write1=open(RecieveOutFilepath, "w")
    # file_to_write1.write("link"+"\t"+"Institute Name"+"\n")
    # for item in all_results:
    #     file_to_write1.write(item)
    # file_to_write1.close()
    #RemoveFxi(folder)

if __name__ == "__main__":
    myMultiprocessing(args['FilePath'],args['OutFile'],args['NumberOfThread'])