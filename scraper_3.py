#!/usr/bin/env python3

import pandas as pd

from scraper_1_first_subcat import BeautifulSoup, requests
from scraper_1_first_subcat import base_url
from scraper_2_second_subcat import relative_urls_nationality

url_northern_ireland = ""
next_pages = []
women_computer_scientists = []

# Now we go through the list "relative_urls_nationality"
for y in relative_urls_nationality:

    # We now concatenate each element "y" from the "relative_urls_nationality"
    # list to the "base_url" and request that.
    nationality_subcategorie_pages = requests.get(base_url + y)
    nationality_subcategorie_pages_content = nationality_subcategorie_pages.content
    nationality_subcategorie_pages_content_soup = BeautifulSoup(nationality_subcategorie_pages_content, "html.parser")

    # Some subcategories are separated over several pages so we need to grab the
    # the relative URL which index to the "next page". In this case, the overall
    # "div" tag which holds the URL which we're interested is
    # "mw-category-generated". In this case we are doint this for the American
    # women computer scientists.
    if nationality_subcategorie_pages_content_soup.find("div", class_="mw-category-generated") and nationality_subcategorie_pages_content_soup.css.select('a[href*="mw-pages"]'):

        # Remember that "find_all" returns a list, so we start a "for" loop which
        # goes through that list.
        for x in nationality_subcategorie_pages_content_soup.find_all("div", class_="mw-category-generated"):

            # We grab the first "a" tag, which holds the relative URL that
            # interests us, and grab the actual URL with ".get("href")".
            next_page = base_url + x.find_all("a")[1].get("href")

            # We append the initial "next page" URL to our "next_pages" variable.
            next_pages.append(next_page)

        # As explained before the subcategories of American scientists are
        # separated over several pages so we need to grab all of the correct
        # URLs. All American computer scientists are in fact spread over 3 pages
        # at the time of this writing. We start a for loop which grabs the first
        # full URL which is stored in out "next_pages" variable/list.
        for x in next_pages:

            # We request the second page of American scientists subcategories.
            # This is the one which holds the relative URL to the third and last
            # page of American scientists subcategories.
            next_page = requests.get(x)
            next_page_content = next_page.content
            next_page_content_soup = BeautifulSoup(next_page_content, "html.parser")

            # We test this condition in order to make sure that our page
            # contains a "next pabe" button/link to our next relative URL
            if next_page_content_soup.find_all("div", class_="mw-category-generated") and next_page_content_soup.css.select('a[href*="mw-pages"]'):

                # Here we test that the "mw-pages", the link that we find, is
                # actually a next page button rather than a relative URL to
                # something else. This is required otherwise our scraper end up
                # grabing the relative URL which points to a scientist page.
                if "mw-pages" not in base_url + next_page_content_soup.find_all("div", class_="mw-category-generated")[0].find_all("a")[2].get("href"):

                    # If we don't find a "next page" button we break out of the loop.
                    break

                else:

                    # If we do find a "next page" button, we append it to our
                    # "next_pages" variable.
                    next_pages.append(base_url + next_page_content_soup.find_all("div", class_="mw-category-generated")[0].find_all("a")[2].get("href"))

    # We also need to get the relative URL for scientists from Northern Ireland.
    # This is indexed from both the "British women computer scientists" page as
    # well as the "Irish women computer scientists" page so we will have to do
    # some data cleaning once we've obtained our dataset.
    if nationality_subcategorie_pages_content_soup.find("div", class_="mw-category-generated") and nationality_subcategorie_pages_content_soup.css.select('a[href*="Northern_Ireland"]'):

        url_northern_ireland = base_url + nationality_subcategorie_pages_content_soup.find("div", class_="mw-category-generated").find_all("a")[0].get("href")

    # If the "nationality_subcategorie_pages" URL holds a large number of
    # entries of scientists, the entries are held under an over "div" with class
    # "mw-category mw-category-columns".
    content = nationality_subcategorie_pages_content_soup.find("div", class_="mw-category mw-category-columns")

    # print(base_url + y)

    # We "try" to find the "a" tag (links) to each scientist if we have a "div"
    # "class_" of "mw-category mw-category-columns".
    try:

        # We look for all "a" tags in our soup.
        for x in content.find_all("a"):
            # print(x.get("href"))

            # The "nationality_subcategorie_pages" for American scientists
            # indexes to a generic page for African American women scientists.
            # It does not hold any entries to specific scientists therefore this
            # page is of no interest to us.
            if "African-American_women_in_computer_science" in x.get("href"):

                # We pass that.
                pass

            # We grab everything else.
            else:

                # print(base_url + y,  x.get("href"))
                women_computer_scientists.append(base_url + x.get("href"))

    # The code raises an error if the "nationality_subcategorie_pages" holds
    # only a few entries of scientists because the overall "div" tag is of a
    # different class from before. In this case the class is "mw-category".
    except:

        content = nationality_subcategorie_pages_content_soup.find("div", class_="mw-category")

        # We look for all "a" tags in our soup.
        for x in content.find_all("a"):

            # The "Irish women computer scientists" is setup a bit differently
            # so in this case we have to do a bit more work to grab each
            # scientist's entry otherwise we end up grabbing a
            # "/wiki/Category:Women_computer_scientists_from_Northern_Ireland"
            # relative URL which is no good to us.
            if "Women_computer_scientists_from_Northern_Ireland" in x.get("href"):

                # We make a list with "find_all" from the soup and grab the
                # second "div" tag with the "mw-category" class. (The first one
                # holds the relative URL which we do not want.)
                for z in nationality_subcategorie_pages_content_soup.find_all("div", class_="mw-category")[1]:

                    # Get each relative URL from from each "a" using our "for" loop.
                    # print(base_url + y,  z.find("a").get("href"))
                    women_computer_scientists.append(base_url + z.find("a").get("href"))

            else:

                # print(base_url + y,  x.get("href"))
                women_computer_scientists.append(base_url + x.get("href"))


