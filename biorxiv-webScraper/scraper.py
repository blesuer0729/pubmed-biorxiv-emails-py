from urllib.request import urlopen
from bs4 import BeautifulSoup
import argparse

# argparse library for getting page range
parser = argparse.ArgumentParser()
parser.add_argument("--start", type=int, help="The first page so start the range from")
parser.add_argument("--stop", type=int, help="The last page that the range stops on")
args = parser.parse_args()

# email_list.txt is the final file shipped for import
email_list = open("email_list.txt", "w+")

def scrape_medrx(span):
    medrx_article_url = "https://www.medrxiv.org/content/"

    # add into list newly built urls that go to content pages
    string = span.text
    # split is using an EM DASH 
    article_url = medrx_article_url + string.split(" —")[0] + "v1.article-info"

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

def scrape_biorx(span):
    biorx_article_url = "https://www.biorxiv.org/content/"

    # add into list newly built urls that go to content pages
    string = span.text
    # split is using an EM DASH 
    article_url = biorx_article_url + string.split(" —")[0] + "v1.article-info"

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

# fill in the range depending on which pages of the list you are scraping
for num in range (args.start, args.stop):
    # Main content page
    main_url = "https://connect.biorxiv.org/relate/content/181?page="+str(num)

    # open the content page to gather url list
    page = urlopen(main_url)
    html_bytes = page.read()
    html_content = html_bytes.decode("utf-8")
    soup_content = BeautifulSoup(html_content, "html.parser")

    # find url extensions for dates and metadata of an article
    get_article_metadata = soup_content.find_all("span", "highwire-cite-metadata-journal")

    print("")
    print("Page " + str(num))
    print("_________________")
    print("Working..")
    # test each article for its containing site
    for span in get_article_metadata:
        link = span.a['href']
        if "medrx" in link:
            scrape_medrx(span)
        elif "biorx" in link:
            scrape_biorx(span)
        else:
            print("ERROR: " + link + " was not scraped because it's site is not supported.")
    print("Page " + str(num) + " done.")
    
email_list.close()