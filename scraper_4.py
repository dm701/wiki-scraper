#!/usr/bin/env python3

import pandas as pd
# pd.set_option('display.max_colwidth', 100)

import requests
import re
import csv

from bs4 import BeautifulSoup

# This script scrapes all of the resumes from the scientists CSV file.

dataset = pd.read_csv("wikipedia_computer_scientists_names_test.csv", header=None)

# Create an empty list to store the names.
scientist_name_list = []

# Create empty lists to store the nationalities. Some scientists have 2
# nationalities so we make 2 lists.
scientist_nationalities_list_1 = []
scientist_nationalities_list_2 = []

# Create an empty list to store the scraped resumes.
scientists_resume_list = []

for url in dataset[0]:
    page = requests.get(url)
    page_content = page.content
    page_content_soup = BeautifulSoup(page_content, "html.parser")

    scientist_name = page_content_soup.find("span", class_="mw-page-title-main").get_text()
    scientist_name_list.append(scientist_name)

    # This is part of the code is aimed at grabbing the nationality of each
    # scientist. This particular line looks IN THE ENTIRE SOUP for a URL, a relative URL in this
    # case, which ends with "women_computer_scientists".
    scientist_nationality = page_content_soup.css.select('a[href*="women_computer_scientists"]')

    # The previous line returns a list. We grab the elements from the list. It's
    # worth noting that some scientists are listed in more than one category of
    # nationality so if the list is greater than 1:
    if len(scientist_nationality) > 1:

        # We grab the first element from the list and add that to our variable.
        scientist_nationality_1 = scientist_nationality[0]

        # Some scientists' nationalities are split into two words (such as
        # "South Koreans"), so we do this conditional with a regex to search for
        # that.
        if re.search(r"\D+\s\D+\swomen", scientist_nationality_1.get_text()):

            # If we do meet the conditional we grab the text from the tags and
            # split it on " " which gives us a list. From that list we grab the
            # first two elements and join them. Then the full nationalities are
            # appened to the "scientist_nationalities_list_1 " list.
            scientist_nationalities_list_1.append(" ".join(scientist_nationality_1.get_text().split(" ")[0:2]))

        else:

            # If the scientist's nationality is made of one word only (such as
            # "American"), we get the text from the object, which returns a
            # string. We the split this string in the " " and get the first
            # element from the resulting list. This element is the actual string
            # which contains the nationality. We then append that to our
            # "scientist_nationalities_list_1" list.
            scientist_nationalities_list_1.append(scientist_nationality_1.get_text().split(" ")[0])

        # Same as above but for the second nationality.
        scientist_nationality_2 = scientist_nationality[1]

        if re.search(r"\D+\s\D+\swomen", scientist_nationality_2.get_text()):

            scientist_nationalities_list_2.append(" ".join(scientist_nationality_2.get_text().split(" ")[0:2]))

        else:

            scientist_nationalities_list_2.append(scientist_nationality_2.get_text().split(" ")[0])

    # If we only have one nationality for a scientist we only execute this code.
    elif len(scientist_nationality) == 1:

        scientist_nationality = scientist_nationality[0]

        if re.search(r"\D+\s\D+\swomen", scientist_nationality.get_text()):

            scientist_nationalities_list_1.append(" ".join(scientist_nationality.get_text().split(" ")[0:2]))

            # We need this "None" here otherwise the results are skewed in the
            # resulting dataframe.
            scientist_nationalities_list_2.append(None)

        else:

            scientist_nationalities_list_1.append(scientist_nationality.get_text().split(" ")[0])

            # We need this "None" here otherwise the results are skewed in the
            # resulting dataframe.
            scientist_nationalities_list_2.append(None)

    # A few scientists do not have their nationalities in places where it is
    # possible to grab them conveniently so we append "None" to both "scientists
    # nationalities lists".
    else:

        scientist_nationalities_list_1.append(None)
        scientist_nationalities_list_2.append(None)

    # We then look for the location for the scientist's resume.
    resume_location = page_content_soup.find("div", class_="mw-body-content")

    # Some "divs" have "p" tags with a "class=mw-empty-elt" with nothing in
    # them. Our scraper grabs them if we don't prevent it. We do this by
    # starting a conditional.
    if resume_location.find("p", class_="mw-empty-elt"):

        # If we meet the conditional we use the "find_all" method to located the
        # second "p" tag, which is where there is the first paragraph that
        # interests us, and get all of the remaining text from that onwards. We
        # also do this "replace" regex type thing but this is fairly obvious.
        # The "join" method is used to join all of the paragraphs which together
        # otherwise we get several lists for the same scientists that would be
        # added for each consecutive scientist.
        scientist_resume = " ".join([para.get_text().replace('\n', ' ').replace('\r', ' ').replace(',', ' ') for para in resume_location.find_all("p")][1:])

        # This regex grabs some "[1]" type of footnotes which have been scraped
        # along the text and replaces them with an empty string.
        scientist_resume = re.sub(r"\[\d\]", "", scientist_resume)
        scientists_resume_list.append(scientist_resume)

    # Some pages feature an "info box" that sometimes contain a "p" tag. We've
    # got to watch out for these as otherwise the scraper grabs this paragraph
    # and stops there without actually grabbing the text that we want. In this
    # case we do a conditional that looks for the "info box".
    elif resume_location.find("table", class_="infobox biography vcard"):

        # This part of the code works for finding the "p" inside the info box.
        # Somehow it is not possible to chain several "find" methods to help us
        # locate a potential "p" tag inside the info box so we assign the
        # content of the info box to a variable.
        info_box = resume_location.find("table", class_="infobox biography vcard")

        # If we do find a "p" tag inside the info box.
        if info_box.find("p"):

            # scientist_resume = resume_location.find_all("p")[1].get_text().replace('\n', ' ').replace('\r', ' ').replace(',', ' ')
            scientist_resume = " ".join([para.get_text().replace('\n', ' ').replace('\r', ' ').replace(',', ' ') for para in resume_location.find_all("p")[1:]])
            scientist_resume = re.sub(r"\[\d\]", "", scientist_resume)
            scientists_resume_list.append(scientist_resume)

        else:

            # If the page does feature a "info box" which does not contain a "p"
            # tag we carry on as normal.
            scientist_resume = " ".join([para.get_text().replace('\n', ' ').replace('\r', ' ').replace(',', ' ') for para in resume_location.find_all("p")])
            scientist_resume = re.sub(r"\[\d\]", "", scientist_resume)
            scientists_resume_list.append(scientist_resume)

    else:

        # If the page does not contain a "p" tag with a "class=mw-empty-elt" or
        # an "info box", we carry on as normal.
        scientist_resume = " ".join([para.get_text().replace('\n', ' ').replace('\r', ' ').replace(',', ' ') for para in resume_location.find_all("p")])
        scientist_resume = re.sub(r"\[\d\]", "", scientist_resume)
        scientists_resume_list.append(scientist_resume)

# We create a new dataframe with the scrapped names.
scientist_name_df = pd.DataFrame(scientist_name_list, columns=['Name'])

# We create a new dataframe with the first scrapped nationalities.
scientist_nationalities_1_df = pd.DataFrame(scientist_nationalities_list_1, columns=['Nationality 1'])

# We create a new dataframe with the second scrapped nationalities
scientist_nationalities_2_df = pd.DataFrame(scientist_nationalities_list_2, columns=['Nationality 2'])

# Create a new DataFrame with the scraped resumes.
resume_df = pd.DataFrame(scientists_resume_list, columns=['Resume'])

# Concatenate all the DataFrames along the columns axis (axis=1)
result_df = pd.concat([dataset, scientist_name_df, scientist_nationalities_1_df, scientist_nationalities_2_df,  resume_df], axis=1)

# Save the updated DataFrame back to the CSV file
result_df.to_csv('wikipedia_computer_scientists_names_test.csv', quoting=csv.QUOTE_ALL, encoding='utf-8', index=False)
