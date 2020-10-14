# Enhanced COVID-19 data for improved prediction of survival

GitHub Repository containing data and code for paper submitted on APBC-2021

----
## Contents ##

* [Data Description](#Data-Description)
* [Scripts Used](#Scripts-Used)

----
## Data Description ##

----
## Scripts Used ##

1. Downloading paper information from medArix and bioArix:
	```
	python3 BioMedArix.py  -h
		usage: BioMedArix.py [-h] -n <total number of paper showed on https://connect.biorxiv.org/relate/content/181> -o <Output file name> -t <Number of Thread>
		   optional arguments:
			  -h, --help            show this help message and exit
			  -n                    <total number of paper showed on https://connect.biorxiv.org/relate/content/181> Enter path to output file name
 			  -o                    <Output file name> Enter path to output file name
			  -t                    <Number of Thread> Enter total Number of thread you want to use
    ```
----
2. Downloading institue detail and address from medArix and bioArix downloaded paper data:
	```
	python3 AuthorInstitutefromBioMedArix.py -h
		usage: AuthorInstitutefromBioMedArix.py [-h] -i <File Path> -o  <OutputFileName> -t <NumberOfThread>
			optional arguments:
				-h, --help           show this help message and exit
				-i <File Path>       Enter the path to csv file
				-o <OutputFileName>  Enter the File Name Your Output
				-t <NumberOfThread>  Enter Number of thread
    ```
----
3. For finding institue address for medArix and bioArix downloaded paper data (not founded by AuthorInstitutefromBioMedArix.py):
	```
	python3 universityAddressFromGoogleMapAndWiki.py -h
		usage: universityAddressFromGoogleMapAndWiki.py [-h] -i <File Path> -o <OutputFileName> -t <NumberOfThread>
			optional arguments:
				-h, --help           show this help message and exit
				-i <File Path>       Enter the path to csv file
				-o <OutputFileName>  Enter the File Name Your Output
				-t <NumberOfThread>  Enter Number of thread
	```
----
4. For processing WHO journal data downloaded on April 13, 2020 (CSV_as_at_09_April_2020-Full_database.xlsx):
	```
	python PulicationListProcessing.py -h
		usage: PulicationListProcessing.py [-h] -i <File Path> -o <OutputFileName> -t <NumberOfThread>
			optional arguments:
				-h, --help           show this help message and exit
				-i <File Path>       Enter the path to csv file
				-o <OutputFileName>  Enter the File Name Your Output
				-t <NumberOfThread>  Enter Number of thread
	```
----