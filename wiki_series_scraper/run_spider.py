import argparse
from scrapy.crawler import CrawlerProcess
from spiders.wiki_series_spider import WikiSeriesSpider
from utils.config import scraped_path


def run_wiki_spider(args):
    """Define and start process for Wikipedia scraping."""
    # overwrite output
    with open(args.output_name, 'w') as f:
        pass

    # run spider
    process = CrawlerProcess(settings={
        'FEED_FORMAT': 'json',
        'FEED_URI': args.output_name,
        'ROBOTSTXT_OBEY': True,
        'DEPTH_LIMIT': 2
    })
    process.crawl(
        WikiSeriesSpider, start_url=args.start_url, allow=args.url_substring, title_keywords=args.title_keywords
    )
    process.start()


def get_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description='Wikipedia series metadata spider.',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument('-s', '--start_url', type=str, required=True,
                        help='start URL for the spider.'
                             'Should be: '
                             'https://en.wikipedia.org/wiki/<Show_Title_With_Underscores_And_Capitalized_Words>. '
                             'Example: https://en.wikipedia.org/wiki/Star_Trek')
    parser.add_argument('-u', '--url_substring', type=str, required=True,
                        help='Wikipedia urls must include this substring otherwise the spider will not enter the URL.'
                             'Ideally, it should be something like: '
                             '<Show_Title_With_Underscores_And_Capitalized_Words>. Example: "Star_Trek"')
    parser.add_argument('-t', '--title_keywords', nargs='*', required=True,
                        help='The title of the Wikipedia page must include these keywords, '
                             'otherwise the spider will not extract anything from the page. '
                             'Good practice: use the lowercase version of the words from the title of the show. '
                             'Example: star trek')
    
    parser.add_argument('-o', '--output-name', type=str, required=False, default='wiki_series_metadata.json',
                        help='Path to the output JSON file. If the file already exists, it will be overwritten.')
    
    args = parser.parse_args()
    args.output_name = scraped_path + '/' + args.output_name
    return args


if __name__ == '__main__':
    args = get_arguments()
    run_wiki_spider(args)
