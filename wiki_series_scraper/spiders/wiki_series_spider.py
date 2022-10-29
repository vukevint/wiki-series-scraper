"""
Crawl and scrape wiki page for tv show data. Adapted from gtp2-episode-summary-generator.

Returns: tv show titles, episode title, episode number (in season), episode number (overall), season (or short/special)

For more information on XPath: http://www.zvon.org/comp/r/tut-XPath_1.html#intro

@author: kevinvu
"""

from bs4 import BeautifulSoup
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from datetime import datetime
from re import search

import logging
import pandas as pd
import numpy as np

from utils.config import log_path


class WikiSeriesSpider(CrawlSpider):
    """Crawler for collecting episode summaries by crawling through Wikipedia and parsing season/episode tables."""

    name = 'wiki_series_spider'
    _now = datetime.now()

    logging.basicConfig(
        filename=log_path + "/debug-" + _now.strftime("%Y-%m-%d-%H%M%S"),
        filemode='w',
        level=logging.INFO
        )

    def __init__(self, start_url, allow, title_keywords, *args, **kwargs):
        super(WikiSeriesSpider, self).__init__(*args, **kwargs)

        self.start_urls = [start_url]
        self.to_allow = allow
        self.title_keywords = [word.lower() for word in title_keywords]

        # set Wiki specific stuff
        self.allowed_domains = ['en.wikipedia.org']
        self.to_deny = ['/Talk:', '/Wikipedia_talk:', '/Category:', '/Wikipedia:', '/Template:']

        # set rules
        self.rules = (Rule(LinkExtractor(allow=self.to_allow,
                                         deny=self.to_deny,
                                         allow_domains=self.allowed_domains),
                           callback='parse_wiki_page',
                           follow=True),)
        super(WikiSeriesSpider, self)._compile_rules()

    def parse_wiki_page(self, response):
        """Parse and yield all relevant episode data from a Wikipedia page."""
       
        page_header = response.xpath("//h1[@id='firstHeading']").get()

        if page_header and all([keyword in page_header.lower() for keyword in self.title_keywords]):
            # parse episode tables that contain summaries
            ep_tables = response.xpath("//table[@class='wikitable plainrowheaders wikiepisodetable']")
            df = self.parse_wiki_data(ep_tables)

            # extract other data            
            page_header = BeautifulSoup(page_header, 'lxml').text
            if search('(?i)List of (.*) episodes', page_header):
                df['Series Title'] = search('(?i)List of (.*) episodes', page_header).group(1)
                df['Season'] = np.nan
            elif search('(?i)(.*)\(Season [0-9]+\)$', page_header):
                df['Series Title'] = search('(?i)(.*) \(Season', page_header).group(1)
                df['Season'] = search('(?i)\(Season (.*)\)$', page_header).group(1)
            else:
                df['Series Title'] = np.nan
                df['Season'] = np.nan

            df['Source URL'] = response.url

            data_yield = pd.DataFrame.to_dict(df, orient='records')
            
            for i in data_yield:
                yield i

    def parse_wiki_data(self, ep_tables):
        """Collect the data from a list of Wikipedia episode tables and other parts on page."""

        metadata = []
        for ep_table in ep_tables:
            # only parses through tables with episode summaries
            if ep_table.xpath(".//tbody/tr[@class='expand-child']/td[@class='description']"):
                soup = BeautifulSoup(ep_table.get(), 'lxml')
                df = pd.read_html(soup.prettify())[0]
                
                # extract description rows and add as columns
                idx_sums = np.nonzero(list(map(lambda x : len(set(x))==1,df.values)))[0]
                md_sums = df.iloc[idx_sums, 0].values
                df = df.drop(idx_sums)
                                
                if len(df) == len(md_sums):
                    df['Description'] = md_sums
                else:
                    logging.info("Table does not contain same number of description rows (e.g. summary info) " 
                                 "than episode metadata rows (e.g. title, episode number). Check /data/scraped/error")
                    # filepath = log_path + "/data-" + self._now.strftime("%Y-%m-%d-%H%M%S")
                    # df.iloc[0].to_excel(filepath)
                    continue
                
                metadata.append(df)
                
        return pd.concat(metadata, ignore_index=True)
