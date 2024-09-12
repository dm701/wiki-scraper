#!/usr/bin/env python3

from scraper_1_first_subcat import requests, BeautifulSoup
from scraper_1_first_subcat import whole_urls_first_subcat

whole_subcat_urls = []
relative_urls_nationality = []
first_subcat_urls_scientists = []
women_computer_scientists = []

# Goes throuth the "whole_urls_first_subcat" list.
for url in whole_urls_first_subcat:

    # This time we will be getting the pages which are indexed by each URL.
    subcategorie_pages = requests.get(url)
    subcategorie_pages_content = subcategorie_pages.content
    subcategorie_pages_content_soup = BeautifulSoup(subcategorie_pages_content, "html.parser")
    content = subcategorie_pages_content_soup.find("div", class_="mw-category mw-category-columns")

    # Since each subcategory indexes to another page, we look for each <a> tag.
    for x in content.find_all("a"):

        # There is a subcategory which actually indexes to another subcategory,
        # so we start an "if" loop which look for the word "Category" in each
        # relative URL.
        if "Category" in x.get("href"):

            # print(x.get("href"))

            # The particular subcategory which we're looking for actually
            # indexes to a page which sorts each entry by nationality, so we
            # happen that to the variable "relative_urls_nationality".
            relative_urls_nationality.append(x.get("href"))

        else:

            # Otherwise we grab the relative URL for each scientists in
            # categories: Women_bioinformaticians, Women_roboticists and
            # Women_logicians, concatenate that to the base URL and append to
            # the "first_subcat_urls_scientists" variable/list.
            first_subcat_urls_scientists.append(url + x.get("href"))
