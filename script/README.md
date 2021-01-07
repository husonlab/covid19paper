# On the application of advanced machine learning methods to analyze enhanced, multimodal data from persons infected with COVID-19

published in computation https://www.mdpi.com/2079-3197/9/1/4/htm

----
## Contents ##
* [Requirements](#requirements)
* [Initial Installation](#initial-installation)
* [How to run](#how-to-run)
* [Publication](#Publication)
* [Citation](#Citation)

----
## Requirements ##

1. [pandas](https://pandas.pydata.org/)
2. [Selenium](https://selenium-python.readthedocs.io/) 
3. [Requests](https://requests.readthedocs.io/en/master/)
4. [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) 
5. [python](http://www.python.org/) (version >= 3.8)

----
## Initial Installation ##
### 1. Installing requirement. ###

It's useful to create a conda environment if you want to install from source.
    ``conda create -n covid python=3.8 ``
    ``conda activate covid``
 
Installing Selenium
    ``conda install -c conda-forge selenium``

Installing Requests
    ``conda install -c anaconda requests``

Installing BeautifulSoup
    ``conda install -c anaconda beautifulsoup4``


### 2. Download covid19paper git ###
Option 1: Development Version

* Create a clone of the repository: 
    
    ``$ git clone https://github.com/husonlab/covid19paper.git``

### 3. cd covid19paper/script ###

----
## How to run ##
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
5. For Weather Crawling:
    ```
    python3 crawl_weather.py -h
        usage: crawl_weather.py [-h] [--input INPUT_FILE] [--browser BROWSERNAME] [--output WEATHER_FILE]
            optional arguments:
                -h, --help            show this help message and exit
                --input INPUT_FILE    input path
                --browser BROWSERNAME chromedriver path
                --output WEATHER_FILE output path
    ```
----

## Publication ##

Publication can be accessed at: https://www.mdpi.com/2079-3197/9/1/4/htm

preprint:https://www.biorxiv.org/content/10.1101/2020.07.08.193144v1.full

----
## Citation ##

For citing code and data please use the citation below.

```{bibtex}
@Article{wenhaun2021,
AUTHOR = {Zeng, Wenhuan and Gautam, Anupam and Huson, Daniel H.},
TITLE = {On the Application of Advanced Machine Learning Methods to Analyze Enhanced, Multimodal Data from Persons Infected with COVID-19},
JOURNAL = {Computation},
VOLUME = {9},
YEAR = {2021},
NUMBER = {1},
ARTICLE-NUMBER = {4},
URL = {https://www.mdpi.com/2079-3197/9/1/4},
ISSN = {2079-3197},
DOI = {10.3390/computation9010004}
}
```
