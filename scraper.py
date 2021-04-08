from urllib.request import urlopen
from bs4 import BeautifulSoup
import argparse

# argparse library for getting page range
parser = argparse.ArgumentParser()
parser.add_argument("--site", type=str, help="The site that the scraper will run the page range on")
parser.add_argument("--start", type=int, help="Where to start grabbing emails from in the page list")
parser.add_argument("--stop", type=int, help="The page that the scraper will finish on")
args = parser.parse_args()

# email_list.txt is the final file shipped for import
email_list = open("email_list.txt", "w+")

def scrape_biorxiv(span, url):
    # add into list newly built urls that go to content pages
    string = span.text
    # split is using an EM DASH 
    article_url = url + string.split(" —")[0] + "v1.article-info"

    # Get markup and read it into BS
    page = urlopen(article_url)
    html_bytes = page.read()
    html_content = html_bytes.decode("utf-8")
    soup_content = BeautifulSoup(html_content, "html.parser")

    # append the corresponding author name before the email 
    name_tag = soup_content.find("span", "name")
    author_name = name_tag.string.extract()

    # Clean and fix the email as a string with @ included
    email_tag = soup_content.find("span", "em-addr")
    email_string = email_tag.string.extract()
    author_email = email_string.replace("{at}", "@")

    email_list.write(author_email + " " + author_name + "\n")

# determine which site the user wanted to scrape first
if (args.site == "biorxiv"):
    print("")
    print("Biorxiv Covid-19 Sars-Cov-2")
    # fill in the range depending on which pages of the list you are scraping
    for num in range (args.start, args.stop + 1):
        # Main content page
        main_url = "https://connect.biorxiv.org/relate/content/181?page="+str(num)

        # open the content page to gather url list
        page = urlopen(main_url)
        html_bytes = page.read()
        html_content = html_bytes.decode("utf-8")
        soup_content = BeautifulSoup(html_content, "html.parser")

        # find url extensions for dates and metadata of an article
        get_article_metadata = soup_content.find_all("span", "highwire-cite-metadata-journal")

        print("\nPage " + str(num))
        print("_________________")
        print("scraping..")
        # test each article for its containing site
        for span in get_article_metadata:
            link = span.a['href']
            if "medrx" in link:
                scrape_biorxiv(span, "https://www.medrxiv.org/content/")
            elif "biorx" in link:
                scrape_biorxiv(span, "https://www.biorxiv.org/content/")
            else:
                print("WARNING -  " + link + " was not scraped because it's site (" + link + ") needs to be added to the biorxiv scraper")
        print("done.")
else:
    print("The site " + args.site + " is not yet supported by the scraper.")

email_list.close()
print("\nrun command 'cat email_list.txt' to see results")