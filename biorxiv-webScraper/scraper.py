from urllib.request import urlopen
from bs4 import BeautifulSoup

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

# Print iterations progress
# THIS FUNCTION IS FROM - https://stackoverflow.com/questions/3173320/text-progress-bar-in-the-console
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    
    # Call in a loop to create terminal progress bar
    # @params:
    #     iteration   - Required  : current iteration (Int)
    #     total       - Required  : total iterations (Int)
    #     prefix      - Optional  : prefix string (Str)
    #     suffix      - Optional  : suffix string (Str)
    #     decimals    - Optional  : positive number of decimals in percent complete (Int)
    #     length      - Optional  : character length of bar (Int)
    #     fill        - Optional  : bar fill character (Str)
    #     printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print()

# email_list.txt is the final file shipped for import
email_list = open("email_list.txt", "w+")

# fill in the range depending on which pages of the list you are scraping
for num in range (1,36):
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