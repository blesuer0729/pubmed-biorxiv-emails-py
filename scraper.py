import requests
from bs4 import BeautifulSoup
import argparse

# argparse library for getting page range
parser = argparse.ArgumentParser()
parser.add_argument("--site", type=str, help="The site that the scraper will run the page range on")
parser.add_argument("--start", type=int, help="Where to start grabbing emails from in the page list")
parser.add_argument("--stop", type=int, help="The page that the scraper will finish on")
args = parser.parse_args()

# email_list.txt is the final file shipped for import
biorxiv_email_list = open("biorxiv_email_list.txt", "w+")
pubmed_email_list = open("pubmed_email_list.txt", "w+")

##
# Scraper functions
##
def scrape_biorxiv_article(span, url):
    # add into list newly built urls that go to content pages
    string = span.text
    # split is using an EM DASH 
    article_url = url + string.split(" —")[0] + "v1.article-info"

    # Get markup and read it into BS
    page = requests.get(article_url).text
    soup_content = BeautifulSoup(page, "html.parser")

    # append the corresponding author name before the email 
    name_tag = soup_content.find("span", "name")
    author_name = name_tag.string.extract()

    # Clean and fix the email as a string with @ included
    email_tag = soup_content.find("span", "em-addr")
    email_string = email_tag.string.extract()
    author_email = email_string.replace("{at}", "@")

    biorxiv_email_list.write(author_email + " " + author_name + "\n")

def scrape_pubmed_article(url, store_emails):
    # Get soup content of article page
    page = requests.get(url).text
    soup_content = BeautifulSoup(page, "html.parser")

    # the PMCID of the article is a link to a page containing the author info
    article_ids = soup_content.findAll("a", {"data-ga-action" : "PMCID"})
    for link in range(len(article_ids)):
        article_pmc = article_ids[link]["href"]
        convert_link = article_pmc.replace("http", "https")
        page = requests.get(convert_link).text
        soup_content = BeautifulSoup(page, "html.parser")
    
        # The source code of the article has author emails in reverse
        # seems like they tried to confuse anyone looking to scrape them?
        emails_in_reverse = soup_content.findAll("a", {"class" : "oemail"})
        temp_emails = []
        for email_tag in range(len(emails_in_reverse)):
             temp_emails.append(emails_in_reverse[email_tag]["data-email"][::-1])
             for e in temp_emails:
                 if e not in store_emails:
                     store_emails.append(e)

## 
# Main page logic
##
# determine which site the user wanted to scrape first
if (args.site == "biorxiv"):
    print("\nBiorxiv preprints related to Covid-19 and Sars-Cov-2")
    # fill in the range depending on which pages of the list you are scraping
    for num in range (args.start, args.stop + 1):
        # Main content page
        main_url = "https://connect.biorxiv.org/relate/content/181?page="+str(num)

        # Give the HTML content Beautiful Soup
        page = requests.get(main_url).text
        soup_content = BeautifulSoup(page, "html.parser")

        # find url extensions for each article
        get_article_metadata = soup_content.find_all("span", "highwire-cite-metadata-journal")

        print("\nPage " + str(num))
        print("_________________")
        print("scraping..")
        # test each article for its containing site
        for span in get_article_metadata:
            link = span.a['href']
            if "medrx" in link:
                scrape_biorxiv_article(span, "https://www.medrxiv.org/content/")
            elif "biorx" in link:
                scrape_biorxiv_article(span, "https://www.biorxiv.org/content/")
            else:
                print("WARNING -  " + link + " was not scraped because it's site needs to be added to the biorxiv scraper")
        print("done.")
elif(args.site == "pubmed"):
    print("\nPubMed articles referencing Covid-19 and Sars-Cov-2")
    # fill in the range depending on which pages of the list you are scraping
    for num in range(args.start, args.stop +1):
        pubmed_url = "https://pubmed.ncbi.nlm.nih.gov/?term=covid-19&page="+str(num)

        # Give the HTML content to Beautiful Soup
        page = requests.get(pubmed_url).text
        soup_content = BeautifulSoup(page, "html.parser")

        # Get each article element off the page
        get_article_metadata = soup_content.find_all("a","docsum-title")

        print("\nPage " + str(num))
        print("_________________")
        print("scraping..")
        # Use the article ID's to scrape their author names
        store_emails = []
        for article in range(len(get_article_metadata)):
            article_id = get_article_metadata[article]["href"]
            scrape_pubmed_article("https://pubmed.ncbi.nlm.nih.gov" + article_id, store_emails)
        for email in store_emails:
            pubmed_email_list.write(email + "\n")
else:
    print("The site " + args.site + " is not yet supported by the scraper.")

biorxiv_email_list.close()
pubmed_email_list.close()
print("\nrun command 'cat <site>_email_list.txt' to see results")