import pandas as pd
import numpy as np
import argparse
import urllib.request, json
from multiprocessing import Queue, Process, cpu_count


<<<<<<< HEAD

=======
>>>>>>> d0189de077aea5eb22ad1f307154ad5d53d492ff
ap = argparse.ArgumentParser()
ap.add_argument("-n", metavar="<total number of paper showed on https://connect.biorxiv.org/relate/content/181>", dest="NumberOfPaper",
    help="Enter path to output file name", required=True)
ap.add_argument("-o", metavar="<Output file name>", dest="OutputFileName",
    help="Enter path to output file name", required=True)
ap.add_argument("-t", metavar="<Number of Thread>", dest="Nthread",
    help="Enter total Number of thread you want to use", required=True)
args = vars(ap.parse_args())

def MakeCombination(TakeNumberOfPaper):
	loopInteration=int(int(TakeNumberOfPaper)/30)
	counter=0
	listToReturn=[0]
	for i in range(loopInteration):
		counter=counter+30
		listToReturn.append(counter)
	return(listToReturn)


def forTakingDataFromTheWebsite(TakeList,TakeOutputfileName,q):
	try:
		result=[]
		FileToWrite=open(TakeOutputfileName,"a")
		for value in TakeList:
			link=str("https://api.biorxiv.org/covid19/")+str(value)+str("/json")
			with urllib.request.urlopen(link) as url:
				data = json.loads(url.read().decode())
			for x in data['collection']:
				rel_abs=x['rel_abs'].strip("\n")
				rel_abs=rel_abs.strip("\r")
				rel_num_authors=x['rel_num_authors']
				#print(x['rel_authors'][0]['author_name'])
				authorName=[]
				authorInstitute=[]
				counter=0
				for i in range(int(rel_num_authors)):
					counter=counter+1
					authorName.append(x['rel_authors'][i]['author_name'].replace("\n"," "))
					authorInstitute.append(x['rel_authors'][i]['author_inst'].replace("\n"," ").replace("\t"," "))
					# if int(counter)==int(rel_num_authors):
					# 	break
				rel_date=x['rel_date'].strip("\n")
				rel_doi=x['rel_doi'].strip("\n")
				rel_link=x['rel_link'].strip("\n")
				rel_site=x['rel_site'].strip("\n")
				rel_title=x['rel_title'].strip("\n")
				version=x['version'].strip("\n")
				license=x['license'].strip("\n")
				rel_type=x['type'].strip("\n")
				category=x['category'].strip("\n")
				FileToWrite.write(str(rel_abs.replace("\n"," "))+"\t"+str(rel_num_authors).strip("\n")+"\t"+"|".join(authorName).replace("\n"," ")+"\t"+"|".join(authorInstitute).replace("\n"," ")+"\t"+str(rel_date).strip("\n")+"\t"+str(rel_doi).strip("\n")+"\t"+str(rel_link).strip("\n")+"\t"+str(rel_site).strip("\n")+"\t"+str(rel_title).replace("\n"," ")+"\t"+str(version).strip("\n")+"\t"+str(license).strip("\n")+"\t"+str(rel_type).strip("\n")+"\t"+str(category).strip("\n")+"\n")
		FileToWrite.close()
		result.append("Done")
	except:
		q.put([])
		raise
	q.put(result)

def main(RecieveNumberOfPaper,RecieveOutFileName,TakeThread):
	listRequire=MakeCombination(RecieveNumberOfPaper)
	listRequire.append(listRequire[-1]+20)  
	#print(listRequire)
	FileToWrite=open(RecieveOutFileName,"w")
	FileToWrite.write(str('rel_abs')+"\t"+str('rel_num_authors')+"\t"+str('authorName')+"\t"+str('authorInstitute')+"\t"+str('rel_date')+"\t"+str('rel_doi')+"\t"+str('rel_link')+"\t"+str('rel_site')+"\t"+str('rel_title')+"\t"+str('version')+"\t"+str('license')+"\t"+str('rel_type')+"\t"+str('category')+"\n")
	FileToWrite.close()
	q = Queue()
	procs = []
	for i in range(0,int(TakeThread)):
		# Split the source filelist into several sublists.
		lst = [listRequire[j] for j in range(0, len(listRequire)) if j % int(TakeThread) == i]
		#print(lst)
		if len(lst)>0:
			#p = Process(target=FastaDetailProcessor, args=([lst, q,RecieveFilepath]))
			p = Process(target=forTakingDataFromTheWebsite, args=([lst, RecieveOutFileName,q]))
			p.start()
			procs += [p]
	# Collect the results:
	all_results = []
	for i in range(0, len(procs)):
		# Save all results from the queue.
		all_results += q.get()

if __name__=="__main__":
    main(args['NumberOfPaper'],args['OutputFileName'],args['Nthread'])