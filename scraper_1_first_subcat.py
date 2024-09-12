#!/usr/bin/env python3

from bs4 import BeautifulSoup
import requests

base_url = "https://en.wikipedia.org"

relative_urls_first_subcat = []

whole_urls_first_subcat = []

x = True

# The following code accesses the URL
# https://en.wikipedia.org/wiki/Category:Women_computer_scientists and gets the
# relative URLs for the each subcategory, namely:
# Women_computer_scientists_by_nationality
# Women_bioinformaticians
# Women_roboticists
# Women_logicians


# Starts a while loop in order to avoid using a "for" loop with the "range"
# class. The variable "x" was declared as True in the previous line of code.
while x:

    # Request https://en.wikipedia.org/wiki/Category:Women_computer_scientists
    # and store it in "main_page" variable
    main_page = requests.get("https://en.wikipedia.org/wiki/Category:Women_computer_scientists")

    # Use the "content" property from "requests" to encode the HTML of the page
    # we just opened and ingested in the previous line as bytes that are
    # interpretable by BeautifulSoup.
    main_page_content = main_page.content

    # Use Beautiful Soup’s HTML parser to differentiate between HTML and the
    # site’s actual content i.e the content is the data which we actually want
    # to scrape.
    main_page_content_soup = BeautifulSoup(main_page_content, "html.parser")

    # Use the "find" function from Beautifulsoup to find a <div> tag that
    # contains the class mw-category. This is the overall <div> tag that
    # contains the content we want to scrape. This assigns parts of HTML block
    # to the variable "content".
    content = main_page_content_soup.find("div", class_="mw-category")

    # Start a "for" loop which goes through "content" via the "find_all" method.
    # The find_all() method looks through a tag’s descendants and retrieves all
    # descendants that match a filter. In this case the filter is "a", because
    # it is it which holds the relative URLs which interests us. This means that
    # the find_all() function will fetch every <a> tag and create a list of them.
    for each_relative_url in content.find_all("a"):

        # In this line of code we extract the actual relative URL from each <a>
        # tag, within "each_relative_url", with the "get" function/method
        # returns the value of the item with the specified key. In this case the
        # key is "href". Each relative URL is then appended with the "append"
        # method to the "relative_urls" variable which was declared above.
        relative_urls_first_subcat.append(each_relative_url.get("href"))

    # This "for" loop goes through each item in the "relative_urls" list.
    for x in relative_urls_first_subcat:

        # We concatenate each relative URL to the base URL and append that to
        # the "whole_urls" variable. The "whole_urls" variable then becomes a
        # list.
        whole_urls_first_subcat.append(base_url + x)

    # We make "x" False so as to get out of the "while" loop.
    x = False