# Next we need to get the scientists from Northern Ireland

a = True

while a:

    scientists_norther_ireland = requests.get(url_northern_ireland)
    scientists_norther_ireland_content = scientists_norther_ireland.content
    scientists_norther_ireland_content_soup = BeautifulSoup(scientists_norther_ireland_content, "html.parser")

    content = scientists_norther_ireland_content_soup.find("div", class_="mw-category")

    for x in content.find_all("a"):

        # print(url_northern_ireland, x.get("href"))
        women_computer_scientists.append(base_url + x.get("href"))

    a = False


# We get the scientists which are index in the URLs which contain a "next page"
# button.

b = True

while b:

    for x in next_pages:

        x = requests.get(x)
        x_content = x.content
        x_content_soup = BeautifulSoup(x_content, "html.parser")

        content = x_content_soup.find("div", class_="mw-category mw-category-columns")

        for y in content.find_all("a"):

            women_computer_scientists.append(base_url + y.get("href"))

    b = False


# We get the scientists which are indexed on the main page of "women computer
# scientists".

c = True

while c:

    scientists_main_page =  requests.get("https://en.wikipedia.org/wiki/Category:Women_computer_scientists")
    scientists_main_page_content = scientists_main_page.content
    scientists_main_page_content_soup = BeautifulSoup(scientists_main_page_content, "html.parser")

    content = scientists_main_page_content_soup.find("div", class_="mw-category mw-category-columns")

    for x in content.find_all("a"):

        women_computer_scientists.append(base_url + x.get("href"))

    c = False


# This last line uses the pandas library to perform some operations on the list
# "women_computer_scientists" and then save the result to a CSV file.

pd.Series(women_computer_scientists).to_csv('wikipedia_computer_scientists_names.csv', encoding='utf-8', header=False, index=False)
