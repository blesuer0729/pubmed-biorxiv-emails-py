import requests
from bs4 import BeautifulSoup

def scraper(file, url, temp_emails):
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
        for email_tag in range(len(emails_in_reverse)):
            if emails_in_reverse[email_tag]["data-email"][::-1] not in temp_emails:
                temp_emails.append(emails_in_reverse[email_tag]["data-email"][::-1])
                file.write(emails_in_reverse[email_tag]["data-email"][::-1] + "\n")

def controller(file, start, stop):
    print("\nPubMed articles referencing Covid-19 and Sars-Cov-2")
    # fill in the range depending on which pages of the list you are scraping
    for num in range(start, stop + 1):
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
        temp_emails = []
        for article in range(len(get_article_metadata)):
            article_id = get_article_metadata[article]["href"]
            scraper(file, "https://pubmed.ncbi.nlm.nih.gov" + article_id, temp_emails)
        print("done.")
