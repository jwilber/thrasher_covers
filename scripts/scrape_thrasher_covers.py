# -*- coding: utf-8 -*-
# author: Jared Wilber
"""scrape_thrasher_covers.py
This script scrapes thrashermagazine.com for all available magazine covers.
Example:
    The function may be called from the cli with or without arguments:
        # call without arguments
        $ python scrape_thrasher_covers.py
        # call with arguments
        $ python scrape_thrasher_covers.py --csv_name covers.csv
"""
import argparse
import re
import requests

import os.path as op
import pandas as pd

from bs4 import BeautifulSoup


def get_year(url):
    """Extract year from url."""
    year = re.search("\d{4}", url).group(0)
    return int(year)


def get_month(url):
    """Get character month from url."""
    month = " ".join(re.findall("[a-zA-Z]+", url))
    return month


def main(csv_name):
    """Run script conditioned on user-input."""
    BASE_URL = "https://www.thrashermagazine.com/{}"
    COVER_URL = BASE_URL.format("covers/")

    page = requests.get(COVER_URL)

    soup = BeautifulSoup(page.content, 'html.parser')
    image_spans = soup.find_all("span", class_="icons")
    date_spans = soup.find_all("span", class_="coverDate")

    cover_urls = []
    month_urls = []
    year_urls = []

    for (date_info, cover) in zip(date_spans, image_spans):
        date = date_info.text
        # track month info
        month = get_month(date)
        month_urls.append(month)
        # track year info
        year = get_year(date)
        year_urls.append(year)
        # track cover info
        img_path = cover.find_all('a')[0]['href']
        cover_urls.append(BASE_URL.format(img_path))

    cover_df = pd.DataFrame({'month': month_urls, 
                  'year': year_urls,
                  'cover_url': cover_urls})

    # save data to csv
    cover_df.to_csv(op.join("..", "data", csv_name), index=False)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description="Scrape Thrasher Magazine covers"
    )
    parser.add_argument('--csv_name', default='thrasher_covers.csv',
                        help="Name of csv file to save data to.")

    args = vars(parser.parse_args())
    main(**args)