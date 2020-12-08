import universities
import argparse
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
from bs4 import BeautifulSoup as soup


ap = argparse.ArgumentParser()

ap.add_argument("-i", metavar="<File Path>", dest="FilePath",
    help="Enter the path to csv file", required=True)
ap.add_argument("-o", metavar="<OutputFileName>", dest="OutFile",
    help="Enter the File Name Your Output", required=True)
ap.add_argument("-t", metavar="<NumberOfThread>", dest="NumberOfThread",
    help="Enter Number of thread", required=True)
args = vars(ap.parse_args())



def FileParse(TakeInFile):
	ArrayToReturn=[]
	file=open(TakeInFile,"r")
	for line in file:
		line=line.strip("\n")
		lineSplit=line.split("\t")
		if lineSplit[2]=='NA':
			ArrayToReturn.append(line)
	return(ArrayToReturn) 
def GetBrowser():
    #PROXY = "http://23.23.23.23:312"  # IP:PORT or HOST:PORT
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('blink-settings=imagesEnabled=false')
    prefs = {
            "translate_whitelists": {"de-DE":"en-us"},
            "translate":{"enabled":"true"}
            }
    options.add_argument("--lang=en-gb")
    #options.add_experimental_option('prefs', {'intl.accept_languages': 'en,en_US'})
    #options.add_experimental_option( "prefs", {'--lang': 'es'})
    #options.add_argument('--proxy-server={PROXY}')
    browser = webdriver.Chrome(options=options,  executable_path=r'/Users/anupamgautam/MyProject/bpgaCheck/pythonScript/covid/chromedriver')
    return browser


def AddressDetail(TakeList,q,TakeOutFilePath):
	driver=GetBrowser()
	try:
		result=[]
		FileOut=open(TakeOutFilePath,'a')
		for line in TakeList:
			resultToWrite=[]
			uni = universities.API() # can specify encoding for use in Python 2
			line=line.strip("\n")
			SplitLine=line.split("\t")
			Splittext=SplitLine[1].split("#")
			if len(Splittext)==1:
				Splittext[0]=Splittext[0].replace("b'","b' ")
				Splittext[0]=Splittext[0].replace('b"','b" ')
			for value in Splittext:
				try:
					value=value.split(" ",1)[1]
				except:
					value=value
				value=value.replace(";","")
				value=value.replace("'","")
				link='https://www.google.com/maps/search/'+value
				'''link='https://en.wikipedia.org/wiki/'+value #for wikipedia '''
				#print (link)
				driver.get(str(link))
				time.sleep(5)
				try:
					page = soup(driver.page_source, 'html.parser')
					content = page.findAll('jsl',{'jstcache':'87'})
					'''content = driver.find_elements_by_class_name('country-name')
					for data in content:
						stringToAppend=str(value)+": address: "+str(data.text)
						resultToWrite.append(stringToAppend)'''
					for tag in content:
						divTag = tag.find_all("div", {"class": "ugiz4pqJLAG__primary-text gm2-body-2"})
						for tag in divTag:
							stringToAppend=str(value)+": address: "+str(tag.text)
							resultToWrite.append(stringToAppend)
							break
				except:
					stringToAppend=str(value)+" :address: "+str("NA")
					resultToWrite.append(stringToAppend)
					pass;
			FileOut.write(str("\t".join(line.split("\t", 2)[:2]))+"\t"+str(len(resultToWrite))+"\t"+str("#".join(resultToWrite))+"\n")
		result.append("Done")
		FileOut.close()
		driver.close()
	except:
		q.put([])
		raise
	q.put(result)

def main(RecieveFile,RecieveOutFilepath,RecieveThreads):
#def myMultiprocessing(folder):
    '''
    Splits the source filelist into sublists according to the number of CPU cores and provides multiprocessing of them.
    '''
    file_to_write1=open(RecieveOutFilepath, "w")
    file_to_write1.write("link"+"\t"+"Institute Name"+"\t"+"countOFInstitue"+"\t"+"InstituteWithAddress"+"\n")
    file_to_write1.close()
    files = FileParse(RecieveFile)
    q = Queue()
    procs = []
    for i in range(0,int(RecieveThreads)):
        # Split the source filelist into several sublists.
        lst = [files[j] for j in range(0, len(files)) if j % int(RecieveThreads) == i]
        if len(lst)>0:
            #p = Process(target=FastaDetailProcessor, args=([lst, q,RecieveFilepath]))
            p = Process(target=AddressDetail, args=([lst, q,RecieveOutFilepath]))
            p.start()
            procs += [p]
    # Collect the results:
    all_results = []
    for i in range(0, len(procs)):
        # Save all results from the queue.
        all_results += q.get()


if __name__=="__main__":
	main(args['FilePath'],args['OutFile'],args['NumberOfThread'])