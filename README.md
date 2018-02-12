# OLX_Scraper
An OLX Scraper using Scrapy + MongoDB. It Scrapes recent ads posted regarding requested product and dumps to NOSQL MONGODB.
## Screenshot

![Screenshot](https://github.com/tal95shah/OLX_Scraper/blob/master/MONGODB.PNG)
## About

A Scrapy Program that scrapes recent ads about products and stores them in MONGODB Database.
All the information regarding product to be searched is in <strong> args.py </strong>
![Screenshot](https://github.com/tal95shah/OLX_Scraper/blob/master/olx_scraper/ARGS.PNG)
<p>Change values after return command</p>

## Usage

For proper usage first install selenium and parsel.Open Command Line and type commands given below
<pre>
pip install pymongo
</pre>
<pre>
Configure these Settings in <strong>settings.py</strong><hr>
ITEM_PIPELINES = {
     'olx_scraper.pipelines.MongoDBPipeline': 300,
}
<hr>
MONGODB_SERVER = "localhost" (can be changed)
MONGODB_PORT = 27017(Set Whatever port mongodb is running on your system)
MONGODB_DB = "" (set this)
MONGODB_COLLECTION = "" (set this)
</pre>
<pre>
After all the above configurations have been successfully done.Then open command line and type:-<br>
scrapy crawl scrape_olx
</pre>
## Result
Open MongoDB GUI and check database, Your result should be like Screenshot shown above.
## Gotchas
1-You must have python 3.6 pre-installed to use this software.<br>
2-Make sure mongodb is running before you run spider. 
## If 
If any issue comes do write in issues column. Thanks!
