# wiki_series_spider: scrape wikipedia for TV show data

**wiki_series_spider** is a crawler adapted from the WikiEpisodeTableSpider class in [karoly-hars/gpt2_episode_summary_generator](https://github.com/karoly-hars/gpt2_episode_summary_generator). The goal with the modified class is to obtain all relevant data of each episode.


## How to use
See the original README, specifically [this](https://github.com/karoly-hars/gpt2_episode_summary_generator#wikipedia-spider) section on how to use the Wikipedia spider.

Example:

> python3 run_spider.py --start_url https://en.wikipedia.org/wiki/Friends --title_keywords friends --url_substring Friends -o friends_wiki.json

The data will be stored in a json under the data/scraped directory.