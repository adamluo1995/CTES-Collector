# CTES Collector

## Introduction
This is a demo code for massively collecting cargo information on Cargos Tracking Electronic System(http://bietc.cgcworld.com/). It uses Scrapy(https://scrapy.org/) as backend to **scrapy your information which have already been displayed on board(which means you can't steal any information!!!).** It can replace days of repeated jobs with several command run in couple minus.
### NOTE:
- Scrapy is actually a wrong choice. Requests(http://docs.python-requests.org/en/master/) and other light HTTP library are more suitable for this job cause it contains no difficult task.
- I wrote these code for a friend who had urgency to collect these information. So I didn't consider the reusability. I put it on github mainly because of the convince of me to refer.

## Modules
### ./run.py
It uses subprocess to run scrapy command to do the collection jobs and save these data as json files separated by month in certain years.
### ./proc.py
It deals with the mass data(cause by the mass of website construction) collected from run.py and make it to one single json file.
### ./to_xlsx
Make json file to xlsx.
### ./cargo/spiders/cargo2_spider.py
Spider to collect information.

## Dependencies
- Scrapy
- demjson
- tqdm
- openpyxl