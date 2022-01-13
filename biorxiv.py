import requests
from bs4 import BeautifulSoup

def controller(file, start, stop):
    print("\nBiorxiv preprints related to Covid-19 and Sars-Cov-2")
    # fill in the range depending on which pages of the list you are scraping
    for num in range (start, stop + 1):
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
                scraper(file, span, "https://www.medrxiv.org/content/")
            elif "biorx" in link:
                scraper(file, span, "https://www.biorxiv.org/content/")
            else:
                print("WARNING -  " + link + " was not scraped because it's site needs to be added to the biorxiv scraper")
        print("done.")

def scraper(file, span, url):
    # add into list newly built urls that go to content pages
    string = span.text
    # split is using an EM DASH 
    article_url = url + string.split(" —")[0] + "v1.article-info"

    # Get markup and read it into BS
    page = requests.get(article_url).text
    soup_content = BeautifulSoup(page, "html.parser")

    # append the corresponding author name before the email 
    name_tag = soup_content.find("span", "name")
    if name_tag is not None:
        author_name = name_tag.string.extract()

        # Clean and fix the email as a string with @ included
        email_tag = soup_content.find("span", "em-addr")
        email_string = email_tag.string.extract()
        author_email = email_string.replace("{at}", "@")

        file.write(author_email + " " + author_name + "\n")
    else:
        # Clean and fix the email as a string with @ included
        email_tag = soup_content.find("span", "em-addr")
        email_string = email_tag.string.extract()
        author_email = email_string.replace("{at}", "@")

        file.write(author_email + "\n")
